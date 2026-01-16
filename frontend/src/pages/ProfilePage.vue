<template>
  <div class="profile-page flex flex-col h-screen bg-slate-900">
    <!-- Header -->
    <header class="sticky top-0 z-50 bg-slate-900 border-b border-blue-900">
      <div class="max-w-md mx-auto px-4 py-3">
        <h1 class="text-xl font-bold text-blue-400">👤 Мой профиль</h1>
      </div>
    </header>

    <!-- Main Content -->
    <main class="flex-1 overflow-y-auto max-w-md mx-auto w-full pb-20">
      <!-- User Info Section -->
      <div class="p-4 space-y-4">
        <!-- Profile Card -->
        <div class="bg-slate-800 rounded-lg p-4 border border-blue-900">
          <div class="flex items-center gap-3 mb-4">
            <div class="w-16 h-16 bg-blue-600 rounded-full flex items-center justify-center text-2xl">
              {{ userData.first_name.charAt(0) }}
            </div>
            <div>
              <p class="font-semibold text-lg">{{ userData.first_name }}</p>
              <p class="text-sm text-gray-400">@{{ userData.username }}</p>
              <p class="text-xs text-gray-500 mt-1">ID: {{ userData.id }}</p>
            </div>
          </div>
        </div>

        <!-- Stats -->
        <div class="grid grid-cols-2 gap-3">
          <div class="bg-blue-900/30 rounded-lg p-3 text-center border border-blue-800">
            <p class="text-2xl font-bold text-blue-400">{{ userStats.ordersCount }}</p>
            <p class="text-xs text-gray-400">Заказов</p>
          </div>
          <div class="bg-green-900/30 rounded-lg p-3 text-center border border-green-800">
            <p class="text-2xl font-bold text-green-400">{{ userStats.rating }}</p>
            <p class="text-xs text-gray-400">Рейтинг</p>
          </div>
        </div>

        <!-- Actions Section -->
        <div class="space-y-2 mt-6">
          <p class="text-sm font-semibold text-gray-400 px-2">Действия</p>

          <!-- Become Provider Button -->
          <button
            v-if="!userStore.isProvider"
            @click="showBecomeProviderModal = true"
            class="w-full bg-gradient-to-r from-blue-600 to-blue-500 hover:from-blue-500 hover:to-blue-400 text-white font-semibold py-3 rounded-lg transition flex items-center justify-center gap-2"
          >
            📝 Стать исполнителем
          </button>

          <!-- Provider Dashboard (if already provider) -->
          <button
            v-else
            @click="goToProviderDashboard"
            class="w-full bg-gradient-to-r from-green-600 to-green-500 hover:from-green-500 hover:to-green-400 text-white font-semibold py-3 rounded-lg transition flex items-center justify-center gap-2"
          >
            📊 Мои услуги
          </button>

          <!-- Settings Button -->
          <button
            @click="showSettingsModal = true"
            class="w-full bg-slate-800 hover:bg-slate-700 border border-blue-900 text-white font-semibold py-3 rounded-lg transition flex items-center justify-center gap-2"
          >
            ⚙️ Настройки
          </button>
        </div>
      </div>
    </main>

    <!-- Become Provider Modal -->
    <BecomeProviderModal
      v-if="showBecomeProviderModal"
      @close="showBecomeProviderModal = false"
      @confirm="handleBecomeProvider"
    />

    <!-- Settings Modal -->
    <SettingsModal
      v-if="showSettingsModal"
      :userData="userData"
      @close="showSettingsModal = false"
      @save="handleSettingsSave"
    />
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useUserStore } from '@/stores/userStore'
import BecomeProviderModal from '@/components/modals/BecomeProviderModal.vue'
import SettingsModal from '@/components/modals/SettingsModal.vue'

const router = useRouter()
const userStore = useUserStore()

const userData = ref({
  first_name: 'Иван',
  username: 'ivan_user',
  id: '123456789'
})

const userStats = ref({
  ordersCount: 5,
  rating: 4.8
})

const showBecomeProviderModal = ref(false)
const showSettingsModal = ref(false)

const handleBecomeProvider = async (providerData) => {
  // Сохраняем данные провайдера в store
  userStore.setProviderInfo(providerData)
  showBecomeProviderModal.value = false
  
  // Переходим на профиль исполнителя
  router.push({ name: 'provider-dashboard' })
}

const handleSettingsSave = (settings) => {
  Object.assign(userData.value, settings)
  showSettingsModal.value = false
}

const goToProviderDashboard = () => {
  router.push({ name: 'provider-dashboard' })
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
