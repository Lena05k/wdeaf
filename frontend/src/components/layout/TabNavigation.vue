<template>
  <nav class="tab-nav fixed bottom-0 inset-x-0 z-40 bg-slate-900 border-t border-slate-800">
    <div class="max-w-md mx-auto flex">
      <button
          v-for="tab in tabs"
          :key="tab.id"
          @click="emit('update:currentTab', tab.id)"
          :class="[
          'tab-btn flex-1 flex flex-col items-center justify-center py-2 text-xs',
          currentTab === tab.id ? 'text-sky-400' : 'text-slate-500'
        ]"
          :title="tab.label"
      >
        <span class="text-base leading-none mb-0.5">
          {{ tab.icon }}
        </span>
        <span class="leading-none">
          {{ tab.label }}
        </span>

        <span
            v-if="currentTab === tab.id"
            class="mt-1 h-0.5 w-8 rounded-full bg-sky-400"
        />
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
  { id: 'browse', label: 'Обзор', labelShort: 'Обзор',} as any,
  { id: 'catalog', label: 'Каталог',},
  { id: 'orders', label: 'Заказы',},
  { id: 'profile', label: 'Профиль' }
]
</script>

<style scoped>
.tab-nav {
  padding: 0;
}

.tab-btn {
  border: none;
  background: transparent;
  cursor: pointer;
  transition: background-color 0.15s ease, color 0.15s ease;
}

.tab-btn:hover {
  background: rgba(15, 23, 42, 0.9);
}

/* Accessibility */
.tab-btn:focus-visible {
  outline: 2px solid #60a5fa;
  outline-offset: -2px;
}
</style>
