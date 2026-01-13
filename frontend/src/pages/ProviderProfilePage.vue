<template>
  <div class="provider-profile-page">
    <Header :userData="userData" class="sticky top-0 z-50" />
    
    <main class="max-w-md mx-auto pb-20 p-4">
      <!-- Back Button -->
      <button 
        @click="goBack"
        class="mb-4 text-blue-400 hover:text-blue-300 flex items-center gap-2"
      >
        ← Назад
      </button>

      <!-- Provider Info -->
      <div class="provider-card">
        <div class="flex items-center gap-3 mb-4 pb-4 border-b border-blue-900">
          <div class="provider-avatar">{{ providerName.charAt(0) }}</div>
          <div class="flex-1">
            <p class="font-bold text-lg">{{ providerName }}</p>
            <p class="text-yellow-400">⭐ 4.8 (156 отзывов)</p>
            <p class="text-sm text-gray-400 mt-1">Ответ в течение 1 часа</p>
          </div>
        </div>

        <!-- Portfolio Section -->
        <div class="mb-4">
          <p class="text-sm text-gray-400 mb-2">📸 Портфолио (3 фото)</p>
          <div class="grid grid-cols-3 gap-2">
            <img 
              src="https://via.placeholder.com/100" 
              class="rounded-lg w-full aspect-square object-cover cursor-pointer hover:opacity-80" 
              alt="portfolio 1"
            >
            <img 
              src="https://via.placeholder.com/100" 
              class="rounded-lg w-full aspect-square object-cover cursor-pointer hover:opacity-80" 
              alt="portfolio 2"
            >
            <img 
              src="https://via.placeholder.com/100" 
              class="rounded-lg w-full aspect-square object-cover cursor-pointer hover:opacity-80" 
              alt="portfolio 3"
            >
          </div>
        </div>

        <!-- Services Section -->
        <div class="mb-4">
          <p class="text-sm text-gray-400 mb-2">📋 Услуги исполнителя (5)</p>
          <div class="space-y-2">
            <div 
              v-for="service in providerServices"
              :key="service.id"
              @click="goToService(service.id)"
              class="bg-blue-900 bg-opacity-20 rounded p-3 text-sm border-l-2 border-blue-500 cursor-pointer hover:bg-opacity-30 transition"
            >
              <p class="font-semibold">{{ service.name }}</p>
              <p class="text-gray-400">{{ service.price }}₽</p>
            </div>
          </div>
        </div>

        <!-- Reviews Section -->
        <div>
          <p class="text-sm text-gray-400 mb-2">💬 Отзывы (10)</p>
          <div class="space-y-2">
            <div class="bg-slate-700 rounded p-3 text-sm">
              <p class="font-semibold mb-1">Клиент 1</p>
              <p class="text-xs text-gray-400 mb-1">⭐ 5.0 • 2 недели назад</p>
              <p class="text-gray-300">Отличная работа! Очень доволен качеством и скоростью выполнения.</p>
            </div>
            <div class="bg-slate-700 rounded p-3 text-sm">
              <p class="font-semibold mb-1">Клиент 2</p>
              <p class="text-xs text-gray-400 mb-1">⭐ 4.8 • 1 месяц назад</p>
              <p class="text-gray-300">Профессионал своего дела, рекомендую!</p>
            </div>
          </div>
        </div>
      </div>

      <!-- Action Buttons -->
      <div class="flex gap-3 mt-6">
        <button 
          @click="contactProvider"
          class="flex-1 btn-primary py-3 rounded-lg font-semibold"
        >
          💬 Написать сообщение
        </button>
        <button 
          @click="goBack"
          class="flex-1 btn-secondary py-3 rounded-lg font-semibold"
        >
          Закрыть
        </button>
      </div>
    </main>

    <Toast v-if="showToast" :message="toastMessage" />
  </div>
</template>

<script>
import Header from '../components/layout/Header.vue'
import Toast from '../components/shared/Toast.vue'

export default {
  name: 'ProviderProfilePage',
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
      providerName: 'Олег М.',
      providerServices: [
        { id: 1, name: 'Услуга сантехника', price: 2500 },
        { id: 2, name: 'Ремонт кранов', price: 1500 },
        { id: 3, name: 'Чистка труб', price: 800 }
      ],
      showToast: false,
      toastMessage: ''
    }
  },
  methods: {
    goBack() {
      this.$router.back();
    },
    goToService(serviceId) {
      this.$router.push({
        name: 'service-detail',
        params: { id: serviceId }
      });
    },
    contactProvider() {
      this.showToast = true;
      this.toastMessage = '✓ Сообщение отправлено!';
      setTimeout(() => {
        this.showToast = false;
      }, 3000);
    }
  }
}
</script>

<style scoped>
.provider-card {
  background: #1a1f2e;
  border: 1px solid #0055FF;
  border-radius: 12px;
  padding: 16px;
}

.provider-avatar {
  width: 70px;
  height: 70px;
  min-width: 70px;
  border-radius: 50%;
  background: linear-gradient(135deg, #0055FF, #0044CC);
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  font-weight: bold;
  font-size: 28px;
}

.btn-primary {
  background: #0055FF;
  color: #FFFFFF;
  transition: all 0.3s ease;
  border: none;
  cursor: pointer;
}

.btn-primary:hover {
  background: #0044CC;
  box-shadow: 0 8px 16px rgba(0, 85, 255, 0.4);
  transform: translateY(-2px);
}

.btn-secondary {
  background: transparent;
  color: #0055FF;
  border: 1px solid #0055FF;
  transition: all 0.3s;
  cursor: pointer;
}

.btn-secondary:hover {
  background: rgba(0, 85, 255, 0.1);
}
</style>
