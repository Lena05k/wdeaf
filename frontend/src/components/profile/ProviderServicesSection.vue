<template>
  <section class="provider-services-section">
    <!-- Header with Add Button -->
    <div class="section-header">
      <div class="header-title">
        <h2 class="title">📦 Мои услуги</h2>
        <span class="services-count">{{ services.length }}</span>
      </div>
      <button @click="$emit('add-service')" class="btn-add-service">
        <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <line x1="12" y1="5" x2="12" y2="19"></line>
          <line x1="5" y1="12" x2="19" y2="12"></line>
        </svg>
        Добавить услугу
      </button>
    </div>

    <!-- Services Grid -->
    <div v-if="services.length === 0" class="empty-state">
      <div class="empty-icon">📦</div>
      <h3>Услуг ещё нет</h3>
      <p>Добавьте первую услугу, чтобы начать принимать заказы</p>
      <button @click="$emit('add-service')" class="btn-add-first">
        <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <line x1="12" y1="5" x2="12" y2="19"></line>
          <line x1="5" y1="12" x2="19" y2="12"></line>
        </svg>
        Добавить первую услугу
      </button>
    </div>

    <div v-else class="services-grid">
      <div
        v-for="service in services"
        :key="service.id"
        class="service-card"
        @click="handleServiceClick(service)"
      >
        <!-- Card Background Image/Icon -->
        <div class="card-image">
          <div class="image-content">
            <span class="service-icon">🎨</span>
          </div>
        </div>

        <!-- Card Content -->
        <div class="card-content">
          <div class="card-header">
            <h3 class="service-title">{{ service.name }}</h3>
            <div class="card-actions" @click.stop>
              <button
                @click.stop="handleQuickEdit(service)"
                class="action-btn edit-btn"
                title="Редактировать"
              >
                <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <path d="M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7"></path>
                  <path d="M18.5 2.5a2.121 2.121 0 0 1 3 3L12 15l-4 1 1-4 9.5-9.5z"></path>
                </svg>
              </button>
              <button
                @click.stop="handleQuickDelete(service)"
                class="action-btn delete-btn"
                title="Удалить"
              >
                <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <polyline points="3 6 5 6 21 6"></polyline>
                  <path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"></path>
                  <line x1="10" y1="11" x2="10" y2="17"></line>
                  <line x1="14" y1="11" x2="14" y2="17"></line>
                </svg>
              </button>
            </div>
          </div>

          <!-- Category and Rating -->
          <p class="service-category">{{ service.category }}</p>

          <!-- Stats Row -->
          <div class="stats-row">
            <div class="stat">
              <span class="stat-value">{{ service.price }}</span>
              <span class="stat-label">₽</span>
            </div>
            <div class="stat">
              <span class="stat-value">{{ service.orders || 0 }}</span>
              <span class="stat-label">заказов</span>
            </div>
            <div class="stat">
              <span class="stat-value">{{ service.rating || 0 }}</span>
              <span class="stat-label">⭐</span>
            </div>
          </div>

          <!-- Description -->
          <p class="service-description">{{ truncateText(service.description, 80) }}</p>

          <!-- Footer Button -->
          <div class="card-footer">
            <span class="view-details">Подробнее →</span>
          </div>
        </div>
      </div>
    </div>

    <!-- Delete Confirmation Modal -->
    <Teleport to="body">
      <Transition name="fade">
        <div v-if="showDeleteConfirm" class="confirmation-overlay" @click.self="showDeleteConfirm = false">
          <div class="confirmation-dialog">
            <div class="confirm-icon">🗑️</div>
            <h3 class="confirm-title">Удалить услугу?</h3>
            <p class="confirm-text">{{ serviceToDelete?.name }}</p>
            <p class="confirm-description">Это действие нельзя отменить. Все данные об услуге будут удалены.</p>
            <div class="confirm-buttons">
              <button
                @click="showDeleteConfirm = false"
                class="btn btn-secondary"
              >
                Отменить
              </button>
              <button
                @click="confirmDelete"
                class="btn btn-danger"
              >
                Да, удалить
              </button>
            </div>
          </div>
        </div>
      </Transition>
    </Teleport>
  </section>
</template>

<script setup lang="ts">
import { ref } from 'vue'

interface Service {
  id: string | number
  name: string
  price: number
  category?: string
  description?: string
  orders?: number
  rating?: number
}

interface Props {
  services: Service[]
}

interface Emits {
  (e: 'add-service'): void
  (e: 'edit-service', service: Service): void
  (e: 'delete-service', serviceId: string | number): void
  (e: 'service-click', service: Service): void
}

defineProps<Props>()
const emit = defineEmits<Emits>()

const showDeleteConfirm = ref(false)
const serviceToDelete = ref<Service | null>(null)

const truncateText = (text: string | undefined, maxLength: number): string => {
  if (!text) return ''
  return text.length > maxLength ? text.substring(0, maxLength) + '...' : text
}

const handleServiceClick = (service: Service) => {
  emit('service-click', service)
}

