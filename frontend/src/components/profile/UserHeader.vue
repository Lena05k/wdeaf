<template>
  <div class="user-header">
    <!-- Hero Section: Avatar + Name (iOS 18 style) -->
    <div class="hero-section">
      <!-- Avatar -->
      <div class="avatar-container">
        <div class="w-24 h-24 bg-gradient-to-br from-blue-500 to-blue-600 rounded-full flex items-center justify-center text-5xl font-bold text-white shadow-lg">
          {{ user.first_name?.charAt(0).toUpperCase() || 'У' }}
        </div>
      </div>

      <!-- Name & Username -->
      <div class="user-info-center">
        <h1 class="text-2xl font-bold text-white">{{ user.first_name }}</h1>
        <p class="text-sm text-gray-400">@{{ user.username }}</p>
        <p v-if="isProvider" class="text-xs text-green-400 mt-1.5">✓ Исполнитель</p>
        <p v-else class="text-xs text-blue-400 mt-1.5">✓ Клиент</p>
      </div>

      <!-- Action Buttons -->
      <div class="flex gap-2 w-full px-2">
        <button
          v-if="!isProvider"
          @click="$emit('become-provider')"
          class="flex-1 bg-gradient-to-r from-blue-600 to-blue-500 hover:from-blue-500 hover:to-blue-400 text-white font-semibold py-2.5 rounded-lg transition active:scale-95"
        >
          💼 Стать исполнителем
        </button>
        <button
          v-else
          @click="openAddServiceModal"
          class="flex-1 bg-gradient-to-r from-green-600 to-green-500 hover:from-green-500 hover:to-green-400 text-white font-semibold py-2.5 rounded-lg transition active:scale-95"
        >
          ➕ Добавить услугу
        </button>
        <button
          @click="$emit('edit-profile')"
          class="bg-slate-700 hover:bg-slate-600 text-white px-4 py-2.5 rounded-lg transition active:scale-95"
        >
          ⚙️
        </button>
      </div>
    </div>

    <!-- ======================== ТОЛЬКО КЛИЕНТ (Нет исполнителя) ======================== -->
    <template v-if="!isProvider">
      <div class="settings-container">
        <!-- История заказов -->
        <div class="settings-section">
          <h2 class="settings-section-title">ВЫ КУПИЛИ</h2>

          <div class="settings-cell-group">
            <!-- My Orders -->
            <button 
              @click="$emit('view-orders')"
              class="settings-cell border-b border-slate-700 hover-cell"
            >
              <div class="cell-icon bg-blue-500">📋</div>
              <div class="cell-content">
                <p class="cell-label">Мои заказы</p>
                <p class="cell-value">{{ ordersCount }} заказов</p>
              </div>
              <svg class="w-5 h-5 text-gray-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7" />
              </svg>
            </button>

            <!-- My Reviews -->
            <button 
              @click="$emit('view-reviews')"
              class="settings-cell border-b border-slate-700 hover-cell"
            >
              <div class="cell-icon bg-yellow-500">⭐</div>
              <div class="cell-content">
                <p class="cell-label">Мои отзывы</p>
                <p class="cell-value">{{ reviewsCount }} отзывов</p>
              </div>
              <svg class="w-5 h-5 text-gray-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7" />
              </svg>
            </button>

            <!-- Saved Services -->
            <button 
              @click="$emit('view-saved')"
              class="settings-cell hover-cell"
            >
              <div class="cell-icon bg-red-500">❤️</div>
              <div class="cell-content">
                <p class="cell-label">Сохраненные услуги</p>
                <p class="cell-value">{{ savedCount }} услуг</p>
              </div>
              <svg class="w-5 h-5 text-gray-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7" />
              </svg>
            </button>
          </div>
        </div>
      </div>
    </template>

    <!-- ======================== ИСПОЛНИТЕЛЬ (может быть одновременно клиентом) ======================== -->
    <template v-else>
      <div class="settings-container">
        <!-- РАЗДЕЛ: Входящие заказы (только исполнитель) -->
        <div class="settings-section">
          <h2 class="settings-section-title">ЗАКАЗЫ ДЛЯ ВАС</h2>

          <div class="settings-cell-group">
            <!-- Incoming Orders -->
            <button 
              @click="$emit('view-incoming-orders')"
              class="settings-cell border-b border-slate-700 hover-cell"
            >
              <div class="cell-icon bg-orange-500">📬</div>
              <div class="cell-content">
                <p class="cell-label">Входящие заказы</p>
                <p class="cell-value">{{ incomingOrdersCount }} новых</p>
              </div>
              <svg class="w-5 h-5 text-gray-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7" />
              </svg>
            </button>

            <!-- Active Orders -->
            <button 
              @click="$emit('view-active-orders')"
              class="settings-cell border-b border-slate-700 hover-cell"
            >
              <div class="cell-icon bg-blue-500">⚡</div>
              <div class="cell-content">
                <p class="cell-label">Активные заказы</p>
                <p class="cell-value">{{ activeOrdersCount }} в работе</p>
              </div>
              <svg class="w-5 h-5 text-gray-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7" />
              </svg>
            </button>

            <!-- Completed Orders -->
            <button 
              @click="$emit('view-completed-orders')"
              class="settings-cell hover-cell"
            >
              <div class="cell-icon bg-green-500">✅</div>
              <div class="cell-content">
                <p class="cell-label">Завершенные</p>
                <p class="cell-value">{{ completedOrdersCount }} заказов</p>
              </div>
              <svg class="w-5 h-5 text-gray-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7" />
              </svg>
            </button>
          </div>
        </div>

        <!-- РАЗДЕЛ: Мои услуги -->
        <div class="settings-section">
          <h2 class="settings-section-title">УСЛУГИ</h2>

          <div class="settings-cell-group">
            <!-- My Services -->
            <button 
              @click="$emit('view-services')"
              class="settings-cell hover-cell"
            >
              <div class="cell-icon bg-purple-500">📦</div>
              <div class="cell-content">
                <p class="cell-label">Мои услуги</p>
                <p class="cell-value">{{ servicesCount }} услуг</p>
              </div>
              <svg class="w-5 h-5 text-gray-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7" />
              </svg>
            </button>
          </div>
        </div>

        <!-- РАЗДЕЛ: Репутация исполнителя -->
        <div class="settings-section">
          <h2 class="settings-section-title">МОЯ РЕПУТАЦИЯ</h2>

          <div class="settings-cell-group">
            <!-- Rating -->
            <button 
              @click="$emit('view-rating')"
              class="settings-cell hover-cell"
            >
              <div class="cell-icon bg-yellow-500">⭐</div>
              <div class="cell-content">
                <p class="cell-label">Рейтинг</p>
                <p class="cell-value">{{ providerRating }}/5 ({{ providerReviews }} отзывов)</p>
              </div>
              <svg class="w-5 h-5 text-gray-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7" />
              </svg>
            </button>
          </div>
        </div>

        <!-- РАЗДЕЛ: Заказы как покупатель (исполнитель тоже может быть клиентом) -->
        <div class="settings-section">
          <h2 class="settings-section-title">ВЫ ТАКЖЕ МОЖЕТЕ ПОКУПАТЬ</h2>

          <div class="settings-cell-group">
            <!-- My Orders as Customer -->
            <button 
              @click="$emit('view-orders')"
              class="settings-cell border-b border-slate-700 hover-cell"
            >
              <div class="cell-icon bg-blue-500">📋</div>
              <div class="cell-content">
                <p class="cell-label">Мои заказы (как покупатель)</p>
                <p class="cell-value">{{ ordersCount }} заказов</p>
              </div>
              <svg class="w-5 h-5 text-gray-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7" />
              </svg>
            </button>

            <!-- My Reviews as Customer -->
            <button 
              @click="$emit('view-reviews')"
              class="settings-cell border-b border-slate-700 hover-cell"
            >
              <div class="cell-icon bg-yellow-500">⭐</div>
              <div class="cell-content">
                <p class="cell-label">Мои отзывы</p>
                <p class="cell-value">{{ reviewsCount }} отзывов</p>
              </div>
              <svg class="w-5 h-5 text-gray-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7" />
              </svg>
            </button>

            <!-- Saved Services -->
            <button 
              @click="$emit('view-saved')"
              class="settings-cell hover-cell"
            >
              <div class="cell-icon bg-red-500">❤️</div>
              <div class="cell-content">
                <p class="cell-label">Сохраненные услуги</p>
                <p class="cell-value">{{ savedCount }} услуг</p>
              </div>
              <svg class="w-5 h-5 text-gray-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7" />
              </svg>
            </button>
          </div>
        </div>
      </div>
    </template>

    <!-- ======================== FOOTER (Both Roles) ======================== -->
    <div class="settings-container">
      <!-- Settings -->
      <div class="settings-section">
        <h2 class="settings-section-title">ДРУГОЕ</h2>

        <div class="settings-cell-group">
          <button class="settings-cell-danger">
            <div class="cell-icon-danger">🔔</div>
            <div class="cell-content">
              <p class="cell-label">Уведомления</p>
              <p class="cell-value" style="color: rgba(148, 163, 184, 0.7)">Включены</p>
            </div>
          </button>
        </div>
      </div>

      <!-- Stop Being Provider (only for providers) -->
      <div v-if="isProvider" class="settings-section">
        <div class="settings-cell-group">
          <button
            @click="$emit('stop-being-provider')"
            class="settings-cell-warning hover:bg-orange-950/30"
          >
            <div class="cell-icon-warning">🔄</div>
            <div class="cell-content">
              <p class="cell-label-warning">Стать обычным пользователем</p>
              <p class="cell-value" style="color: rgba(248, 113, 113, 0.7); font-size: 0.75rem; margin-top: 0.25rem">Вы перестанете быть исполнителем</p>
            </div>
          </button>
        </div>
        <p class="section-footer">После этого ваши услуги будут скрыты, но вы сможете покупать услуги других</p>
      </div>

      <!-- Danger Zone: Logout -->
      <div class="settings-section">
        <div class="settings-cell-group">
          <button
            @click="$emit('logout')"
            class="settings-cell-danger hover:bg-red-950/50"
          >
            <div class="cell-icon-danger bg-red-500/20">🚪</div>
            <div class="cell-content">
              <p class="cell-label-danger">Выйти из аккаунта</p>
            </div>
          </button>
        </div>
        <p class="section-footer">Вы выйдете из своего аккаунта на этом устройстве</p>
      </div>
    </div>

    <!-- ======================== SERVICE MODAL ======================== -->
    <ServiceModal
      v-if="showServiceModal"
      :service="null"
      :is-editing="false"
      @submit="handleAddService"
      @close="showServiceModal = false"
    />
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import ServiceModal from '@/components/profile/modals/ServiceModal.vue'

