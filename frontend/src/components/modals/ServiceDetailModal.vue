<template>
  <Modal
    :is-open="isOpen"
    :title="service?.name || 'Детали услуги'"
    :large="true"
    @close="emit('close')"
  >
    <template v-if="service">
      <!-- Image Carousel -->
      <div v-if="service.images && service.images.length > 0" class="image-carousel">
        <img
          :src="service.images[currentImageIndex]"
          :alt="service.name"
          class="service-image"
        />
        <!-- Image Counter -->
        <div v-if="service.images.length > 1" class="image-counter">
          {{ currentImageIndex + 1 }}/{{ service.images.length }}
        </div>
        <!-- Navigation Arrows -->
        <div v-if="service.images.length > 1" class="image-nav">
          <button @click="prevImage" class="nav-btn nav-prev" aria-label="Предыдущее фото">‹</button>
          <button @click="nextImage" class="nav-btn nav-next" aria-label="Следующее фото">›</button>
        </div>
      </div>
      <div v-else class="image-placeholder">
        <p>Нет фотографий</p>
      </div>

      <!-- Provider Card -->
      <div class="provider-card">
        <div class="provider-header">
          <div class="avatar" :style="avatarStyle">{{ getInitials(service.provider) }}</div>
          <div class="provider-info">
            <h3 class="provider-name">{{ service.provider }}</h3>
            <p class="rating">
              <span class="stars">★</span> {{ service.providerRating }}
              <span class="reviews-count">({{ service.reviews }} отзывов)</span>
            </p>
          </div>
        </div>
        <div class="provider-meta">
          <div class="meta-item">
            <span class="meta-icon">📍</span>
            <span class="meta-text">Россия, {{ randomCity }}</span>
          </div>
          <div class="meta-item">
            <span class="meta-icon">⏱️</span>
            <span class="meta-text">Ответит {{ service.response_time }}</span>
          </div>
        </div>
      </div>

      <!-- Description Section -->
      <div class="description-section">
        <h4 class="section-title">Описание</h4>
        <p class="description-text">{{ service.fullDescription }}</p>
      </div>

      <!-- Service Details -->
      <div class="details-section">
        <h4 class="section-title">Информация об услуге</h4>
        <div class="details-grid">
          <div class="detail-item">
            <span class="detail-label">Категория</span>
            <span class="detail-value">{{ service.category }}</span>
          </div>
          <div class="detail-item">
            <span class="detail-label">Цена</span>
            <span class="detail-value detail-price">{{ formatPrice(service.price) }}</span>
          </div>
          <div class="detail-item">
            <span class="detail-label">Время ответа</span>
            <span class="detail-value">{{ service.response_time }}</span>
          </div>
          <div class="detail-item">
            <span class="detail-label">Рейтинг</span>
            <span class="detail-value">{{ service.providerRating }} / 5.0</span>
          </div>
        </div>
      </div>

      <!-- Reviews Section -->
      <div class="reviews-section">
        <h4 class="section-title">Отзывы</h4>
        <div class="reviews-list">
          <div v-for="review in displayedReviews" :key="review.id" class="review-item">
            <div class="review-header">
              <div class="reviewer-avatar">{{ getInitials(review.author) }}</div>
              <div class="reviewer-info">
                <p class="reviewer-name">{{ review.author }}</p>
                <p class="review-rating">★ {{ review.rating }}.0</p>
              </div>
            </div>
            <p class="review-text">{{ review.text }}</p>
            <p class="review-date">{{ review.date }}</p>
          </div>
          <button
            v-if="service.reviews > displayedReviews.length"
            @click="showAllReviews = !showAllReviews"
            class="btn-show-more"
          >
            {{ showAllReviews ? 'Скрыть отзывы' : `Показать все (${service.reviews})` }}
          </button>
        </div>
      </div>
    </template>

    <!-- Footer with Action Buttons -->
    <template #footer>
      <button
        class="btn btn-secondary"
        @click="emit('close')"
      >
        Назад
      </button>
      <button
        class="btn btn-primary"
        @click="contactProvider"
      >
        📞 Связаться
      </button>
    </template>
  </Modal>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import Modal from '@/components/shared/Modal.vue'

interface Props {
  isOpen: boolean
  service?: any
}

const props = defineProps<Props>()

