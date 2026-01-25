<template>
  <div class="profile-view">
    <!-- Render based on user role -->
    <UserHeader 
      :user="userStore.user" 
      :is-provider="userStore.isProvider"
      :services="providerServices"
      :orders-count="customerOrders.length"
      :reviews-count="userReviews.length"
      :saved-count="savedServices.length"
      :incoming-orders-count="incomingOrders.length"
      :active-orders-count="providerActiveOrders.length"
      :completed-orders-count="providerCompletedOrders.length"
      :provider-rating="providerRating"
      :provider-reviews="providerReviews"
      @become-provider="showBecomeProviderModal = true"
      @add-service="openAddService"
      @edit-service="openEditService"
      @delete-service="deleteServiceConfirm"
      @edit-profile="openEditProfile"
      @stop-being-provider="handleStopBeingProvider"
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

    <!-- Edit Profile Modal -->
    <EditProfileModal
      v-if="showEditProfileModal"
      :user="userStore.user"
      @submit="submitEditProfile"
      @close="showEditProfileModal = false"
    />
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import { useUserStore } from '@/stores/userStore'
import UserHeader from '@/components/profile/UserHeader.vue'
import BecomeProviderModal from '@/components/profile/modals/BecomeProviderModal.vue'
import ServiceModal from '@/components/profile/modals/ServiceModal.vue'
import EditProfileModal from '@/components/profile/modals/EditProfileModal.vue'

// ======================== INTERFACES ========================
interface Service {
  id: string | number
  name: string
  price: number
  description?: string
  category?: string
}

