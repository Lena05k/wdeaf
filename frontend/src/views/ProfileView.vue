<template>
  <div class="profile-view">
    <!-- User Header -->
    <UserHeader :user="userStore.user" :is-provider="userStore.isProvider" />

    <!-- User Statistics (only for non-providers) -->
    <UserStats v-if="!userStore.isProvider" :orders-count="ordersCount" />

    <!-- Provider Statistics (only for providers) -->
    <ProviderStats v-else-if="userStore.isProvider && userStore.getProviderInfo()" />

    <!-- Tab Navigation (iOS-style) -->
    <TabBar 
      :active-tab="activeTab" 
      :is-provider="userStore.isProvider"
      @select-tab="activeTab = $event"
    />

    <!-- Tab Content -->
    <div class="tab-content">
      <!-- Tab 1: For Non-Provider -->
      <div v-if="!userStore.isProvider" class="space-y-4">
        <!-- Orders Tab -->
        <div v-if="activeTab === 'orders'" class="px-4 pt-4">
          <OrdersSection :orders="userOrders" />
        </div>

        <!-- Saved Services Tab -->
        <div v-if="activeTab === 'saved'" class="px-4 pt-4">
          <SavedServicesSection :saved-services="savedServices" />
        </div>

        <!-- Reviews Tab -->
        <div v-if="activeTab === 'reviews'" class="px-4 pt-4">
          <ReviewsSection :reviews="userReviews" />
        </div>

        <!-- Actions Section -->
        <div class="px-4 py-6 space-y-2 border-t border-slate-700">
          <button
            @click="showBecomeProviderModal = true"
            class="w-full bg-gradient-to-r from-blue-600 to-blue-500 hover:from-blue-500 hover:to-blue-400 text-white font-semibold py-3 rounded-xl transition active:scale-95 flex items-center justify-center gap-2 shadow-lg"
          >
            <span class="text-lg">📝</span> Стать исполнителем
          </button>
          <button
            @click="openSettings"
            class="w-full bg-slate-800 hover:bg-slate-700 border border-slate-700 text-white font-semibold py-3 rounded-xl transition active:scale-95 flex items-center justify-center gap-2"
          >
            <span class="text-lg">⚙️</span> Настройки
          </button>
        </div>
      </div>

      <!-- Tab 2: For Provider -->
      <div v-else class="space-y-4">
        <!-- Services Tab -->
        <div v-if="activeTab === 'services'" class="px-4 pt-4">
          <ProviderServicesSection 
            :services="userStore.providerServices"
            @edit="openEditService"
            @delete="deleteServiceConfirm"
            @add="addNewService"
          />
        </div>

        <!-- Orders Tab (for provider) -->
        <div v-if="activeTab === 'orders'" class="px-4 pt-4">
          <ProviderOrdersSection :orders="providerOrders" />
        </div>

        <!-- Analytics Tab -->
        <div v-if="activeTab === 'analytics' && providerInfo" class="px-4 pt-4">
          <AnalyticsSection :provider-info="providerInfo" />
        </div>

        <!-- Profile Settings (provider) -->
        <div v-if="activeTab === 'profile' && providerInfo" class="px-4 pt-4 pb-6">
          <ProviderProfileSection 
            :provider-info="providerInfo"
            @edit="editProviderProfile"
          />
          <button
            @click="openSettings"
            class="w-full mt-4 bg-slate-800 hover:bg-slate-700 border border-slate-700 text-white font-semibold py-3 rounded-xl transition active:scale-95 flex items-center justify-center gap-2"
          >
            <span class="text-lg">⚙️</span> Настройки
          </button>
        </div>
      </div>
    </div>

    <!-- ======================== MODALS ======================== -->

    <!-- Become Provider Modal -->
    <BecomeProviderModal
      v-if="showBecomeProviderModal"
      @submit="submitProviderProfile"
      @close="closeBecomeProviderModal"
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
import UserStats from '@/components/profile/UserStats.vue'
import ProviderStats from '@/components/profile/ProviderStats.vue'
import TabBar from '@/components/profile/TabBar.vue'
import OrdersSection from '@/components/profile/sections/OrdersSection.vue'
import SavedServicesSection from '@/components/profile/sections/SavedServicesSection.vue'
import ReviewsSection from '@/components/profile/sections/ReviewsSection.vue'
import ProviderServicesSection from '@/components/profile/sections/ProviderServicesSection.vue'
import ProviderOrdersSection from '@/components/profile/sections/ProviderOrdersSection.vue'
import AnalyticsSection from '@/components/profile/sections/AnalyticsSection.vue'
import ProviderProfileSection from '@/components/profile/sections/ProviderProfileSection.vue'
import BecomeProviderModal from '@/components/profile/modals/BecomeProviderModal.vue'
import ServiceModal from '@/components/profile/modals/ServiceModal.vue'

