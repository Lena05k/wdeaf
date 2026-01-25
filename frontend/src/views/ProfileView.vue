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
      @edit-profile="openEditProfile"
      @view-orders="showTabModal('orders')"
      @view-reviews="showTabModal('reviews')"
      @view-saved="showTabModal('saved')"
      @view-incoming-orders="showTabModal('incoming')"
      @view-active-orders="showTabModal('activeProvider')"
      @view-completed-orders="showTabModal('completedProvider')"
      @view-services="showTabModal('services')"
      @view-rating="showTabModal('rating')"
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

    <!-- Tab Content Modals -->
    <!-- Orders Modal (Customer) -->
    <div v-if="activeTabModal === 'orders'" class="modal-overlay" @click="closeTabModal">
      <div class="modal-content" @click.stop>
        <div class="modal-header">
          <h2>📋 Мои заказы</h2>
          <button @click="closeTabModal" class="close-btn">✕</button>
        </div>
        <div class="modal-body">
          <div v-if="customerOrders.length === 0" class="empty-state">
            <p>Нет заказов</p>
          </div>
          <div v-else class="items-list">
            <div v-for="order in customerOrders" :key="order.id" class="item-card">
              <div class="item-header">
                <h3>{{ order.service }}</h3>
                <span class="status-badge" :class="`status-${order.status}`">{{ order.status }}</span>
              </div>
              <p><strong>Мастер:</strong> {{ order.provider }}</p>
              <p><strong>Цена:</strong> {{ order.price }} ₽</p>
              <p><strong>Дата:</strong> {{ order.date }}</p>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Reviews Modal -->
    <div v-if="activeTabModal === 'reviews'" class="modal-overlay" @click="closeTabModal">
      <div class="modal-content" @click.stop>
        <div class="modal-header">
          <h2>⭐ Мои отзывы</h2>
          <button @click="closeTabModal" class="close-btn">✕</button>
        </div>
        <div class="modal-body">
          <div v-if="userReviews.length === 0" class="empty-state">
            <p>Нет отзывов</p>
          </div>
          <div v-else class="items-list">
            <div v-for="review in userReviews" :key="review.id" class="item-card">
              <div class="item-header">
                <h3>{{ review.serviceName }}</h3>
                <span class="rating">{{ review.rating }}⭐</span>
              </div>
              <p><strong>Мастер:</strong> {{ review.provider }}</p>
              <p>{{ review.text }}</p>
              <p class="date">{{ review.date }}</p>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Saved Services Modal -->
    <div v-if="activeTabModal === 'saved'" class="modal-overlay" @click="closeTabModal">
      <div class="modal-content" @click.stop>
        <div class="modal-header">
          <h2>❤️ Сохраненные услуги</h2>
          <button @click="closeTabModal" class="close-btn">✕</button>
        </div>
        <div class="modal-body">
          <div v-if="savedServices.length === 0" class="empty-state">
            <p>Нет сохраненных услуг</p>
          </div>
          <div v-else class="items-list">
            <div v-for="service in savedServices" :key="service.id" class="item-card">
              <h3>{{ service.name }}</h3>
              <p>{{ service.description }}</p>
              <p><strong>Цена:</strong> {{ service.price }} ₽</p>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Incoming Orders Modal (Provider) -->
    <div v-if="activeTabModal === 'incoming'" class="modal-overlay" @click="closeTabModal">
      <div class="modal-content" @click.stop>
        <div class="modal-header">
          <h2>📬 Входящие заказы</h2>
          <button @click="closeTabModal" class="close-btn">✕</button>
        </div>
        <div class="modal-body">
          <div v-if="incomingOrders.length === 0" class="empty-state">
            <p>Нет входящих заказов</p>
          </div>
          <div v-else class="items-list">
            <div v-for="order in incomingOrders" :key="order.id" class="item-card">
              <div class="item-header">
                <h3>{{ order.service }}</h3>
                <span class="badge-pending">Пендинг</span>
              </div>
              <p><strong>Цена:</strong> {{ order.price }} ₽</p>
              <p><strong>Дата:</strong> {{ order.date }}</p>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Active Orders Modal (Provider) -->
    <div v-if="activeTabModal === 'activeProvider'" class="modal-overlay" @click="closeTabModal">
      <div class="modal-content" @click.stop>
        <div class="modal-header">
          <h2>⚡ Активные заказы</h2>
          <button @click="closeTabModal" class="close-btn">✕</button>
        </div>
        <div class="modal-body">
          <div v-if="providerActiveOrders.length === 0" class="empty-state">
            <p>Нет активных заказов</p>
          </div>
          <div v-else class="items-list">
            <div v-for="order in providerActiveOrders" :key="order.id" class="item-card">
              <div class="item-header">
                <h3>{{ order.service }}</h3>
                <span class="badge-active">В работе</span>
              </div>
              <p><strong>Цена:</strong> {{ order.price }} ₽</p>
              <p><strong>Дата:</strong> {{ order.date }}</p>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Completed Orders Modal (Provider) -->
    <div v-if="activeTabModal === 'completedProvider'" class="modal-overlay" @click="closeTabModal">
      <div class="modal-content" @click.stop>
        <div class="modal-header">
          <h2>✅ Завершенные заказы</h2>
          <button @click="closeTabModal" class="close-btn">✕</button>
        </div>
        <div class="modal-body">
          <div v-if="providerCompletedOrders.length === 0" class="empty-state">
            <p>Нет завершенных заказов</p>
          </div>
          <div v-else class="items-list">
            <div v-for="order in providerCompletedOrders" :key="order.id" class="item-card">
              <div class="item-header">
                <h3>{{ order.service }}</h3>
                <span class="badge-completed">{{ order.rating }}⭐</span>
              </div>
              <p><strong>Цена:</strong> {{ order.price }} ₽</p>
              <p><strong>Дата:</strong> {{ order.date }}</p>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Services Modal (Provider) -->
    <div v-if="activeTabModal === 'services'" class="modal-overlay" @click="closeTabModal">
      <div class="modal-content" @click.stop>
        <div class="modal-header">
          <h2>📦 Мои услуги</h2>
          <button @click="closeTabModal" class="close-btn">✕</button>
        </div>
        <div class="modal-body">
          <div v-if="providerServices.length === 0" class="empty-state">
            <p>Нет услуг</p>
          </div>
          <div v-else class="items-list">
            <div v-for="service in providerServices" :key="service.id" class="item-card">
              <h3>{{ service.name }}</h3>
              <p>{{ service.description }}</p>
              <p><strong>Цена:</strong> {{ service.price }} ₽</p>
              <p><strong>Категория:</strong> {{ service.category }}</p>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Rating Modal (Provider) -->
    <div v-if="activeTabModal === 'rating'" class="modal-overlay" @click="closeTabModal">
      <div class="modal-content" @click.stop>
        <div class="modal-header">
          <h2>⭐ Моя репутация</h2>
          <button @click="closeTabModal" class="close-btn">✕</button>
        </div>
        <div class="modal-body">
          <div class="rating-display">
            <div class="rating-big">{{ providerRating }}</div>
            <div class="rating-stats">
              <p><strong>{{ providerReviews }} отзывов</strong></p>
              <p>{{ providerCompletedOrders.length }} завершенных заказов</p>
            </div>
          </div>
        </div>
      </div>
    </div>
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
const activeTabModal = ref<string | null>(null)

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

