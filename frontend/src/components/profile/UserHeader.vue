<template>
  <div class="user-header">
    <!-- Sticky Header with Tabs -->
    <div class="header-sticky">
      <!-- Logo -->
      <div class="logo-section">
        <div class="logo">W</div>
      </div>

      <!-- Navigation Tabs -->
      <button
        v-for="tab in tabs"
        :key="tab.id"
        @click="selectTab(tab.id)"
        class="nav-tab"
        :class="{ 'nav-tab-active': activeTab === tab.id }"
      >
        <span class="tab-icon">{{ tab.icon }}</span>
        <span class="tab-label">{{ tab.label }}</span>
      </button>

      <!-- Add Service Button (Only for Provider) -->
      <button v-if="isProvider" class="nav-tab nav-tab-add" @click="showModal('add-service')">
        <span class="tab-icon">+</span>
      </button>

      <!-- Profile Button -->
      <button class="profile-btn" @click="toggleProfile">
        {{ userInitial }}
      </button>
    </div>

    <!-- Profile Modal -->
    <Modal v-if="showProfileModal" title="👤 Мой профиль" @close="toggleProfile">
      <div class="profile-modal-content">
        <!-- Avatar Section -->
        <div class="profile-header">
          <div class="avatar-circle">{{ userInitial }}</div>
          <h2 class="profile-name">{{ userData.first_name }}</h2>
          <p class="profile-username">@{{ userData.username }}</p>
          <p v-if="isProvider" class="profile-badge">✓ Исполнитель</p>
        </div>

        <!-- Stats -->
        <div class="stats-grid">
          <div class="stat-card">
            <p class="stat-value">4.9</p>
            <p class="stat-label">Рейтинг</p>
          </div>
          <div class="stat-card">
            <p class="stat-value">28</p>
            <p class="stat-label">Заказов</p>
          </div>
          <div class="stat-card">
            <p class="stat-value">124</p>
            <p class="stat-label">Отзывов</p>
          </div>
        </div>

        <!-- Action Buttons -->
        <div class="action-buttons">
          <button class="btn btn-primary">Редактировать</button>
          <button class="btn btn-secondary">Настройки</button>
        </div>

        <!-- Logout -->
        <button class="btn btn-danger">Выход</button>
      </div>
    </Modal>

    <!-- Tab Content Modal -->
    <Modal v-if="activeModal" :title="getModalTitle" @close="closeModal">
      <OrdersTab v-if="activeModal === 'orders'" :orders="orders" />
      <div v-else-if="activeModal === 'catalog'" class="placeholder">
        📂 Каталог скоростя
      </div>
      <SavedTab v-else-if="activeModal === 'saved'" :services="savedServices" />
      <AnalyticsTab v-else-if="activeModal === 'analytics'" />
      <div v-else-if="activeModal === 'add-service'" class="space-y-4">
        <p class="text-gray-300">Добавьте новую услугу:</p>
        <div>
          <label class="block text-sm text-gray-400 mb-2">Название</label>
          <input v-model="newService.name" type="text" placeholder="Web-дизайн" class="w-full bg-slate-700 border border-slate-600 rounded-lg px-3 py-2 text-white focus:outline-none focus:border-blue-500" />
        </div>
        <div>
          <label class="block text-sm text-gray-400 mb-2">Цена (₽)</label>
          <input v-model="newService.price" type="number" placeholder="15000" class="w-full bg-slate-700 border border-slate-600 rounded-lg px-3 py-2 text-white focus:outline-none focus:border-blue-500" />
        </div>
        <button @click="saveService" class="w-full bg-blue-600 hover:bg-blue-500 text-white font-semibold py-2 rounded-lg transition">
          Сохранить
        </button>
      </div>
    </Modal>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import Modal from '@/components/common/Modal.vue'
import OrdersTab from '@/components/profile/OrdersTab.vue'
import SavedTab from '@/components/profile/SavedTab.vue'
import AnalyticsTab from '@/components/profile/AnalyticsTab.vue'

const isProvider = ref(true)
const activeTab = ref('orders')
const activeModal = ref<string | null>(null)
const showProfileModal = ref(false)

const userData = ref({
  first_name: 'Лена',
  username: 'lena_user'
})

const userInitial = computed(() => userData.value.first_name.charAt(0).toUpperCase())

const newService = ref({
  name: '',
  price: ''
})

// Navigation Tabs
const tabs = computed(() => [
  { id: 'orders', icon: '🔍', label: 'Обзор' },
  { id: 'catalog', icon: '📂', label: 'Каталог' },
  { id: 'saved', icon: '📄', label: 'Заказы' },
  { id: 'analytics', icon: '📂', label: 'Удаленные' }
])

const getModalTitle = computed(() => {
  const titles: Record<string, string> = {
    'orders': '🔍 Обзор',
    'catalog': '📂 Каталог',
    'saved': '📄 Заказы',
    'analytics': '📂 Удаленные',
    'add-service': '➕ Новая услуга'
  }
  return titles[activeModal.value || ''] || ''
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
  }
])

const savedServices = ref([
  {
    id: 1,
    name: 'Web-дизайн сайта',
    provider: 'Артем К.',
    price: 15000,
    rating: 4.9
  }
])

// Functions
const selectTab = (tabId: string) => {
  activeTab.value = tabId
  activeModal.value = tabId
}