interface Order {
  id: string | number
  clientName: string
  serviceName: string
  date: string
  status: string
  price: number
}

interface ProviderInfo {
  id?: string | number
  name?: string
  bio?: string
  location?: string
  experience?: string
  specializations?: string[]
  email?: string
  phone?: string
  rating?: number
  reviews?: number
  completedOrders?: number
  totalEarnings?: number
  activeServices?: number
  monthlyOrders?: number
  monthlyEarnings?: number
}

const userStore = useUserStore()

interface Props {
  ordersCount?: number
}

withDefaults(defineProps<Props>(), {
  ordersCount: 0
})

// ======================== STATE ========================
const activeTab = ref<string>(!userStore.isProvider ? 'orders' : 'services')
const showBecomeProviderModal = ref(false)
const showServiceModal = ref(false)
const isEditingService = ref(false)
const providerInfo = computed(() => userStore.getProviderInfo())

// Mock data (будет заменено на API данные)
const userOrders = ref([
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

const savedServices = ref([
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

const userReviews = ref([
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

const providerOrders = ref<Order[]>([
  {
    id: 101,
    clientName: 'Анна П.',
    serviceName: 'Web-дизайн',
    date: '15 янв 2025',
    status: 'in_progress',
    price: 15000
  },
  {
    id: 102,
    clientName: 'Иван К.',
    serviceName: 'Дизайн логотипа',
    date: '12 янв 2025',
    status: 'completed',
    price: 3000
  }
])

const currentService = ref<any>(null)

// ======================== COMPUTED ========================
const defaultService = computed(() => ({
  serviceName: '',
  description: '',
  category: '',
  price: 0,
  availability: {
    weekdays: true,
    weekends: false,
    evenings: true
  },
  images: []
}))

// ======================== METHODS ========================
const addNewService = () => {
  isEditingService.value = false
  currentService.value = { ...defaultService.value }
  showServiceModal.value = true
}

const openEditService = (service: any) => {
  isEditingService.value = true
  currentService.value = JSON.parse(JSON.stringify(service))
  showServiceModal.value = true
}

const submitProviderProfile = () => {
  closeBecomeProviderModal()
}

const closeBecomeProviderModal = () => {
  showBecomeProviderModal.value = false
}

const closeServiceModal = () => {
  showServiceModal.value = false
  currentService.value = null
  isEditingService.value = false
}

const submitService = () => {
  closeServiceModal()
}

const deleteServiceConfirm = (serviceId: string | number) => {
  if (confirm('Вы уверены? Услуга будет удалена.')) {
    userStore.deleteService(serviceId)
  }
}

const editProviderProfile = () => {
  showBecomeProviderModal.value = true
}

const openSettings = () => {
  console.log('⚙️ Opening settings')
}
</script>

<style scoped>
.profile-view {
  background: linear-gradient(to bottom, #0f172a, #0f1319);
  min-height: 100vh;
  padding-bottom: 80px;
}

.tab-content {
  animation: fadeIn 0.3s ease-out;
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
</style>
