<template>
  <div class="tab-bar sticky top-0 z-30 bg-gradient-to-b from-slate-800 to-slate-900 border-b border-slate-700">
    <div class="px-4 py-3 flex gap-1 overflow-x-auto scrollbar-hide">
      <!-- For Non-Providers -->
      <template v-if="!isProvider">
        <button
          v-for="tab in userTabs"
          :key="tab.id"
          @click="$emit('selectTab', tab.id)"
          :class="[
            'px-4 py-2 rounded-lg font-semibold transition whitespace-nowrap',
            activeTab === tab.id
              ? 'bg-blue-600 text-white shadow-lg'
              : 'bg-slate-700/50 text-gray-400 hover:text-gray-300'
          ]"
        >
          {{ tab.icon }} {{ tab.label }}
        </button>
      </template>

      <!-- For Providers -->
      <template v-else>
        <button
          v-for="tab in providerTabs"
          :key="tab.id"
          @click="$emit('selectTab', tab.id)"
          :class="[
            'px-4 py-2 rounded-lg font-semibold transition whitespace-nowrap',
            activeTab === tab.id
              ? 'bg-green-600 text-white shadow-lg'
              : 'bg-slate-700/50 text-gray-400 hover:text-gray-300'
          ]"
        >
          {{ tab.icon }} {{ tab.label }}
        </button>
      </template>
    </div>
  </div>
</template>

<script setup lang="ts">
const userTabs = [
  { id: 'orders', label: 'Заказы', icon: '📦' },
  { id: 'saved', label: 'Сохранённые', icon: '❤️' },
  { id: 'reviews', label: 'Отзывы', icon: '⭐' }
]

const providerTabs = [
  { id: 'services', label: 'Услуги', icon: '📋' },
  { id: 'orders', label: 'Заказы', icon: '📦' },
  { id: 'analytics', label: 'Аналитика', icon: '📊' },
  { id: 'profile', label: 'Профиль', icon: '👤' }
]

defineProps<{
  activeTab: string
  isProvider: boolean
}>()

defineEmits<{
  selectTab: [id: string]
}>()
</script>

<style scoped>
.scrollbar-hide::-webkit-scrollbar {
  display: none;
}

.scrollbar-hide {
  -ms-overflow-style: none;
  scrollbar-width: none;
}
</style>
