<template>
  <div class="space-y-3">
    <div v-if="orders.length === 0" class="text-center py-8">
      <p class="text-2xl">📭</p>
      <p class="text-gray-400 mt-2">Нет заказов</p>
    </div>
    <div v-for="order in orders" :key="order.id" class="bg-slate-700 rounded-lg p-4 border border-slate-600 hover:border-blue-500 transition">
      <div class="flex justify-between items-start mb-2">
        <h3 class="font-semibold text-white flex-1">{{ order.serviceName }}</h3>
        <span :class="`px-2 py-1 rounded text-xs font-semibold whitespace-nowrap ml-2 ${
          order.status === 'completed' ? 'bg-green-900 text-green-300' : 'bg-blue-900 text-blue-300'
        }`">
          {{ order.status === 'completed' ? '✓ Завершен' : '⏳ На рассмотрении' }}
        </span>
      </div>
      <p class="text-sm text-gray-400">от {{ order.provider }}</p>
      <p class="text-xs text-gray-500 mt-2">{{ order.date }}</p>
    </div>
  </div>
</template>

<script setup lang="ts">
import { defineProps } from 'vue'

interface Order {
  id: number
  serviceName: string
  provider: string
  date: string
  status: string
}

defineProps<{
  orders: Order[]
}>()
</script>