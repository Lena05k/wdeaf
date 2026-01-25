<template>
  <Teleport to="body">
    <!-- Backdrop -->
    <Transition name="fade">
      <div
        v-if="isOpen"
        class="modal-backdrop"
        @click="closeModal"
      />
    </Transition>

    <!-- Modal -->
    <Transition name="slide-up">
      <div
        v-if="isOpen"
        class="modal-container"
        @touchstart="handleTouchStart"
        @touchmove="handleTouchMove"
        @touchend="handleTouchEnd"
      >
        <!-- Drag Handle -->
        <div class="drag-handle" />

        <!-- Content -->
        <div class="modal-content">
          <!-- EDIT MODE: Form -->
          <div v-if="isEditMode" class="edit-form">
            <h2 class="edit-title">Редактировать услугу</h2>
            
            <div class="form-group">
              <label class="form-label">Название услуги</label>
              <input
                v-model="formData.name"
                type="text"
                class="form-input"
                placeholder="Введите название"
              />
            </div>

            <div class="form-group">
              <label class="form-label">Категория</label>
              <input
                v-model="formData.category"
                type="text"
                class="form-input"
                placeholder="Введите категорию"
              />
            </div>

            <div class="form-group">
              <label class="form-label">Цена (₽)</label>
              <input
                v-model.number="formData.price"
                type="number"
                class="form-input"
                placeholder="Введите цену"
              />
            </div>

            <div class="form-group">
              <label class="form-label">Описание</label>
              <textarea
                v-model="formData.fullDescription"
                class="form-textarea"
                placeholder="Введите описание услуги"
                rows="4"
              ></textarea>
            </div>

            <p class="form-note">📷 Галерею нельзя редактировать в этом окне</p>
          </div>

          <!-- VIEW MODE: Service Details -->
          <div v-else>
            <!-- Image Carousel -->
            <div v-if="service?.images && service.images.length > 0" class="image-section">
              <div class="image-carousel">
                <img
                  :src="service.images[currentImageIndex]"
                  :alt="service.name"
                  class="service-image"
                />
                <!-- Image Counter -->
                <div v-if="service.images.length > 1" class="image-counter">
                  <span>{{ currentImageIndex + 1 }}/{{ service.images.length }}</span>
                </div>
                <!-- Navigation Arrows -->
                <div v-if="service.images.length > 1" class="image-nav">
                  <button
                    @click="prevImage"
                    class="nav-btn nav-prev"
                    aria-label="Предыдущее фото"
                  >
                    <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                      <polyline points="15 18 9 12 15 6"></polyline>
                    </svg>
                  </button>
                  <button
                    @click="nextImage"
                    class="nav-btn nav-next"
                    aria-label="Следующее фото"
                  >
                    <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                      <polyline points="9 18 15 12 9 6"></polyline>
                    </svg>
                  </button>
                </div>
              </div>
            </div>
            <div v-else class="image-placeholder">
              <svg width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
                <rect x="3" y="3" width="18" height="18" rx="2" ry="2"></rect>
                <circle cx="8.5" cy="8.5" r="1.5"></circle>
                <polyline points="21 15 16 10 5 21"></polyline>
              </svg>
            </div>

            <!-- Provider Info (only show if not provider mode) -->
            <div v-if="!isProviderMode" class="provider-section">
              <div class="provider-header">
                <div class="avatar">{{ getInitials(service?.provider) }}</div>
                <div class="provider-meta">
                  <h2 class="provider-name">{{ service?.provider }}</h2>
                  <div class="rating-row">
                    <span class="stars">★</span>
                    <span class="rating-value">{{ service?.providerRating }}</span>
                    <span class="reviews-count">({{ service?.reviews }} отзывов)</span>
                  </div>
                  <div class="location">📍 Россия, {{ randomCity }}</div>
                </div>
              </div>
            </div>

            <!-- Service Title -->
            <h1 class="service-title">{{ service?.name }}</h1>

            <!-- Service Details Grid -->
            <div class="details-grid">
              <div class="detail-card">
                <span class="detail-label">Цена</span>
                <span class="detail-value detail-price">{{ formatPrice(service?.price) }}</span>
              </div>
              <div class="detail-card">
                <span class="detail-label">Время ответа</span>
                <span class="detail-value">{{ service?.response_time || 'Сразу' }}</span>
              </div>
              <div class="detail-card">
                <span class="detail-label">Категория</span>
                <span class="detail-value">{{ service?.category }}</span>
              </div>
              <div v-if="!isProviderMode" class="detail-card">
                <span class="detail-label">Рейтинг</span>
                <span class="detail-value">{{ service?.providerRating }}/5.0</span>
              </div>
            </div>

            <!-- Description -->
            <div class="description-section">
              <h3 class="section-title">Описание</h3>
              <p class="description-text">{{ service?.fullDescription }}</p>
            </div>

            <!-- Reviews (only show if not provider mode) -->
            <div v-if="!isProviderMode" class="reviews-section">
              <h3 class="section-title">Отзывы</h3>
              <div class="reviews-list">
                <div v-for="review in displayedReviews" :key="review.id" class="review-item">
                  <div class="review-top">
                    <div class="review-avatar">{{ getInitials(review.author) }}</div>
                    <div class="review-info">
                      <p class="review-author">{{ review.author }}</p>
                      <p class="review-date">{{ review.date }}</p>
                    </div>
                    <div class="review-rating">★ {{ review.rating }}</div>
                  </div>
                  <p class="review-text">{{ review.text }}</p>
                </div>
              </div>
              <button
                v-if="service && service.reviews > displayedReviews.length"
                @click="showAllReviews = !showAllReviews"
                class="btn-show-more"
              >
                {{ showAllReviews ? 'Свернуть' : `Показать все (${service.reviews})` }}
              </button>
            </div>
          </div>
        </div>

        <!-- Bottom Action -->
        <div class="modal-footer">
          <!-- Provider Mode: Edit/Delete Buttons -->
          <div v-if="isProviderMode" class="button-group">
            <button
              class="btn btn-secondary"
              @click="toggleEditMode"
            >
              <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7"></path>
                <path d="M18.5 2.5a2.121 2.121 0 0 1 3 3L12 15l-4 1 1-4 9.5-9.5z"></path>
              </svg>
              {{ isEditMode ? 'Отменить' : 'Редактировать' }}
            </button>
            <button
              class="btn btn-danger"
              @click="confirmDelete"
            >
              <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <polyline points="3 6 5 6 21 6"></polyline>
                <path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"></path>
              </svg>
              Удалить
            </button>
          </div>

          <!-- Save/Contact Button (conditional) -->
          <div v-if="!isProviderMode" class="button-group">
            <button
              class="btn btn-primary"
              @click="contactProvider"
            >
              <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72 12.84 12.84 0 0 0 .7 2.81 2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45 12.84 12.84 0 0 0 2.81.7A2 2 0 0 1 22 16.92z"></path>
              </svg>
              Связаться с исполнителем
            </button>
          </div>
          <div v-else-if="isEditMode" class="button-group">
            <button
              class="btn btn-primary"
              @click="saveChanges"
            >
              <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M19 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h11l5 5v11a2 2 0 0 1-2 2z"></path>
                <polyline points="17 21 17 13 7 13 7 21"></polyline>
                <polyline points="7 3 7 8 15 8"></polyline>
              </svg>
              Сохранить
            </button>
          </div>
        </div>
      </div>
    </Transition>

    <!-- Delete Confirmation Modal -->
    <Transition name="fade">
      <div v-if="showDeleteConfirm" class="confirmation-overlay" @click.self="showDeleteConfirm = false">
        <div class="confirmation-dialog">
          <h3 class="confirmation-title">Удалить услугу?</h3>
          <p class="confirmation-text">Это действие нельзя отменить. Все данные об услуге будут удалены.</p>
          <div class="confirmation-buttons">
            <button
              class="btn btn-secondary"
              @click="showDeleteConfirm = false"
            >
              Нет
            </button>
            <button
              class="btn btn-danger"
              @click="handleDelete"
            >
              Да, удалить
            </button>
          </div>
        </div>
      </div>
    </Transition>
  </Teleport>
