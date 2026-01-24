<template>
  <div id="app" class="bg-slate-900 min-h-screen">
    <!-- Header - Simple top bar -->
    <header class="fixed top-0 left-0 right-0 z-50 bg-slate-900 border-b border-slate-800 h-12 flex items-center px-4 max-w-md mx-auto">
      <!-- Back Button (shown only when not in profile) -->
      <button
        v-if="currentView !== 'profile'"
        @click="goBack"
        class="text-blue-400 hover:text-blue-300 text-xl"
      >
        ‹
      </button>
      <div class="flex-1" />
      <!-- Title -->
      <h1 class="text-sm font-semibold text-white">{{ pageTitle }}</h1>
      <div class="flex-1" />
    </header>

    <!-- Main Content -->
    <main class="max-w-md mx-auto pt-12 pb-24">
      <!-- Profile View (Default) -->
      <div v-if="currentView === 'profile'" class="p-4">
        <!-- Avatar - Centered -->
        <div class="flex flex-col items-center mb-8 mt-8">
          <div class="w-24 h-24 bg-gradient-to-br from-blue-500 to-blue-600 rounded-full flex items-center justify-center text-4xl font-bold text-white mb-4">
            {{ userData.first_name.charAt(0) }}
          </div>
          <h2 class="text-2xl font-bold text-white">{{ userData.first_name }}</h2>
          <p class="text-gray-400 text-sm">@{{ userData.username }}</p>
        </div>

        <!-- Tabs Grid (iOS 18 Style) -->
        <div class="space-y-3">
          <!-- Browse Tab -->
          <button
            @click="currentView = 'browse'"
            class="w-full bg-slate-800 hover:bg-slate-700 border border-slate-700 rounded-2xl p-4 text-left transition active:scale-95"
          >
            <p class="text-2xl mb-2">🔍</p>
            <p class="text-white font-semibold">Обзор</p>
            <p class="text-gray-400 text-sm mt-1">Найти услугу</p>
          </button>

          <!-- Catalog Tab -->
          <button
            @click="currentView = 'catalog'"
            class="w-full bg-slate-800 hover:bg-slate-700 border border-slate-700 rounded-2xl p-4 text-left transition active:scale-95"
          >
            <p class="text-2xl mb-2">📂</p>
            <p class="text-white font-semibold">Каталог</p>
            <p class="text-gray-400 text-sm mt-1">Все категории</p>
          </button>

          <!-- Orders Tab -->
          <button
            @click="currentView = 'orders'"
            class="w-full bg-slate-800 hover:bg-slate-700 border border-slate-700 rounded-2xl p-4 text-left transition active:scale-95 relative"
          >
            <p class="text-2xl mb-2">&#x1F4B3;</p>
            <p class="text-white font-semibold">Мои заказы</p>
            <p class="text-gray-400 text-sm mt-1">{{ userOrders.length }} активных</p>
            <!-- Badge -->
            <div v-if="userOrders.length > 0" class="absolute top-2 right-2 bg-red-500 text-white text-xs font-bold rounded-full w-6 h-6 flex items-center justify-center">
              {{ userOrders.length }}
            </div>
          </button>

          <!-- Settings Tab -->
          <button
            @click="currentView = 'settings'"
            class="w-full bg-slate-800 hover:bg-slate-700 border border-slate-700 rounded-2xl p-4 text-left transition active:scale-95"
          >
            <p class="text-2xl mb-2">⚙️</p>
            <p class="text-white font-semibold">Настройки</p>
            <p class="text-gray-400 text-sm mt-1">Аккаунт и профиль</p>
          </button>
        </div>
      </div>

      <!-- Browse View -->
      <div v-else-if="currentView === 'browse'">
        <BrowseServices 
          :services="services"
          :searchQuery="searchQuery"
          :selectedCategory="selectedCategory"
          :categories="categories"
          @update:searchQuery="searchQuery = $event"
          @update:selectedCategory="selectedCategory = $event"
          @order-service="orderService"
        />
      </div>

      <!-- Catalog View -->
      <div v-else-if="currentView === 'catalog'">
        <CatalogView 
          :catalogCategories="catalogCategories"
          @category-selected="onCategorySelected"
        />
      </div>

      <!-- Orders View -->
      <div v-else-if="currentView === 'orders'">
        <OrdersView 
          :userOrders="userOrders"
          @cancel-order="cancelOrder"
        />
      </div>

      <!-- Settings View -->
      <div v-else-if="currentView === 'settings'" class="p-4 space-y-4">
        <div class="bg-slate-800 border border-slate-700 rounded-2xl p-6 space-y-4">
          <h3 class="text-lg font-bold text-white mb-4">Настройки профиля</h3>
          
          <div>
            <label class="block text-sm font-semibold text-gray-400 mb-2">Имя</label>
            <p class="text-white">{{ userData.first_name }}</p>
          </div>
          
          <div>
            <label class="block text-sm font-semibold text-gray-400 mb-2">Username</label>
            <p class="text-white">@{{ userData.username }}</p>
          </div>
          
          <div>
            <label class="block text-sm font-semibold text-gray-400 mb-2">ID</label>
            <p class="text-white font-mono text-xs">{{ userData.id }}</p>
          </div>
          
          <div class="border-t border-slate-700 pt-4 mt-4">
            <button class="w-full bg-red-600 hover:bg-red-500 text-white font-semibold py-2 rounded-lg transition active:scale-95">
              Выход
            </button>
          </div>
        </div>
      </div>
    </main>

    <!-- Toast Notification -->
    <Toast 
      v-if="showToast"
      :message="toastMessage"
    />
  </div>
