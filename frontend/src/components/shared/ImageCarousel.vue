<template>
  <div class="image-carousel" @touchstart="handleTouchStart" @touchend="handleTouchEnd">
    <!-- Main Image with Smooth Transition -->
    <div class="carousel-inner">
      <img
        :src="images[currentIndex]"
        :alt="'Image ' + currentIndex"
        class="carousel-image"
        @error="handleImageError"
      />
    </div>

    <!-- Navigation Arrows (only visible on hover for mobile-friendly) -->
    <button
      v-if="images.length > 1"
      class="carousel-nav prev"
      @click.stop="prevImage"
      aria-label="Previous image"
    >
      <svg width="20" height="20" viewBox="0 0 20 20" fill="none">
        <path d="M12.5 5L7.5 10L12.5 15" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
      </svg>
    </button>

    <button
      v-if="images.length > 1"
      class="carousel-nav next"
      @click.stop="nextImage"
      aria-label="Next image"
    >
      <svg width="20" height="20" viewBox="0 0 20 20" fill="none">
        <path d="M7.5 5L12.5 10L7.5 15" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
      </svg>
    </button>

    <!-- Dots Indicators (Instagram-style) -->
    <div v-if="images.length > 1" class="carousel-dots">
      <button
        v-for="(_, idx) in images"
        :key="idx"
        :class="['dot', { active: idx === currentIndex }]"
        @click.stop="goToImage(idx)"
        :aria-label="`Go to image ${idx + 1}`"
      />
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'

const props = defineProps({
  images: {
    type: Array,
    required: true,
    default: () => []
  }
})

const emit = defineEmits(['update:index'])
const currentIndex = ref(0)
const touchStartX = ref(0)

const prevImage = () => {
  currentIndex.value = (currentIndex.value - 1 + props.images.length) % props.images.length
  emit('update:index', currentIndex.value)
}

const nextImage = () => {
  currentIndex.value = (currentIndex.value + 1) % props.images.length
  emit('update:index', currentIndex.value)
}

const goToImage = (idx) => {
  currentIndex.value = idx
  emit('update:index', currentIndex.value)
}

// Touch swipe support for mobile
const handleTouchStart = (e) => {
  touchStartX.value = e.touches[0].clientX
}

const handleTouchEnd = (e) => {
  const touchEndX = e.changedTouches[0].clientX
  const diff = touchStartX.value - touchEndX
  
  if (Math.abs(diff) > 50) {
    if (diff > 0) {
      nextImage()
    } else {
      prevImage()
    }
  }
}

const handleImageError = () => {
  // Placeholder for failed image load
  console.warn('Image failed to load at index:', currentIndex.value)
}
</script>

<style scoped>
.image-carousel {
  position: relative;
  width: 100%;
  height: 100%;
  overflow: hidden;
  background: linear-gradient(135deg, #f5f5f5 0%, #e9e9e9 100%);
  display: flex;
  align-items: center;
  justify-content: center;
}

.carousel-inner {
  width: 100%;
  height: 100%;
  position: relative;
  display: flex;
  align-items: center;
  justify-content: center;
}

.carousel-image {
  width: 100%;
  height: 100%;
  object-fit: cover;
  animation: fadeIn 0.3s ease-in-out;
}

@keyframes fadeIn {
  from {
    opacity: 0.8;
  }
  to {
    opacity: 1;
  }
}

/* Navigation Arrows */
.carousel-nav {
  position: absolute;
  top: 50%;
  transform: translateY(-50%);
  background: rgba(0, 0, 0, 0.4);
  color: white;
  border: none;
  width: 36px;
  height: 36px;
  border-radius: 50%;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.2s ease;
  opacity: 0;
  z-index: 10;
}

.carousel-nav:hover {
  background: rgba(0, 0, 0, 0.6);
  opacity: 1;
}

.carousel-nav.prev {
  left: 8px;
}

.carousel-nav.next {
  right: 8px;
}

/* Show arrows on focus for accessibility */
.carousel-nav:focus-visible {
  opacity: 1;
  outline: 2px solid rgba(255, 255, 255, 0.5);
  outline-offset: -2px;
}

/* Dots Indicators (Instagram-style) */
.carousel-dots {
  position: absolute;
  bottom: 8px;
  left: 50%;
  transform: translateX(-50%);
  display: flex;
  gap: 4px;
  z-index: 5;
}

.dot {
  width: 6px;
  height: 6px;
  border-radius: 50%;
  background: rgba(255, 255, 255, 0.5);
  border: none;
  cursor: pointer;
  transition: all 0.2s ease;
  padding: 0;
}

.dot:hover {
  background: rgba(255, 255, 255, 0.7);
}

.dot.active {
  background: rgba(255, 255, 255, 1);
  width: 8px;
}

/* Mobile optimizations */
@media (max-width: 768px) {
  .carousel-nav {
    width: 32px;
    height: 32px;
  }
  
  .carousel-nav svg {
    width: 16px;
    height: 16px;
  }
}

/* Touch-device specific */
@media (hover: none) and (pointer: coarse) {
  .carousel-nav {
    opacity: 0.6;
  }
  
  .carousel-nav:active {
    background: rgba(0, 0, 0, 0.7);
  }
}
</style>
