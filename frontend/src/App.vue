<template>
  <div class="home-page" :style="{ backgroundColor: bgColor, color: textColor }">
    <!-- Улучшенный Header: Минимализм, Красота, Фокусируемость -->
    <header 
      class="sticky top-0 z-50 transition-all duration-300 ease-out"
      :class="{
        'shadow-lg backdrop-blur-sm bg-white/95': isScrolled,
        'shadow-none bg-white': !isScrolled
      }"
      :style="headerDynamicStyle"
    >
      <div class="max-w-md mx-auto px-4 py-3">
        <!-- Header Container: Responsive Grid Layout -->
        <div class="flex items-center justify-between gap-4">
          <!-- Logo & Brand (Left) -->
          <button
            @click="goHome"
            @keydown.enter="goHome"
            @keydown.space="goHome"
            class="logo-btn group flex items-center gap-2.5 flex-shrink-0"
            title="На главную"
            aria-label="WDEAF Главная"
          >
            <!-- Логотип с анимацией -->
            <div class="logo-container w-9 h-9 flex-shrink-0 transition-all duration-300 group-hover:scale-110 group-focus-visible:scale-110">
              <svg
                viewBox="0 0 220 220"
                fill="none"
                xmlns="http://www.w3.org/2000/svg"
                class="w-full h-full"
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
            <!-- Brand Text (скрыт на мобилах) -->
            <span class="hidden sm:inline text-sm font-bold text-gray-900">WDEAF</span>
          </button>

          <!-- Navigation Tabs (Center) - Улучшенный дизайн 2025 -->
          <nav 
            class="flex gap-1.5 flex-1 justify-center items-center flex-wrap"
            role="tablist"
          >
            <!-- Обзор Tab -->
            <button
              role="tab"
              :aria-selected="currentTab === 'browse'"
              :aria-controls="`panel-browse`"
              @click="currentTab = 'browse'"
              @keydown.arrow-right="selectNextTab"
              @keydown.arrow-left="selectPrevTab"
              class="nav-tab"
              :class="{ 'nav-tab--active': currentTab === 'browse' }"
              title="Обзор доступных услуг"
            >
              <svg class="w-4 h-4" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5">
                <circle cx="11" cy="11" r="8"></circle>
                <path d="m21 21-4.35-4.35"></path>
              </svg>
              <span class="hidden sm:inline text-sm font-medium">Обзор</span>
            </button>

            <!-- Каталог Tab -->
            <button
              role="tab"
              :aria-selected="currentTab === 'catalog'"
              :aria-controls="`panel-catalog`"
              @click="currentTab = 'catalog'"
              class="nav-tab"
              :class="{ 'nav-tab--active': currentTab === 'catalog' }"
              title="Категории услуг"
            >
              <svg class="w-4 h-4" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5">
                <path d="M22 19a2 2 0 0 1-2 2H4a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h5l2 3h9a2 2 0 0 1 2 2z"></path>
              </svg>
              <span class="hidden sm:inline text-sm font-medium">Каталог</span>
            </button>

            <!-- Заказы Tab -->
            <button
              role="tab"
              :aria-selected="currentTab === 'orders'"
              :aria-controls="`panel-orders`"
              @click="currentTab = 'orders'"
              class="nav-tab"
              :class="{ 'nav-tab--active': currentTab === 'orders' }"
              title="Мои заказы"
            >
              <svg class="w-4 h-4" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5">
                <path d="M6 2h12a2 2 0 0 1 2 2v16a2 2 0 0 1-2 2H6a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2z"></path>
                <line x1="6" y1="6" x2="18" y2="6"></line>
                <line x1="6" y1="10" x2="18" y2="10"></line>
                <line x1="6" y1="14" x2="18" y2="14"></line>
              </svg>
              <span class="hidden sm:inline text-sm font-medium">Заказы</span>
            </button>

            <!-- Add Service Button (для исполнителей) -->
            <button
              v-if="isProvider"
              @click="addService"
              class="nav-tab nav-tab--add"
              title="Добавить новую услугу"
              aria-label="Добавить услугу"
            >
              <svg class="w-4 h-4" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3">
                <line x1="12" y1="5" x2="12" y2="19"></line>
                <line x1="5" y1="12" x2="19" y2="12"></line>
              </svg>
            </button>
          </nav>

          <!-- Right Actions (Profile & More) -->
          <div class="flex items-center gap-2.5 flex-shrink-0">
            <!-- Profile Button - Улучшенная версия -->
            <button
              v-if="userData?.username"
              @click="currentTab = 'profile'"
              @keydown.enter="currentTab = 'profile'"
              class="profile-btn"
              :title="`Профиль ${userData.first_name}`"
              :aria-label="`Профиль пользователя ${userData.first_name}`"
              :style="{
                backgroundColor: buttonColor,
                borderColor: buttonColor
              }"
            >
              <span class="font-semibold text-xs sm:text-sm">{{ getUserInitials(userData.first_name) }}</span>
            </button>
          </div>
        </div>
      </div>
    </header>

    <!-- Main Content -->
    <main class="max-w-md mx-auto pb-20">
      <!-- Browse Services View -->
      <div id="panel-browse" role="tabpanel" :aria-labelledby="'browse-tab'">
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
      </div>

      <!-- Catalog View -->
      <div id="panel-catalog" role="tabpanel" :aria-labelledby="'catalog-tab'">
        <CatalogView
          v-else-if="currentTab === 'catalog'"
          :catalogCategories="catalogCategories"
          @category-selected="onCategorySelected"
        />
      </div>

      <!-- Orders View -->
      <div id="panel-orders" role="tabpanel" :aria-labelledby="'orders-tab'">
        <OrdersView
          v-else-if="currentTab === 'orders'"
          :userOrders="userOrders"
          @browse-services="currentTab = 'browse'"
          @cancel-order="cancelOrder"
        />
      </div>

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
import { ref, computed, onMounted, onUnmounted } from 'vue'
import Header from '@/components/layout/Header.vue'
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
const isScrolled = ref(false)

