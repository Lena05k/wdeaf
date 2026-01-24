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
            @click="handleBecomeProvider"
            class="w-full bg-gradient-to-r from-blue-600 to-blue-500 hover:from-blue-500 hover:to-blue-400 text-white font-semibold py-3 rounded-lg transition flex items-center justify-center gap-2"
          >
            📝 Стать исполнителем
          </button>

          <!-- Settings Button -->
          <button
            @click="handleOpenSettings"
            class="w-full bg-slate-800 hover:bg-slate-700 border border-blue-900 text-white font-semibold py-3 rounded-lg transition flex items-center justify-center gap-2"
          >
            ⚙️ Настройки
          </button>
        </div>
      </div>
    </main>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useUserStore } from '@/stores/userStore'

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

const handleBecomeProvider = () => {
  alert('📝 Функциональность "Стать исполнителем" в арраировании')
}

const handleOpenSettings = () => {
  alert('⚙️ Настройки в арраировании')
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