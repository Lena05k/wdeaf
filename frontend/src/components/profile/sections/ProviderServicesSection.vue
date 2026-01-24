<template>
  <div class="provider-services-section">
    <!-- Header -->
    <div class="flex items-center justify-between mb-4">
      <h3 class="text-xl font-bold text-white">{{ services?.length ?? 0 }} услуг</h3>
      <button
        @click="addService"
        class="bg-green-600 hover:bg-green-500 text-white font-semibold px-4 py-2 rounded-lg transition active:scale-95 flex items-center gap-2"
      >
        <span>+</span> Новая услуга
      </button>
    </div>

    <!-- Empty State -->
    <div v-if="!services || services.length === 0" class="text-center py-12 bg-slate-800 rounded-xl">
      <p class="text-5xl mb-4">🚧</p>
      <p class="text-gray-400 text-lg">Нет услуг</p>
      <p class="text-gray-500 text-sm mt-2">Начните с создания первой услуги</p>
    </div>

    <!-- Services List -->
    <div v-else class="space-y-3">
      <div
        v-for="service in services"
        :key="service.id"
        class="bg-slate-800 border border-slate-700 rounded-xl p-4 hover:border-blue-500 transition group"
      >
        <!-- Service Info -->
        <div class="flex items-start justify-between mb-3">
          <div class="flex-1">
            <h4 class="font-bold text-white group-hover:text-blue-300 transition">
              {{ service.serviceName }}
            </h4>
            <p class="text-sm text-gray-400 mt-1">
              {{ service.category }}
            </p>
          </div>
          <div class="text-right">
            <p class="text-lg font-bold text-green-400">
              {{ formatPrice(service.price) }}
            </p>
            <div class="flex gap-1 mt-1">
              <span v-for="i in 5" :key="i" class="text-xs" :class="i <= (service.rating ?? 0) ? 'text-yellow-400' : 'text-gray-600'">
                ★
              </span>
            </div>
          </div>
        </div>

        <!-- Description -->
        <p class="text-sm text-gray-300 line-clamp-2 mb-3">
          {{ service.description }}
        </p>

        <!-- Availability -->
        <div class="text-xs text-gray-400 mb-4">
          <span v-if="service.availability?.weekdays" class="inline-block mr-2">
            📅 Пн-Пт
          </span>
          <span v-if="service.availability?.weekends" class="inline-block mr-2">
            👫 Сб-Вс
          </span>
          <span v-if="service.availability?.evenings" class="inline-block">
            🌙 Вечерам
          </span>
        </div>

        <!-- Actions -->
        <div class="flex gap-2">
          <button
            @click="editService(service)"
            class="flex-1 bg-blue-600 hover:bg-blue-500 text-white font-semibold py-2 rounded-lg transition active:scale-95 flex items-center justify-center gap-1"
          >
            ✍️ Отредактировать
          </button>
          <button
            @click="deleteService(service.id)"
            class="px-3 bg-red-600 hover:bg-red-500 text-white font-semibold py-2 rounded-lg transition active:scale-95"
          >
            🗑️
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
interface Service {
  id: string | number
  serviceName: string
  category: string
  description: string
  price: number
  rating?: number
  availability?: {
    weekdays: boolean
    weekends: boolean
    evenings: boolean
  }
}

defineProps<{
  services?: Service[]
}>()

const emit = defineEmits<{
  edit: [service: Service]
  delete: [id: string | number]
  add: []
}>()

const formatPrice = (price: number): string => {
  return new Intl.NumberFormat('ru-RU', {
    style: 'currency',
    currency: 'RUB',
    minimumFractionDigits: 0
  }).format(price)
}

const addService = () => {
  emit('add')
}

const editService = (service: Service) => {
  emit('edit', service)
}

const deleteService = (id: string | number) => {
  if (confirm('Удалить эту услугу?')) {
    emit('delete', id)
  }
}
</script>
