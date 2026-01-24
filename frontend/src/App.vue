<template>
  <div class="home-page">
    <!-- Header with Logo, Tabs, and Avatar -->
    <Header
      :user-name="userData?.first_name"
      :user-initials="getUserInitials(userData?.first_name)"
      :button-color="buttonColor"
      :current-tab="currentTab"
      @go-home="goHome"
      @open-profile="currentTab = 'profile'"
      @update:current-tab="currentTab = $event"
    />

    <!-- Main Content -->
    <main class="max-w-md mx-auto pb-20">
      <!-- Browse Services View -->
      <BrowseServices
        v-if="currentTab === 'browse'"
        :services="services"
        :searchQuery="searchQuery"
        :selectedCategory="selectedCategory"
        :categories="categories"
        @update:searchQuery="searchQuery = $event"
        @update:selectedCategory="selectedCategory = $event"
        @select-service="selectService"
        @order-service="orderService"
      />

      <!-- Catalog View -->
      <CatalogView
        v-else-if="currentTab === 'catalog'"
        :catalogCategories="catalogCategories"
        @category-selected="onCategorySelected"
      />

      <!-- Orders View -->
      <OrdersView
        v-else-if="currentTab === 'orders'"
        :userOrders="userOrders"
        @browse-services="currentTab = 'browse'"
        @cancel-order="cancelOrder"
      />

      <!-- Profile View -->
      <ProfileView
        v-else-if="currentTab === 'profile'"
        :userData="userData"
        :ordersCount="userOrders.length"
        @become-provider="becomeProvider"
        @open-settings="openSettings"
      />
    </main>

    <!-- Order Modal -->
    <Modal
      :is-open="showOrderModal"
      :title="selectedService?.name"
      :large="true"
      @close="closeOrderModal"
    >
      <template v-if="selectedService">
        <!-- Service Image -->
        <img
          v-if="selectedService.images?.[0]"
          :src="selectedService.images[0]"
          :alt="selectedService.name"
          class="service-image"
        />

        <!-- Provider Info -->
        <div class="provider-info">
          <div class="avatar" :style="avatarStyle">{{ getInitials(selectedService.provider) }}</div>
          <div class="provider-details">
            <p class="provider-name">{{ selectedService.provider }}</p>
            <p class="rating">★ {{ selectedService.providerRating }} ({{ selectedService.reviews }} отзывов)</p>
          </div>
        </div>

        <!-- Description -->
        <div class="description">
          <h3 class="description-title">Описание</h3>
          <p class="description-text">{{ selectedService.fullDescription }}</p>
        </div>

        <!-- Details -->
        <div class="details-grid">
          <div class="detail-item">
            <span class="detail-label">Цена</span>
            <span class="detail-value">{{ formatPrice(selectedService.price) }}</span>
          </div>
          <div class="detail-item">
            <span class="detail-label">Ответит в</span>
            <span class="detail-value">{{ selectedService.response_time }}</span>
          </div>
          <div class="detail-item">
            <span class="detail-label">Категория</span>
            <span class="detail-value">{{ selectedService.category }}</span>
          </div>
          <div class="detail-item">
            <span class="detail-label">Отзывов</span>
            <span class="detail-value">{{ selectedService.reviews }}</span>
          </div>
        </div>
      </template>

      <template #footer>
        <button
          class="btn btn-secondary"
          @click="closeOrderModal"
        >
          Назад
        </button>
        <button
          class="btn btn-primary"
          @click="confirmOrder"
        >
          Подтвердить заказ
        </button>
      </template>
    </Modal>

    <!-- Toast Notification -->
    <Toast
      v-if="showToast"
      :message="toastMessage"
    />
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import Header from '@/components/layout/Header.vue'
import Modal from '@/components/shared/Modal.vue'
import Toast from '@/components/shared/Toast.vue'
import BrowseServices from '@/views/BrowseServices.vue'
import CatalogView from '@/views/CatalogView.vue'
import OrdersView from '@/views/OrdersView.vue'
import ProfileView from '@/views/ProfileView.vue'

