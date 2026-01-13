<template>
  <div class="empty-state">
    <p class="empty-icon">{{ icon }}</p>
    <h3 class="empty-title">{{ title }}</h3>
    <p v-if="description" class="empty-description">{{ description }}</p>
    <button v-if="actionLabel && actionCallback" class="btn btn-primary" @click="actionCallback">
      {{ actionLabel }}
    </button>
  </div>
</template>

<script setup lang="ts">
import { defineProps } from 'vue'

defineProps<{
  icon?: string
  title: string
  description?: string
  actionLabel?: string
  actionCallback?: () => void
}>()
</script>

<style scoped>
.empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 32px 16px;
  text-align: center;
  gap: 16px;
}

.empty-icon {
  font-size: 48px;
  margin: 0;
}

.empty-title {
  margin: 0;
  font-size: 18px;
  font-weight: 600;
  color: var(--color-text-primary);
}

.empty-description {
  margin: 0;
  color: var(--color-text-secondary);
  font-size: 14px;
}

.btn-primary {
  background: var(--color-primary);
  color: #ffffff;
  padding: 10px 24px;
  border-radius: 8px;
  border: none;
  cursor: pointer;
  font-weight: 600;
  transition: all 0.3s;
}

.btn-primary:hover {
  background: #0044cc;
  box-shadow: 0 8px 16px rgba(0, 85, 255, 0.4);
}
</style>