</template>

<script setup lang="ts">
import { ref, computed, watch } from 'vue'

interface Props {
  isOpen: boolean
  service?: any
  isProviderMode?: boolean
}

const props = withDefaults(defineProps<Props>(), {
  isProviderMode: false
})

const emit = defineEmits<{
  'close': []
  'contact-provider': [service: any]
  'edit': [service: any]
  'delete': [serviceId: string | number]
}>()

const currentImageIndex = ref(0)
const showAllReviews = ref(false)
const touchStartY = ref(0)
const touchCurrentY = ref(0)
const isEditMode = ref(false)
const showDeleteConfirm = ref(false)

const formData = ref({
  name: '',
  category: '',
  price: 0,
  fullDescription: ''
})

watch(() => props.service, (newService) => {
  if (newService) {
    formData.value = {
      name: newService.name || '',
      category: newService.category || '',
      price: newService.price || 0,
      fullDescription: newService.fullDescription || ''
    }
  }
}, { immediate: true })

watch(() => props.isOpen, (newOpen) => {
  if (!newOpen) {
    isEditMode.value = false
    showDeleteConfirm.value = false
  }
}, { immediate: true })

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

const closeModal = () => {
  isEditMode.value = false
  emit('close')
}

const contactProvider = () => {
  emit('contact-provider', props.service)
}

