<template>
  <div v-if="isOpen" class="modal-overlay" @click="closeModal">
    <div class="modal-content" @click.stop>
      <!-- Header -->
      <div class="modal-header">
        <h2 class="modal-title">{{ service.name }}</h2>
        <button @click="closeModal" class="btn-close">
          <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <line x1="18" y1="6" x2="6" y2="18"></line>
            <line x1="6" y1="6" x2="18" y2="18"></line>
          </svg>
        </button>
      </div>

      <!-- Scrollable Content -->
      <div class="modal-body">
        <!-- Image Carousel -->
        <div class="image-carousel" v-if="service.images && service.images.length > 0">
          <img
            :src="service.images[currentImageIndex]"
            :alt="service.name"
            class="carousel-image"
          />
          <button
            v-if="service.images.length > 1"
            @click="prevImage"
            class="carousel-btn prev"
            aria-label="Previous image"
          >
            <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <polyline points="15 18 9 12 15 6"></polyline>
            </svg>
          </button>
          <button
            v-if="service.images.length > 1"
            @click="nextImage"
            class="carousel-btn next"
            aria-label="Next image"
          >
            <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <polyline points="9 18 15 12 9 6"></polyline>
            </svg>
          </button>

          <!-- Image Dots -->
          <div class="carousel-dots" v-if="service.images.length > 1">
            <button
              v-for="(_, idx) in service.images"
              :key="idx"
              :class="['dot', { active: idx === currentImageIndex }]"
              @click="currentImageIndex = idx"
              :aria-label="`Image ${idx + 1}`"
            />
          </div>
        </div>

        <!-- Service Info -->
        <div class="service-info">
          <div class="info-row">
            <span class="label">Категория</span>
            <span class="value">{{ service.category }}</span>
          </div>
          <div class="info-row">
            <span class="label">Цена</span>
            <span class="value price">{{ service.price }} ₽</span>
          </div>
          <div class="info-row" v-if="service.reviews">
            <span class="label">Отзывы</span>
            <span class="value">⭐ {{ service.reviews }}</span>
          </div>
        </div>

        <!-- Description -->
        <div class="description-section" v-if="service.description">
          <h3 class="section-title">Описание</h3>
          <p class="description-text">{{ service.description }}</p>
        </div>

        <!-- Provider Info -->
        <div class="provider-section" v-if="service.provider">
          <h3 class="section-title">Исполнитель</h3>
          <div class="provider-card">
            <div class="provider-avatar">
              <div class="avatar-placeholder">{{ service.provider.charAt(0).toUpperCase() }}</div>
            </div>
            <div class="provider-details">
              <p class="provider-name">{{ service.provider }}</p>
              <p class="provider-meta" v-if="service.providerId">
                ID: {{ service.providerId }}
              </p>
            </div>
          </div>
        </div>
      </div>

      <!-- Footer Action Buttons -->
      <div class="modal-footer">
        <button
          v-if="!isProvider && !isSaved"
          @click="emit('save')"
          class="btn btn-secondary"
        >
          <span class="btn-icon">📑</span>
          Сохранить
        </button>
        <button
          v-if="!isProvider && isSaved"
          @click="emit('unsave')"
          class="btn btn-secondary"
        >
          <span class="btn-icon">📕</span>
          Удалить
        </button>
        <button
          v-if="isProvider"
          @click="emit('edit')"
          class="btn btn-secondary"
        >
          <span class="btn-icon">✏️</span>
          Редактировать
        </button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'

interface Service {
  id: string | number
  name: string
  price: number
  description: string
  category: string
  provider?: string
  providerId?: string
  images?: string[]
  reviews?: number
  currentImageIndex?: number
}

interface Props {
  isOpen: boolean
  service: Service
  isProvider?: boolean
  isSaved?: boolean
}

defineProps<Props>()

const emit = defineEmits<{
  (e: 'close'): void
  (e: 'save'): void
  (e: 'unsave'): void
  (e: 'edit'): void
}>()

const currentImageIndex = ref(0)

const closeModal = () => emit('close')

const nextImage = () => {
  const service = defineProps<Props>().service as Service
  if (!service.images || service.images.length === 0) return
  currentImageIndex.value = (currentImageIndex.value + 1) % service.images.length
}

const prevImage = () => {
  const service = defineProps<Props>().service as Service
  if (!service.images || service.images.length === 0) return
  currentImageIndex.value = (currentImageIndex.value - 1 + service.images.length) % service.images.length
}
</script>

