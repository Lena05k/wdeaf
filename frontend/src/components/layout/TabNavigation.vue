<template>
  <nav class="sticky top-14 z-40 bg-white border-b border-gray-200">
    <div class="max-w-md mx-auto flex h-12">
      <button
        v-for="tab in tabs"
        :key="tab.id"
        @click="emit('update:currentTab', tab.id)"
        :class="[
          'flex-1 flex flex-col items-center justify-center text-xs font-medium transition-all',
          currentTab === tab.id
            ? 'text-blue-600 border-b-2 border-blue-600'
            : 'text-gray-600 hover:text-gray-900 border-b-2 border-transparent hover:border-gray-300'
        ]"
        :title="tab.label"
        aria-label="tab.label"
      >
        <span class="text-base leading-none">{{ tab.icon }}</span>
        <span class="text-xs mt-0.5 font-medium leading-none">{{ tab.label }}</span>
      </button>
    </div>
  </nav>
</template>

<script setup lang="ts">
interface Tab {
  id: string
  label: string
  icon: string
}

interface Props {
  currentTab: string
}

defineProps<Props>()

const emit = defineEmits<{
  'update:currentTab': [value: string]
}>()

const tabs: Tab[] = [
  { id: 'browse', label: 'Обзор', icon: '🔍' },
  { id: 'catalog', label: 'Каталог', icon: '📂' },
  { id: 'orders', label: 'Заказы', icon: '📑' },
  { id: 'profile', label: 'Профиль', icon: '👤' }
]
</script>

<style scoped>
/* Smooth transitions */
button {
  transition: all 0.2s cubic-bezier(0.16, 1, 0.3, 1);
}

button:hover {
  background-color: rgba(59, 130, 246, 0.05);
}

button:active {
  transform: scale(0.98);
}

/* Focus states */
button:focus-visible {
  outline: 2px solid #3b82f6;
  outline-offset: -2px;
}
</style>
