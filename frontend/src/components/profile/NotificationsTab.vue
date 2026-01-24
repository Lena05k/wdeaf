<template>
  <div class="space-y-4">
    <div class="bg-slate-700 rounded-lg p-4 border border-slate-600 space-y-4">
      <div class="flex justify-between items-center">
        <span class="text-gray-300">🔔 Новые заказы</span>
        <label class="relative inline-flex items-center">
          <input type="checkbox" v-model="settings.orders" class="sr-only peer" />
          <div class="w-11 h-6 bg-slate-600 peer-focus:outline-none peer-focus:ring-2 peer-focus:ring-blue-500 rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:rounded-full after:h-5 after:w-5 after:transition-all peer-checked:bg-blue-600"></div>
        </label>
      </div>

      <div class="flex justify-between items-center border-t border-slate-600 pt-4">
        <span class="text-gray-300">💬 Сообщения</span>
        <label class="relative inline-flex items-center">
          <input type="checkbox" v-model="settings.messages" class="sr-only peer" />
          <div class="w-11 h-6 bg-slate-600 peer-focus:outline-none peer-focus:ring-2 peer-focus:ring-blue-500 rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:rounded-full after:h-5 after:w-5 after:transition-all peer-checked:bg-blue-600"></div>
        </label>
      </div>

      <div class="flex justify-between items-center border-t border-slate-600 pt-4">
        <span class="text-gray-300">⭐ Отзывы</span>
        <label class="relative inline-flex items-center">
          <input type="checkbox" v-model="settings.reviews" class="sr-only peer" />
          <div class="w-11 h-6 bg-slate-600 peer-focus:outline-none peer-focus:ring-2 peer-focus:ring-blue-500 rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:rounded-full after:h-5 after:w-5 after:transition-all peer-checked:bg-blue-600"></div>
        </label>
      </div>

      <div class="flex justify-between items-center border-t border-slate-600 pt-4">
        <span class="text-gray-300">🎁 Промо и скидки</span>
        <label class="relative inline-flex items-center">
          <input type="checkbox" v-model="settings.promo" class="sr-only peer" />
          <div class="w-11 h-6 bg-slate-600 peer-focus:outline-none peer-focus:ring-2 peer-focus:ring-blue-500 rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:rounded-full after:h-5 after:w-5 after:transition-all peer-checked:bg-blue-600"></div>
        </label>
      </div>
    </div>

    <button 
      @click="saveSettings"
      class="w-full bg-blue-600 hover:bg-blue-500 text-white font-semibold py-2 rounded-lg transition"
    >
      Сохранить
    </button>
  </div>
</template>

<script setup lang="ts">
import { reactive } from 'vue'

const settings = reactive({
  orders: true,
  messages: true,
  reviews: true,
  promo: false
})

const saveSettings = () => {
  console.log('✅ Уведомления сохранены:', settings)
  alert('✅ Настройки уведомлений сохранены!')
}
</script>