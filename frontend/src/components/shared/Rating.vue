<template>
  <div class="rating">
    <div class="rating-stars">
      <span
          v-for="star in 5"
          :key="star"
          class="star"
          :class="{ filled: star <= Math.round(value) }"
      >
        ★
      </span>
    </div>
    <p v-if="showValue" class="rating-value">{{ value.toFixed(1) }}</p>
    <p v-if="showCount && reviewCount" class="rating-count">({{ reviewCount }} отзывов)</p>
  </div>
</template>

<script setup lang="ts">
import { defineProps, withDefaults } from 'vue'

withDefaults(
    defineProps<{
      value: number
      showValue?: boolean
      showCount?: boolean
      reviewCount?: number
    }>(),
    {
      showValue: true,
      showCount: false,
      reviewCount: 0
    }
)
</script>

<style scoped>
.rating {
  display: flex;
  align-items: center;
  gap: 8px;
}

.rating-stars {
  display: flex;
  gap: 2px;
}

.star {
  font-size: 16px;
  color: var(--color-text-secondary);
  transition: color 0.3s;
}

.star.filled {
  color: #fbbf24;
}

.rating-value {
  margin: 0;
  font-size: 14px;
  font-weight: 600;
  color: var(--color-text-primary);
}

.rating-count {
  margin: 0;
  font-size: 12px;
  color: var(--color-text-secondary);
}
</style>
