<template>
  <div class="home-page">
    <!-- Header + TabNavigation Combined -->
    <header class="sticky top-0 z-50 bg-white border-b border-gray-200 shadow-sm" :style="headerStyle">
      <div class="max-w-md mx-auto px-4 py-2">
        <!-- Header Row: Logo + Tabs + Actions -->
        <div class="flex items-center justify-between gap-2">
          <!-- Logo & Branding -->
          <a href="#" @click.prevent="goHome" class="flex items-center gap-2 flex-shrink-0 group">
            <!-- Logo SVG -->
            <div class="w-10 h-10 flex-shrink-0 transition-transform group-hover:scale-105">
              <svg
                viewBox="0 0 220 220"
                fill="none"
                xmlns="http://www.w3.org/2000/svg"
              >
                <g clip-path="url(#clip0_4001_20)">
                  <path d="M1.52588e-05 47.2652C1.52588e-05 21.1613 21.1614 0 47.2652 0L173.306 1.81017e-10C199.41 2.08283e-10 220.571 21.1613 220.571 47.2652L220.571 173.306C220.571 199.41 199.41 220.571 173.306 220.571L47.2652 220.571C21.1614 220.571 1.5259e-05 199.41 1.5259e-05 173.306L1.52588e-05 47.2652Z" fill="#0E1117"/>
                  <mask id="mask0_4001_20" style="mask-type:alpha" maskUnits="userSpaceOnUse" x="0" y="0" width="221" height="221">
                    <path d="M1.52588e-05 47.2652C1.52588e-05 21.1613 21.1614 -1.52588e-05 47.2652 -1.52587e-05L173.306 -1.52586e-05C199.41 -1.52586e-05 220.571 21.1613 220.571 47.2652L220.571 173.306C220.571 199.409 199.41 220.571 173.306 220.571L47.2652 220.571C21.1614 220.571 1.5259e-05 199.409 1.5259e-05 173.306L1.52588e-05 47.2652Z" fill="#4747A6"/>
                  </mask>
                  <g mask="url(#mask0_4001_20)">
                    <path d="M114.697 114.224C51.3516 114.224 3.4062e-05 62.8727 2.02174e-05 -0.472626L1.52589e-05 -23.1599C1.41428e-06 -86.5052 51.3516 -137.857 114.697 -137.857L168.894 -137.857C232.24 -137.857 283.591 -86.5053 283.591 -23.1599L283.591 -0.472687C283.591 62.8726 232.24 114.224 168.894 114.224L114.697 114.224Z" fill="#155DFC"/>
                    <path d="M88.3104 181.183C85.198 181.183 82.4546 179.127 81.5624 176.126L43.6266 48.5098C42.2747 43.962 45.6584 39.3877 50.3745 39.3877L83.7892 39.3877C87.0614 39.3877 89.9027 41.6561 90.6477 44.8633L102.578 96.2214C104.251 103.427 114.396 103.557 116.252 96.3963L129.649 44.6883C130.458 41.5662 133.259 39.3877 136.464 39.3877L172.51 39.3877C175.723 39.3877 178.529 41.5761 179.331 44.7076L192.477 96.0354C194.317 103.222 204.502 103.092 206.16 95.8601L217.85 44.8829C218.587 41.6662 221.433 39.3876 224.713 39.3876L256.849 39.3876C261.565 39.3876 264.949 43.9619 263.597 48.5098L225.661 176.126C224.769 179.127 222.026 181.183 218.913 181.183L181.333 181.183C178.155 181.183 175.37 179.041 174.536 175.954L160.36 123.484C158.47 116.491 148.606 116.52 146.756 123.523L132.918 175.915C132.098 179.021 129.304 181.183 126.111 181.183L88.3104 181.183Z" fill="white"/>
                  </g>
                </g>
                <defs>
                  <clipPath id="clip0_4001_20">
                    <rect width="220.571" height="220.571" fill="white" transform="translate(1.52588e-05 220.571) rotate(-90)"/>
                  </clipPath>
                </defs>
              </svg>
            </div>

            <!-- Brand Text -->
            <div class="flex flex-col gap-0.5">
              <span class="font-bold text-sm leading-none" :style="{ color: textColor }">Deaf</span>
              <span class="text-xs leading-none" :style="{ color: hintColor }">услуги</span>
            </div>
          </a>

          <!-- Navigation Tabs (Center) -->
          <div class="flex gap-2 flex-1 justify-center">
            <button
              v-for="tab in tabs"
              :key="tab.id"
              @click="currentTab = tab.id"
              class="flex items-center justify-center px-2 py-1 rounded-md text-xs font-medium transition-all"
              :class="currentTab === tab.id ? 'bg-white border border-black text-black' : 'bg-gray-100 border border-gray-200 text-gray-600 hover:bg-gray-200'"
              :title="tab.label"
            >
              <component :is="getTabIcon(tab.id)" class="w-4 h-4" />
              <span class="hidden sm:inline ml-1">{{ tab.label }}</span>
            </button>

            <!-- Add Service Button (для исполнителей) -->
            <button
              v-if="isProvider"
              @click="addService"
              class="flex items-center justify-center px-2 py-1 rounded-md text-xs font-medium bg-gray-100 border border-gray-200 text-gray-600 hover:bg-gray-200 transition-all"
              title="Добавить услугу"
            >
              <span class="text-lg">+</span>
            </button>
          </div>

          <!-- Right Actions -->
          <div class="flex items-center gap-2 flex-shrink-0">
            <!-- Profile Button -->
            <button
              v-if="userData?.username"
              @click="currentTab = 'profile'"
              class="flex items-center justify-center w-9 h-9 rounded-full text-white text-xs font-bold hover:shadow-md transition-all active:scale-95"
              :style="avatarStyle"
              :title="userData.first_name"
            >
              {{ getUserInitials(userData.first_name) }}
            </button>
          </div>
        </div>
      </div>
    </header>

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

    <!-- Toast Notification -->
    <Toast
      v-if="showToast"
      :message="toastMessage"
    />
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import Header from '../components/layout/Header.vue'
import Toast from '../components/shared/Toast.vue'
import BrowseServices from '../views/BrowseServices.vue'
import CatalogView from '../views/CatalogView.vue'
import OrdersView from '../views/OrdersView.vue'
import ProfileView from '../views/ProfileView.vue'

