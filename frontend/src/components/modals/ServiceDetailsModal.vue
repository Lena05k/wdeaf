<template>
  <div v-if="service" class="modal-overlay fixed inset-0 bg-black/50 flex items-end z-50">
    <div class="modal-content bg-slate-800 w-full max-w-md rounded-t-2xl border-t border-blue-900 max-h-[90vh] overflow-y-auto">
      <!-- Header -->
      <div class="sticky top-0 bg-slate-800 border-b border-blue-900 p-4 flex justify-between items-center">
        <h2 class="text-xl font-bold truncate">{{ service.serviceName }}</h2>
        <button
            @click="emit('close')"
            class="text-gray-400 hover:text-white text-2xl ml-2"
        >
          ✕
        </button>
      </div>

      <!-- Content -->
      <div class="p-4 space-y-4">
        <!-- Image Carousel -->
        <div v-if="service.images && service.images.length > 0" class="relative">
          <img
              :src="service.images[imageIndex].preview || service.images[imageIndex]"
              :alt="'Service image ' + (imageIndex + 1)"
              class="w-full h-48 object-cover rounded-lg"
          />

          <!-- Navigation Arrows -->
          <div v-if="service.images.length > 1" class="absolute inset-0 flex items-center justify-between px-2 rounded-lg">
            <button
                @click="imageIndex = (imageIndex - 1 + service.images.length) % service.images.length"
                class="bg-black/50 text-white p-2 rounded-full hover:bg-black/70"
            >
              ←
            </button>
            <button
                @click="imageIndex = (imageIndex + 1) % service.images.length"
                class="bg-black/50 text-white p-2 rounded-full hover:bg-black/70"
            >
              →
            </button>
          </div>

          <!-- Image Counter -->
          <div class="absolute bottom-2 right-2 bg-black/50 text-white px-2 py-1 rounded text-xs">
            {{ imageIndex + 1 }}/{{ service.images.length }}
          </div>
        </div>

        <!-- Service Details -->
        <div class="space-y-3">
          <div>
            <p class="text-xs text-gray-400 mb-1">КАТЕГОРИЯ</p>
            <p class="font-semibold">{{ service.category }}</p>
          </div>

          <div>
            <p class="text-xs text-gray-400 mb-1">ОПИСАНИЕ</p>
            <p class="text-sm">{{ service.description }}</p>
          </div>

          <div>
            <p class="text-xs text-gray-400 mb-1">ЦЕНА</p>
            <p class="text-2xl font-bold text-blue-400">{{ service.price }}₽</p>
          </div>

          <div>
            <p class="text-xs text-gray-400 mb-2">ГРАФИК РАБОТЫ</p>
            <div class="text-sm space-y-1">
              <p v-if="service.availability?.weekdays" class="text-green-400">✓ Будни (Пн-Пт)</p>
              <p v-if="service.availability?.weekends" class="text-green-400">✓ Выходные (Сб-Вс)</p>
              <p v-if="service.availability?.evenings" class="text-green-400">✓ Вечерние часы (18:00-23:00)</p>
            </div>
          </div>

          <div>
            <p class="text-xs text-gray-400 mb-1">ЧАСОВОЙ ПОЯС</p>
            <p class="text-sm">{{ service.timezone }}</p>
          </div>
        </div>

        <!-- Stats -->
        <div class="grid grid-cols-2 gap-3 bg-slate-700/50 rounded-lg p-3">
          <div class="text-center">
            <p class="text-2xl font-bold text-yellow-400">⭐</p>
            <p class="text-xs text-gray-400">{{ service.rating || 4.9 }} Рейтинг</p>
          </div>
          <div class="text-center">
            <p class="text-2xl font-bold text-green-400">✓</p>
            <p class="text-xs text-gray-400">{{ service.reviewsCount || 0 }} Отзывов</p>
          </div>
        </div>
      </div>

      <!-- Footer Buttons -->
      <div class="sticky bottom-0 bg-slate-800 border-t border-blue-900 p-4 flex gap-2">
        <button
            @click="emit('delete')"
            class="flex-1 bg-red-600 hover:bg-red-500 text-white font-semibold py-2 rounded-lg transition flex items-center justify-center gap-2"
        >
          🗑️ Удалить
        </button>
        <button
            @click="handleEdit"
            class="flex-1 bg-blue-600 hover:bg-blue-500 text-white font-semibold py-2 rounded-lg transition flex items-center justify-center gap-2"
        >
          🔍 Редактировать
        </button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'

interface Service {
  id: string
  serviceName: string
  description: string
  category: string
  price: number
  timezone?: string
  images?: Array<{ preview?: string }>
  availability?: {
    weekdays?: boolean
    weekends?: boolean
    evenings?: boolean
  }
  rating?: number
  reviewsCount?: number
}

interface Props {
  service: Service | null
}

const props = defineProps<Props>()

const emit = defineEmits<{
  'close': []
  'delete': []
  'edit': [service: Service]
}>()

const imageIndex = ref(0)

const handleEdit = () => {
  if (props.service) {
    emit('edit', props.service)
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