const toggleEditMode = () => {
  isEditMode.value = !isEditMode.value
  if (!isEditMode.value && props.service) {
    // Reset form when canceling
    formData.value = {
      name: props.service.name || '',
      category: props.service.category || '',
      price: props.service.price || 0,
      fullDescription: props.service.fullDescription || ''
    }
  }
}

const saveChanges = () => {
  emit('edit', {
    ...props.service,
    ...formData.value
  })
  isEditMode.value = false
}

const confirmDelete = () => {
  showDeleteConfirm.value = true
}

const handleDelete = () => {
  emit('delete', props.service?.id)
  showDeleteConfirm.value = false
  closeModal()
}

const handleTouchStart = (e: TouchEvent) => {
  touchStartY.value = e.touches[0].clientY
}

const handleTouchMove = (e: TouchEvent) => {
  touchCurrentY.value = e.touches[0].clientY
}

const handleTouchEnd = () => {
  const diff = touchCurrentY.value - touchStartY.value
  // Если свайп вниз больше чем 60px - закрываем модалку
  if (diff > 60 && !isEditMode.value) {
    closeModal()
  }
  touchStartY.value = 0
  touchCurrentY.value = 0
}
</script>

<style scoped>
/* Backdrop */
.modal-backdrop {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.4);
  backdrop-filter: blur(4px);
  z-index: 999;
}

/* Modal Container */
.modal-container {
  position: fixed;
  bottom: 0;
  left: 0;
  right: 0;
  max-height: 92vh;
  background: linear-gradient(135deg, #ffffff 0%, #f8f9fa 100%);
  border-radius: 24px 24px 0 0;
  display: flex;
  flex-direction: column;
  z-index: 1000;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.15);
  overflow: hidden;
}

/* Drag Handle */
.drag-handle {
  width: 40px;
  height: 4px;
  background: #d1d5db;
  border-radius: 2px;
  margin: 12px auto 0;
}

/* Modal Content */
.modal-content {
  flex: 1;
  overflow-y: auto;
  padding: 16px 16px 20px;
  scroll-behavior: smooth;
}

.modal-content::-webkit-scrollbar {
  width: 4px;
}

.modal-content::-webkit-scrollbar-track {
  background: transparent;
}

.modal-content::-webkit-scrollbar-thumb {
  background: #d1d5db;
  border-radius: 2px;
}