<style scoped>
.modal-overlay {
  position: fixed;
  inset: 0;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: flex-end;
  z-index: 1000;
  padding: 0;
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

.modal-content {
  background: var(--color-surface, #fff);
  width: 100%;
  max-height: 90vh;
  border-radius: 20px 20px 0 0;
  display: flex;
  flex-direction: column;
  box-shadow: 0 -2px 20px rgba(0, 0, 0, 0.1);
  animation: slideUp 0.3s ease;
}

@keyframes slideUp {
  from {
    transform: translateY(100%);
  }
  to {
    transform: translateY(0);
  }
}

.modal-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 16px 20px;
  border-bottom: 1px solid var(--color-border, #e0e0e0);
  flex-shrink: 0;
}

.modal-title {
  font-size: 18px;
  font-weight: 600;
  color: var(--color-text, #000);
  margin: 0;
  flex: 1;
}

.btn-close {
  background: none;
  border: none;
  cursor: pointer;
  color: var(--color-text, #000);
  padding: 4px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 50%;
  transition: background 0.2s;
}

.btn-close:hover {
  background: var(--color-secondary, rgba(0, 0, 0, 0.05));
}

.modal-body {
  flex: 1;
  overflow-y: auto;
  -webkit-overflow-scrolling: touch;
  padding: 16px;
}

.image-carousel {
  position: relative;
  width: 100%;
  height: 280px;
  background: #f0f0f0;
  border-radius: 12px;
  overflow: hidden;
  margin-bottom: 20px;
}

.carousel-image {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.carousel-btn {
  position: absolute;
  top: 50%;
  transform: translateY(-50%);
  background: rgba(0, 85, 255, 0.9);
  color: white;
  border: none;
  width: 40px;
  height: 40px;
  border-radius: 50%;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.2s;
  z-index: 10;
}

.carousel-btn:hover {
  background: rgba(0, 85, 255, 1);
  transform: translateY(-50%) scale(1.1);
}

.carousel-btn.prev {
  left: 12px;
}

.carousel-btn.next {
  right: 12px;
}

.carousel-dots {
  position: absolute;
  bottom: 12px;
  left: 50%;
  transform: translateX(-50%);
  display: flex;
  gap: 8px;
  z-index: 10;
}

.dot {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background: rgba(255, 255, 255, 0.5);
  border: none;
  cursor: pointer;
  transition: all 0.2s;
  padding: 0;
}

.dot:hover {
  background: rgba(255, 255, 255, 0.7);
}

.dot.active {
  background: #0055FF;
}

.service-info {
  background: var(--color-secondary, rgba(0, 0, 0, 0.03));
  border-radius: 12px;
  padding: 16px;
  margin-bottom: 20px;
}

.info-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 8px 0;
  border-bottom: 1px solid var(--color-border, #e0e0e0);
}

.info-row:last-child {
  border-bottom: none;
}

.label {
  font-size: 14px;
  color: var(--color-text-secondary, #666);
  font-weight: 500;
}

.value {
  font-size: 14px;
  color: var(--color-text, #000);
  font-weight: 600;
}

.value.price {
  color: #0055FF;
  font-size: 16px;
}

.description-section {
  margin-bottom: 20px;
}

.section-title {
  font-size: 16px;
  font-weight: 600;
  color: var(--color-text, #000);
  margin: 0 0 12px 0;
}

.description-text {
  font-size: 14px;
  line-height: 1.6;
  color: var(--color-text, #000);
  margin: 0;
}

.provider-section {
  margin-bottom: 20px;
}

.provider-card {
  display: flex;
  align-items: center;
  gap: 12px;
  background: var(--color-secondary, rgba(0, 0, 0, 0.03));
  border-radius: 12px;
  padding: 12px;
}

.provider-avatar {
  flex-shrink: 0;
}

.avatar-placeholder {
  width: 48px;
  height: 48px;
  border-radius: 50%;
  background: linear-gradient(135deg, #0055FF, #0088FF);
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 600;
  font-size: 20px;
}

.provider-details {
  flex: 1;
  min-width: 0;
}

.provider-name {
  font-size: 14px;
  font-weight: 600;
  color: var(--color-text, #000);
  margin: 0;
}

.provider-meta {
  font-size: 12px;
  color: var(--color-text-secondary, #666);
  margin: 4px 0 0 0;
}

.modal-footer {
  display: flex;
  gap: 12px;
  padding: 16px 20px;
  border-top: 1px solid var(--color-border, #e0e0e0);
  flex-shrink: 0;
}

.btn {
  flex: 1;
  padding: 12px 16px;
  border: none;
  border-radius: 8px;
  font-size: 14px;
  font-weight: 600;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  transition: all 0.2s;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.btn-icon {
  font-size: 16px;
}

.btn-secondary {
  background: var(--color-secondary, rgba(0, 0, 0, 0.08));
  color: var(--color-text, #000);
  border: 1px solid var(--color-border, #e0e0e0);
}

.btn-secondary:hover {
  background: var(--color-secondary, rgba(0, 0, 0, 0.12));
  transform: translateY(-2px);
}

.btn-secondary:active {
  transform: translateY(0);
}

/* Mobile optimization */
@media (max-width: 768px) {
  .modal-content {
    max-height: 95vh;
  }

  .image-carousel {
    height: 240px;
  }

  .modal-body {
    padding: 12px;
  }

  .modal-footer {
    padding: 12px 16px;
  }
}
</style>
