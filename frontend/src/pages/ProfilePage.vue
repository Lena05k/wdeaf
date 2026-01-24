<template>
  <div class="profile-page flex flex-col h-screen bg-slate-900">
    <!-- Header -->
    <header class="sticky top-0 z-40 bg-slate-900 border-b border-blue-900">
      <div class="max-w-md mx-auto px-4 py-3">
        <h1 class="text-xl font-bold text-blue-400">👤 Мой профиль</h1>
      </div>
    </header>

    <!-- Main Content -->
    <main class="flex-1 overflow-y-auto max-w-md mx-auto w-full pb-20">
      <!-- User Header Component -->
      <UserHeader
        :user="userData"
        :is-provider="false"
        :orders-count="orders.length"
        :reviews-count="reviews.length"
        :saved-count="savedServices.length"
        @show-orders="showModal('orders')"
        @show-reviews="showModal('reviews')"
        @show-saved="showModal('saved')"
        @show-provider-orders="showModal('provider-orders')"
        @show-provider-reviews="showModal('provider-reviews')"
        @show-analytics="showModal('analytics')"
        @show-notifications="showModal('notifications')"
        @become-provider="showModal('become-provider')"
        @add-service="showModal('add-service')"
        @edit-profile="showModal('edit-profile')"
        @logout="handleLogout"
      />
    </main>

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

    <!-- Become Provider Modal -->
    <Modal v-if="activeModal === 'become-provider'" title="🚀 Стать исполнителем" @close="closeModal">
      <div class="space-y-4">
        <p class="text-gray-300">Хотите начать создавать услуги и зарабатывать на WDEAF?</p>
        <div class="bg-slate-700 rounded-lg p-4 border border-slate-600 space-y-2">
          <p class="text-sm text-gray-400">✓ Создавайте свои услуги</p>
          <p class="text-sm text-gray-400">✓ Получайте заказы от клиентов</p>
          <p class="text-sm text-gray-400">✓ Зарабатывайте без комиссии</p>
          <p class="text-sm text-gray-400">✓ Строите свой рейтинг</p>
        </div>
        <button @click="confirmBecomeProvider" class="w-full bg-blue-600 hover:bg-blue-500 text-white font-semibold py-2 rounded-lg transition">
          Стать исполнителем
        </button>
      </div>
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
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useUserStore } from '@/stores/userStore'

// Components
import UserHeader from '@/components/profile/UserHeader.vue'
import Modal from '@/components/common/Modal.vue'
import OrdersTab from '@/components/profile/OrdersTab.vue'
import ReviewsTab from '@/components/profile/ReviewsTab.vue'
import SavedTab from '@/components/profile/SavedTab.vue'
import AnalyticsTab from '@/components/profile/AnalyticsTab.vue'
import NotificationsTab from '@/components/profile/NotificationsTab.vue'

const router = useRouter()
const userStore = useUserStore()

const activeModal = ref<string | null>(null)

const userData = ref({
  first_name: 'Иван',
  username: 'ivan_user',
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
    serviceName: 'Веб-дизайн',
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

const confirmBecomeProvider = () => {
  alert('✅ Вы стали исполнителем!')
  closeModal()
}

const saveProfile = () => {
  alert('✅ Профиль сохранен!')
  closeModal()
}

const handleLogout = () => {
  alert('👋 Вы вышли из аккаунта')
}

onMounted(() => {
  userStore.initFromTelegram()
  console.log('✅ ProfilePage mounted')
})
</script>

<style scoped>
.profile-page {
  background: linear-gradient(135deg, #0f1319 0%, #1a1f2e 100%);
}
</style>