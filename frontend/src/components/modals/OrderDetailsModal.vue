<template>
  <div v-if="order" class="modal-overlay fixed inset-0 bg-black/50 flex items-end z-50">
    <div class="modal-content bg-slate-800 w-full max-w-md rounded-t-2xl border-t border-blue-900 max-h-[90vh] overflow-y-auto">
      <!-- Header -->
      <div class="sticky top-0 bg-slate-800 border-b border-blue-900 p-3 flex justify-between items-center">
        <h2 class="text-lg font-bold">📄 Детали заказа</h2>
        <button
            @click="emit('close')"
            class="text-gray-400 hover:text-white text-2xl"
        >
          ✕
        </button>
      </div>

      <!-- Content -->
      <div class="p-4 space-y-4">
        <!-- Status Badge -->
        <div class="flex items-center justify-between bg-slate-700/50 rounded-lg p-3 border border-slate-700">
          <span class="text-sm font-semibold text-gray-400">СТАТУС</span>
          <span :class="[
            'text-xs font-semibold px-3 py-1 rounded-full',
            order.status === 'active' ? 'bg-green-900 text-green-300' : 'bg-yellow-900 text-yellow-300'
          ]">
            {{ order.status === 'active' ? '✅ Активен' : '⚠️ Ожидание' }}
          </span>
        </div>

        <!-- Main Info -->
        <div class="space-y-3">
          <!-- Service -->
          <div>
            <p class="text-xs text-gray-400 mb-1">УСЛУГА</p>
            <p class="font-semibold text-lg">{{ order.service }}</p>
          </div>

          <!-- Provider -->
          <div>
            <p class="text-xs text-gray-400 mb-1">ИСПОЛНИТЕЛЬ</p>
            <p class="font-medium">{{ order.provider }}</p>
          </div>

          <!-- Price -->
          <div class="flex items-center justify-between bg-slate-700/50 rounded-lg p-3 border border-slate-700">
            <span class="text-sm font-semibold text-gray-400">ЦЕНА</span>
            <span class="text-2xl font-bold text-blue-400">{{ order.price }}₽</span>
          </div>
        </div>

        <!-- Divider -->
        <div class="h-px bg-slate-700"></div>

        <!-- Date & Time Info -->
        <div class="space-y-3">
          <!-- Order Date -->
          <div>
            <p class="text-xs text-gray-400 mb-1">ДАТА ЗАКАЗА</p>
            <p class="font-medium">{{ formatDate(order.date) }}</p>
          </div>

          <!-- Deadline -->
          <div v-if="order.deadline" >
            <p class="text-xs text-gray-400 mb-1">СРОК ВЫПОлНЕНИЯ</p>
            <p class="font-medium" :class="isDeadlineApproaching ? 'text-red-400' : 'text-white'">
              {{ formatDate(order.deadline) }}
              <span v-if="isDeadlineApproaching" class="text-xs text-red-400 ml-2">🚨 Спешно!</span>
            </p>
          </div>
        </div>

        <!-- Divider -->
        <div class="h-px bg-slate-700"></div>

        <!-- Description -->
        <div>
          <p class="text-xs text-gray-400 mb-1">ОПИСАНИЕ</p>
          <p class="text-sm text-gray-300">{{ order.description || 'Но описания' }}</p>
        </div>

        <!-- Stats -->
        <div class="grid grid-cols-2 gap-2">
          <div class="bg-slate-700/50 rounded-lg p-3 border border-slate-700 text-center">
            <p class="text-xs text-gray-400 mb-1">НОМЕР</p>
            <p class="font-semibold text-blue-400">#{{ order.id }}</p>
          </div>
          <div class="bg-slate-700/50 rounded-lg p-3 border border-slate-700 text-center">
            <p class="text-xs text-gray-400 mb-1">КАТЕГОРИЯ</p>
            <p class="font-semibold text-white">{{ order.category || '—' }}</p>
          </div>
        </div>
      </div>

      <!-- Footer Buttons -->
      <div class="sticky bottom-0 bg-slate-800 border-t border-blue-900 p-3 flex gap-2">
        <button
            @click="emit('close')"
            class="flex-1 bg-slate-700 hover:bg-slate-600 text-white font-semibold py-2 text-sm rounded-lg transition"
        >
          ✕ Закрыть
        </button>
        <button
            v-if="order.status === 'pending'"
            @click="handleCancel"
            class="flex-1 bg-red-600 hover:bg-red-500 text-white font-semibold py-2 text-sm rounded-lg transition flex items-center justify-center gap-2"
        >
          ❌ Отменить
        </button>
        <button
            v-else
            @click="emit('message')"
            class="flex-1 bg-blue-600 hover:bg-blue-500 text-white font-semibold py-2 text-sm rounded-lg transition flex items-center justify-center gap-2"
        >
          💬 Написать
        </button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'

interface Order {
  id: string | number
  service: string
  provider: string
  status: 'active' | 'pending' | 'completed' | 'cancelled'
  price: number
  date: string | Date
  deadline?: string | Date
  description?: string
  category?: string
}

interface Props {
  order: Order | null
}

const props = defineProps<Props>()

const emit = defineEmits<{
  'close': []
  'cancel': []
  'message': []
}>()

// Проверяем близость дедлайна (меньше 24 часов)
const isDeadlineApproaching = computed(() => {
  if (!props.order?.deadline) return false
  const now = new Date()
  const deadline = new Date(props.order.deadline)
  const hoursLeft = (deadline.getTime() - now.getTime()) / (1000 * 60 * 60)
  return hoursLeft > 0 && hoursLeft < 24
})

// Форматирование даты
const formatDate = (date: string | Date | undefined): string => {
  if (!date) return 'Не указано'
  const d = new Date(date)
  const options: Intl.DateTimeFormatOptions = {
    year: 'numeric',
    month: 'long',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit'
  }
  return d.toLocaleDateString('ru-RU', options)
}

const handleCancel = () => {
  if (confirm('Вы уверены? Заказ будет отменен.')) {
    emit('cancel')
  }
}
</script>

<style scoped>
.modal-overlay {
  animation: fadeIn 0.3s ease-out;
}

.modal-content {
  animation: slideUp 0.3s ease-out;
}

@keyframes fadeIn {
  from {
    opacity: 0;
  }
  to {
    opacity: 1;
  }
}

@keyframes slideUp {
  from {
    transform: translateY(100%);
  }
  to {
    transform: translateY(0);
  }
}
</style>
