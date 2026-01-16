<template>
  <div class="grid grid-cols-2 gap-3">
    <div class="bg-blue-900/30 rounded-lg p-3 text-center border border-blue-800">
      <p class="text-2xl font-bold text-blue-400">{{ ordersCount }}</p>
      <p class="text-xs text-gray-400">Заказов</p>
    </div>
    <div class="bg-green-900/30 rounded-lg p-3 text-center border border-green-800">
      <p class="text-2xl font-bold text-green-400">{{ rating }}</p>
      <p class="text-xs text-gray-400">Рейтинг</p>
    </div>
  </div>
</template>

<script setup lang="ts">
interface Props {
  ordersCount: number
  rating?: number
}

const props = withDefaults(defineProps<Props>(), {
  rating: 4.8
})
</script>

<style scoped></style>