const handleQuickEdit = (service: Service) => {
  emit('edit-service', service)
}

const handleQuickDelete = (service: Service) => {
  serviceToDelete.value = service
  showDeleteConfirm.value = true
}

const confirmDelete = () => {
  if (serviceToDelete.value) {
    emit('delete-service', serviceToDelete.value.id)
    showDeleteConfirm.value = false
    serviceToDelete.value = null
  }
}
</script>

<style scoped>
.provider-services-section {
  padding: 0;
}

/* Header */
.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 24px;
  gap: 12px;
}

.header-title {
  display: flex;
  align-items: center;
  gap: 10px;
}

.title {
  margin: 0;
  font-size: 1.5rem;
  font-weight: 700;
  color: white;
}

.services-count {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 32px;
  height: 32px;
  background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%);
  color: white;
  border-radius: 8px;
  font-weight: 600;
  font-size: 0.9rem;
}

.btn-add-service {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  padding: 10px 16px;
  background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%);
  color: white;
  border: none;
  border-radius: 10px;
  font-weight: 600;
  font-size: 0.9rem;
  cursor: pointer;
  transition: all 0.3s cubic-bezier(0.16, 1, 0.3, 1);
  box-shadow: 0 4px 12px rgba(37, 99, 235, 0.3);
}

.btn-add-service:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 20px rgba(37, 99, 235, 0.4);
}

.btn-add-service:active {
  transform: scale(0.98);
}

.btn-add-service svg {
  width: 20px;
  height: 20px;
}

/* Empty State */
.empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  min-height: 300px;
  background: linear-gradient(135deg, rgba(30, 41, 59, 0.3) 0%, rgba(30, 41, 59, 0.1) 100%);
  border: 1px dashed rgba(148, 163, 184, 0.3);
  border-radius: 16px;
  padding: 40px 20px;
  text-align: center;
}

.empty-icon {
  font-size: 3rem;
  margin-bottom: 16px;
  opacity: 0.6;
}

.empty-state h3 {
  margin: 0 0 8px 0;
  font-size: 1.1rem;
  font-weight: 600;
  color: #e2e8f0;
}

.empty-state p {
  margin: 0 0 20px 0;
  font-size: 0.9rem;
  color: #94a3b8;
}

.btn-add-first {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  padding: 12px 20px;
  background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%);
  color: white;
  border: none;
  border-radius: 10px;
  font-weight: 600;
  font-size: 0.95rem;
  cursor: pointer;
  transition: all 0.3s cubic-bezier(0.16, 1, 0.3, 1);
  box-shadow: 0 4px 12px rgba(37, 99, 235, 0.3);
}

.btn-add-first:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 20px rgba(37, 99, 235, 0.4);
}

.btn-add-first:active {
  transform: scale(0.98);
}

.btn-add-first svg {
  width: 20px;
  height: 20px;
}

/* Services Grid */
.services-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 16px;
  animation: fadeIn 0.4s ease;
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

/* Service Card */
.service-card {
  background: linear-gradient(135deg, rgba(30, 41, 59, 0.6) 0%, rgba(30, 41, 59, 0.3) 100%);
  border: 1px solid rgba(148, 163, 184, 0.2);
  border-radius: 16px;
  overflow: hidden;
  cursor: pointer;
  transition: all 0.3s cubic-bezier(0.16, 1, 0.3, 1);
  display: flex;
  flex-direction: column;
  height: 100%;
  backdrop-filter: blur(10px);
}

.service-card:hover {
  border-color: rgba(59, 130, 246, 0.4);
  background: linear-gradient(135deg, rgba(30, 41, 59, 0.8) 0%, rgba(30, 41, 59, 0.5) 100%);
  transform: translateY(-8px);
  box-shadow: 0 12px 40px rgba(0, 0, 0, 0.3), 0 0 1px rgba(59, 130, 246, 0.3);
}

/* Card Image */
.card-image {
  height: 120px;
  background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  position: relative;
  overflow: hidden;
}

.card-image::before {
  content: '';
  position: absolute;
  top: -50%;
  right: -50%;
  width: 200%;
  height: 200%;
  background: radial-gradient(circle, rgba(255, 255, 255, 0.1) 1px, transparent 1px);
  background-size: 50px 50px;
  animation: movePattern 20s linear infinite;
}

@keyframes movePattern {
  0% {
    transform: translate(0, 0);
  }
  100% {
    transform: translate(50px, 50px);
  }
}

.image-content {
  position: relative;
  z-index: 1;
}

.service-icon {
  font-size: 2.5rem;
  display: block;
}

/* Card Content */
.card-content {
  padding: 16px;
  display: flex;
  flex-direction: column;
  flex: 1;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  gap: 10px;
  margin-bottom: 10px;
}

.service-title {
  margin: 0;
  font-size: 1rem;
  font-weight: 700;
  color: white;
  line-height: 1.3;
  flex: 1;
}

.card-actions {
  display: flex;
  gap: 6px;
  flex-shrink: 0;
}

