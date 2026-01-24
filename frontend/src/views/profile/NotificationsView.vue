<template>
  <div class="view-container">
    <div class="fixed top-0 left-0 right-0 z-50 bg-slate-900 border-b border-slate-800 p-4 flex items-center gap-3 max-w-md mx-auto">
      <button @click="$router.back()" class="text-blue-400 text-xl">‹</button>
      <h1 class="text-white font-semibold flex-1">Уведомления</h1>
    </div>

    <div class="pt-20 p-4 space-y-4">
      <div class="bg-slate-800 border border-slate-700 rounded-lg p-4">
        <h3 class="text-white font-semibold mb-4">Настройки уведомлений</h3>
        
        <div class="space-y-3">
          <div class="flex justify-between items-center">
            <span class="text-gray-300">Новые заказы</span>
            <input type="checkbox" checked class="w-5 h-5" />
          </div>
          <div class="flex justify-between items-center">
            <span class="text-gray-300">Сообщения</span>
            <input type="checkbox" checked class="w-5 h-5" />
          </div>
          <div class="flex justify-between items-center">
            <span class="text-gray-300">Отзывы</span>
            <input type="checkbox" checked class="w-5 h-5" />
          </div>
          <div class="flex justify-between items-center">
            <span class="text-gray-300">Промо и скидки</span>
            <input type="checkbox" class="w-5 h-5" />
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