<template>
  <div class="user-header bg-gradient-to-br from-slate-800 to-slate-900 border-b border-slate-700 p-4 space-y-4">
    <!-- User Avatar & Info -->
    <div class="flex items-center gap-4">
      <div class="w-20 h-20 bg-gradient-to-br from-blue-500 to-blue-600 rounded-full flex items-center justify-center text-3xl font-bold text-white shadow-lg">
        {{ user?.first_name?.charAt(0)?.toUpperCase() || '?' }}
      </div>
      <div class="flex-1">
        <h1 class="text-xl font-bold text-white">{{ user?.first_name || 'Пользователь' }}</h1>
        <p class="text-sm text-gray-400">@{{ user?.username || 'user' }}</p>
        <p v-if="isProvider" class="text-xs text-blue-400 mt-1">✓ Исполнитель</p>
      </div>
    </div>

    <!-- Verification Badge -->
    <div v-if="isProvider" class="bg-blue-900/30 border border-blue-700 rounded-lg p-3 flex items-center gap-2">
      <span class="text-lg">✓</span>
      <div class="text-sm">
        <p class="font-semibold text-blue-300">Профиль верифицирован</p>
        <p class="text-xs text-gray-400">ID: {{ user?.id }}</p>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
interface User {
  id?: string | number
  first_name?: string
  last_name?: string
  username?: string
}

defineProps<{
  user?: User
  isProvider: boolean
}>()
</script>

<style scoped>
.user-header {
  backdrop-filter: blur(10px);
}
</style>