const tabOrder = ['browse', 'catalog', 'orders', 'profile']

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

const headerDynamicStyle = computed(() => ({
  backgroundColor: bgColor.value,
  color: textColor.value,
  borderBottomColor: isDarkMode.value ? '#2d3748' : '#f3f4f6',
  borderBottomWidth: isScrolled.value ? '1px' : '0px'
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

const selectNextTab = () => {
  const currentIndex = tabOrder.indexOf(currentTab.value)
  const nextIndex = (currentIndex + 1) % tabOrder.length
  currentTab.value = tabOrder[nextIndex]
}

const selectPrevTab = () => {
  const currentIndex = tabOrder.indexOf(currentTab.value)
  const prevIndex = (currentIndex - 1 + tabOrder.length) % tabOrder.length
  currentTab.value = tabOrder[prevIndex]
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

const handleScroll = () => {
  isScrolled.value = window.scrollY > 8
}

onMounted(() => {
  if (window.Telegram?.WebApp) {
    const tg = window.Telegram.WebApp
    tg.ready()
    tg.setHeaderColor('#FFFFFF')
  }
  window.addEventListener('scroll', handleScroll, { passive: true })
})

onUnmounted(() => {
  window.removeEventListener('scroll', handleScroll)
})
</script>

<style scoped>
/* ======================== ANIMATIONS ======================== */
@keyframes slideDown {
  from {
    opacity: 0;
    transform: translateY(-12px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

@keyframes pulse-subtle {
  0%, 100% {
    opacity: 1;
  }
  50% {
    opacity: 0.8;
  }
}

header {
  animation: slideDown 0.4s cubic-bezier(0.16, 1, 0.3, 1);
  border-bottom: 1px solid transparent;
}

/* ======================== LOGO BUTTON ======================== */
.logo-btn {
  background: none;
  border: none;
  padding: 0.25rem;
  cursor: pointer;
  border-radius: 8px;
  transition: background-color 0.2s ease-out;
  position: relative;
}

.logo-btn:hover {
  background-color: rgba(0, 0, 0, 0.04);
}

.logo-btn:focus-visible {
  outline: 2px solid #3b82f6;
  outline-offset: 2px;
}

.logo-container {
  will-change: transform;
}

/* ======================== NAVIGATION TABS ======================== */
.nav-tab {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 0.375rem;
  padding: 0.5rem 0.875rem;
  border-radius: 18px;
  border: 1.5px solid transparent;
  font-size: 0.75rem;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.25s cubic-bezier(0.16, 1, 0.3, 1);
  white-space: nowrap;
  color: #6b7280;
  background-color: #f3f4f6;
  position: relative;
  will-change: background-color, color, transform;
  font-family: inherit;
}

/* Default state */
.nav-tab:not(.nav-tab--active) {
  opacity: 0.85;
}

/* Hover state */
.nav-tab:not(.nav-tab--active):hover {
  background-color: #e5e7eb;
  opacity: 1;
  transform: translateY(-1px);
}

/* Focus state */
.nav-tab:focus-visible {
  outline: 2px solid #3b82f6;
  outline-offset: 2px;
}

/* Active state - Modern 2025 Style */
.nav-tab--active {
  background: linear-gradient(135deg, #ffffff 0%, #f8f9fa 100%);
  color: #1f2937;
  border-color: #d1d5db;
  box-shadow: 
    0 2px 8px rgba(0, 0, 0, 0.08),
    inset 0 1px 2px rgba(255, 255, 255, 0.8);
  font-weight: 600;
  opacity: 1;
}

/* Active dark variant */
.nav-tab--active:hover {
  box-shadow: 
    0 4px 12px rgba(0, 0, 0, 0.12),
    inset 0 1px 2px rgba(255, 255, 255, 0.8);
}

/* ======================== ADD SERVICE BUTTON ======================== */
.nav-tab--add {
  width: 2rem;
  height: 2rem;
  padding: 0;
  border-radius: 50%;
  background-color: #f3f4f6;
  border-color: #d1d5db;
  color: #374151;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
  position: relative;
}

.nav-tab--add:hover {
  background-color: #e5e7eb;
  border-color: #9ca3af;
  transform: translateY(-1px) scale(1.05);
}

.nav-tab--add:active {
  transform: translateY(0) scale(0.95);
}

.nav-tab--add svg {
  transition: transform 0.2s ease-out;
}

.nav-tab--add:hover svg {
  transform: scale(1.1);
}

/* ======================== PROFILE BUTTON ======================== */
.profile-btn {
  width: 2.25rem;
  height: 2.25rem;
  border-radius: 50%;
  color: white;
  border: 2px solid currentColor;
  cursor: pointer;
  font-weight: 700;
  font-size: 0.75rem;
  transition: all 0.2s cubic-bezier(0.16, 1, 0.3, 1);
  flex-shrink: 0;
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.15);
  position: relative;
  will-change: transform, box-shadow;
}

.profile-btn::before {
  content: '';
  position: absolute;
  inset: 0;
  border-radius: 50%;
  background: linear-gradient(135deg, rgba(255, 255, 255, 0.2) 0%, rgba(255, 255, 255, 0) 100%);
  pointer-events: none;
}

.profile-btn:hover {
  transform: translateY(-3px) scale(1.08);
  box-shadow: 0 6px 16px rgba(0, 0, 0, 0.2);
}

.profile-btn:active {
  transform: translateY(-1px) scale(0.95);
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.15);
}

.profile-btn:focus-visible {
  outline: 2px solid white;
  outline-offset: 2px;
}

/* ======================== RESPONSIVE DESIGN ======================== */
@media (max-width: 640px) {
  .nav-tab {
    padding: 0.5rem 0.625rem;
  }

  .nav-tab svg {
    width: 1rem;
    height: 1rem;
  }
}

/* ======================== ACCESSIBILITY ======================== */
button {
  font-family: inherit;
  font-size: inherit;
}

/* High contrast mode support */
@media (prefers-contrast: more) {
  .nav-tab--active {
    border-width: 2px;
  }

  .profile-btn {
    border-width: 3px;
  }
}

/* Reduced motion support */
@media (prefers-reduced-motion: reduce) {
  * {
    animation-duration: 0.01ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: 0.01ms !important;
  }
}
</style>