/* Edit Form */
.edit-form {
  animation: fadeIn 0.3s ease;
}

@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.edit-title {
  font-size: 1.25rem;
  font-weight: 700;
  color: #111827;
  margin: 0 0 20px 0;
}

.form-group {
  margin-bottom: 16px;
}

.form-label {
  display: block;
  font-size: 0.8rem;
  font-weight: 600;
  color: #374151;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  margin-bottom: 6px;
}

.form-input,
.form-textarea {
  width: 100%;
  padding: 12px;
  border: 1px solid #e5e7eb;
  border-radius: 10px;
  font-family: inherit;
  font-size: 0.95rem;
  color: #111827;
  background: rgba(255, 255, 255, 0.8);
  transition: all 0.3s ease;
  box-sizing: border-box;
}

.form-input:focus,
.form-textarea:focus {
  outline: none;
  border-color: #3b82f6;
  box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
  background: white;
}

.form-textarea {
  resize: vertical;
  font-family: inherit;
}

.form-note {
  font-size: 0.8rem;
  color: #6b7280;
  margin-top: 16px;
  padding: 10px;
  background: rgba(251, 191, 36, 0.1);
  border-left: 3px solid #fbbf24;
  border-radius: 6px;
}

/* Image Section */
.image-section {
  margin: 0 -16px 20px -16px;
}

.image-carousel {
  position: relative;
  width: 100%;
  aspect-ratio: 1.2 / 1;
  background: linear-gradient(135deg, #e5e7eb 0%, #d1d5db 100%);
  overflow: hidden;
}

.service-image {
  width: 100%;
  height: 100%;
  object-fit: cover;
  display: block;
}

.image-placeholder {
  width: 100%;
  height: 200px;
  background: linear-gradient(135deg, #f3f4f6 0%, #e5e7eb 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  color: #9ca3af;
  margin: 0 -16px 20px -16px;
}

.image-placeholder svg {
  opacity: 0.6;
}

.image-counter {
  position: absolute;
  bottom: 12px;
  right: 12px;
  background: rgba(0, 0, 0, 0.5);
  backdrop-filter: blur(12px);
  color: white;
  padding: 6px 12px;
  border-radius: 12px;
  font-size: 0.75rem;
  font-weight: 600;
}

.image-counter span {
  display: block;
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
  background: rgba(255, 255, 255, 0.3);
  backdrop-filter: blur(12px);
  color: white;
  border: 1px solid rgba(255, 255, 255, 0.2);
  width: 40px;
  height: 40px;
  border-radius: 50%;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.3s cubic-bezier(0.16, 1, 0.3, 1);
}

.nav-btn:hover {
  background: rgba(255, 255, 255, 0.4);
  border-color: rgba(255, 255, 255, 0.3);
  transform: scale(1.1);
}

.nav-btn:active {
  transform: scale(0.95);
}

.nav-btn svg {
  width: 20px;
  height: 20px;
}

/* Provider Section */
.provider-section {
  margin-bottom: 20px;
}

.provider-header {
  display: flex;
  gap: 12px;
  align-items: flex-start;
}

.avatar {
  width: 56px;
  height: 56px;
  border-radius: 16px;
  background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%);
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 700;
  font-size: 1.1rem;
  flex-shrink: 0;
  box-shadow: 0 4px 12px rgba(37, 99, 235, 0.3);
}

.provider-meta {
  flex: 1;
}

.provider-name {
  font-weight: 700;
  font-size: 1rem;
  color: #111827;
  margin: 0 0 6px 0;
}

.rating-row {
  display: flex;
  align-items: center;
  gap: 6px;
  margin-bottom: 6px;
}

.stars {
  color: #f59e0b;
  font-size: 1rem;
}

.rating-value {
  font-weight: 600;
  font-size: 0.9rem;
  color: #111827;
}

.reviews-count {
  color: #6b7280;
  font-size: 0.8rem;
}

.location {
  font-size: 0.8rem;
  color: #6b7280;
  margin-top: 4px;
}

/* Service Title */
.service-title {
  font-size: 1.25rem;
  font-weight: 700;
  color: #111827;
  margin: 0 0 20px 0;
  line-height: 1.3;
}

/* Details Grid */
.details-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 10px;
  margin-bottom: 24px;
}

