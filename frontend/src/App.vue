<template>
  <div id="app" class="bg-slate-900 min-h-screen">
    <!-- Header Component with tab update listener -->
    <Header 
      :userData="userData"
      class="sticky top-0 z-50"
      @update:currentTab="currentTab = $event"
    />

    <!-- Tab Navigation Component -->
    <TabNavigation 
      :currentTab="currentTab"
      @update:currentTab="currentTab = $event"
      class="sticky top-16 z-40"
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

    <!-- Toast Notification -->
    <Toast 
      v-if="showToast"
      :message="toastMessage"
    />
  </div>
</template>

<script>
import Header from '@/components/layout/Header.vue'
import TabNavigation from '@/components/layout/TabNavigation.vue'
import BrowseServices from '@/views/BrowseServices.vue'
import CatalogView from '@/views/CatalogView.vue'
import OrdersView from '@/views/OrdersView.vue'
import ProfileView from '@/views/ProfileView.vue'
import Toast from '@/components/shared/Toast.vue'

export default {
  name: 'App',
  components: {
    Header,
    TabNavigation,
    BrowseServices,
    CatalogView,
    OrdersView,
    ProfileView,
    Toast
  },
  data() {
    return {
      userData: {
        first_name: 'Иван',
        id: '123456789',
        username: 'ivan_user'
      },
      currentTab: 'browse',
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
  methods: {
    selectService(service) {
      // Модальное окно для деталей услуги
      console.log('Service selected:', service)
    },
    orderService(service) {
      this.userOrders.unshift({
        id: Date.now(),
        service: service.name,
        provider: service.provider,
        status: 'pending',
        price: service.price,
        date: 'завтра в ' + new Date().toLocaleTimeString('ru-RU', { hour: '2-digit', minute: '2-digit' })
      });
      
      this.showToast = true;
      this.toastMessage = '✓ Заказ создан! Исполнитель свяжется с вами';
      setTimeout(() => {
        this.showToast = false;
      }, 3000);
    },
    onCategorySelected(category) {
      this.selectedCategory = category.name;
      this.currentTab = 'browse';
    },
    cancelOrder(orderId) {
      this.userOrders = this.userOrders.filter(order => order.id !== orderId);
      this.showToast = true;
      this.toastMessage = '✓ Заказ отменен';
      setTimeout(() => {
        this.showToast = false;
      }, 3000);
    },
    becomeProvider() {
      this.showToast = true;
      this.toastMessage = 'Скоро вы сможете стать исполнителем!';
      setTimeout(() => {
        this.showToast = false;
      }, 3000);
    },
    openSettings() {
      this.showToast = true;
      this.toastMessage = 'Настройки откроются вскоре';
      setTimeout(() => {
        this.showToast = false;
      }, 3000);
    }
  },
  mounted() {
    if (window.Telegram?.WebApp) {
      const tg = window.Telegram.WebApp;
      tg.ready();
      tg.setHeaderColor('#FFFFFF');
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