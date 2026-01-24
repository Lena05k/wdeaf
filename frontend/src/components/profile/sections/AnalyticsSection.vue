<template>
  <div class="analytics-section space-y-4">
    <!-- Header -->
    <h3 class="text-xl font-bold text-white">Ваша аналитика</h3>

    <!-- Stats Grid -->
    <div class="grid grid-cols-2 gap-3">
      <!-- Total Earnings -->
      <div class="bg-gradient-to-br from-green-900 to-green-800 border border-green-700 rounded-xl p-4">
        <p class="text-gray-300 text-sm">Заработано</p>
        <p class="text-2xl font-bold text-green-300 mt-2">
          {{ formatPrice(providerInfo?.totalEarnings ?? 0) }}
        </p>
        <p class="text-xs text-gray-400 mt-2">💰 Всё время</p>
      </div>

      <!-- Completed Orders -->
      <div class="bg-gradient-to-br from-blue-900 to-blue-800 border border-blue-700 rounded-xl p-4">
        <p class="text-gray-300 text-sm">Завершено заказов</p>
        <p class="text-2xl font-bold text-blue-300 mt-2">
          {{ providerInfo?.completedOrders ?? 0 }}
        </p>
        <p class="text-xs text-gray-400 mt-2">✅ Выполнено</p>
      </div>

      <!-- Rating -->
      <div class="bg-gradient-to-br from-yellow-900 to-yellow-800 border border-yellow-700 rounded-xl p-4">
        <p class="text-gray-300 text-sm">Ваш рейтинг</p>
        <p class="text-2xl font-bold text-yellow-300 mt-2">
          {{ (providerInfo?.rating ?? 0).toFixed(1) }}
        </p>
        <div class="flex gap-1 mt-2">
          <span v-for="i in 5" :key="i" :class="i <= Math.round(providerInfo?.rating ?? 0) ? 'text-yellow-400' : 'text-gray-600'">
            ⭐
          </span>
        </div>
      </div>

      <!-- Active Services -->
      <div class="bg-gradient-to-br from-purple-900 to-purple-800 border border-purple-700 rounded-xl p-4">
        <p class="text-gray-300 text-sm">Активные услуги</p>
        <p class="text-2xl font-bold text-purple-300 mt-2">
          {{ providerInfo?.activeServices ?? 0 }}
        </p>
        <p class="text-xs text-gray-400 mt-2">📋 Услуг</p>
      </div>
    </div>

    <!-- Monthly Stats -->
    <div class="bg-slate-800 border border-slate-700 rounded-xl p-4">
      <h4 class="font-bold text-white mb-4">Этот месяц</h4>
      <div class="space-y-3">
        <div class="flex items-center justify-between">
          <span class="text-gray-400">Заказов получено</span>
          <span class="font-bold text-white">{{ providerInfo?.monthlyOrders ?? 0 }}</span>
        </div>
        <div class="flex items-center justify-between">
          <span class="text-gray-400">Доход за месяц</span>
          <span class="font-bold text-green-400">{{ formatPrice(providerInfo?.monthlyEarnings ?? 0) }}</span>
        </div>
        <div class="flex items-center justify-between">
          <span class="text-gray-400">Среднее за заказ</span>
          <span class="font-bold text-blue-400">
            {{ formatPrice(calculateAverageOrder()) }}
          </span>
        </div>
      </div>
    </div>

    <!-- Performance Tips -->
    <div class="bg-slate-800 border border-slate-700 rounded-xl p-4">
      <h4 class="font-bold text-white mb-3">💡 Советы по увеличению доходов</h4>
      <ul class="space-y-2 text-sm text-gray-300">
        <li class="flex gap-2">
          <span>✨</span>
          <span>Поддерживайте высокий рейтинг (4.5+)</span>
        </li>
        <li class="flex gap-2">
          <span>⚡</span>
          <span>Быстро отвечайте на заказы</span>
        </li>
        <li class="flex gap-2">
          <span>📸</span>
          <span>Добавьте фото к услугам</span>
        </li>
        <li class="flex gap-2">
          <span>📝</span>
          <span>Напишите подробное описание</span>
        </li>
      </ul>
    </div>
  </div>
</template>

<script setup lang="ts">
interface ProviderInfo {
  totalEarnings: number
  completedOrders: number
  rating: number
  activeServices: number
  monthlyOrders: number
  monthlyEarnings: number
}

defineProps<{
  providerInfo?: ProviderInfo
}>()

const formatPrice = (price: number): string => {
  return new Intl.NumberFormat('ru-RU', {
    style: 'currency',
    currency: 'RUB',
    minimumFractionDigits: 0
  }).format(price)
}

const calculateAverageOrder = (): number => {
  const monthlyOrders = (props.providerInfo?.monthlyOrders ?? 0) || 1
  const monthlyEarnings = props.providerInfo?.monthlyEarnings ?? 0
  return monthlyEarnings / monthlyOrders
}

const props = defineProps<{
  providerInfo?: ProviderInfo
}>()
</script>