const currentTab = ref('browse')
const searchQuery = ref('')
const selectedCategory = ref('')
const showToast = ref(false)
const toastMessage = ref('')
const isProvider = ref(true)
const isDarkMode = ref(false)
const showOrderModal = ref(false)
const selectedService = ref<any>(null)

const userData = ref({
  first_name: 'Иван',
  id: '123456789',
  username: 'ivan_user'
})

const categories = ['Ремонт', 'Бизнес', 'Мода', 'Обучение', 'Дизайн']
const catalogCategories = [
  { id: 1, name: 'Ремонт', icon: '🔧', count: 23 },
  { id: 2, name: 'Бизнес', icon: '📊', count: 18 },
  { id: 3, name: 'Мода', icon: '✌️', count: 34 },
  { id: 4, name: 'Обучение', icon: '📖', count: 45 },
  { id: 5, name: 'Дизайн', icon: '🎭', count: 29 },
  { id: 6, name: 'IT', icon: '💻', count: 56 }
]

const services = ref([
  {
    id: 1,
    name: 'Услуга сантехника',
    provider: 'Олег М.',
    category: 'Ремонт',
    description: 'Профессиональный ремонт и монтаж сантехники',
    fullDescription: 'Профессиональный ремонт и монтаж сантехники с гарантией. Выполняю любые работы: замену кранов, чистку труб, установку полотенцесушителей. 10 лет опыта, работаю быстро и аккуратно.',
    price: 2500,
    reviews: 156,
    response_time: '< 1 часа',
    providerRating: 4.9,
    images: ['https://via.placeholder.com/300x200?text=Сантехника+1', 'https://via.placeholder.com/300x200?text=Сантехника+2', 'https://via.placeholder.com/300x200?text=Сантехника+3'],
    currentImageIndex: 0
  },
  {
    id: 2,
    name: 'Консультация бухгалтера',
    provider: 'Мария С.',
    category: 'Бизнес',
    description: 'Налоговое планирование и бухгалтерская отчетность',
    fullDescription: 'Профессиональная консультация по налоговому планированию, ведение бухгалтерского учета, подготовка отчетности. Помогу оптимизировать налоги и разобраться в законодательстве.',
    price: 3000,
    reviews: 89,
    response_time: '< 2 часов',
    providerRating: 4.7,
    images: ['https://via.placeholder.com/300x200?text=Бухгалтер+1', 'https://via.placeholder.com/300x200?text=Бухгалтер+2'],
    currentImageIndex: 0
  },
  {
    id: 3,
    name: 'Пошив платья',
    provider: 'Анна Т.',
    category: 'Мода',
    description: 'Изготовление платьев и костюмов по индивидуальному заказу',
    fullDescription: 'Создам платье вашей мечты! Работаю с любыми тканями, помогу с выбором фасона. Изготовлю платье, юбку, костюм - всё шьются по вашим меркам и предпочтениям.',
    price: 5000,
    reviews: 234,
    response_time: '< 3 часов',
    providerRating: 4.8,
    images: ['https://via.placeholder.com/300x200?text=Платье+1', 'https://via.placeholder.com/300x200?text=Платье+2', 'https://via.placeholder.com/300x200?text=Платье+3'],
    currentImageIndex: 0
  },
  {
    id: 4,
    name: 'Уроки английского',
    provider: 'Джон Д.',
    category: 'Обучение',
    description: 'Индивидуальные занятия по английскому языку',
    fullDescription: 'Native speaker проводит индивидуальные занятия английским. Программа подбирается под ваш уровень и цели. Разговорный курс, подготовка к экзаменам, бизнес-английский.',
    price: 1500,
    reviews: 412,
    response_time: '< 30 мин',
    providerRating: 4.9,
    images: ['https://via.placeholder.com/300x200?text=Учитель+1', 'https://via.placeholder.com/300x200?text=Учитель+2'],
    currentImageIndex: 0
  },
  {
    id: 5,
    name: 'Web-дизайн сайта',
    provider: 'Артем К.',
    category: 'Дизайн',
    description: 'Создание современного дизайна вашего сайта',
    fullDescription: 'Создам красивый и функциональный дизайн вашего сайта. Работаю в современных стилях, адаптирую под мобильные устройства, учитываю ваши пожелания и особенности бизнеса.',
    price: 15000,
    reviews: 67,
    response_time: '< 4 часов',
    providerRating: 4.9,
    images: ['https://via.placeholder.com/300x200?text=Дизайн+1', 'https://via.placeholder.com/300x200?text=Дизайн+2', 'https://via.placeholder.com/300x200?text=Дизайн+3'],
    currentImageIndex: 0
  },
  {
    id: 6,
    name: 'Обслуживание ПК',
    provider: 'Вадим Н.',
    category: 'Ремонт',
    description: 'Чистка, диагностика и ремонт компьютеров',
    fullDescription: 'Профессиональная диагностика и ремонт компьютеров. Чищу от пыли, устраняю ошибки, устанавливаю ПО, заменяю неисправные детали. Быстрая и качественная работа.',
    price: 1800,
    reviews: 178,
    response_time: '< 2 часов',
    providerRating: 4.8,
    images: ['https://via.placeholder.com/300x200?text=ПК+1', 'https://via.placeholder.com/300x200?text=ПК+2'],
    currentImageIndex: 0
  }
])

