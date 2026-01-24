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
          <!-- Status Badge -->
          <div class="status-section">
            <span :class="['status-badge', `status-${order?.status}`]">
              {{ getStatusLabel(order?.status) }}
            </span>
          </div>

          <!-- Service Title -->
          <h1 class="service-title">{{ order?.service }}</h1>

          <!-- Provider Info -->
          <div class="provider-section">
            <div class="provider-header">
              <div class="avatar">{{ getInitials(order?.provider) }}</div>
              <div class="provider-info">
                <h3 class="provider-name">{{ order?.provider }}</h3>
                <p class="provider-role">Исполнитель</p>
              </div>
            </div>
          </div>

          <!-- Order Details Grid -->
          <div class="details-grid">
            <div class="detail-card">
              <span class="detail-label">Стоимость</span>
              <span class="detail-value detail-price">{{ formatPrice(order?.price) }}</span>
            </div>
            <div class="detail-card">
              <span class="detail-label">Статус</span>
              <span class="detail-value">{{ getStatusLabel(order?.status) }}</span>
            </div>
            <div class="detail-card">
              <span class="detail-label">Дата заказа</span>
              <span class="detail-value">{{ formatDate(order?.date) }}</span>
            </div>
            <div v-if="order?.deadline" class="detail-card">
              <span class="detail-label">Крайний срок</span>
              <span class="detail-value">{{ formatDate(order?.deadline) }}</span>
            </div>
          </div>

          <!-- Category -->
          <div v-if="order?.category" class="info-section">
            <h3 class="section-title">Категория</h3>
            <p class="info-text">{{ order.category }}</p>
          </div>

          <!-- Description -->
          <div v-if="order?.description" class="description-section">
            <h3 class="section-title">Описание заказа</h3>
            <p class="description-text">{{ order.description }}</p>
          </div>

          <!-- Timeline -->
          <div class="timeline-section">
            <h3 class="section-title">История</h3>
            <div class="timeline">
              <div class="timeline-item">
                <div class="timeline-dot"></div>
                <div class="timeline-content">
                  <p class="timeline-title">Заказ создан</p>
                  <p class="timeline-date">{{ formatDate(order?.date) }}</p>
                </div>
              </div>
              <div v-if="order?.status === 'active'" class="timeline-item">
                <div class="timeline-dot timeline-dot-active"></div>
                <div class="timeline-content">
                  <p class="timeline-title">В процессе</p>
                  <p class="timeline-date">Исполнитель работает над заказом</p>
                </div>
              </div>
              <div v-else-if="order?.status === 'completed'" class="timeline-item">
                <div class="timeline-dot timeline-dot-completed"></div>
                <div class="timeline-content">
                  <p class="timeline-title">Завершено</p>
                  <p class="timeline-date">Заказ успешно выполнен</p>
                </div>
              </div>
              <div v-else-if="order?.status === 'cancelled'" class="timeline-item">
                <div class="timeline-dot timeline-dot-cancelled"></div>
                <div class="timeline-content">
                  <p class="timeline-title">Отменено</p>
                  <p class="timeline-date">Заказ был отменен</p>
                </div>
              </div>
              <div v-else class="timeline-item">
                <div class="timeline-dot"></div>
                <div class="timeline-content">
                  <p class="timeline-title">Ожидание подтверждения</p>
                  <p class="timeline-date">Исполнитель рассматривает заказ</p>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Footer with Actions -->
        <div class="modal-footer">
          <button
            v-if="order?.status === 'pending'"
            class="btn btn-danger"
            @click="cancelOrder"
          >
            Отменить заказ
          </button>
          <button
            v-else
            class="btn btn-primary"
            @click="sendMessage"
          >
            Написать исполнителю
          </button>
        </div>
      </div>
    </Transition>
  </Teleport>
</template>

<script setup lang="ts">
import { ref } from 'vue'

interface Order {
  id: string | number
  service: string
  provider: string
  status: 'active' | 'pending' | 'completed' | 'cancelled'
  price: number
  date: string | Date
  deadline?: string | Date
  description?: string
  category?: string
}

interface Props {
  isOpen: boolean
  order?: Order
}

const props = defineProps<Props>()

const emit = defineEmits<{
  'close': []
  'cancel': [order: Order]
  'message': [order: Order]
}>()

const touchStartY = ref(0)
const touchCurrentY = ref(0)

const getStatusLabel = (status?: string): string => {
  const labels: Record<string, string> = {
    'active': 'Активен',
    'pending': 'Ожидание',
    'completed': 'Завершено',
    'cancelled': 'Отменено'
  }
  return labels[status || ''] || 'Неизвестно'
}

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
  if (!price) return 'Не указано'
  return new Intl.NumberFormat('ru-RU', {
    style: 'currency',
    currency: 'RUB',
    minimumFractionDigits: 0
  }).format(price)
}

const formatDate = (date: string | Date | undefined): string => {
  if (!date) return 'Не указано'
  const d = new Date(date)
  const options: Intl.DateTimeFormatOptions = {
    month: 'short',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit'
  }
  return d.toLocaleDateString('ru-RU', options)
}