interface Order {
  id: string | number
  service: string
  provider: string
  status: 'pending' | 'active' | 'completed' | 'cancelled'
  price: number
  date: string
  customer_id?: string
  provider_id?: string
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

// ======================== STORE ========================
const userStore = useUserStore()

// ======================== STATE ========================
const showBecomeProviderModal = ref(false)
const showServiceModal = ref(false)
const showEditProfileModal = ref(false)
const isEditingService = ref(false)
const currentService = ref<Service | null>(null)

// ======================== CUSTOMER DATA ========================
// Orders where user is a customer (buyer)
const customerOrders = ref<Order[]>([
  {
    id: 1,
    service: 'Уроки английского',
    provider: 'Джон Д.',
    status: 'completed',
    price: 1500,
    date: '12 янв 2025',
    customer_id: userStore.user.id,
    provider_id: 'provider_4',
    rating: 5
  },
  {
    id: 2,
    service: 'Консультация бухгалтера',
    provider: 'Мария С.',
    status: 'active',
    price: 3000,
    date: '8 янв 2025',
    customer_id: userStore.user.id,
    provider_id: 'provider_2'
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
    price: 15000,
    description: 'Профессиональный дизайн сайта'
  },
  {
    id: 2,
    name: 'Пошив платья',
    price: 5000,
    description: 'Изготовление платьев по заказу'
  }
])

// ======================== PROVIDER DATA ========================
// Orders where user is a provider (seller)
const incomingOrders = ref<Order[]>([
  {
    id: 101,
    service: 'Веб-дизайн сайта',
    provider: 'Мне',
    status: 'pending',
    price: 15000,
    date: '25 янв 2025, 12:45',
    customer_id: 'customer_1',
    provider_id: userStore.user.id
  },
  {
    id: 102,
    service: 'Дизайн логотипа',
    provider: 'Мне',
    status: 'pending',
    price: 3000,
    date: '24 янв 2025, 18:30',
    customer_id: 'customer_2',
    provider_id: userStore.user.id
  }
])

const providerActiveOrders = ref<Order[]>([
  {
    id: 201,
    service: 'Дизайн интерфейса',
    provider: 'Мне',
    status: 'active',
    price: 8000,
    date: '20 янв 2025',
    customer_id: 'customer_3',
    provider_id: userStore.user.id
  }
])

const providerCompletedOrders = ref<Order[]>([
  {
    id: 301,
    service: 'Создание логотипа',
    provider: 'Мне',
    status: 'completed',
    price: 5000,
    date: '15 янв 2025',
    customer_id: 'customer_4',
    provider_id: userStore.user.id,
    rating: 5
  },
  {
    id: 302,
    service: 'Макеты для мобильного',
    provider: 'Мне',
    status: 'completed',
    price: 7000,
    date: '10 янв 2025',
    customer_id: 'customer_5',
    provider_id: userStore.user.id,
    rating: 4
  }
])

const providerServices = ref<Service[]>([
  {
    id: 1,
    name: 'Web-дизайн сайта',
    price: 15000,
    description: 'Профессиональный дизайн сайта',
    category: 'Дизайн'
  },
  {
    id: 2,
    name: 'Дизайн логотипа',
    price: 3000,
    description: 'Креативные логотипы',
    category: 'Дизайн'
  },
  {
    id: 3,
    name: 'Мокеты и прототипы',
    price: 8000,
    description: 'Прототипы и макеты интерфейсов',
    category: 'Дизайн'
  }
])

// Provider statistics
const completedOrders = computed(() => providerCompletedOrders.value.length)
const providerRating = ref(4.9)
const providerReviews = ref(124)

// ======================== METHODS ========================

/**
 * КРИТИЧНОЕ ИСПРАВЛЕНИЕ: Правильное сохранение профиля провайдера
 * Раньше: userStore.isProvider = true (прямая запись)
 * Теперь: userStore.setProviderInfo({...}) (через метод store)
 */
const submitProviderProfile = (profileData: any) => {
  // Передаем полные данные в store
  userStore.setProviderInfo({
    serviceName: profileData.name || 'Мои услуги',
    description: profileData.description,
    categories: profileData.categories,
    price: 0, // Будет задано при создании услуги
    timezone: profileData.timezone,
    availability: profileData.availability,
    maxConcurrentOrders: 5
  })

  showBecomeProviderModal.value = false
  
  // Можно добавить toast уведомление
  console.log('✅ Профиль исполнителя создан успешно!', profileData)
}

const openAddService = () => {
  isEditingService.value = false
  currentService.value = null
  showServiceModal.value = true
}

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
    // Update existing service
    const index = providerServices.value.findIndex(s => s.id === service.id)
    if (index !== -1) {
      providerServices.value[index] = service
    }
  } else {
    // Add new service
    const newService: Service = {
      ...service,
      id: Date.now()
    }
    providerServices.value.push(newService)
    
    // Also add to userStore
    userStore.addService({
      name: service.name,
      serviceName: service.name,
      description: service.description || '',
      category: service.category || '',
      price: service.price,
      timezone: userStore.providerInfo?.timezone || 'UTC+3',
      availability: userStore.providerInfo?.availability || {
        weekdays: true,
        weekends: false,
        evenings: true
      }
    })
  }
  closeServiceModal()
}

const deleteServiceConfirm = (serviceId: string | number) => {
  if (confirm('Вы уверены? Услуга будет удалена.')) {
    providerServices.value = providerServices.value.filter(s => s.id !== serviceId)
    userStore.deleteService(serviceId)
  }
}

const openEditProfile = () => {
  showEditProfileModal.value = true
}

const submitEditProfile = (profileData: any) => {
  userStore.setUser({
    ...userStore.user,
    first_name: profileData.first_name,
    username: profileData.username
  })
  showEditProfileModal.value = false
  console.log('✅ Профиль обновлен')
}

/**
 * НОВО: Отказ от роли исполнителя
 * Можно покупать, но не подавать услуги
 */
const handleStopBeingProvider = () => {
  const confirmed = confirm(
    'Вы действительно хотите прекратить быть исполнителем?\n\nПосле этого:\n- Ваши услуги будут скрыты\n- Клиенты не смогут платить вам\n- Вы останетесь обычным пользователем\n- Вы сможете купить услуги других'
  )
  
  if (confirmed) {
    // Убрание роли исполнителя
    userStore.removeProviderRole()
    providerServices.value = []
    incomingOrders.value = []
    providerActiveOrders.value = []
    providerCompletedOrders.value = []
    console.log('🚪 Вы прекратили быть исполнителем')
  }
}

const handleLogout = () => {
  if (confirm('Вы уверены что выходите?')) {
    userStore.logout()
    console.log('👋 Выход из аккаунта')
    // Redirect to login/home would happen here
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