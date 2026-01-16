<template>
  <div v-if="services.length > 0" class="mt-6">
    <h3 class="text-lg font-bold mb-3">📋 Мои услуги</h3>

    <!-- Service Cards Grid -->
    <div class="grid grid-cols-1 gap-3 mb-3">
      <div
          v-for="service in services"
          :key="service.id"
          @click="emit('select-service', service)"
          class="bg-slate-800 rounded-lg border border-blue-900 overflow-hidden cursor-pointer hover:border-blue-500 transition transform hover:scale-105"
      >
        <!-- Service Image -->
        <div v-if="service.images && service.images.length > 0" class="relative h-32 bg-slate-700 overflow-hidden">
          <img
              :src="service.images[0].preview || service.images[0]"
              :alt="service.serviceName"
              class="w-full h-full object-cover"
          />
          <span class="absolute top-2 right-2 bg-blue-600 text-white px-2 py-1 rounded text-xs">
            {{ service.category }}
          </span>
        </div>
        <div v-else class="h-32 bg-slate-700 flex items-center justify-center text-gray-500">
          📷 Нет фото
        </div>

        <!-- Service Info -->
        <div class="p-3">
          <h4 class="font-bold text-sm mb-1">{{ service.serviceName || service.name }}</h4>
          <p class="text-xs text-gray-400 mb-2 line-clamp-2">{{ service.description }}</p>

          <div class="flex justify-between items-center">
            <span class="text-yellow-400 text-sm">⭐ 4.9</span>
            <span class="font-bold text-blue-400">{{ service.price }}₽</span>
          </div>
        </div>
      </div>
    </div>

    <button
        @click="emit('add-service')"
        class="w-full bg-blue-600 hover:bg-blue-500 text-white font-semibold py-2 rounded-lg transition"
    >
      + Добавить услугу
    </button>
  </div>
</template>

<script setup lang="ts">
interface Service {
  id: string
  serviceName?: string
  name?: string
  description: string
  category: string
  price: number
  images?: Array<{ preview?: string }>
}

interface Props {
  services: Service[]
}

defineProps<Props>()

const emit = defineEmits<{
  'select-service': [service: Service]
  'add-service': []
}>()
</script>

<style scoped></style>
