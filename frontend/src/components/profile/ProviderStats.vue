<template>
  <div class="px-4 py-4 space-y-3">
    <!-- Main Stats Grid -->
    <div class="grid grid-cols-3 gap-3">
      <!-- Rating -->
      <div class="bg-gradient-to-br from-yellow-900/40 to-yellow-800/20 border border-yellow-700 rounded-xl p-4 text-center">
        <p class="text-2xl font-bold text-yellow-400">4.8</p>
        <p class="text-xs text-gray-400 mt-1">⭐ Рейтинг</p>
      </div>

      <!-- Reviews Count -->
      <div class="bg-gradient-to-br from-blue-900/40 to-blue-800/20 border border-blue-700 rounded-xl p-4 text-center">
        <p class="text-2xl font-bold text-blue-400">24</p>
        <p class="text-xs text-gray-400 mt-1">💬 Отзывы</p>
      </div>

      <!-- Active Orders -->
      <div class="bg-gradient-to-br from-green-900/40 to-green-800/20 border border-green-700 rounded-xl p-4 text-center">
        <p class="text-2xl font-bold text-green-400">3</p>
        <p class="text-xs text-gray-400 mt-1">📦 Активных</p>
      </div>
    </div>

    <!-- Performance Badge -->
    <div class="bg-gradient-to-r from-green-900/30 to-green-800/20 border border-green-700 rounded-xl p-4 space-y-2">
      <div class="flex items-center justify-between">
        <h3 class="font-semibold text-green-300 flex items-center gap-2">
          <span>✓</span> Ваша репутация
        </h3>
      </div>
      <div class="grid grid-cols-2 gap-2 text-sm">
        <div>
          <p class="text-gray-400 text-xs">Ответ в течение</p>
          <p class="font-semibold text-green-400">&lt; 30 мин</p>
        </div>
        <div>
          <p class="text-gray-400 text-xs">Полномочия</p>
          <p class="font-semibold text-green-400">100%</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
interface ProviderInfo {
  serviceName?: string
  description?: string
  rating?: number
  reviews?: number
  categories?: string[]
}

defineProps<{
  providerInfo?: ProviderInfo
}>()
</script>

<style scoped>
</style>
