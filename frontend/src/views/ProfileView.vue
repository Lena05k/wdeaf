<template>
  <div class="profile-view">
    <!-- User Header (iOS 18 Settings Style) -->
    <UserHeader 
      :user="userStore.user" 
      :is-provider="userStore.isProvider"
      :services="providerServices"
      :orders-count="userOrders.length"
      :reviews-count="userReviews.length"
      :saved-count="savedServices.length"
      :completed-orders="completedOrders"
      :provider-rating="providerRating"
      :provider-reviews="providerReviews"
      :total-earnings="totalEarnings"
      @become-provider="showBecomeProviderModal = true"
      @add-service="showServiceModal = true"
      @edit-service="openEditService"
      @delete-service="deleteServiceConfirm"
      @edit-profile="openEditProfile"
      @logout="handleLogout"
    />

    <!-- ======================== MODALS ======================== -->

    <!-- Become Provider Modal -->
    <BecomeProviderModal
      v-if="showBecomeProviderModal"
      :user="userStore.user"
      @submit="submitProviderProfile"
      @close="showBecomeProviderModal = false"
    />

    <!-- Create/Edit Service Modal -->
    <ServiceModal
      v-if="showServiceModal"
      :service="currentService"
      :is-editing="isEditingService"
      @submit="submitService"
      @close="closeServiceModal"
    />
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import { useUserStore } from '@/stores/userStore'
import UserHeader from '@/components/profile/UserHeader.vue'
import BecomeProviderModal from '@/components/profile/modals/BecomeProviderModal.vue'
import ServiceModal from '@/components/profile/modals/ServiceModal.vue'

interface Service {
  id: string | number
  name: string
  price: number
  description?: string
  category?: string
}

interface Order {
  id: string | number
  serviceName: string
  provider: string
  date: string
  status: string
  rating?: number
}

interface Review {
  id: string | number
  serviceName: string
  provider: string
  text: string
  rating: number
  date: string
}

const userStore = useUserStore()

// ======================== STATE ========================
const showBecomeProviderModal = ref(false)
const showServiceModal = ref(false)
const isEditingService = ref(false)
const currentService = ref<Service | null>(null)

// Mock data for regular user
const userOrders = ref<Order[]>([
  {
    id: 1,
    serviceName: 'Уроки английского',
    provider: 'Джон Д.',
    date: '12 янв 2025',
    status: 'completed',
    rating: 5
  },
  {
    id: 2,
    serviceName: 'Консультация бухгалтера',
    provider: 'Мария С.',
    date: '8 янв 2025',
    status: 'completed',
    rating: 4
  }
])

const userReviews = ref<Review[]>([
  {
    id: 1,
    serviceName: 'Уроки английского',
    provider: 'Джон Д.',
    text: 'Отличный преподаватель, очень доволен результатом!',
    rating: 5,
    date: '12 янв 2025'
  },
  {
    id: 2,
    serviceName: 'Консультация бухгалтера',
    provider: 'Мария С.',
    text: 'Все понятно объяснила, рекомендую!',
    rating: 4,
    date: '8 янв 2025'
  }
])

const savedServices = ref<Service[]>([
  {
    id: 1,
    name: 'Web-дизайн',
    provider: 'Артем К.',
    price: 15000,
    rating: 4.9
  },
  {
    id: 2,
    name: 'Пошив платья',
    provider: 'Анна Т.',
    price: 5000,
    rating: 4.8
  }
])

// Provider services
const providerServices = ref<Service[]>([
  {
    id: 1,
    name: 'Web-дизайн сайта',
    price: 15000,
    description: 'Профессиональный дизайн сайта'
  },
  {
    id: 2,
    name: 'Дизайн логотипа',
    price: 3000,
    description: 'Креативные логотипы'
  },
  {
    id: 3,
    name: 'Мокеты и прототипы',
    price: 8000,
    description: 'Низковерные прототипы'
  }
])

// Provider stats
const completedOrders = ref(28)
const providerRating = ref(4.9)
const providerReviews = ref(124)
const totalEarnings = ref(425000)

// ======================== METHODS ========================
const openEditService = (service: Service) => {
  isEditingService.value = true
  currentService.value = JSON.parse(JSON.stringify(service))
  showServiceModal.value = true
}

const closeServiceModal = () => {
  showServiceModal.value = false
  currentService.value = null
  isEditingService.value = false
}

const submitService = (service: Service) => {
  if (isEditingService.value) {
    // Обновить услугу
    const index = providerServices.value.findIndex(s => s.id === service.id)
    if (index !== -1) {
      providerServices.value[index] = service
    }
  } else {
    // Добавить новую
    providerServices.value.push({ ...service, id: Date.now() })
  }
  closeServiceModal()
}

const deleteServiceConfirm = (serviceId: string | number) => {
  if (confirm('Вы уверены? Услуга будет удалена.')) {
    providerServices.value = providerServices.value.filter(s => s.id !== serviceId)
  }
}

const submitProviderProfile = (profileData: any) => {
  // Сохранить профиль исполнителя
  userStore.isProvider = true
  showBecomeProviderModal.value = false
  console.log('Профиль исполнителя сохранен:', profileData)
}

const openEditProfile = () => {
  console.log('Открыть редактор профиля')
}

const handleLogout = () => {
  if (confirm('Вы суре что выходите?')) {
    // Логика выхода
    console.log('Выход')
  }
}
</script>

<style scoped>
.profile-view {
  background: linear-gradient(to bottom, #0f172a, #0f1319);
  min-height: 100vh;
  padding-bottom: 80px;
}
</style>