</template>

<script>
import BrowseServices from '@/views/BrowseServices.vue'
import CatalogView from '@/views/CatalogView.vue'
import OrdersView from '@/views/OrdersView.vue'
import Toast from '@/components/shared/Toast.vue'

export default {
  name: 'App',
  components: {
    BrowseServices,
    CatalogView,
    OrdersView,
    Toast
  },
  data() {
    return {
      currentView: 'profile', // profile, browse, catalog, orders, settings
      userData: {
        first_name: 'Иван',
        id: '123456789',
        username: 'ivan_user'
      },
      searchQuery: '',
      selectedCategory: '',
      showToast: false,
      toastMessage: '',
      categories: ['Ремонт', 'Бизнес', 'Мода', 'Обучение', 'Дизайн'],
      catalogCategories: [
        { id: 1, name: 'Ремонт', icon: '🔧', count: 23 },
        { id: 2, name: 'Бизнес', icon: '📊', count: 18 },
        { id: 3, name: 'Мода', icon: '✌️', count: 34 },
        { id: 4, name: 'Обучение', icon: '📖', count: 45 },
        { id: 5, name: 'Дизайн', icon: '🎭', count: 29 },
        { id: 6, name: 'IT', icon: '💻', count: 56 }
      ],
      services: [
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
          images: ['https://via.placeholder.com/300x200?text=Сантехника+1', 'https://via.placeholder.com/300x200?text=Сантехника+2', 'https://via.placeholder.com/300x200?text=Сантехника+3']
        },
        {
          id: 2,
          name: 'Консультация бухгалтера',
          provider: 'Мария С.',
          category: 'Бизнес',
          description: 'Налоговое планирование и бухгалтерская отчетность',
          fullDescription: 'Профессиональная консультация по налоговому планированию, ведение бухгалтерского учета, подготовка отчетности.',
          price: 3000,
          reviews: 89,
          response_time: '< 2 часов',
          providerRating: 4.7,
          images: ['https://via.placeholder.com/300x200?text=Бухгалтер+1', 'https://via.placeholder.com/300x200?text=Бухгалтер+2']
        },
        {
          id: 3,
          name: 'Пошив платья',
          provider: 'Анна Т.',
          category: 'Мода',
          description: 'Изготовление платьев и костюмов по индивидуальному заказу',
          fullDescription: 'Создам платье вашей мечты! Работаю с любыми тканями, помогу с выбором фасона.',
          price: 5000,
          reviews: 234,
          response_time: '< 3 часов',
          providerRating: 4.8,
          images: ['https://via.placeholder.com/300x200?text=Платье+1', 'https://via.placeholder.com/300x200?text=Платье+2', 'https://via.placeholder.com/300x200?text=Платье+3']
        },
        {
          id: 4,
          name: 'Уроки английского',
          provider: 'Джон Д.',
          category: 'Обучение',
          description: 'Индивидуальные занятия по английскому языку',
          fullDescription: 'Native speaker проводит индивидуальные занятия.',
          price: 1500,
          reviews: 412,
          response_time: '< 30 мин',
          providerRating: 4.9,
          images: ['https://via.placeholder.com/300x200?text=Учитель+1', 'https://via.placeholder.com/300x200?text=Учитель+2']
        },
        {
          id: 5,
          name: 'Web-дизайн сайта',
          provider: 'Артем К.',
          category: 'Дизайн',
          description: 'Создание современного дизайна',
          fullDescription: 'Создам красивый и функциональный дизайн.',
          price: 15000,
          reviews: 67,
          response_time: '< 4 часов',
          providerRating: 4.9,
          images: ['https://via.placeholder.com/300x200?text=Дизайн+1', 'https://via.placeholder.com/300x200?text=Дизайн+2']
        },
        {
          id: 6,
          name: 'Обслуживание ПК',
          provider: 'Вадим Н.',
          category: 'Ремонт',
          description: 'Чистка, диагностика и ремонт',
          fullDescription: 'Профессиональная диагностика и ремонт.',
          price: 1800,
          reviews: 178,
          response_time: '< 2 часов',
          providerRating: 4.8,
          images: ['https://via.placeholder.com/300x200?text=ПК+1', 'https://via.placeholder.com/300x200?text=ПК+2']
        }
      ],
      userOrders: [
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
      ]
    }
  },
  computed: {
    pageTitle() {
      const titles = {
        profile: 'Профиль',
        browse: 'Обзор',
        catalog: 'Каталог',
        orders: 'Мои заказы',
        settings: 'Настройки'
      }
      return titles[this.currentView] || ''
    }
  },
  methods: {
    goBack() {
      this.currentView = 'profile'
      this.searchQuery = ''
      this.selectedCategory = ''
    },
    orderService(service) {
      this.userOrders.unshift({
        id: Date.now(),
        service: service.name,
        provider: service.provider,
        status: 'pending',
        price: service.price,
        date: 'завтра в ' + new Date().toLocaleTimeString('ru-RU', { hour: '2-digit', minute: '2-digit' })
      })
      
      this.showToast = true
      this.toastMessage = '✓ Заказ создан! Исполнитель свяжется с вами'
      setTimeout(() => {
        this.showToast = false
      }, 3000)
    },
    onCategorySelected(category) {
      this.selectedCategory = category.name
      this.currentView = 'browse'
    },
    cancelOrder(orderId) {
      this.userOrders = this.userOrders.filter(order => order.id !== orderId)
      this.showToast = true
      this.toastMessage = '✓ Заказ отменен'
      setTimeout(() => {
        this.showToast = false
      }, 3000)
    }
  },
  mounted() {
    if (window.Telegram?.WebApp) {
      const tg = window.Telegram.WebApp
      tg.ready()
      tg.setHeaderColor('#0F1319')
      tg.setBackgroundColor('#0F1319')
    }
  }
}
</script>

<style>
* { box-sizing: border-box; }
body {
  margin: 0;
  padding: 0;
  background: #0F1319;
  min-height: 100vh;
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
  color: #FFFFFF;
}
</style>