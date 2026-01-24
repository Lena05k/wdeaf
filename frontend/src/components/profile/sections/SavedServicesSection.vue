<template>
  <div class="saved-services-section">
    <!-- Empty State -->
    <div v-if="!savedServices || savedServices.length === 0" class="text-center py-12">
      <p class="text-5xl mb-4">❤️</p>
      <p class="text-gray-400 text-lg">Нет сохранённых услуг</p>
      <p class="text-gray-500 text-sm mt-2">Сохраняйте услуги, которые вам нравятся</p>
    </div>

    <!-- Services Grid -->
    <div v-else class="grid grid-cols-1 md:grid-cols-2 gap-4 pb-4">
      <div
        v-for="service in savedServices"
        :key="service.id"
        class="bg-gradient-to-br from-slate-800 to-slate-900 border border-slate-700 rounded-xl p-4 hover:border-blue-500 transition group"
      >
        <!-- Image -->
        <div v-if="service.image" class="mb-3 rounded-lg overflow-hidden h-40 bg-slate-700">
          <img
            :src="service.image"
            :alt="service.name"
            class="w-full h-full object-cover group-hover:scale-105 transition"
          />
        </div>
        <div v-else class="mb-3 rounded-lg overflow-hidden h-40 bg-gradient-to-br from-blue-900 to-blue-800 flex items-center justify-center">
          <span class="text-4xl">🎨</span>
        </div>

        <!-- Content -->
        <div class="space-y-2">
          <!-- Title -->
          <h3 class="font-bold text-white line-clamp-2 group-hover:text-blue-300 transition">
            {{ service.name }}
          </h3>

          <!-- Provider -->
          <p class="text-sm text-gray-400">
            👤 {{ service.provider }}
          </p>

          <!-- Price -->
          <p class="text-lg font-semibold text-green-400">
            {{ formatPrice(service.price) }}
          </p>

          <!-- Rating -->
          <div class="flex items-center gap-2">
            <span class="text-yellow-400">⭐</span>
            <span class="text-sm text-gray-300">{{ service.rating }}</span>
          </div>
        </div>

        <!-- Actions -->
        <div class="mt-4 flex gap-2">
          <button
            @click="viewService(service)"
            class="flex-1 bg-blue-600 hover:bg-blue-500 text-white font-semibold py-2 rounded-lg transition active:scale-95"
          >
            Просмотр
          </button>
          <button
            @click="removeSaved(service.id)"
            class="px-3 bg-slate-700 hover:bg-red-600 text-white font-semibold py-2 rounded-lg transition active:scale-95"
            title="Удалить из сохранённых"
          >
            ❌
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
interface Service {
  id: string | number
  name: string
  provider: string
  price: number
  rating: number
  image?: string
  description?: string
}

defineProps<{
  savedServices?: Service[]
}>()

const emit = defineEmits<{
  view: [service: Service]
  remove: [id: string | number]
}>()

const formatPrice = (price: number): string => {
  return new Intl.NumberFormat('ru-RU', {
    style: 'currency',
    currency: 'RUB',
    minimumFractionDigits: 0
  }).format(price)
}

const viewService = (service: Service) => {
  emit('view', service)
}

const removeSaved = (id: string | number) => {
  if (confirm('Удалить из сохранённых?')) {
    emit('remove', id)
  }
}
</script>
