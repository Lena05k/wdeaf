<template>
  <div class="view-container">
    <div class="fixed top-0 left-0 right-0 z-50 bg-slate-900 border-b border-slate-800 p-4 flex items-center gap-3 max-w-md mx-auto">
      <button @click="$router.back()" class="text-blue-400 text-xl">‹</button>
      <h1 class="text-white font-semibold flex-1">Сохраненные услуги</h1>
    </div>

    <div class="pt-20 p-4 space-y-4">
      <div v-if="savedServices.length === 0" class="text-center py-12">
        <p class="text-gray-400">Нет сохраненных услуг</p>
      </div>

      <div v-for="service in savedServices" :key="service.id" class="bg-slate-800 border border-slate-700 rounded-lg p-4">
        <h3 class="text-white font-semibold">{{ service.name }}</h3>
        <p class="text-gray-400 text-sm">{{ service.provider }}</p>
        <div class="flex justify-between items-center mt-3">
          <span class="text-blue-400 font-semibold">{{ formatPrice(service.price) }} ₽</span>
          <span class="text-yellow-400">⭐ {{ service.rating }}</span>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'

interface Service {
  id: string | number
  name: string
  provider?: string
  price: number
  rating?: number
}

const savedServices = ref<Service[]>([
  {
    id: 1,
    name: 'Web-дизайн',
    provider: 'Артем К.',
    price: 15000,
    rating: 4.9
  }
])

const formatPrice = (price: number): string => {
  return new Intl.NumberFormat('ru-RU').format(price)
}
</script>

<style scoped>
.view-container {
  background: linear-gradient(to bottom, #0f172a, #0f1319);
  min-height: 100vh;
  padding-bottom: 40px;
}
</style>