const userOrders = ref([
  {
    id: 1,
    service: 'Уроки английского',
    provider: 'Джон Д.',
    status: 'active',
    price: 1500,
    date: 'сегодня 15:00'
  },
  {
    id: 2,
    service: 'Консультация бухгалтера',
    provider: 'Мария С.',
    status: 'pending',
    price: 3000,
    date: 'завтра 10:00'
  }
])

const getTelegramThemeParams = () => {
  if (!window.Telegram?.WebApp?.themeParams) {
    return {
      bg_color: '#ffffff',
      text_color: '#000000',
      hint_color: '#6b7280',
      button_color: '#2563eb'
    }
  }
  return window.Telegram.WebApp.themeParams
}

const themeParams = computed(() => getTelegramThemeParams())

const textColor = computed(() => themeParams.value.text_color || '#000000')
const hintColor = computed(() => themeParams.value.hint_color || '#6b7280')
const bgColor = computed(() => themeParams.value.bg_color || '#ffffff')
const buttonColor = computed(() => themeParams.value.button_color || '#2563eb')

const avatarStyle = computed(() => ({
  backgroundColor: '#2563eb',
  borderColor: '#2563eb'
}))

const getUserInitials = (name?: string): string => {
  if (!name) return '?'
  return name
    .split(' ')
    .map(word => word[0])
    .join('')
    .toUpperCase()
    .slice(0, 2)
}

const getInitials = (name?: string): string => {
  if (!name) return '?'
  return name
    .split(' ')
    .map(word => word[0])
    .join('')
    .toUpperCase()
    .slice(0, 2)
}

const formatPrice = (price?: number) => {
  if (!price) return '—'
  return new Intl.NumberFormat('ru-RU', {
    style: 'currency',
    currency: 'RUB',
    minimumFractionDigits: 0
  }).format(price)
}

const goHome = () => {
  currentTab.value = 'browse'
}

const selectService = (service: any) => {
  console.log('Услуга выбрана:', service.name)
}

const orderService = (service: any) => {
  selectedService.value = service
  showOrderModal.value = true
}

const closeOrderModal = () => {
  showOrderModal.value = false
  selectedService.value = null
}