.detail-card {
  background: rgba(255, 255, 255, 0.8);
  backdrop-filter: blur(12px);
  border: 1px solid rgba(229, 231, 235, 0.8);
  border-radius: 12px;
  padding: 12px;
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.detail-label {
  font-size: 0.7rem;
  color: #6b7280;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.detail-value {
  font-size: 0.95rem;
  font-weight: 600;
  color: #111827;
}

.detail-price {
  color: #2563eb;
  font-size: 1.1rem;
}

/* Sections */
.section-title {
  font-size: 0.95rem;
  font-weight: 700;
  color: #111827;
  margin: 0 0 12px 0;
}

.description-section,
.reviews-section {
  margin-bottom: 24px;
}

.description-text {
  font-size: 0.85rem;
  line-height: 1.6;
  color: #4b5563;
  margin: 0;
}

/* Reviews */
.reviews-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
  margin-bottom: 12px;
}

.review-item {
  background: rgba(255, 255, 255, 0.6);
  backdrop-filter: blur(8px);
  border: 1px solid rgba(229, 231, 235, 0.5);
  border-radius: 12px;
  padding: 12px;
}

.review-top {
  display: flex;
  gap: 10px;
  align-items: center;
  margin-bottom: 8px;
}

.review-avatar {
  width: 32px;
  height: 32px;
  border-radius: 8px;
  background: linear-gradient(135deg, #e5e7eb 0%, #d1d5db 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 700;
  font-size: 0.7rem;
  flex-shrink: 0;
}

.review-info {
  flex: 1;
}

.review-author {
  font-weight: 600;
  font-size: 0.8rem;
  color: #111827;
  margin: 0;
}

.review-date {
  font-size: 0.7rem;
  color: #9ca3af;
  margin: 2px 0 0 0;
}

.review-rating {
  font-size: 0.8rem;
  color: #f59e0b;
  font-weight: 600;
}

.review-text {
  font-size: 0.8rem;
  color: #4b5563;
  line-height: 1.5;
  margin: 0;
}

.btn-show-more {
  width: 100%;
  padding: 10px 12px;
  background: rgba(255, 255, 255, 0.6);
  backdrop-filter: blur(8px);
  border: 1px solid rgba(229, 231, 235, 0.8);
  border-radius: 10px;
  color: #2563eb;
  font-weight: 600;
  font-size: 0.8rem;
  cursor: pointer;
  transition: all 0.3s ease;
}

.btn-show-more:hover {
  background: rgba(255, 255, 255, 0.8);
  border-color: #2563eb;
}

.btn-show-more:active {
  transform: scale(0.98);
}

/* Footer */
.modal-footer {
  padding: 16px;
  background: linear-gradient(180deg, transparent 0%, rgba(255, 255, 255, 0.8) 20%, #ffffff 100%);
  backdrop-filter: blur(12px);
  border-top: 1px solid rgba(229, 231, 235, 0.5);
}

.button-group {
  display: flex;
  gap: 10px;
  width: 100%;
}

.button-group .btn {
  flex: 1;
}

/* Button */
.btn {
  padding: 14px 16px;
  border: none;
  border-radius: 12px;
  font-weight: 600;
  font-size: 0.95rem;
  cursor: pointer;
  transition: all 0.3s cubic-bezier(0.16, 1, 0.3, 1);
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
}

.btn-primary {
  background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%);
  color: white;
  box-shadow: 0 8px 24px rgba(37, 99, 235, 0.3);
}

.btn-primary:hover {
  transform: translateY(-2px);
  box-shadow: 0 12px 32px rgba(37, 99, 235, 0.4);
}

.btn-primary:active {
  transform: scale(0.98);
}

.btn-secondary {
  background: rgba(255, 255, 255, 0.8);
  color: #374151;
  border: 1px solid rgba(229, 231, 235, 0.8);
}

.btn-secondary:hover {
  background: white;
  border-color: #d1d5db;
}

.btn-secondary:active {
  transform: scale(0.98);
}

.btn-danger {
  background: linear-gradient(135deg, #ef4444 0%, #dc2626 100%);
  color: white;
  box-shadow: 0 8px 24px rgba(220, 38, 38, 0.3);
}

.btn-danger:hover {
  transform: translateY(-2px);
  box-shadow: 0 12px 32px rgba(220, 38, 38, 0.4);
}

.btn-danger:active {
  transform: scale(0.98);
}

.btn svg {
  width: 20px;
  height: 20px;
}

/* Confirmation Modal */
.confirmation-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.5);
  backdrop-filter: blur(8px);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1001;
  animation: fadeIn 0.3s ease;
}

