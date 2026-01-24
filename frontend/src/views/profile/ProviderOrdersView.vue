<template>
  <div class="view-container">
    <div class="fixed top-0 left-0 right-0 z-50 bg-slate-900 border-b border-slate-800 p-4 flex items-center gap-3 max-w-md mx-auto">
      <button @click="$router.back()" class="text-blue-400 text-xl">‹</button>
      <h1 class="text-white font-semibold flex-1">Заказы</h1>
    </div>

    <div class="pt-20 p-4 space-y-4">
      <div v-if="orders.length === 0" class="text-center py-12">
        <p class="text-gray-400">Нет заказов</p>
      </div>

      <div v-for="order in orders" :key="order.id" class="bg-slate-800 border border-slate-700 rounded-lg p-4">
        <h3 class="text-white font-semibold">{{ order.serviceName }}</h3>
        <p class="text-gray-400 text-sm">{{ order.clientName }}</p>
        <p class="text-gray-400 text-sm">{{ order.date }}</p>
        <div class="flex justify-between items-center mt-3">
          <span class="text-blue-400 font-semibold">{{ formatPrice(order.price) }} ₽</span>
          <span class="text-green-400 text-xs">✓ {{ order.status }}</span>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'

interface Order {
  id: string | number
  serviceName: string
  clientName: string
  date: string
  status: string
  price: number
}

const orders = ref<Order[]>([
  {
    id: 1,
    serviceName: 'Web-дизайн',
    clientName: 'Анна П.',
    date: '15 янв 2025',
    status: 'выполнен',
    price: 15000
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