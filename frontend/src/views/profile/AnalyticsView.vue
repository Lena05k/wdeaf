<template>
  <div class="view-container">
    <div class="fixed top-0 left-0 right-0 z-50 bg-slate-900 border-b border-slate-800 p-4 flex items-center gap-3 max-w-md mx-auto">
      <button @click="$router.back()" class="text-blue-400 text-xl">‹</button>
      <h1 class="text-white font-semibold flex-1">Аналитика</h1>
    </div>

    <div class="pt-20 p-4 space-y-4">
      <div class="bg-slate-800 border border-slate-700 rounded-lg p-4">
        <h3 class="text-white font-semibold mb-4">Статистика</h3>
        
        <div class="space-y-3">
          <div class="flex justify-between">
            <span class="text-gray-400">Выполнено заказов:</span>
            <span class="text-white font-semibold">28</span>
          </div>
          <div class="flex justify-between">
            <span class="text-gray-400">Общий доход:</span>
            <span class="text-blue-400 font-semibold">425,000 ₽</span>
          </div>
          <div class="flex justify-between">
            <span class="text-gray-400">Рейтинг:</span>
            <span class="text-yellow-400 font-semibold">4.9/5.0</span>
          </div>
          <div class="flex justify-between">
            <span class="text-gray-400">Отзывов:</span>
            <span class="text-white font-semibold">124</span>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts"></script>

<style scoped>
.view-container {
  background: linear-gradient(to bottom, #0f172a, #0f1319);
  min-height: 100vh;
  padding-bottom: 40px;
}
</style>