const emit = defineEmits<{
  'close': []
  'contact-provider': [service: any]
}>()

const currentImageIndex = ref(0)
const showAllReviews = ref(false)

// Sample reviews data
const allReviews = [
  {
    id: 1,
    author: 'Александр П.',
    rating: 5,
    text: 'Отличная работа! Быстро и качественно выполнил заказ. Рекомендую!',
    date: '2 дня назад'
  },
  {
    id: 2,
    author: 'Мария К.',
    rating: 5,
    text: 'Все просто супер! Исполнитель очень ответственный и профессиональный.',
    date: '1 неделю назад'
  },
  {
    id: 3,
    author: 'Иван С.',
    rating: 4,
    text: 'Хорошо, но немного дольше чем обещал. В целом доволен.',
    date: '2 недели назад'
  },
  {
    id: 4,
    author: 'Ольга В.',
    rating: 5,
    text: 'Спасибо за помощь! Всё получилось отлично.',
    date: '3 недели назад'
  }
]

const cities = ['Москва', 'Санкт-Петербург', 'Екатеринбург', 'Новосибирск', 'Казань']
const randomCity = ref(cities[Math.floor(Math.random() * cities.length)])

const avatarStyle = computed(() => ({
  backgroundColor: '#2563eb',
  borderColor: '#2563eb'
}))

const displayedReviews = computed(() => {
  return showAllReviews.value ? allReviews : allReviews.slice(0, 2)
})

const getInitials = (name?: string): string => {
  if (!name) return '?'
  return name
    .split(' ')
    .map(word => word[0])
    .join('')
    .toUpperCase()
    .slice(0, 2)
}

const formatPrice = (price?: number) => {
  if (!price) return '—'
  return new Intl.NumberFormat('ru-RU', {
    style: 'currency',
    currency: 'RUB',
    minimumFractionDigits: 0
  }).format(price)
}

const nextImage = () => {
  if (props.service?.images) {
    currentImageIndex.value = (currentImageIndex.value + 1) % props.service.images.length
  }
}

const prevImage = () => {
  if (props.service?.images) {
    currentImageIndex.value = (currentImageIndex.value - 1 + props.service.images.length) % props.service.images.length
  }
}

const contactProvider = () => {
  emit('contact-provider', props.service)
}
</script>

<style scoped>
/* Image Carousel */
.image-carousel {
  position: relative;
  width: 100%;
  aspect-ratio: 1.2 / 1;
  background: #f5f5f5;
  overflow: hidden;
  margin: -16px -16px 16px -16px;
  border-radius: 0;
}

