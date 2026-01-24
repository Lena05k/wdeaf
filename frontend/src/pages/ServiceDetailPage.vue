<template>
  <div class="service-detail-page">
    <Header :userData="userData" class="sticky top-0 z-50" />
    
    <main class="max-w-md mx-auto pb-20 p-4" v-if="service">
      <!-- Back Button -->
      <button 
        @click="goBack"
        class="mb-4 text-blue-400 hover:text-blue-300 flex items-center gap-2"
      >
        ← Назад к услугам
      </button>

      <!-- Service Details -->
      <div class="bg-slate-800 border border-slate-700 rounded-xl p-6 space-y-4">
        <!-- Images Carousel -->
        <div class="relative bg-slate-700 rounded-lg overflow-hidden aspect-video">
          <img 
            :src="service.images[modalImageIndex]"
            :alt="service.name"
            class="w-full h-full object-cover"
          />
          <!-- Navigation -->
          <div class="absolute inset-0 flex items-center justify-between px-4">
            <button @click="prevImage" class="bg-black/50 hover:bg-black/70 text-white p-2 rounded-full">
              ‹
            </button>
            <button @click="nextImage" class="bg-black/50 hover:bg-black/70 text-white p-2 rounded-full">
              ›
            </button>
          </div>
        </div>

        <!-- Service Info -->
        <div>
          <h1 class="text-2xl font-bold text-white mb-2">{{ service.name }}</h1>
          <div class="flex items-center justify-between mb-4">
            <div>
              <p class="text-gray-400 text-sm">{{ service.category }}</p>
              <p class="text-yellow-400 font-semibold">⭐ {{ service.providerRating }} ({{ service.reviews }} отзывов)</p>
            </div>
            <div class="text-right">
              <p class="text-2xl font-bold text-white">{{ service.price.toLocaleString('ru-RU') }} ₽</p>
              <p class="text-gray-400 text-sm">{{ service.response_time }}</p>
            </div>
          </div>
        </div>

        <!-- Provider Info -->
        <div class="border-t border-slate-700 pt-4">
          <button
            @click="handleViewProvider(service.provider)"
            class="w-full text-left px-4 py-3 bg-slate-700 hover:bg-slate-600 rounded-lg transition"
          >
            <p class="text-gray-300 text-sm">Исполнитель</p>
            <p class="text-white font-semibold">{{ service.provider }}</p>
          </button>
        </div>

        <!-- Description -->
        <div>
          <h3 class="text-lg font-semibold text-white mb-2">Описание</h3>
          <p class="text-gray-300 leading-relaxed">{{ service.fullDescription }}</p>
        </div>

        <!-- Action Buttons -->
        <div class="grid grid-cols-2 gap-3 pt-4">
          <button
            @click="goBack"
            class="px-4 py-3 bg-slate-700 hover:bg-slate-600 text-white font-semibold rounded-lg transition"
          >
            Отмена
          </button>
          <button
            @click="handleOrder"
            class="px-4 py-3 bg-blue-600 hover:bg-blue-500 text-white font-semibold rounded-lg transition"
          >
            Заказать
          </button>
        </div>
      </div>
    </main>

    <Toast v-if="showToast" :message="toastMessage" />
  </div>
</template>

<script>
import Header from '../components/layout/Header.vue'
import Toast from '../components/shared/Toast.vue'

export default {
  name: 'ServiceDetailPage',
  components: {
    Header,
    Toast
  },
  data() {
    return {
      userData: {
        first_name: 'Иван',
        id: '123456789',
        username: 'ivan_user'
      },
      service: null,
      modalImageIndex: 0,
      showToast: false,
      toastMessage: ''
    }
  },
  computed: {
    serviceId() {
      return this.$route.params.id;
    }
  },
  methods: {
    loadService() {
      // Имитация загрузки услуги из API
      const services = [
        {
          id: 1,
          name: 'Услуга сантехника',
          provider: 'Олег М.',
          category: '🏠 Ремонт',
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
          category: '💼 Бизнес',
          description: 'Налоговое планирование и бухгалтерская отчетность',
          fullDescription: 'Профессиональная консультация по налоговому планированию, ведение бухгалтерского учета, подготовка отчетности.',
          price: 3000,
          reviews: 89,
          response_time: '< 2 часов',
          providerRating: 4.7,
          images: ['https://via.placeholder.com/300x200?text=Бухгалтер+1', 'https://via.placeholder.com/300x200?text=Бухгалтер+2'],
          currentImageIndex: 0
        }
      ];
      this.service = services.find(s => s.id === parseInt(this.serviceId)) || null;
    },
    goBack() {
      this.$router.back();
    },
    handleOrder() {
      this.showToast = true;
      this.toastMessage = '✓ Заказ создан! Исполнитель свяжется с вами';
      setTimeout(() => {
        this.showToast = false;
        this.$router.push({ name: 'orders' });
      }, 2000);
    },
    handleViewProvider(providerName) {
      this.showToast = true;
      this.toastMessage = '📁 Профиль исполнителя: ' + providerName;
      setTimeout(() => {
        this.showToast = false;
      }, 2000);
    },
    nextImage() {
      if (!this.service || !this.service.images) return;
      this.modalImageIndex = (this.modalImageIndex + 1) % this.service.images.length;
    },
    prevImage() {
      if (!this.service || !this.service.images) return;
      this.modalImageIndex = (this.modalImageIndex - 1 + this.service.images.length) % this.service.images.length;
    }
  },
  mounted() {
    this.loadService();
  }
}
</script>

<style scoped>
</style>