const showTabModal = (tab: string) => {
  activeTabModal.value = tab
}

const closeTabModal = () => {
  activeTabModal.value = null
}

/**
 * КРИТИЧНОЕ ИСПРАВЛЕНИЕ: Правильное сохранение профиля провайдера
 */
const submitProviderProfile = (profileData: any) => {
  userStore.setProviderInfo({
    serviceName: profileData.name || 'Мои услуги',
    description: profileData.description,
    categories: profileData.categories,
    price: 0,
    timezone: profileData.timezone,
    availability: profileData.availability,
    maxConcurrentOrders: 5
  })

  showBecomeProviderModal.value = false
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
    const index = providerServices.value.findIndex(s => s.id === service.id)
    if (index !== -1) {
      providerServices.value[index] = service
    }
  } else {
    const newService: Service = {
      ...service,
      id: Date.now()
    }
    providerServices.value.push(newService)
    
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

const handleStopBeingProvider = () => {
  const confirmed = confirm(
    'Вы действительно хотите прекратить быть исполнителем?\n\nПосле этого:\n- Ваши услуги будут скрыты\n- Клиенты не смогут платить вам\n- Вы останетесь обычным пользователем\n- Вы сможете купить услуги других'
  )
  
  if (confirmed) {
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
  }
}
</script>

<style scoped>
.profile-view {
  background: linear-gradient(to bottom, #0f172a, #0f1319);
  min-height: 100vh;
  padding-bottom: 80px;
}

/* Modal Overlay */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.8);
  display: flex;
  align-items: flex-end;
  z-index: 100;
  animation: slideUp 0.3s ease;
}

