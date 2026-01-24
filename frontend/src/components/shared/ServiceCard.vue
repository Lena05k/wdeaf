<template>
  <div class="service-card" @click="emit('select', service)">
    <!-- Image Carousel Section -->
    <div class="carousel-wrapper">
      <ImageCarousel
        :images="service.images"
        @update:index="currentImageIndex = $event"
      />
      
      <!-- Image Counter Badge -->
      <div v-if="service.images && service.images.length > 1" class="image-counter">
        {{ (currentImageIndex || 0) + 1 }}/{{ service.images.length }}
      </div>
    </div>

    <!-- Content Section -->
    <div class="card-content">
      <!-- Header with Category Badge -->
      <div class="card-header">
        <div class="header-left">
          <h3 class="service-name">{{ service.name }}</h3>
          <p class="provider-name">{{ service.provider }}</p>
        </div>
        <span class="category-badge">{{ service.category }}</span>
      </div>

      <!-- Description -->
      <p class="service-description">
        {{ service.description }}
      </p>

      <!-- Footer with Rating and Price -->
      <div class="card-footer">
        <div class="rating-section">
          <span class="rating">★ {{ service.providerRating }}</span>
          <span class="reviews">({{ service.reviews }})</span>
        </div>
        <span class="price">{{ formatPrice(service.price) }}</span>
      </div>

      <!-- Order Button -->
      <button
        class="btn-order"
        @click.stop="emit('order', service)"
      >
        Заказать
      </button>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import ImageCarousel from './ImageCarousel.vue'

const props = defineProps({
  service: {
    type: Object,
    required: true
  }
})

const emit = defineEmits(['select', 'order'])
const currentImageIndex = ref(0)

const formatPrice = (price) => {
  if (!price) return '—'
  return new Intl.NumberFormat('ru-RU', {
    style: 'currency',
    currency: 'RUB',
    minimumFractionDigits: 0
  }).format(price)
}
</script>

<style scoped>
.service-card {
  background: var(--color-surface, #fff);
  border-radius: 12px;
  overflow: hidden;
  cursor: pointer;
  transition: all 0.3s cubic-bezier(0.16, 1, 0.3, 1);
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
  border: 1px solid var(--color-card-border, #e5e5e5);
  display: flex;
  flex-direction: column;
  height: 100%;
}

.service-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.12);
  border-color: var(--color-primary, #0055FF);
}

.service-card:active {
  transform: translateY(-2px);
}

/* Carousel Section */
.carousel-wrapper {
  position: relative;
  width: 100%;
  aspect-ratio: 1.2 / 1;
  background: var(--color-bg-secondary, #f9f9f9);
  overflow: hidden;
}

.image-counter {
  position: absolute;
  bottom: 8px;
  right: 8px;
  background: rgba(0, 0, 0, 0.6);
  color: white;
  padding: 4px 8px;
  border-radius: 6px;
  font-size: 0.75rem;
  font-weight: 600;
  backdrop-filter: blur(4px);
}

/* Content Section */
.card-content {
  padding: 12px 12px 12px 12px;
  flex: 1;
  display: flex;
  flex-direction: column;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  gap: 8px;
  margin-bottom: 8px;
}

.header-left {
  flex: 1;
  min-width: 0;
}

.service-name {
  font-size: 0.95rem;
  font-weight: 600;
  color: var(--color-text, #000);
  margin: 0;
  line-height: 1.3;
  word-break: break-word;
}

.provider-name {
  font-size: 0.75rem;
  color: var(--color-text-secondary, #666);
  margin: 2px 0 0 0;
}

.category-badge {
  display: inline-block;
  padding: 4px 8px;
  background: var(--color-bg-1, #e0f0ff);
  color: var(--color-primary, #0055FF);
  border-radius: 6px;
  font-size: 0.7rem;
  font-weight: 600;
  white-space: nowrap;
  flex-shrink: 0;
}

/* Description */
.service-description {
  font-size: 0.8rem;
  color: var(--color-text-secondary, #666);
  margin: 0 0 8px 0;
  line-height: 1.4;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

/* Footer with Rating and Price */
.card-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 10px;
  padding-top: 8px;
  border-top: 1px solid var(--color-border, #e5e5e5);
}

.rating-section {
  display: flex;
  align-items: center;
  gap: 4px;
}

.rating {
  font-size: 0.8rem;
  font-weight: 600;
  color: #ffa500;
}

.reviews {
  font-size: 0.7rem;
  color: var(--color-text-secondary, #999);
}

.price {
  font-size: 0.9rem;
  font-weight: 700;
  color: var(--color-primary, #0055FF);
}

/* Order Button */
.btn-order {
  width: 100%;
  padding: 10px 12px;
  background: var(--color-primary, #0055FF);
  color: white;
  border: none;
  border-radius: 8px;
  font-size: 0.875rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s ease;
  margin-top: auto;
}

.btn-order:hover {
  background: var(--color-primary-hover, #0044cc);
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(0, 85, 255, 0.3);
}

.btn-order:active {
  transform: scale(0.98);
}

/* Dark mode support */
@media (prefers-color-scheme: dark) {
  .service-card {
    background: #1e1e1e;
    border-color: #333;
  }
  
  .carousel-wrapper {
    background: #2a2a2a;
  }
  
  .service-name {
    color: #fff;
  }
  
  .provider-name {
    color: #aaa;
  }
  
  .service-description {
    color: #999;
  }
  
  .category-badge {
    background: rgba(0, 85, 255, 0.15);
    color: #60a5fa;
  }
  
  .card-footer {
    border-top-color: #333;
  }
}
</style>
