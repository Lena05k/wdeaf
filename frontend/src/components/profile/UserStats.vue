<template>
  <div class="px-4 py-4 space-y-3">
    <div class="grid grid-cols-3 gap-3">
      <!-- Orders Count -->
      <div class="bg-gradient-to-br from-blue-900/40 to-blue-800/20 border border-blue-700 rounded-xl p-4 text-center">
        <p class="text-2xl font-bold text-blue-400">{{ ordersCount }}</p>
        <p class="text-xs text-gray-400 mt-1">Мои заказы</p>
      </div>

      <!-- Completed Orders -->
      <div class="bg-gradient-to-br from-green-900/40 to-green-800/20 border border-green-700 rounded-xl p-4 text-center">
        <p class="text-2xl font-bold text-green-400">5</p>
        <p class="text-xs text-gray-400 mt-1">Выполнено</p>
      </div>

      <!-- Reviews Left -->
      <div class="bg-gradient-to-br from-purple-900/40 to-purple-800/20 border border-purple-700 rounded-xl p-4 text-center">
        <p class="text-2xl font-bold text-purple-400">2</p>
        <p class="text-xs text-gray-400 mt-1">Отзывы</p>
      </div>
    </div>

    <!-- Info message -->
    <div class="bg-slate-800/50 border border-slate-700 rounded-xl p-3 text-center">
      <p class="text-xs text-gray-400">📄 Можно стать исполнителем и получать заказы</p>
    </div>
  </div>
</template>

<script setup lang="ts">
defineProps<{
  ordersCount: number
}>()
</script>

<style scoped>
</style>
