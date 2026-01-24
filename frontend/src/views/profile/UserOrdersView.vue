<template>
  <div class="view-container">
    <!-- Back Button -->
    <div class="fixed top-0 left-0 right-0 z-50 bg-slate-900 border-b border-slate-800 p-4 flex items-center gap-3 max-w-md mx-auto">
      <button @click="$router.back()" class="text-blue-400 text-xl">‹</button>
      <h1 class="text-white font-semibold flex-1">Мои заказы</h1>
    </div>

    <div class="pt-20 p-4 space-y-4">
      <!-- Empty State -->
      <div v-if="orders.length === 0" class="text-center py-12">
        <p class="text-gray-400">Нет заказов</p>
      </div>

      <!-- Orders List -->
      <div v-for="order in orders" :key="order.id" class="bg-slate-800 border border-slate-700 rounded-lg p-4">
        <h3 class="text-white font-semibold">{{ order.serviceName }}</h3>
        <p class="text-gray-400 text-sm">{{ order.provider }}</p>
        <p class="text-gray-400 text-sm mt-2">{{ order.date }}</p>
        <span :class="`inline-block mt-2 px-3 py-1 rounded text-xs font-semibold ${
          order.status === 'completed' ? 'bg-green-900 text-green-300' : 'bg-blue-900 text-blue-300'
        }`">
          {{ order.status === 'completed' ? 'Завершен' : 'На рассмотрении' }}
        </span>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'

interface Order {
  id: string | number
  serviceName: string
  provider: string
  date: string
  status: string
}

const orders = ref<Order[]>([
  {
    id: 1,
    serviceName: 'Уроки английского',
    provider: 'Джон Д.',
    date: '12 янв 2025',
    status: 'completed'
  },
  {
    id: 2,
    serviceName: 'Консультация бухгалтера',
    provider: 'Мария С.',
    date: '8 янв 2025',
    status: 'active'
  }
])
</script>

<style scoped>
.view-container {
  background: linear-gradient(to bottom, #0f172a, #0f1319);
  min-height: 100vh;
  padding-bottom: 40px;
}
</style>