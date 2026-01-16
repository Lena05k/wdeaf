<template>
  <div class="bg-slate-800 rounded-lg p-4 border border-blue-900">
    <div class="flex items-center gap-3 mb-4">
      <div class="w-16 h-16 bg-blue-600 rounded-full flex items-center justify-center text-2xl">
        {{ userStore.user?.first_name?.charAt(0) || '?' }}
      </div>
      <div>
        <p class="font-semibold text-lg">{{ userStore.user?.first_name || 'Пользователь' }}</p>
        <p class="text-sm text-gray-400">@{{ userStore.user?.username || 'user' }}</p>
        <p class="text-xs text-gray-500 mt-1">ID: {{ userStore.user?.id || 'N/A' }}</p>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { useUserStore } from '@/stores/userStore'

const userStore = useUserStore()
</script>

<style scoped></style>