.action-btn {
  background: rgba(148, 163, 184, 0.1);
  border: 1px solid rgba(148, 163, 184, 0.2);
  color: #94a3b8;
  width: 32px;
  height: 32px;
  border-radius: 8px;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.2s ease;
  flex-shrink: 0;
}

.action-btn:hover {
  background: rgba(148, 163, 184, 0.2);
  border-color: rgba(148, 163, 184, 0.4);
}

.edit-btn:hover {
  color: #3b82f6;
  border-color: rgba(59, 130, 246, 0.4);
}

.delete-btn:hover {
  color: #ef4444;
  border-color: rgba(239, 68, 68, 0.4);
}

.action-btn:active {
  transform: scale(0.95);
}

.action-btn svg {
  width: 18px;
  height: 18px;
}

/* Category */
.service-category {
  margin: 0 0 12px 0;
  font-size: 0.75rem;
  font-weight: 600;
  color: #3b82f6;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

/* Stats Row */
.stats-row {
  display: flex;
  justify-content: space-between;
  gap: 10px;
  margin-bottom: 12px;
  padding-bottom: 12px;
  border-bottom: 1px solid rgba(148, 163, 184, 0.1);
}

.stat {
  flex: 1;
  display: flex;
  align-items: baseline;
  gap: 4px;
}

.stat-value {
  font-size: 1rem;
  font-weight: 700;
  color: #fbbf24;
}

.stat-label {
  font-size: 0.7rem;
  color: #94a3b8;
  font-weight: 500;
}

/* Description */
.service-description {
  margin: 0 0 12px 0;
  font-size: 0.8rem;
  color: #cbd5e1;
  line-height: 1.4;
  flex: 1;
}

/* Footer */
.card-footer {
  display: flex;
  justify-content: flex-end;
  padding-top: 12px;
  border-top: 1px solid rgba(148, 163, 184, 0.1);
}

.view-details {
  font-size: 0.75rem;
  color: #3b82f6;
  font-weight: 600;
  transition: color 0.2s ease;
}

.service-card:hover .view-details {
  color: #60a5fa;
}

/* Confirmation Modal */
.confirmation-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.6);
  backdrop-filter: blur(8px);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1001;
  padding: 20px;
}

.confirmation-dialog {
  background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%);
  border: 1px solid rgba(148, 163, 184, 0.2);
  border-radius: 16px;
  padding: 32px 24px;
  max-width: 380px;
  width: 100%;
  text-align: center;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
  animation: slideUp 0.3s cubic-bezier(0.16, 1, 0.3, 1);
}

@keyframes slideUp {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.confirm-icon {
  font-size: 2.5rem;
  display: block;
  margin-bottom: 16px;
  animation: pulse 1s ease-in-out infinite;
}

@keyframes pulse {
  0%, 100% {
    transform: scale(1);
  }
  50% {
    transform: scale(1.1);
  }
}

.confirm-title {
  margin: 0 0 8px 0;
  font-size: 1.25rem;
  font-weight: 700;
  color: white;
}

.confirm-text {
  margin: 0 0 8px 0;
  font-size: 1rem;
  font-weight: 600;
  color: #e2e8f0;
}

.confirm-description {
  margin: 0 0 24px 0;
  font-size: 0.9rem;
  color: #94a3b8;
  line-height: 1.5;
}

.confirm-buttons {
  display: flex;
  gap: 10px;
}

/* Buttons */
.btn {
  flex: 1;
  padding: 12px 16px;
  border: none;
  border-radius: 10px;
  font-weight: 600;
  font-size: 0.9rem;
  cursor: pointer;
  transition: all 0.3s ease;
  display: flex;
  align-items: center;
  justify-content: center;
}

.btn-secondary {
  background: rgba(148, 163, 184, 0.1);
  border: 1px solid rgba(148, 163, 184, 0.2);
  color: #e2e8f0;
}

.btn-secondary:hover {
  background: rgba(148, 163, 184, 0.2);
  border-color: rgba(148, 163, 184, 0.4);
}

.btn-secondary:active {
  transform: scale(0.98);
}

.btn-danger {
  background: linear-gradient(135deg, #ef4444 0%, #dc2626 100%);
  color: white;
  box-shadow: 0 4px 12px rgba(220, 38, 38, 0.3);
}

.btn-danger:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 20px rgba(220, 38, 38, 0.4);
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

/* Responsive */
@media (max-width: 768px) {
  .services-grid {
    grid-template-columns: repeat(auto-fill, minmax(240px, 1fr));
    gap: 12px;
  }

  .section-header {
    flex-wrap: wrap;
    margin-bottom: 20px;
  }

  .btn-add-service {
    width: 100%;
  }
}

@media (max-width: 480px) {
  .services-grid {
    grid-template-columns: 1fr;
  }

  .section-header {
    flex-direction: column;
    gap: 12px;
  }

  .header-title {
    width: 100%;
  }

  .btn-add-service {
    width: 100%;
  }

  .confirmation-dialog {
    padding: 24px 16px;
  }
}
</style>
