<template>
  <div class="view-container">
    <div class="fixed top-0 left-0 right-0 z-50 bg-slate-900 border-b border-slate-800 p-4 flex items-center gap-3 max-w-md mx-auto">
      <button @click="$router.back()" class="text-blue-400 text-xl">‹</button>
      <h1 class="text-white font-semibold flex-1">Отзывы</h1>
    </div>

    <div class="pt-20 p-4 space-y-4">
      <div v-if="reviews.length === 0" class="text-center py-12">
        <p class="text-gray-400">Нет отзывов</p>
      </div>

      <div v-for="review in reviews" :key="review.id" class="bg-slate-800 border border-slate-700 rounded-lg p-4">
        <div class="flex justify-between items-start mb-2">
          <h3 class="text-white font-semibold">{{ review.clientName }}</h3>
          <span class="text-yellow-400">⭐ {{ review.rating }}/5</span>
        </div>
        <p class="text-gray-300 mt-3">{{ review.text }}</p>
        <p class="text-gray-500 text-xs mt-2">{{ review.date }}</p>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'

interface Review {
  id: string | number
  clientName: string
  text: string
  rating: number
  date: string
}

const reviews = ref<Review[]>([
  {
    id: 1,
    clientName: 'Иван П.',
    text: 'Отличная работа! Все сделано качественно и в срок.',
    rating: 5,
    date: '12 янв 2025'
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