.service-image {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.image-placeholder {
  width: 100%;
  height: 200px;
  background: #f5f5f5;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #999;
  font-size: 0.875rem;
  margin: -16px -16px 16px -16px;
  border-radius: 0;
}

.image-counter {
  position: absolute;
  bottom: 12px;
  right: 12px;
  background: rgba(0, 0, 0, 0.6);
  color: white;
  padding: 6px 12px;
  border-radius: 8px;
  font-size: 0.75rem;
  font-weight: 600;
  backdrop-filter: blur(4px);
}

.image-nav {
  position: absolute;
  top: 50%;
  left: 0;
  right: 0;
  transform: translateY(-50%);
  display: flex;
  justify-content: space-between;
  padding: 0 12px;
  pointer-events: none;
}

.nav-btn {
  pointer-events: all;
  background: rgba(0, 0, 0, 0.4);
  color: white;
  border: none;
  width: 40px;
  height: 40px;
  border-radius: 50%;
  font-size: 1.5rem;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: background 0.2s ease;
}

.nav-btn:hover {
  background: rgba(0, 0, 0, 0.6);
}

/* Provider Card */
.provider-card {
  background: #f9f9f9;
  border-radius: 12px;
  padding: 16px;
  margin-bottom: 20px;
}

.provider-header {
  display: flex;
  gap: 12px;
  align-items: center;
  margin-bottom: 12px;
}

.avatar {
  width: 56px;
  height: 56px;
  border-radius: 50%;
  background: #2563eb;
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 700;
  font-size: 1rem;
  flex-shrink: 0;
}

.provider-info {
  flex: 1;
}

.provider-name {
  font-weight: 700;
  font-size: 0.95rem;
  color: #000;
  margin: 0 0 4px 0;
}

.rating {
  font-size: 0.8rem;
  color: #666;
  margin: 0;
  display: flex;
  align-items: center;
  gap: 4px;
}

.stars {
  color: #ffa500;
  font-size: 1rem;
}

.reviews-count {
  color: #999;
  font-size: 0.75rem;
}

.provider-meta {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.meta-item {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 0.8rem;
  color: #666;
}

.meta-icon {
  font-size: 0.9rem;
}

.meta-text {
  line-height: 1.3;
}

/* Sections */
.section-title {
  font-size: 0.95rem;
  font-weight: 700;
  color: #000;
  margin: 0 0 12px 0;
}

.description-section,
.details-section,
.reviews-section {
  margin-bottom: 20px;
}

.description-text {
  font-size: 0.85rem;
  line-height: 1.6;
  color: #666;
  margin: 0;
}

/* Details Grid */
.details-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 12px;
}

.detail-item {
  background: white;
  border: 1px solid #e5e5e5;
  border-radius: 8px;
  padding: 12px;
  display: flex;
  flex-direction: column;
}

.detail-label {
  font-size: 0.7rem;
  color: #999;
  font-weight: 600;
  margin-bottom: 4px;
  text-transform: uppercase;
}

.detail-value {
  font-size: 0.9rem;
  font-weight: 600;
  color: #000;
}

.detail-price {
  color: #2563eb;
  font-size: 1rem;
}

/* Reviews */
.reviews-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.review-item {
  background: #f9f9f9;
  border-radius: 8px;
  padding: 12px;
}

.review-header {
  display: flex;
  gap: 10px;
  align-items: center;
  margin-bottom: 8px;
}

.reviewer-avatar {
  width: 36px;
  height: 36px;
  border-radius: 50%;
  background: #e5e5e5;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 700;
  font-size: 0.75rem;
  flex-shrink: 0;
}

.reviewer-info {
  flex: 1;
}

.reviewer-name {
  font-weight: 600;
  font-size: 0.8rem;
  color: #000;
  margin: 0 0 2px 0;
}

.review-rating {
  font-size: 0.75rem;
  color: #ffa500;
  margin: 0;
}

.review-text {
  font-size: 0.8rem;
  color: #666;
  line-height: 1.4;
  margin: 0 0 6px 0;
}

.review-date {
  font-size: 0.7rem;
  color: #999;
  margin: 0;
}

.btn-show-more {
  width: 100%;
  padding: 10px 12px;
  background: none;
  border: 1px solid #e5e5e5;
  border-radius: 8px;
  color: #2563eb;
  font-weight: 600;
  font-size: 0.8rem;
  cursor: pointer;
  transition: all 0.2s ease;
  margin-top: 8px;
}

.btn-show-more:hover {
  background: #f9f9f9;
  border-color: #2563eb;
}

/* Buttons */
.btn {
  flex: 1;
  padding: 12px 16px;
  border: none;
  border-radius: 8px;
  font-weight: 600;
  font-size: 0.875rem;
  cursor: pointer;
  transition: all 0.2s ease;
}

.btn-primary {
  background: #2563eb;
  color: white;
}

.btn-primary:hover {
  background: #1d4ed8;
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(37, 99, 235, 0.3);
}

.btn-primary:active {
  transform: scale(0.98);
}

.btn-secondary {
  background: #f0f0f0;
  color: #000;
}

.btn-secondary:hover {
  background: #e0e0e0;
  transform: translateY(-1px);
}

.btn-secondary:active {
  transform: scale(0.98);
}

/* Dark mode */
@media (prefers-color-scheme: dark) {
  .provider-card,
  .detail-item,
  .review-item,
  .image-placeholder {
    background: #2a2a2a;
  }

  .detail-item {
    border-color: #333;
  }

  .provider-name,
  .detail-value,
  .reviewer-name {
    color: #fff;
  }

  .provider-meta,
  .description-text,
  .review-text,
  .meta-item {
    color: #aaa;
  }

  .image-placeholder {
    color: #666;
  }

  .btn-show-more {
    border-color: #333;
    background: none;
  }

  .btn-show-more:hover {
    background: #333;
    border-color: #2563eb;
  }

  .btn-secondary {
    background: #333;
    color: #fff;
  }

  .btn-secondary:hover {
    background: #444;
  }
}
</style>