@keyframes slideUp {
  from {
    opacity: 0;
    transform: translateY(100%);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.modal-content {
  background: linear-gradient(to bottom, #1e293b, #0f1319);
  width: 100%;
  max-height: 90vh;
  border-radius: 24px 24px 0 0;
  border: 1px solid rgba(148, 163, 184, 0.1);
  border-bottom: none;
  display: flex;
  flex-direction: column;
  overflow: hidden;
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1.5rem;
  border-bottom: 1px solid rgba(148, 163, 184, 0.1);
  background: linear-gradient(to bottom, #1e293b, #0f172a);
  flex-shrink: 0;
}

.modal-header h2 {
  margin: 0;
  font-size: 1.25rem;
  color: white;
}

.close-btn {
  background: none;
  border: none;
  color: #94a3b8;
  font-size: 1.5rem;
  cursor: pointer;
  padding: 0;
  width: 32px;
  height: 32px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 8px;
  transition: all 0.2s ease;
}

.close-btn:hover {
  background: rgba(148, 163, 184, 0.1);
  color: white;
}

.modal-body {
  flex: 1;
  overflow-y: auto;
  padding: 1.5rem;
}

.empty-state {
  display: flex;
  align-items: center;
  justify-content: center;
  min-height: 200px;
  color: #64748b;
  text-align: center;
}

.empty-state p {
  margin: 0;
  font-size: 0.9375rem;
}

.items-list {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.item-card {
  background: rgba(30, 41, 59, 0.5);
  border: 1px solid rgba(148, 163, 184, 0.1);
  border-radius: 12px;
  padding: 1rem;
  color: white;
}

.item-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 0.75rem;
}

.item-header h3 {
  margin: 0;
  font-size: 1rem;
  color: white;
}

.status-badge,
.badge-pending,
.badge-active,
.badge-completed {
  display: inline-block;
  padding: 0.25rem 0.75rem;
  border-radius: 12px;
  font-size: 0.75rem;
  font-weight: 500;
}

.status-pending {
  background: rgba(251, 146, 60, 0.2);
  color: #fb923c;
}

.status-active {
  background: rgba(59, 130, 246, 0.2);
  color: #3b82f6;
}

.status-completed {
  background: rgba(34, 197, 94, 0.2);
  color: #22c55e;
}

.badge-pending {
  background: rgba(251, 146, 60, 0.2);
  color: #fb923c;
}

.badge-active {
  background: rgba(59, 130, 246, 0.2);
  color: #3b82f6;
}

.badge-completed {
  background: rgba(34, 197, 94, 0.2);
  color: #22c55e;
}

.rating {
  color: #fbbf24;
  font-weight: 600;
}

.item-card p {
  margin: 0.5rem 0;
  font-size: 0.875rem;
  color: rgba(226, 232, 240, 0.8);
}

.item-card p strong {
  color: #e2e8f0;
}

.item-card .date {
  margin-top: 0.75rem;
  color: #64748b;
  font-size: 0.75rem;
}

.rating-display {
  display: flex;
  align-items: center;
  gap: 2rem;
  padding: 2rem;
  background: rgba(30, 41, 59, 0.5);
  border-radius: 12px;
  border: 1px solid rgba(148, 163, 184, 0.1);
}

.rating-big {
  font-size: 3rem;
  font-weight: bold;
  color: #fbbf24;
}

.rating-stats p {
  margin: 0.5rem 0;
  color: #e2e8f0;
}

.rating-stats p:first-child {
  font-size: 1.125rem;
  font-weight: 600;
}

.rating-stats p:last-child {
  color: #94a3b8;
  font-size: 0.875rem;
}
</style>