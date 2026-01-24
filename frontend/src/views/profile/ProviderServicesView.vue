<template>
  <div class="view-container">
    <div class="fixed top-0 left-0 right-0 z-50 bg-slate-900 border-b border-slate-800 p-4 flex items-center gap-3 max-w-md mx-auto">
      <button @click="$router.back()" class="text-blue-400 text-xl">‹</button>
      <h1 class="text-white font-semibold flex-1">Мои услуги</h1>
    </div>

    <div class="pt-20 p-4 space-y-4">
      <div v-if="services.length === 0" class="text-center py-12">
        <p class="text-gray-400">Нет услуг</p>
      </div>

      <div v-for="service in services" :key="service.id" class="bg-slate-800 border border-slate-700 rounded-lg p-4">
        <h3 class="text-white font-semibold">{{ service.name }}</h3>
        <p class="text-gray-400 text-sm">{{ service.description }}</p>
        <p class="text-blue-400 font-semibold mt-3">{{ formatPrice(service.price) }} ₽</p>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'

interface Service {
  id: string | number
  name: string
  price: number
  description?: string
}

const services = ref<Service[]>([
  {
    id: 1,
    name: 'Web-дизайн сайта',
    price: 15000,
    description: 'Профессиональный дизайн сайта'
  },
  {
    id: 2,
    name: 'Дизайн логотипа',
    price: 3000,
    description: 'Креативные логотипы'
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