interface User {
  id: string | number
  first_name: string
  username?: string
  email?: string
}

interface Props {
  user: User
  isProvider: boolean
  ordersCount?: number
  reviewsCount?: number
  savedCount?: number
  incomingOrdersCount?: number
  activeOrdersCount?: number
  completedOrdersCount?: number
  servicesCount?: number
  providerRating?: number
  providerReviews?: number
}

defineProps<Props>()

const emit = defineEmits<{
  'become-provider': []
  'add-service': [service: any]
  'edit-profile': []
  'stop-being-provider': []
  'view-orders': []
  'view-reviews': []
  'view-saved': []
  'view-incoming-orders': []
  'view-active-orders': []
  'view-completed-orders': []
  'view-services': []
  'view-rating': []
  'logout': []
}>()

const showServiceModal = ref(false)

const openAddServiceModal = () => {
  showServiceModal.value = true
}

const handleAddService = (service: any) => {
  emit('add-service', service)
  showServiceModal.value = false
}
</script>

<style scoped>
.user-header {
  background: linear-gradient(to bottom, #0f1319, #0f1319);
  min-height: 100vh;
  padding-bottom: 40px;
}

/* Hero Section */
.hero-section {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 1rem;
  padding: 2rem 1rem 1.5rem;
  border-bottom: 1px solid rgba(148, 163, 184, 0.1);
}

.avatar-container {
  display: flex;
  align-items: center;
  justify-content: center;
}

.user-info-center {
  text-align: center;
}

/* Settings Container */
.settings-container {
  padding: 1.5rem 1rem;
  display: flex;
  flex-direction: column;
  gap: 2rem;
}

/* Section Title (iOS 18 style) */
.settings-section-title {
  font-size: 0.8125rem;
  font-weight: 600;
  letter-spacing: 0.05em;
  color: rgba(148, 163, 184, 0.6);
  margin-bottom: 0.75rem;
  padding: 0 0.5rem;
  text-transform: uppercase;
}

/* Section */
.settings-section {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}

/* Cell Group (iOS 18 style) */
.settings-cell-group {
  background: rgba(30, 41, 59, 0.5);
  border: 1px solid rgba(148, 163, 184, 0.1);
  border-radius: 0.875rem;
  overflow: hidden;
  backdrop-filter: blur(10px);
}

/* Settings Cell */
.settings-cell {
  display: flex;
  align-items: center;
  gap: 1rem;
  width: 100%;
  padding: 1rem;
  background: transparent;
  border: none;
  cursor: pointer;
  transition: all 0.2s ease;
}

.settings-cell:hover {
  background: rgba(59, 130, 246, 0.05);
}

.settings-cell:active {
  background: rgba(59, 130, 246, 0.1);
}

.hover-cell:hover {
  background: rgba(59, 130, 246, 0.05) !important;
}

.hover-cell:active {
  background: rgba(59, 130, 246, 0.1) !important;
}

/* Cell Icon */
.cell-icon {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 2.5rem;
  height: 2.5rem;
  border-radius: 0.625rem;
  font-size: 1.25rem;
  flex-shrink: 0;
}

/* Cell Content */
.cell-content {
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
  flex: 1;
  text-align: left;
}

.cell-label {
  font-size: 0.9375rem;
  font-weight: 500;
  color: #ffffff;
  margin: 0;
}

.cell-value {
  font-size: 0.8125rem;
  color: rgba(148, 163, 184, 0.7);
  margin: 0;
}

/* Danger Zone */
.settings-cell-danger {
  display: flex;
  align-items: center;
  gap: 1rem;
  width: 100%;
  padding: 1rem;
  background: transparent;
  border: none;
  cursor: pointer;
  transition: all 0.2s ease;
}

.settings-cell-danger:hover {
  background: rgba(239, 68, 68, 0.05);
}

.settings-cell-danger:active {
  background: rgba(239, 68, 68, 0.1);
}

.cell-icon-danger {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 2.5rem;
  height: 2.5rem;
  border-radius: 0.625rem;
  font-size: 1.25rem;
  background: rgba(239, 68, 68, 0.2);
  flex-shrink: 0;
}

.cell-label-danger {
  font-size: 0.9375rem;
  font-weight: 500;
  color: #ef4444;
  margin: 0;
}

/* Warning Zone (Stop Being Provider) */
.settings-cell-warning {
  display: flex;
  align-items: center;
  gap: 1rem;
  width: 100%;
  padding: 1rem;
  background: transparent;
  border: none;
  cursor: pointer;
  transition: all 0.2s ease;
}

.settings-cell-warning:hover {
  background: rgba(251, 146, 60, 0.05);
}

.settings-cell-warning:active {
  background: rgba(251, 146, 60, 0.1);
}

.cell-icon-warning {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 2.5rem;
  height: 2.5rem;
  border-radius: 0.625rem;
  font-size: 1.25rem;
  background: rgba(251, 146, 60, 0.2);
  flex-shrink: 0;
}

.cell-label-warning {
  font-size: 0.9375rem;
  font-weight: 500;
  color: #fb923c;
  margin: 0;
}

/* Section Footer */
.section-footer {
  font-size: 0.75rem;
  color: rgba(148, 163, 184, 0.5);
  padding: 0.5rem 1rem;
  text-align: center;
  margin-top: -0.5rem;
}

/* Responsive */
@media (max-width: 640px) {
  .settings-container {
    padding: 1rem 0.75rem;
    gap: 1.5rem;
  }

  .settings-cell,
  .settings-cell-danger,
  .settings-cell-warning {
    padding: 0.875rem;
  }

  .cell-icon {
    width: 2.25rem;
    height: 2.25rem;
    font-size: 1rem;
  }
}
</style>
