<template>
  <div class="header-with-nav">
    <!-- Top Header -->
    <div class="top-header">
      <!-- Logo + Status -->
      <div class="header-left">
        <div class="logo-status">
          <div class="logo">👤</div>
          <span class="status-dot"></span>
        </div>
      </div>

      <!-- Right Icons -->
      <div class="header-right">
        <button class="icon-button" @click="toggleProfile">
          {{ userInitial }}
        </button>
      </div>
    </div>

    <!-- Navigation Tabs -->
    <div class="nav-tabs-container">
      <!-- Search / Overview -->
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
        <span class="tab-label">Добавить</span>
      </button>
    </div>

    <!-- Profile Modal -->
    <Modal v-if="showProfileModal" title="👤 Мой профиль" @close="toggleProfile">
      <ProfileContent :is-provider="isProvider" />
    </Modal>

    <!-- Tab Content Modal -->
    <Modal v-if="activeModal" :title="getModalTitle" @close="closeModal">
      <OrdersTab v-if="activeModal === 'orders'" :orders="orders" />
      <ReviewsTab v-else-if="activeModal === 'reviews'" :reviews="reviews" />
      <SavedTab v-else-if="activeModal === 'saved'" :services="savedServices" />
      <AnalyticsTab v-else-if="activeModal === 'analytics'" />
      <NotificationsTab v-else-if="activeModal === 'notifications'" />
      <div v-else-if="activeModal === 'add-service'" class="space-y-4">
        <p class="text-gray-300">Добавьте новую услугу:</p>
        <div>
          <label class="block text-sm text-gray-400 mb-2">Название услуги</label>
          <input v-model="newService.name" type="text" placeholder="Напр. Web-дизайн" class="w-full bg-slate-700 border border-slate-600 rounded-lg px-3 py-2 text-white focus:outline-none focus:border-blue-500" />
        </div>
        <div>
          <label class="block text-sm text-gray-400 mb-2">Цена (₽)</label>
          <input v-model="newService.price" type="number" placeholder="15000" class="w-full bg-slate-700 border border-slate-600 rounded-lg px-3 py-2 text-white focus:outline-none focus:border-blue-500" />
        </div>
        <button @click="saveService" class="w-full bg-blue-600 hover:bg-blue-500 text-white font-semibold py-2 rounded-lg transition">
          Сохранить услугу
        </button>
      </div>
    </Modal>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import Modal from '@/components/common/Modal.vue'
import ProfileContent from '@/components/profile/ProfileContent.vue'
import OrdersTab from '@/components/profile/OrdersTab.vue'
import ReviewsTab from '@/components/profile/ReviewsTab.vue'
import SavedTab from '@/components/profile/SavedTab.vue'
import AnalyticsTab from '@/components/profile/AnalyticsTab.vue'
import NotificationsTab from '@/components/profile/NotificationsTab.vue'

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
const tabs = computed(() => {
  const baseTabs = [
    { id: 'orders', icon: '📋', label: 'Обзор' },
    { id: 'catalog', icon: '📂', label: 'Каталог' },
    { id: 'saved', icon: '❤️', label: 'Нравится' },
    { id: 'analytics', icon: '📊', label: 'Аналитика' }
  ]
  return baseTabs
})

const getModalTitle = computed(() => {
  const titles: Record<string, string> = {
    'orders': '📋 Мои заказы',
    'reviews': '⭐ Отзывы',
    'saved': '❤️ Нравится',
    'analytics': '📊 Аналитика',
    'notifications': '🔔 Уведомления',
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

const reviews = ref([
  {
    id: 1,
    serviceName: 'Уроки английского',
    provider: 'Джон Д.',
    text: 'Отличный преподаватель!',
    rating: 5,
    date: '12 янв 2025'
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
    alert(`✅ Услуга "Д${newService.value.name}" сохранена за ₽${newService.value.price}`)
    newService.value = { name: '', price: '' }
    closeModal()
  }
}
</script>

<style scoped>
.header-with-nav {
  background: linear-gradient(to bottom, #0f1319, #0f1319);
  position: sticky;
  top: 0;
  z-index: 40;
}

/* Top Header */
.top-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 1rem;
  border-bottom: 1px solid rgba(148, 163, 184, 0.1);
  max-width: 768px;
  margin: 0 auto;
  width: 100%;
  box-sizing: border-box;
}

.header-left {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.logo-status {
  display: flex;
  align-items: center;
  position: relative;
}

.logo {
  font-size: 1.5rem;
}

.status-dot {
  display: inline-block;
  width: 10px;
  height: 10px;
  background: #10b981;
  border-radius: 50%;
  position: absolute;
  bottom: -2px;
  right: -2px;
  border: 2px solid #0f1319;
}

.header-right {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.icon-button {
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
}

.icon-button:hover {
  background: #2563eb;
}

.icon-button:active {
  background: #1d4ed8;
}

/* Navigation Tabs */
.nav-tabs-container {
  display: flex;
  gap: 0;
  border-top: 1px solid rgba(148, 163, 184, 0.1);
  border-bottom: 1px solid rgba(148, 163, 184, 0.1);
  overflow-x: auto;
  -webkit-overflow-scrolling: touch;
  max-width: 768px;
  margin: 0 auto;
  width: 100%;
  box-sizing: border-box;
}

.nav-tab {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 0.25rem;
  flex: 1;
  min-width: 80px;
  padding: 0.75rem 0.5rem;
  background: transparent;
  border: none;
  cursor: pointer;
  color: #a0aec0;
  font-size: 0.75rem;
  font-weight: 500;
  transition: all 0.2s ease;
  position: relative;
  white-space: nowrap;
  border-bottom: 2px solid transparent;
}

.nav-tab:hover {
  color: #cbd5e1;
  background: rgba(59, 130, 246, 0.05);
}

.nav-tab-active {
  color: #3b82f6;
  border-bottom-color: #3b82f6;
  background: rgba(59, 130, 246, 0.1);
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
  color: #8b5cf6;
}

.nav-tab-add:hover {
  color: #a78bfa;
  background: rgba(139, 92, 246, 0.05);
}

/* Responsive */
@media (max-width: 640px) {
  .top-header {
    padding: 0.75rem;
  }

  .nav-tabs-container {
    gap: 0;
  }

  .nav-tab {
    min-width: 70px;
    padding: 0.5rem 0.25rem;
    font-size: 0.7rem;
  }

  .tab-icon {
    font-size: 1.1rem;
  }
}
</style>