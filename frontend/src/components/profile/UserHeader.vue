<template>
  <div class="user-header">
    <!-- Hero Section: Avatar + Name (iOS 18 style) -->
    <div class="hero-section">
      <!-- Avatar -->
      <div class="avatar-container">
        <div class="w-24 h-24 bg-gradient-to-br from-blue-500 to-blue-600 rounded-full flex items-center justify-center text-5xl font-bold text-white shadow-lg">
          Л
        </div>
      </div>

      <!-- Name & Username -->
      <div class="user-info-center">
        <h1 class="text-2xl font-bold text-white">Лена</h1>
        <p class="text-sm text-gray-400">@lena_user</p>
        <p class="text-xs text-blue-400 mt-1.5">✓ Исполнитель</p>
      </div>
    </div>

    <!-- Settings Sections (iOS 18 style) -->
    <div class="settings-container">
      <!-- Мои заказы -->
      <div class="settings-section">
        <h2 class="settings-section-title">ИСТОРИЯ</h2>
        
        <div class="settings-cell-group">
          <button 
            @click="showModal('orders')"
            class="settings-cell border-b border-slate-700"
          >
            <div class="cell-icon bg-blue-500">📋</div>
            <div class="cell-content">
              <p class="cell-label">Мои заказы</p>
              <p class="cell-value">{{ orders.length }} активных</p>
            </div>
            <svg class="w-5 h-5 text-gray-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7" />
            </svg>
          </button>

          <!-- Reviews -->
          <button 
            @click="showModal('reviews')"
            class="settings-cell border-b border-slate-700"
          >
            <div class="cell-icon bg-yellow-500">⭐</div>
            <div class="cell-content">
              <p class="cell-label">Оставленные отзывы</p>
              <p class="cell-value">{{ reviews.length }} отзывов</p>
            </div>
            <svg class="w-5 h-5 text-gray-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7" />
            </svg>
          </button>

          <!-- Saved Services -->
          <button 
            @click="showModal('saved')"
            class="settings-cell"
          >
            <div class="cell-icon bg-red-500">❤️</div>
            <div class="cell-content">
              <p class="cell-label">Сохраненные услуги</p>
              <p class="cell-value">{{ savedServices.length }} услуг</p>
            </div>
            <svg class="w-5 h-5 text-gray-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7" />
            </svg>
          </button>
        </div>
      </div>

      <!-- Статистика -->
      <div class="settings-section">
        <h2 class="settings-section-title">СТАТИСТИКА</h2>
        
        <div class="settings-cell-group">
          <button 
            @click="showModal('analytics')"
            class="settings-cell border-b border-slate-700"
          >
            <div class="cell-icon bg-purple-500">📊</div>
            <div class="cell-content">
              <p class="cell-label">Аналитика</p>
              <p class="cell-value">425,000 ₽ доход</p>
            </div>
            <svg class="w-5 h-5 text-gray-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7" />
            </svg>
          </button>

          <button 
            @click="showModal('notifications')"
            class="settings-cell"
          >
            <div class="cell-icon bg-orange-500">🔔</div>
            <div class="cell-content">
              <p class="cell-label">Уведомления</p>
              <p class="cell-value">Включены</p>
            </div>
            <svg class="w-5 h-5 text-gray-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7" />
            </svg>
          </button>
        </div>
      </div>

      <!-- Профиль -->
      <div class="settings-section">
        <h2 class="settings-section-title">ПРОФИЛЬ</h2>
        
        <div class="settings-cell-group">
          <button 
            @click="showModal('edit-profile')"
            class="settings-cell"
          >
            <div class="cell-icon bg-blue-500">✏️</div>
            <div class="cell-content">
              <p class="cell-label">Редактировать профиль</p>
              <p class="cell-value">Лена</p>
            </div>
            <svg class="w-5 h-5 text-gray-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7" />
            </svg>
          </button>
        </div>
      </div>

      <!-- Danger Zone -->
      <div class="settings-section">
        <div class="settings-cell-group">
          <button 
            @click="handleLogout"
            class="settings-cell-danger"
          >
            <div class="cell-icon-danger">🚪</div>
            <div class="cell-content">
              <p class="cell-label-danger">Выйти из аккаунта</p>
            </div>
          </button>
        </div>
        <p class="section-footer">Вы выдете из своего аккаунта на этом устройстве</p>
      </div>
    </div>

    <!-- MODALS -->
    
    <!-- Orders Modal -->
    <Modal v-if="activeModal === 'orders'" title="📋 Мои заказы" @close="closeModal">
      <OrdersTab :orders="orders" />
    </Modal>

    <!-- Reviews Modal -->
    <Modal v-if="activeModal === 'reviews'" title="⭐ Оставленные отзывы" @close="closeModal">
      <ReviewsTab :reviews="reviews" />
    </Modal>

    <!-- Saved Services Modal -->
    <Modal v-if="activeModal === 'saved'" title="❤️ Сохраненные услуги" @close="closeModal">
      <SavedTab :services="savedServices" />
    </Modal>

    <!-- Analytics Modal -->
    <Modal v-if="activeModal === 'analytics'" title="📊 Аналитика" @close="closeModal">
      <AnalyticsTab />
    </Modal>

    <!-- Notifications Modal -->
    <Modal v-if="activeModal === 'notifications'" title="🔔 Уведомления" @close="closeModal">
      <NotificationsTab />
    </Modal>

    <!-- Edit Profile Modal -->
    <Modal v-if="activeModal === 'edit-profile'" title="✏️ Редактировать профиль" @close="closeModal">
      <div class="space-y-4">
        <div>
          <label class="block text-sm text-gray-400 mb-2">Имя</label>
          <input v-model="userData.first_name" type="text" class="w-full bg-slate-700 border border-slate-600 rounded-lg px-3 py-2 text-white focus:outline-none focus:border-blue-500" />
        </div>
        <div>
          <label class="block text-sm text-gray-400 mb-2">Юзернейм</label>
          <input v-model="userData.username" type="text" class="w-full bg-slate-700 border border-slate-600 rounded-lg px-3 py-2 text-white focus:outline-none focus:border-blue-500" />
        </div>
        <button @click="saveProfile" class="w-full bg-blue-600 hover:bg-blue-500 text-white font-semibold py-2 rounded-lg transition">
          Сохранить
        </button>
      </div>
    </Modal>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import Modal from '@/components/common/Modal.vue'
