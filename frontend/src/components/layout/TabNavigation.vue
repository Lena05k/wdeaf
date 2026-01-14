<template>
  <div class="tab-navigation sticky top-0 z-40 bg-slate-900">
    <div class="flex justify-around max-w-md mx-auto">
      <button
        v-for="tab in tabs"
        :key="tab.id"
        @click="handleTabClick(tab.id)"
        :class="[
          'flex-1 py-3 px-4 text-center font-semibold transition',
          currentTab === tab.id
            ? 'text-blue-400 border-b-2 border-blue-400'
            : 'text-gray-400 hover:text-gray-300'
        ]"
      >
        {{ tab.icon }} {{ tab.label }}
      </button>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'

interface Tab {
  id: string
  label: string
  icon: string
}

const props = defineProps<{
  currentTab: string
}>()

const emit = defineEmits<{
  'update:currentTab': [value: string]
}>()

const tabs: Tab[] = [
  { id: 'browse', label: 'Обзор', icon: '🏪' },
  { id: 'catalog', label: 'Каталог', icon: '📚' },
  { id: 'orders', label: 'Заказы', icon: '📦' },
  { id: 'profile', label: 'Профиль', icon: '👤' }
]

const handleTabClick = (tabId: string) => {
  emit('update:currentTab', tabId)
}
</script>

<style scoped>
.tab-navigation {
  background: #0f1319;
}
</style>
