<template>
  <div class="space-y-3">
    <div v-if="reviews.length === 0" class="text-center py-8">
      <p class="text-2xl">📝</p>
      <p class="text-gray-400 mt-2">Нет отзывов</p>
    </div>
    <div v-for="review in reviews" :key="review.id" class="bg-slate-700 rounded-lg p-4 border border-slate-600 hover:border-blue-500 transition">
      <div class="flex justify-between items-start mb-2">
        <h3 class="font-semibold text-white">{{ review.serviceName }}</h3>
        <span class="text-yellow-400 font-semibold">⭐ {{ review.rating }}/5</span>
      </div>
      <p class="text-sm text-gray-400">{{ review.provider }}</p>
      <p class="text-gray-300 text-sm mt-3">{{ review.text }}</p>
      <p class="text-gray-500 text-xs mt-2">{{ review.date }}</p>
    </div>
  </div>
</template>

<script setup lang="ts">
import { defineProps } from 'vue'

interface Review {
  id: number
  serviceName: string
  provider: string
  text: string
  rating: number
  date: string
}

defineProps<{
  reviews: Review[]
}>()
</script>