const currentTab = ref('browse')
const searchQuery = ref('')
const selectedCategory = ref('')
const showToast = ref(false)
const toastMessage = ref('')
const isProvider = ref(true)
const isDarkMode = ref(false)

const userData = ref({
  first_name: 'Иван',
  id: '123456789',
  username: 'ivan_user'
})

const tabs = [
  { id: 'browse', label: 'Обзор', icon: 'IconSearch' },
  { id: 'catalog', label: 'Каталог', icon: 'IconFolder' },
  { id: 'orders', label: 'Заказы', icon: 'IconOrders' }
]

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

const headerStyle = computed(() => ({
  backgroundColor: bgColor.value,
  color: textColor.value,
  borderColor: isDarkMode.value ? '#374151' : '#e5e5e5'
}))

const avatarStyle = computed(() => ({
  background: `linear-gradient(135deg, ${buttonColor.value} 0%, rgba(37, 99, 235, 0.8) 100%)`
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

const getTabIcon = (tabId: string) => {
  const icons: Record<string, any> = {
    browse: { template: '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="11" cy="11" r="8"></circle><path d="m21 21-4.35-4.35"></path></svg>' },
    catalog: { template: '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M22 19a2 2 0 0 1-2 2H4a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h5l2 3h9a2 2 0 0 1 2 2z"></path></svg>' },
    orders: { template: '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M6 2h12a2 2 0 0 1 2 2v16a2 2 0 0 1-2 2H6a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2z"></path><line x1="6" y1="6" x2="18" y2="6"></line><line x1="6" y1="10" x2="18" y2="10"></line><line x1="6" y1="14" x2="18" y2="14"></line></svg>' }
  }
  return icons[tabId] || { template: '' }
}

const goHome = () => {
  currentTab.value = 'browse'
}

const selectService = (service: any) => {
  console.log('Услуга выбрана:', service.name)
}

const orderService = (service: any) => {
  console.log('Заказ услуги:', service.name)
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
@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(-2px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

header {
  animation: fadeIn 0.3s ease-out;
}

button:focus-visible {
  outline: 2px solid #0055ff;
  outline-offset: 2px;
}

button {
  transition: all 0.2s ease;
}

button:active {
  transition: transform 0.1s ease;
}
</style>