<template>
  <div
      class="provider-card cursor-pointer transition-all hover:border-blue-500 hover:shadow-lg hover:shadow-blue-900/30"
      @click="emit('select')"
  >
    <div class="flex justify-between items-start mb-2">
      <h3 class="font-bold">{{ order.service }}</h3>
      <span :class="[
        'text-xs font-semibold px-3 py-1 rounded-full',
        order.status === 'active' ? 'bg-green-900 text-green-300' : 'bg-yellow-900 text-yellow-300'
      ]">
        {{ order.status === 'active' ? '✓ Активен' : '⏳ Ожидание' }}
      </span>
    </div>

    <p class="text-sm text-gray-400 mb-2">📋 Исполнитель: {{ order.provider }}</p>

    <div class="flex justify-between items-center mb-3">
      <span class="text-sm text-gray-500">📅 {{ formatDate(order.date) }}</span>
      <span class="font-bold text-blue-400">{{ order.price }}₽</span>
    </div>

    <!-- Description Preview -->
    <p v-if="order.description" class="text-xs text-gray-500 mb-3 line-clamp-2">
      {{ order.description }}
    </p>

    <!-- Action Button (shown on status) -->
    <button
        v-if="order.status === 'pending'"
        @click.stop="emit('cancel')"
        class="btn-secondary w-full py-1 rounded text-xs font-semibold"
    >
      ✕ Отменить
    </button>
    <button
        v-else
        @click.stop="emit('message')"
        class="btn-primary w-full py-1 rounded text-xs font-semibold"
    >
      💬 Написать
    </button>

    <!-- Tap indicator -->
    <div class="text-xs text-gray-500 text-center mt-2 opacity-70">
      👆 Нажмите для подробностей
    </div>
  </div>
</template>

<script setup lang="ts">
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
  order: Order
}

defineProps<Props>()

const emit = defineEmits<{
  'select': []
  'cancel': []
  'message': []
}>()

const formatDate = (date: string | Date | undefined): string => {
  if (!date) return 'Не указано'
  const d = new Date(date)
  const options: Intl.DateTimeFormatOptions = {
    month: 'short',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit'
  }
  return d.toLocaleDateString('ru-RU', options)
}
</script>

<style scoped>
.provider-card {
  background: #1a1f2e;
  border: 1px solid #0055FF;
  border-radius: 12px;
  padding: 16px;
  margin-bottom: 12px;
  transition: all 0.3s ease;
}

.provider-card:hover {
  border-color: #0077ff;
  box-shadow: 0 4px 12px rgba(0, 85, 255, 0.2);
  transform: translateY(-2px);
}

.btn-primary {
  background: #0055FF;
  color: white;
  border: 1px solid #0055FF;
  transition: all 0.3s;
  cursor: pointer;
}

.btn-primary:hover {
  background: #0044cc;
  border-color: #0044cc;
}

.btn-secondary {
  background: transparent;
  color: #0055FF;
  border: 1px solid #0055FF;
  transition: all 0.3s;
  cursor: pointer;
}

.btn-secondary:hover {
  background: rgba(0, 85, 255, 0.1);
}

.text-gray-400 { color: #999999; }
.text-gray-500 { color: #777777; }

.line-clamp-2 {
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}
</style>