.confirmation-dialog {
  background: white;
  border-radius: 16px;
  padding: 24px;
  max-width: 320px;
  width: 90%;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
  animation: slideUp 0.3s cubic-bezier(0.16, 1, 0.3, 1);
}

.confirmation-title {
  font-size: 1.1rem;
  font-weight: 700;
  color: #111827;
  margin: 0 0 10px 0;
}

.confirmation-text {
  font-size: 0.9rem;
  color: #6b7280;
  margin: 0 0 20px 0;
  line-height: 1.5;
}

.confirmation-buttons {
  display: flex;
  gap: 10px;
}

.confirmation-buttons .btn {
  flex: 1;
  padding: 12px;
  font-size: 0.9rem;
}

/* Animations */
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.3s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}

.slide-up-enter-active,
.slide-up-leave-active {
  transition: all 0.35s cubic-bezier(0.16, 1, 0.3, 1);
}

.slide-up-enter-from {
  transform: translateY(100%);
  opacity: 0;
}

.slide-up-leave-to {
  transform: translateY(100%);
  opacity: 0;
}

/* Dark Mode */
@media (prefers-color-scheme: dark) {
  .modal-container {
    background: linear-gradient(135deg, #1f2937 0%, #111827 100%);
  }

  .provider-name,
  .service-title,
  .section-title,
  .detail-value,
  .review-author,
  .edit-title {
    color: #f3f4f6;
  }

  .description-text,
  .location,
  .reviews-count,
  .review-text,
  .detail-label {
    color: #d1d5db;
  }

  .detail-card,
  .review-item {
    background: rgba(31, 41, 55, 0.6);
    border-color: rgba(75, 85, 99, 0.3);
  }

  .drag-handle {
    background: #4b5563;
  }

  .btn-show-more {
    background: rgba(31, 41, 55, 0.6);
    border-color: rgba(75, 85, 99, 0.3);
  }

  .btn-show-more:hover {
    background: rgba(31, 41, 55, 0.8);
  }

  .form-input,
  .form-textarea {
    background: rgba(31, 41, 55, 0.8);
    border-color: rgba(75, 85, 99, 0.3);
    color: #f3f4f6;
  }

  .form-input:focus,
  .form-textarea:focus {
    border-color: #3b82f6;
    box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
    background: rgba(31, 41, 55, 0.9);
  }

  .form-label {
    color: #d1d5db;
  }

  .form-note {
    background: rgba(180, 83, 9, 0.1);
  }

  .confirmation-dialog {
    background: #1f2937;
  }

  .confirmation-title {
    color: #f3f4f6;
  }

  .confirmation-text {
    color: #d1d5db;
  }

  .btn-secondary {
    background: rgba(75, 85, 99, 0.2);
    color: #f3f4f6;
    border-color: rgba(75, 85, 99, 0.3);
  }

  .btn-secondary:hover {
    background: rgba(75, 85, 99, 0.3);
    border-color: rgba(75, 85, 99, 0.5);
  }
}
</style>