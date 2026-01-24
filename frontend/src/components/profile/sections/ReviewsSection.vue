<template>
  <div class="reviews-section">
    <!-- Empty State -->
    <div v-if="!reviews || reviews.length === 0" class="text-center py-12">
      <p class="text-5xl mb-4">📝</p>
      <p class="text-gray-400 text-lg">Нет отзывов</p>
      <p class="text-gray-500 text-sm mt-2">Этот раздел пополнится после первого заказа</p>
    </div>

    <!-- Reviews List -->
    <div v-else class="space-y-3">
      <div
        v-for="review in reviews"
        :key="review.id"
        class="bg-slate-800 border border-slate-700 rounded-xl p-4 hover:border-blue-500 transition"
      >
        <!-- Header -->
        <div class="flex items-start justify-between mb-2">
          <div>
            <!-- Service Name -->
            <p class="font-bold text-blue-400 text-sm">
              {{ review.serviceName }}
            </p>
            <!-- Provider -->
            <p class="text-gray-400 text-xs mt-1">
              👤 {{ review.provider }}
            </p>
          </div>
          <!-- Rating Stars -->
          <div class="flex gap-1">
            <span v-for="i in 5" :key="i" class="text-sm" :class="i <= review.rating ? 'text-yellow-400' : 'text-gray-600'">
              ★
            </span>
          </div>
        </div>

        <!-- Review Text -->
        <p class="text-gray-300 text-sm leading-relaxed mb-3">
          {{ review.text }}
        </p>

        <!-- Footer -->
        <div class="flex items-center justify-between text-xs text-gray-500">
          <span>📅 {{ formatDate(review.date) }}</span>
          <span class="font-semibold text-yellow-400">{{ review.rating }}.0</span>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
interface Review {
  id: string | number
  serviceName: string
  provider: string
  text: string
  rating: number
  date: string
}

defineProps<{
  reviews?: Review[]
}>()

const formatDate = (dateStr: string): string => {
  try {
    const date = new Date(dateStr)
    return new Intl.DateTimeFormat('ru-RU', {
      year: 'numeric',
      month: 'short',
      day: 'numeric'
    }).format(date)
  } catch {
    return dateStr
  }
}
</script>
