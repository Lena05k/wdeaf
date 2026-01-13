<template>
  <div class="reviews-container">
    <h4 class="reviews-title">💬 Отзывы ({{ reviews.length }})</h4>
    <div class="reviews-list">
      <div v-for="review in reviews" :key="review.id || review.author" class="review-item">
        <div class="review-header">
          <p class="review-author">{{ review.author }}</p>
          <Rating :value="review.rating" :show-value="true" />
        </div>
        <p class="review-text">{{ review.text }}</p>
        <p v-if="review.date" class="review-date">{{ review.date }}</p>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { defineProps } from 'vue'
import Rating from './Rating.vue'

interface Review {
  id?: number
  author: string
  rating: number
  text: string
  date?: string
}

defineProps<{
  reviews: Review[]
  providerName?: string
}>()
</script>

<style scoped>
.reviews-container {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.reviews-title {
  margin: 0;
  font-size: 14px;
  font-weight: 700;
  color: var(--color-text-primary);
}

.reviews-list {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.review-item {
  padding: 12px;
  background: var(--color-bg-secondary);
  border-left: 3px solid var(--color-primary);
  border-radius: 6px;
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.review-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 8px;
}

.review-author {
  margin: 0;
  font-size: 13px;
  font-weight: 600;
  color: var(--color-text-primary);
}

.review-text {
  margin: 0;
  font-size: 13px;
  color: var(--color-text-secondary);
  line-height: 1.5;
}

.review-date {
  margin: 0;
  font-size: 12px;
  color: var(--color-text-secondary);
  opacity: 0.7;
}
</style>
