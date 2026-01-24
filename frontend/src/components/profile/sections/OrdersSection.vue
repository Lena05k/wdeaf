<template>
  <div class="space-y-3 pb-4">
    <div v-if="orders.length === 0" class="text-center py-12 text-gray-400">
      <p class="text-4xl mb-2"> 📦</p>
      <p class="text-sm font-semibold" >У вас ещё нет заказов</p>
      <p class="text-xs text-gray-500 mt-1">Начните с просмотра доступных услуг</p>
    </div>

    <div v-for="order in orders" :key="order.id" class="bg-slate-800 border border-slate-700 rounded-xl p-4 space-y-3 hover:border-blue-600 transition">
      <div class="flex justify-between items-start gap-3">
        <div class="flex-1">
          <h3 class="font-semibold text-white line-clamp-1">{{ order.serviceName }}</h3>
          <p class="text-sm text-gray-400">{{ order.provider }}</p>
        </div>
        <span v-if="order.status === 'completed'" class="bg-green-900/40 text-green-400 text-xs px-2 py-1 rounded-full border border-green-700 whitespace-nowrap">
          ✓ Завершен
        </span>
        <span v-else class="bg-blue-900/40 text-blue-400 text-xs px-2 py-1 rounded-full border border-blue-700 whitespace-nowrap">
          ⏳ В процессе
        </span>
      </div>

      <p class="text-xs text-gray-500 flex items-center gap-1">
        <span>📅</span> {{ order.date }}
      </p>

      <div v-if="order.status === 'completed' && !order.rating" class="pt-2 border-t border-slate-700 flex gap-2">
        <button class="flex-1 text-xs text-blue-400 hover:text-blue-300 transition py-2 rounded hover:bg-blue-900/20">
          ⭐ Оставить отзыв
        </button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
defineProps<{
  orders: any[]
}>()
</script>