import OrdersTab from '@/components/profile/OrdersTab.vue'
import ReviewsTab from '@/components/profile/ReviewsTab.vue'
import SavedTab from '@/components/profile/SavedTab.vue'
import AnalyticsTab from '@/components/profile/AnalyticsTab.vue'
import NotificationsTab from '@/components/profile/NotificationsTab.vue'

const activeModal = ref<string | null>(null)

const userData = ref({
  first_name: 'Лена',
  username: 'lena_user',
  id: '123456789'
})

// Mock data
const orders = ref([
  {
    id: 1,
    serviceName: 'Уроки английского',
    provider: 'Джон Д.',
    date: '12 янв 2025',
    status: 'completed'
  },
  {
    id: 2,
    serviceName: 'Консультация бухгалтера',
    provider: 'Мария С.',
    date: '8 янв 2025',
    status: 'active'
  },
  {
    id: 3,
    serviceName: 'Web-дизайн',
    provider: 'Артем К.',
    date: '5 янв 2025',
    status: 'completed'
  }
])

const reviews = ref([
  {
    id: 1,
    serviceName: 'Уроки английского',
    provider: 'Джон Д.',
    text: 'Отличный преподаватель, очень доволен результатом! Рекомендую всем.',
    rating: 5,
    date: '12 янв 2025'
  },
  {
    id: 2,
    serviceName: 'Консультация бухгалтера',
    provider: 'Мария С.',
    text: 'Помогла разобраться с налогами, спасибо!',
    rating: 5,
    date: '8 янв 2025'
  }
])

const savedServices = ref([
  {
    id: 1,
    name: 'Web-дизайн сайта',
    provider: 'Артем К.',
    price: 15000,
    rating: 4.9
  },
  {
    id: 2,
    name: 'Продвижение в соцсетях',
    provider: 'Виктория Л.',
    price: 5000,
    rating: 4.8
  }
])

// Functions
const showModal = (modal: string) => {
  console.log('📱 Открываю модаль:', modal)
  activeModal.value = modal
}

const closeModal = () => {
  console.log('❌ Закрываю модаль')
  activeModal.value = null
}

const saveProfile = () => {
  alert('✅ Профиль сохранен!')
  closeModal()
}

const handleLogout = () => {
  alert('👋 Вы вышли из аккаунта')
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
  .settings-cell-danger {
    padding: 0.875rem;
  }

  .cell-icon {
    width: 2.25rem;
    height: 2.25rem;
    font-size: 1rem;
  }
}
</style>