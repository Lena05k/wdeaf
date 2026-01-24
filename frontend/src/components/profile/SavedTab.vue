<template>
  <div class="space-y-3">
    <div v-if="services.length === 0" class="text-center py-8">
      <p class="text-2xl">❤️</p>
      <p class="text-gray-400 mt-2">Нет сохраненных услуг</p>
    </div>
    <div v-for="service in services" :key="service.id" class="bg-slate-700 rounded-lg p-4 border border-slate-600 hover:border-blue-500 transition">
      <div class="flex justify-between items-start mb-2">
        <h3 class="font-semibold text-white">{{ service.name }}</h3>
        <span class="text-yellow-400">⭐ {{ service.rating }}</span>
      </div>
      <p class="text-sm text-gray-400 mb-3">{{ service.provider }}</p>
      <p class="text-blue-400 font-semibold">{{ formatPrice(service.price) }} ₽</p>
    </div>
  </div>
</template>

<script setup lang="ts">
import { defineProps } from 'vue'

interface Service {
  id: number
  name: string
  provider: string
  price: number
  rating: number
}

defineProps<{
  services: Service[]
}>()

const formatPrice = (price: number): string => {
  return new Intl.NumberFormat('ru-RU').format(price)
}
</script>