const toggleProfile = () => {
  showProfileModal.value = !showProfileModal.value
}

const closeModal = () => {
  activeModal.value = null
}

const showModal = (modal: string) => {
  activeModal.value = modal
}

const saveService = () => {
  if (newService.value.name && newService.value.price) {
    alert(`✅ Услуга "Д${newService.value.name}" сохранена`)
    newService.value = { name: '', price: '' }
    closeModal()
  }
}
</script>

<style scoped>
.user-header {
  background: linear-gradient(to bottom, #0f1319, #0f1319);
  min-height: 100vh;
}

/* Header Sticky */
.header-sticky {
  position: sticky;
  top: 0;
  z-index: 40;
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.75rem;
  background: #ffffff;
  border-bottom: 1px solid #e5e7eb;
  max-width: 768px;
  margin: 0 auto;
  width: 100%;
  box-sizing: border-box;
  overflow-x: auto;
  -webkit-overflow-scrolling: touch;
}

.logo-section {
  display: flex;
  align-items: center;
  flex-shrink: 0;
}

.logo {
  width: 2.5rem;
  height: 2.5rem;
  background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%);
  color: white;
  border-radius: 0.5rem;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: bold;
  font-size: 1.25rem;
}

/* Navigation Tab */
.nav-tab {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 0.25rem;
  padding: 0.5rem 0.75rem;
  background: #f3f4f6;
  border: 1px solid #e5e7eb;
  border-radius: 0.5rem;
  cursor: pointer;
  transition: all 0.2s ease;
  color: #6b7280;
  font-size: 0.75rem;
  font-weight: 500;
  white-space: nowrap;
  flex-shrink: 0;
}

.nav-tab:hover {
  background: #e5e7eb;
  border-color: #d1d5db;
}

.nav-tab-active {
  background: #ffffff;
  border: 2px solid #000000;
  color: #000000;
}

.tab-icon {
  font-size: 1.25rem;
  display: block;
}

.tab-label {
  display: block;
}

/* Add Service Button */
.nav-tab-add {
  background: #f3f4f6;
  border: 1px solid #e5e7eb;
  font-size: 1.5rem;
  padding: 0.5rem;
}

.nav-tab-add:hover {
  background: #e5e7eb;
}

/* Profile Button */
.profile-btn {
  width: 2.5rem;
  height: 2.5rem;
  border-radius: 50%;
  background: #3b82f6;
  color: white;
  border: none;
  cursor: pointer;
  font-weight: bold;
  font-size: 1rem;
  transition: all 0.2s ease;
  flex-shrink: 0;
  margin-left: auto;
}

.profile-btn:hover {
  background: #2563eb;
}

.profile-btn:active {
  background: #1d4ed8;
}

/* Profile Modal Content */
.profile-modal-content {
  padding: 1rem 0;
}

.profile-header {
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
  padding: 1.5rem 0;
  border-bottom: 1px solid rgba(148, 163, 184, 0.1);
  margin-bottom: 1.5rem;
}

.avatar-circle {
  width: 4rem;
  height: 4rem;
  border-radius: 50%;
  background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.5rem;
  font-weight: bold;
  color: white;
  margin-bottom: 1rem;
}

.profile-name {
  font-size: 1.5rem;
  font-weight: bold;
  color: white;
  margin: 0.5rem 0 0.25rem;
}

.profile-username {
  color: #a0aec0;
  font-size: 0.875rem;
  margin: 0.25rem 0;
}

.profile-badge {
  color: #3b82f6;
  font-size: 0.875rem;
  font-weight: 500;
  margin-top: 0.5rem;
}

/* Stats Grid */
.stats-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 0.75rem;
  margin-bottom: 1.5rem;
}

.stat-card {
  background: rgba(30, 41, 59, 0.5);
  border: 1px solid rgba(148, 163, 184, 0.1);
  border-radius: 0.75rem;
  padding: 1rem;
  text-align: center;
}

.stat-value {
  font-size: 1.25rem;
  font-weight: bold;
  color: #3b82f6;
  margin: 0 0 0.25rem;
}

.stat-label {
  font-size: 0.75rem;
  color: #a0aec0;
  margin: 0;
  text-transform: uppercase;
  letter-spacing: 0.02em;
}

/* Action Buttons */
.action-buttons {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
  margin-bottom: 1.5rem;
}

.btn {
  padding: 0.75rem 1rem;
  border-radius: 0.75rem;
  border: none;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s ease;
  font-size: 0.875rem;
}

.btn-primary {
  background: #3b82f6;
  color: white;
}

.btn-primary:hover {
  background: #2563eb;
}

.btn-secondary {
  background: rgba(148, 163, 184, 0.1);
  color: #e2e8f0;
  border: 1px solid rgba(148, 163, 184, 0.2);
}

.btn-secondary:hover {
  background: rgba(148, 163, 184, 0.15);
}

.btn-danger {
  background: rgba(239, 68, 68, 0.1);
  color: #ef4444;
  border: 1px solid rgba(239, 68, 68, 0.2);
}

.btn-danger:hover {
  background: rgba(239, 68, 68, 0.15);
}

/* Placeholder */
.placeholder {
  text-align: center;
  padding: 2rem;
  color: #a0aec0;
  font-size: 1.125rem;
}
</style>