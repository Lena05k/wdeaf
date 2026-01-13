<template>
  <div class="lightbox-overlay" @click.self="emit('close')">
    <button class="lightbox-close" @click="emit('close')">✕</button>

    <button v-if="currentIndex > 0" class="lightbox-nav prev" @click="emit('prev')">
      ‹
    </button>

    <img
        :src="images[currentIndex].image_url"
        :alt="images[currentIndex].title"
        class="lightbox-image"
    />

    <button v-if="currentIndex < images.length - 1" class="lightbox-nav next" @click="emit('next')">
      ›
    </button>

    <div class="lightbox-info">
      <h3 class="lightbox-title">{{ images[currentIndex].title }}</h3>
      <p class="lightbox-description">{{ images[currentIndex].description }}</p>
      <p class="lightbox-counter">{{ currentIndex + 1 }} / {{ images.length }}</p>
    </div>
  </div>
</template>

<script setup lang="ts">
import { defineProps, defineEmits } from 'vue'

interface PortfolioItem {
  id: number
  image_url: string
  title: string
  description: string
}

defineProps<{
  images: PortfolioItem[]
  currentIndex: number
}>()

defineEmits<{
  close: []
  prev: []
  next: []
}>()
</script>

<style scoped>
.lightbox-overlay {
  position: fixed;
  inset: 0;
  background: rgba(0, 0, 0, 0.95);
  z-index: 2000;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 16px;
  animation: fadeIn 0.3s ease;
}

@keyframes fadeIn {
  from {
    opacity: 0;
  }
  to {
    opacity: 1;
  }
}

.lightbox-image {
  max-width: 90%;
  max-height: 70vh;
  object-fit: contain;
  border-radius: 8px;
}

.lightbox-nav {
  position: absolute;
  top: 50%;
  transform: translateY(-50%);
  background: rgba(0, 85, 255, 0.8);
  color: #ffffff;
  border: none;
  width: 44px;
  height: 44px;
  border-radius: 50%;
  cursor: pointer;
  font-size: 24px;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: background 0.3s;
  z-index: 10;
}

.lightbox-nav:hover {
  background: #0055ff;
}

.lightbox-nav.prev {
  left: 16px;
}

.lightbox-nav.next {
  right: 16px;
}

.lightbox-close {
  position: absolute;
  top: 16px;
  right: 16px;
  background: rgba(0, 85, 255, 0.8);
  color: #ffffff;
  border: none;
  width: 40px;
  height: 40px;
  border-radius: 50%;
  cursor: pointer;
  font-size: 24px;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: background 0.3s;
}

.lightbox-close:hover {
  background: #0055ff;
}

.lightbox-info {
  background: rgba(0, 0, 0, 0.7);
  color: #ffffff;
  padding: 16px;
  border-radius: 8px;
  max-width: 400px;
  text-align: center;
}

.lightbox-title {
  margin: 0 0 8px 0;
  font-size: 16px;
  font-weight: 700;
}

.lightbox-description {
  margin: 0 0 8px 0;
  font-size: 13px;
  opacity: 0.8;
}

.lightbox-counter {
  margin: 0;
  font-size: 12px;
  opacity: 0.6;
}
</style>
