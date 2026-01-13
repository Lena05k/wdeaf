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
      <ServiceDetailsModal 
        :service="service"
        :modalImageIndex="modalImageIndex"
        @close="goBack"
        @order-confirm="handleOrder"
        @view-provider="handleViewProvider"
        @next-image="nextImage"
        @prev-image="prevImage"
      />
    </main>

    <!-- Provider Profile Modal -->
    <ProviderProfileModal 
      v-if="providerProfileModal"
      :providerName="providerProfileModal"
      @close="providerProfileModal = null"
    />

    <Toast v-if="showToast" :message="toastMessage" />
  </div>
</template>

<script>
import Header from '../components/layout/Header.vue'
import ServiceDetailsModal from '../components/modals/ServiceDetailsModal.vue'
import ProviderProfileModal from '../components/modals/ProviderProfileModal.vue'
import Toast from '../components/shared/Toast.vue'

export default {
  name: 'ServiceDetailPage',
  components: {
    Header,
    ServiceDetailsModal,
    ProviderProfileModal,
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
      providerProfileModal: null,
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
      this.providerProfileModal = providerName;
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
