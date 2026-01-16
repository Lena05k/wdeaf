<template>
  <div class="provider-dashboard flex flex-col h-screen bg-slate-900">
    <!-- Header -->
    <header class="sticky top-0 z-50 bg-slate-900 border-b border-blue-900">
      <div class="max-w-md mx-auto px-4 py-3 flex justify-between items-center">
        <div>
          <h1 class="text-xl font-bold text-blue-400">📊 Мой профиль</h1>
          <p class="text-xs text-gray-400">Исполнитель</p>
        </div>
        <router-link to="/profile" class="text-2xl hover:text-blue-400">
          ⬅️
        </router-link>
      </div>
    </header>

    <!-- Main Content -->
    <main class="flex-1 overflow-y-auto max-w-md mx-auto w-full pb-20">
      <div class="p-4 space-y-4">
        <!-- Provider Info -->
        <div class="bg-slate-800 rounded-lg p-4 border border-blue-900">
          <h2 class="text-lg font-bold mb-3">{{ providerInfo?.serviceName }}</h2>
          <div class="space-y-2 text-sm">
            <div class="flex justify-between">
              <span class="text-gray-400">Рейтинг</span>
              <span class="text-yellow-400">⭐ {{ providerInfo?.rating || 'Новый' }}</span>
            </div>
            <div class="flex justify-between">
              <span class="text-gray-400">Цена</span>
              <span class="text-green-400 font-semibold">{{ providerInfo?.price }}₽</span>
            </div>
            <div class="flex justify-between">
              <span class="text-gray-400">Категория</span>
              <span>{{ providerInfo?.category }}</span>
            </div>
            <div class="flex justify-between">
              <span class="text-gray-400">Активных заказов</span>
              <span class="font-semibold">{{ activeOrders.length }}/{{ providerInfo?.maxConcurrentOrders }}</span>
            </div>
          </div>
        </div>

        <!-- Stats -->
        <div class="grid grid-cols-3 gap-2">
          <div class="bg-blue-900/30 rounded-lg p-3 text-center border border-blue-800">
            <p class="text-xl font-bold text-blue-400">{{ stats.views }}</p>
            <p class="text-xs text-gray-400">Просмотры</p>
          </div>
          <div class="bg-green-900/30 rounded-lg p-3 text-center border border-green-800">
            <p class="text-xl font-bold text-green-400">{{ stats.orders }}</p>
            <p class="text-xs text-gray-400">Заказы</p>
          </div>
          <div class="bg-purple-900/30 rounded-lg p-3 text-center border border-purple-800">
            <p class="text-xl font-bold text-purple-400">{{ stats.reviews }}</p>
            <p class="text-xs text-gray-400">Отзывы</p>
          </div>
        </div>

        <!-- Actions -->
        <div class="flex gap-2">
          <button
            @click="showEditModal = true"
            class="flex-1 bg-blue-600 hover:bg-blue-500 text-white font-semibold py-2 rounded-lg transition flex items-center justify-center gap-2"
          >
            ✏️ Редактировать
          </button>
          <button
            @click="toggleActive"
            :class="[
              'flex-1 font-semibold py-2 rounded-lg transition flex items-center justify-center gap-2',
              isActive
                ? 'bg-green-600 hover:bg-green-500 text-white'
                : 'bg-yellow-600 hover:bg-yellow-500 text-white'
            ]"
          >
            {{ isActive ? '✓ Активна' : '⏸️ Заморозить' }}
          </button>
        </div>

        <!-- Active Orders Section -->
        <div>
          <h3 class="text-lg font-bold mb-3">📦 Активные заказы ({{ activeOrders.length }})</h3>
          <div v-if="activeOrders.length > 0" class="space-y-2">
            <div
              v-for="order in activeOrders"
              :key="order.id"
              class="bg-slate-800 rounded-lg p-3 border border-green-900"
            >
              <div class="flex justify-between items-start mb-2">
                <div>
                  <p class="font-semibold">{{ order.clientName }}</p>
                  <p class="text-xs text-gray-400">ID: {{ order.id }}</p>
                </div>
                <span class="text-xs bg-green-900 text-green-300 px-2 py-1 rounded">
                  {{ order.status }}
                </span>
              </div>
              <p class="text-sm text-gray-400 mb-2">{{ order.details }}</p>
              <div class="flex gap-2">
                <button class="flex-1 bg-blue-600 hover:bg-blue-500 text-white text-xs py-1 rounded">
                  💬 Чат
                </button>
                <button class="flex-1 bg-green-600 hover:bg-green-500 text-white text-xs py-1 rounded">
                  ✓ Завершить
                </button>
              </div>
            </div>
          </div>
          <div v-else class="text-center py-6 text-gray-400">
            <p>Нет активных заказов</p>
          </div>
        </div>

        <!-- Completed Orders Section -->
        <div>
          <h3 class="text-lg font-bold mb-3">✓ Завершенные заказы ({{ completedOrders.length }})</h3>
          <div v-if="completedOrders.length > 0" class="space-y-2">
            <div
              v-for="order in completedOrders"
              :key="order.id"
              class="bg-slate-800/50 rounded-lg p-3 border border-slate-700"
            >
              <div class="flex justify-between items-start mb-2">
                <div>
                  <p class="font-semibold">{{ order.clientName }}</p>
                  <p class="text-xs text-gray-500">{{ order.completedDate }}</p>
                </div>
                <span class="text-sm text-yellow-400">⭐ {{ order.rating }}</span>
              </div>
              <p class="text-sm text-gray-400">{{ order.review }}</p>
            </div>
          </div>
          <div v-else class="text-center py-6 text-gray-400">
            <p>Нет завершенных заказов</p>
          </div>
        </div>
      </div>
    </main>

    <!-- Edit Modal -->
    <EditProviderModal
      v-if="showEditModal"
      :provider="providerInfo"
      @close="showEditModal = false"
      @save="handleSaveProvider"
    />
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useUserStore } from '../stores/userStore'
import EditProviderModal from '../components/modals/EditProviderModal.vue'

const userStore = useUserStore()
const showEditModal = ref(false)
const isActive = ref(true)

const providerInfo = computed(() => userStore.getProviderInfo())

const activeOrders = ref([
  {
    id: 1,
    clientName: 'Александр М.',
    status: 'В процессе',
    details: 'Уроки английского - 5 занятий завершено из 10'
  },
  {
    id: 2,
    clientName: 'Мария К.',
    status: 'Ожидает оплаты',
    details: 'Веб-дизайн сайта - макеты готовы'
  }
])

const completedOrders = ref([
  {
    id: 101,
    clientName: 'Иван П.',
    completedDate: '10 января 2026',
    rating: 5,
    review: 'Отличный результат! Очень доволен. Рекомендую!'
  },
  {
    id: 102,
    clientName: 'Елена Ф.',
    completedDate: '5 января 2026',
    rating: 4.5,
    review: 'Хороший специалист, но расписание немного не совпадало'
  }
])

const stats = ref({
  views: 124,
  orders: 3,
  reviews: 2
})

const toggleActive = () => {
  isActive.value = !isActive.value
}

const handleSaveProvider = (updatedProvider) => {
  userStore.updateProviderInfo(updatedProvider)
  showEditModal.value = false
}

onMounted(() => {
  // Загружаем данные исполнителя
  if (!providerInfo.value) {
    console.log('Исполнитель не инициализирован')
  }
})
</script>

<style scoped>
.provider-dashboard {
  background: linear-gradient(135deg, #0f1319 0%, #1a1f2e 100%);
}
</style>
