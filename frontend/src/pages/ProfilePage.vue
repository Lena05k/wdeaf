<template>
  <div class="profile-page flex flex-col h-screen bg-slate-900">
    <!-- Header -->
    <header class="sticky top-0 z-40 bg-slate-900 border-b border-blue-900">
      <div class="max-w-md mx-auto px-4 py-3">
        <h1 class="text-xl font-bold text-blue-400">👤 Мой профиль</h1>
      </div>
    </header>

    <!-- Main Content -->
    <main class="flex-1 overflow-y-auto max-w-md mx-auto w-full pb-20">
      <!-- User Header Component -->
      <UserHeader
        :user="userData"
        :is-provider="false"
        :orders-count="5"
        :reviews-count="12"
        :saved-count="8"
        @show-orders="showModal('orders')"
        @show-reviews="showModal('reviews')"
        @show-saved="showModal('saved')"
        @show-provider-orders="showModal('provider-orders')"
        @show-provider-reviews="showModal('provider-reviews')"
        @show-analytics="showModal('analytics')"
        @show-notifications="showModal('notifications')"
        @become-provider="showModal('become-provider')"
        @add-service="showModal('add-service')"
        @edit-profile="showModal('edit-profile')"
        @logout="handleLogout"
      />
    </main>

    <!-- Modals -->
    <!-- Orders Modal -->
    <Modal 
      v-if="activeModal === 'orders'"
      title="Мои заказы"
      @close="closeModal"
    >
      <div class="space-y-3">
        <div v-if="orders.length === 0" class="text-center py-8">
          <p class="text-gray-400">Нет заказов</p>
        </div>
        <div v-for="order in orders" :key="order.id" class="bg-slate-700 rounded-lg p-3 border border-slate-600">
          <h3 class="font-semibold text-white">{{ order.serviceName }}</h3>
          <p class="text-sm text-gray-400">{{ order.provider }}</p>
          <p class="text-sm text-gray-400 mt-1">{{ order.date }}</p>
          <span :class="`inline-block mt-2 px-3 py-1 rounded text-xs font-semibold ${
            order.status === 'completed' ? 'bg-green-900 text-green-300' : 'bg-blue-900 text-blue-300'
          }`">
            {{ order.status === 'completed' ? 'Завершен' : 'На рассмотрении' }}
          </span>
        </div>
      </div>
    </Modal>

    <!-- Reviews Modal -->
    <Modal 
      v-if="activeModal === 'reviews'"
      title="Оставленные отзывы"
      @close="closeModal"
    >
      <div class="space-y-3">
        <div v-if="reviews.length === 0" class="text-center py-8">
          <p class="text-gray-400">Нет отзывов</p>
        </div>
        <div v-for="review in reviews" :key="review.id" class="bg-slate-700 rounded-lg p-3 border border-slate-600">
          <div class="flex justify-between items-start mb-2">
            <h3 class="font-semibold text-white">{{ review.serviceName }}</h3>
            <span class="text-yellow-400">⭐ {{ review.rating }}/5</span>
          </div>
          <p class="text-sm text-gray-400">{{ review.provider }}</p>
          <p class="text-gray-300 text-sm mt-2">{{ review.text }}</p>
          <p class="text-gray-500 text-xs mt-2">{{ review.date }}</p>
        </div>
      </div>
    </Modal>

    <!-- Saved Services Modal -->
    <Modal 
      v-if="activeModal === 'saved'"
      title="Сохраненные услуги"
      @close="closeModal"
    >
      <div class="space-y-3">
        <div v-if="savedServices.length === 0" class="text-center py-8">
          <p class="text-gray-400">Нет сохраненных услуг</p>
        </div>
        <div v-for="service in savedServices" :key="service.id" class="bg-slate-700 rounded-lg p-3 border border-slate-600">
          <h3 class="font-semibold text-white">{{ service.name }}</h3>
          <p class="text-sm text-gray-400">{{ service.provider }}</p>
          <div class="flex justify-between items-center mt-2">
            <span class="text-blue-400 font-semibold">{{ formatPrice(service.price) }} ₽</span>
            <span class="text-yellow-400">⭐ {{ service.rating }}</span>
          </div>
        </div>
      </div>
    </Modal>

    <!-- Provider Orders Modal -->
    <Modal 
      v-if="activeModal === 'provider-orders'"
      title="Заказы"
      @close="closeModal"
    >
      <div class="space-y-3">
        <div v-if="providerOrders.length === 0" class="text-center py-8">
          <p class="text-gray-400">Нет заказов</p>
        </div>
        <div v-for="order in providerOrders" :key="order.id" class="bg-slate-700 rounded-lg p-3 border border-slate-600">
          <h3 class="font-semibold text-white">{{ order.serviceName }}</h3>
          <p class="text-sm text-gray-400">{{ order.clientName }}</p>
          <p class="text-sm text-gray-400">{{ order.date }}</p>
          <div class="flex justify-between items-center mt-2">
            <span class="text-blue-400 font-semibold">{{ formatPrice(order.price) }} ₽</span>
            <span class="text-green-400 text-xs">✓ {{ order.status }}</span>
          </div>
        </div>
      </div>
    </Modal>

    <!-- Provider Reviews Modal -->
    <Modal 
      v-if="activeModal === 'provider-reviews'"
      title="Отзывы"
      @close="closeModal"
    >
      <div class="space-y-3">
        <div v-if="providerReviews.length === 0" class="text-center py-8">
          <p class="text-gray-400">Нет отзывов</p>
        </div>
        <div v-for="review in providerReviews" :key="review.id" class="bg-slate-700 rounded-lg p-3 border border-slate-600">
          <div class="flex justify-between items-start mb-2">
            <h3 class="font-semibold text-white">{{ review.clientName }}</h3>
            <span class="text-yellow-400">⭐ {{ review.rating }}/5</span>
          </div>
          <p class="text-gray-300 text-sm">{{ review.text }}</p>
          <p class="text-gray-500 text-xs mt-2">{{ review.date }}</p>
        </div>
      </div>
    </Modal>

    <!-- Analytics Modal -->
    <Modal 
      v-if="activeModal === 'analytics'"
      title="Аналитика"
      @close="closeModal"
    >
      <div class="bg-slate-700 rounded-lg p-4 border border-slate-600 space-y-3">
        <div class="flex justify-between">
          <span class="text-gray-400">Выполнено заказов:</span>
          <span class="text-white font-semibold">28</span>
        </div>
        <div class="flex justify-between border-t border-slate-600 pt-3">
          <span class="text-gray-400">Общий доход:</span>
          <span class="text-blue-400 font-semibold">425,000 ₽</span>
        </div>
        <div class="flex justify-between border-t border-slate-600 pt-3">
          <span class="text-gray-400">Рейтинг:</span>
          <span class="text-yellow-400 font-semibold">4.9/5.0</span>
        </div>
        <div class="flex justify-between border-t border-slate-600 pt-3">
          <span class="text-gray-400">Отзывов:</span>
          <span class="text-white font-semibold">124</span>
        </div>
      </div>
    </Modal>

    <!-- Notifications Modal -->
    <Modal 
      v-if="activeModal === 'notifications'"
      title="Уведомления"
      @close="closeModal"
    >
      <div class="bg-slate-700 rounded-lg p-4 border border-slate-600 space-y-3">
        <div class="flex justify-between items-center">
          <span class="text-gray-300">Новые заказы</span>
          <input type="checkbox" checked class="w-5 h-5 accent-blue-500" />
        </div>
        <div class="flex justify-between items-center border-t border-slate-600 pt-3">
          <span class="text-gray-300">Сообщения</span>
          <input type="checkbox" checked class="w-5 h-5 accent-blue-500" />
        </div>
        <div class="flex justify-between items-center border-t border-slate-600 pt-3">
          <span class="text-gray-300">Отзывы</span>
          <input type="checkbox" checked class="w-5 h-5 accent-blue-500" />
        </div>
        <div class="flex justify-between items-center border-t border-slate-600 pt-3">
          <span class="text-gray-300">Промо и скидки</span>
          <input type="checkbox" class="w-5 h-5 accent-blue-500" />
        </div>
      </div>
    </Modal>

    <!-- Become Provider Modal -->
    <Modal 
      v-if="activeModal === 'become-provider'"
      title="Стать исполнителем"
      @close="closeModal"
    >
      <div class="space-y-4">
        <p class="text-gray-300">Хотите начать создавать услуги и зарабатывать на WDEAF?</p>
        <div class="bg-slate-700 rounded-lg p-4 border border-slate-600 space-y-2">
          <p class="text-sm text-gray-400">✓ Создавайте свои услуги</p>
          <p class="text-sm text-gray-400">✓ Получайте заказы от клиентов</p>
          <p class="text-sm text-gray-400">✓ Зарабатывайте без комиссии</p>
          <p class="text-sm text-gray-400">✓ Строите свой рейтинг</p>
        </div>
        <button 
          @click="confirmBecomeProvider"
          class="w-full bg-blue-600 hover:bg-blue-500 text-white font-semibold py-2 rounded-lg transition"
        >
          Стать исполнителем
        </button>
      </div>
    </Modal>

    <!-- Edit Profile Modal -->
    <Modal 
      v-if="activeModal === 'edit-profile'"
      title="Редактировать профиль"
      @close="closeModal"
    >
      <div class="space-y-4">
        <div>
          <label class="block text-sm text-gray-400 mb-2">Имя</label>
          <input 
            v-model="userData.first_name"
            type="text" 
            class="w-full bg-slate-700 border border-slate-600 rounded-lg px-3 py-2 text-white focus:outline-none focus:border-blue-500"
          />
        </div>
        <div>
          <label class="block text-sm text-gray-400 mb-2">Юзернейм</label>
          <input 
            v-model="userData.username"
            type="text" 
            class="w-full bg-slate-700 border border-slate-600 rounded-lg px-3 py-2 text-white focus:outline-none focus:border-blue-500"
          />
        </div>
        <button 
          @click="saveProfile"
          class="w-full bg-blue-600 hover:bg-blue-500 text-white font-semibold py-2 rounded-lg transition"
        >
          Сохранить
        </button>
      </div>
    </Modal>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useUserStore } from '@/stores/userStore'
import UserHeader from '@/components/profile/UserHeader.vue'
import Modal from '@/components/common/Modal.vue'

const router = useRouter()
const userStore = useUserStore()

const activeModal = ref<string | null>(null)

const userData = ref({
  first_name: 'Иван',
  username: 'ivan_user',
  id: '123456789'
})

// Mock data
const orders = ref([
  {
    id: 1,
    serviceName: 'Уроки английского',
    provider: 'Джон Д.',
    date: '12 янв 2025',
    status: 'completed'
  },
  {
    id: 2,
    serviceName: 'Консультация бухгалтера',
    provider: 'Мария С.',
    date: '8 янв 2025',
    status: 'active'
  }
])

const reviews = ref([
  {
    id: 1,
    serviceName: 'Уроки английского',
    provider: 'Джон Д.',
    text: 'Отличный преподаватель, очень доволен результатом!',
    rating: 5,
    date: '12 янв 2025'
  }
])

const savedServices = ref([
  {
    id: 1,
    name: 'Web-дизайн сайта',
    provider: 'Артем К.',
    price: 15000,
    rating: 4.9
  }
])

const providerOrders = ref([
  {
    id: 1,
    serviceName: 'Web-дизайн',
    clientName: 'Анна П.',
    date: '15 янв 2025',
    status: 'выполнен',
    price: 15000
  }
])

const providerReviews = ref([
  {
    id: 1,
    clientName: 'Иван П.',
    text: 'Отличная работа! Все сделано качественно и в срок.',
    rating: 5,
    date: '12 янв 2025'
  }
])

// Functions
const showModal = (modal: string) => {
  activeModal.value = modal
}

const closeModal = () => {
  activeModal.value = null
}

const confirmBecomeProvider = () => {
  alert('✅ Вы стали исполнителем!')
  closeModal()
}

const saveProfile = () => {
  alert('✅ Профиль сохранен!')
  closeModal()
}

const handleLogout = () => {
  alert('👋 Вы вышли из аккаунта')
}

const formatPrice = (price: number): string => {
  return new Intl.NumberFormat('ru-RU').format(price)
}

onMounted(() => {
  userStore.initFromTelegram()
})
</script>

<style scoped>
.profile-page {
  background: linear-gradient(135deg, #0f1319 0%, #1a1f2e 100%);
}
</style>