const closeModal = () => {
  emit('close')
}

const cancelOrder = () => {
  if (props.order) {
    emit('cancel', props.order)
  }
}

const sendMessage = () => {
  if (props.order) {
    emit('message', props.order)
  }
}

const handleTouchStart = (e: TouchEvent) => {
  touchStartY.value = e.touches[0].clientY
}

const handleTouchMove = (e: TouchEvent) => {
  touchCurrentY.value = e.touches[0].clientY
}

const handleTouchEnd = () => {
  const diff = touchCurrentY.value - touchStartY.value
  if (diff > 60) {
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

.modal-content::-webkit-scrollbar-thumb {
  background: #d1d5db;
  border-radius: 2px;
}

/* Status Section */
.status-section {
  margin-bottom: 16px;
}

.status-badge {
  display: inline-block;
  padding: 6px 12px;
  border-radius: 12px;
  font-size: 0.8rem;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.status-active {
  background: rgba(34, 197, 94, 0.1);
  color: #22c55e;
  border: 1px solid rgba(34, 197, 94, 0.3);
}

.status-pending {
  background: rgba(245, 158, 11, 0.1);
  color: #f59e0b;
  border: 1px solid rgba(245, 158, 11, 0.3);
}

.status-completed {
  background: rgba(34, 197, 94, 0.1);
  color: #22c55e;
  border: 1px solid rgba(34, 197, 94, 0.3);
}

.status-cancelled {
  background: rgba(239, 68, 68, 0.1);
  color: #ef4444;
  border: 1px solid rgba(239, 68, 68, 0.3);
}

/* Service Title */
.service-title {
  font-size: 1.5rem;
  font-weight: 700;
  color: #111827;
  margin: 0 0 20px 0;
  line-height: 1.3;
}

/* Provider Section */
.provider-section {
  margin-bottom: 24px;
}

.provider-header {
  display: flex;
  gap: 12px;
  align-items: center;
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

.provider-info {
  flex: 1;
}

.provider-name {
  font-weight: 700;
  font-size: 1rem;
  color: #111827;
  margin: 0;
}

.provider-role {
  font-size: 0.8rem;
  color: #6b7280;
  margin: 4px 0 0 0;
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

/* Info Sections */
.info-section,
.description-section,
.timeline-section {
  margin-bottom: 24px;
}

.section-title {
  font-size: 0.95rem;
  font-weight: 700;
  color: #111827;
  margin: 0 0 12px 0;
}

.info-text,
.description-text {
  font-size: 0.85rem;
  line-height: 1.6;
  color: #4b5563;
  margin: 0;
}

/* Timeline */
.timeline {
  position: relative;
  padding-left: 24px;
}

.timeline::before {
  content: '';
  position: absolute;
  left: 8px;
  top: 0;
  bottom: 0;
  width: 2px;
  background: linear-gradient(180deg, #d1d5db 0%, transparent 100%);
}

.timeline-item {
  position: relative;
  margin-bottom: 20px;
  padding-bottom: 0;
}

.timeline-item:last-child {
  margin-bottom: 0;
}

.timeline-dot {
  position: absolute;
  left: -24px;
  top: 2px;
  width: 12px;
  height: 12px;
  border-radius: 50%;
  background: #d1d5db;
  border: 2px solid white;
  box-shadow: 0 0 0 2px #d1d5db;
}

.timeline-dot-active {
  background: #3b82f6;
  box-shadow: 0 0 0 2px #3b82f6, 0 0 8px rgba(59, 130, 246, 0.5);
}

.timeline-dot-completed {
  background: #22c55e;
  box-shadow: 0 0 0 2px #22c55e;
}

.timeline-dot-cancelled {
  background: #ef4444;
  box-shadow: 0 0 0 2px #ef4444;
}

.timeline-title {
  font-weight: 600;
  font-size: 0.9rem;
  color: #111827;
  margin: 0 0 4px 0;
}

.timeline-date {
  font-size: 0.8rem;
  color: #6b7280;
  margin: 0;
}

/* Footer */
.modal-footer {
  padding: 16px;
  background: linear-gradient(180deg, transparent 0%, rgba(255, 255, 255, 0.8) 20%, #ffffff 100%);
  backdrop-filter: blur(12px);
  border-top: 1px solid rgba(229, 231, 235, 0.5);
}

/* Button */
.btn {
  width: 100%;
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

  .service-title,
  .section-title,
  .detail-value,
  .provider-name,
  .timeline-title {
    color: #f3f4f6;
  }

  .provider-role,
  .detail-label,
  .info-text,
  .description-text,
  .timeline-date {
    color: #d1d5db;
  }

  .detail-card {
    background: rgba(31, 41, 55, 0.6);
    border-color: rgba(75, 85, 99, 0.3);
  }

  .drag-handle {
    background: #4b5563;
  }

  .timeline::before {
    background: linear-gradient(180deg, #4b5563 0%, transparent 100%);
  }
}
</style>