const confirmOrder = () => {
  if (!selectedService.value) return

  // Add to user orders
  userOrders.value.push({
    id: Math.max(...userOrders.value.map(o => o.id), 0) + 1,
    service: selectedService.value.name,
    provider: selectedService.value.provider,
    status: 'pending',
    price: selectedService.value.price,
    date: 'ожидание подтверждения'
  })

  // Show success message
  showToast.value = true
  toastMessage.value = `✓ Заказ "${selectedService.value.name}" создан!`
  setTimeout(() => {
    showToast.value = false
  }, 3000)

  closeOrderModal()
}

const onCategorySelected = (category: any) => {
  selectedCategory.value = category.name
  currentTab.value = 'browse'
}

const cancelOrder = (orderId: number) => {
  userOrders.value = userOrders.value.filter(order => order.id !== orderId)
  showToast.value = true
  toastMessage.value = '✓ Заказ отменен'
  setTimeout(() => {
    showToast.value = false
  }, 3000)
}

const becomeProvider = () => {
  showToast.value = true
  toastMessage.value = 'Скоро вы сможете стать исполнителем!'
  setTimeout(() => {
    showToast.value = false
  }, 3000)
}

const openSettings = () => {
  showToast.value = true
  toastMessage.value = 'Настройки откроются вскоре'
  setTimeout(() => {
    showToast.value = false
  }, 3000)
}

const addService = () => {
  showToast.value = true
  toastMessage.value = '+ Добавить новую услугу'
  setTimeout(() => {
    showToast.value = false
  }, 3000)
}

onMounted(() => {
  if (window.Telegram?.WebApp) {
    const tg = window.Telegram.WebApp
    tg.ready()
    tg.setHeaderColor('#FFFFFF')
  }
})
</script>

<style scoped>
.home-page {
  width: 100%;
  height: 100%;
}

/* Modal Styles */
.service-image {
  width: 100%;
  height: 200px;
  object-fit: cover;
  border-radius: 0;
  margin: -16px -16px 16px -16px;
}

.provider-info {
  display: flex;
  gap: 12px;
  align-items: center;
  padding: 12px;
  background: #f9f9f9;
  border-radius: 12px;
  margin-bottom: 16px;
}

.avatar {
  width: 48px;
  height: 48px;
  border-radius: 50%;
  background: #2563eb;
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 700;
  font-size: 0.875rem;
  flex-shrink: 0;
}

.provider-details {
  flex: 1;
}

.provider-name {
  font-weight: 600;
  color: #000;
  margin: 0 0 4px 0;
  font-size: 0.95rem;
}

.rating {
  font-size: 0.8rem;
  color: #666;
  margin: 0;
}

.description {
  margin-bottom: 16px;
}

.description-title {
  font-size: 0.95rem;
  font-weight: 600;
  color: #000;
  margin: 0 0 8px 0;
}

.description-text {
  font-size: 0.875rem;
  color: #666;
  line-height: 1.5;
  margin: 0;
}

.details-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 12px;
  margin-bottom: 16px;
}

.detail-item {
  padding: 12px;
  background: #f9f9f9;
  border-radius: 8px;
  display: flex;
  flex-direction: column;
}

.detail-label {
  font-size: 0.75rem;
  color: #999;
  font-weight: 500;
  margin-bottom: 4px;
}

.detail-value {
  font-size: 0.95rem;
  font-weight: 600;
  color: #000;
}

/* Buttons */
.btn {
  flex: 1;
  padding: 12px 16px;
  border: none;
  border-radius: 8px;
  font-weight: 600;
  font-size: 0.875rem;
  cursor: pointer;
  transition: all 0.2s ease;
}

.btn-primary {
  background: #2563eb;
  color: white;
}

.btn-primary:hover {
  background: #1d4ed8;
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(37, 99, 235, 0.3);
}

.btn-primary:active {
  transform: scale(0.98);
}

.btn-secondary {
  background: #f0f0f0;
  color: #000;
}

.btn-secondary:hover {
  background: #e0e0e0;
  transform: translateY(-1px);
}

.btn-secondary:active {
  transform: scale(0.98);
}
</style>