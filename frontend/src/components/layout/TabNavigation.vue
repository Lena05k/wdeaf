<template>
  <div class="tab-nav sticky top-0 z-40 bg-slate-900 border-b border-slate-800">
    <div class="flex justify-between px-2">
      <button
        v-for="tab in tabs"
        :key="tab.id"
        @click="emit('update:currentTab', tab.id)"
        :class="{
          active: currentTab === tab.id,
          'tab-btn': true
        }"
        :title="tab.label"
      >
        <span class="text-lg">{{ tab.icon }}</span>
        <span class="text-xs font-medium ml-1">{{ tab.label }}</span>
      </button>
    </div>
  </div>
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

// Оптимизированный список табов
const tabs: Tab[] = [
  { id: 'browse', label: 'Обзор', icon: '🏪' },
  { id: 'catalog', label: 'Каталог', icon: '📚' },
  { id: 'orders', label: 'Заказы', icon: '📦' },
  { id: 'profile', label: 'Профиль', icon: '👤' }
]
</script>

<style scoped>
.tab-nav {
  background: #0f1319;
  padding: 0;
}

.tab-btn {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.25rem;
  padding: 0.75rem 0.5rem;
  color: #999999;
  background: transparent;
  border: none;
  border-bottom: 2px solid transparent;
  cursor: pointer;
  transition: all 0.15s ease;
  font-size: 14px;
}

.tab-btn:hover {
  color: #bbb;
  background: rgba(0, 85, 255, 0.05);
}

.tab-btn.active {
  color: #60a5fa;
  border-bottom-color: #60a5fa;
  background: rgba(0, 85, 255, 0.08);
}

/* Mobile optimization */
@media (max-width: 400px) {
  .tab-btn {
    padding: 0.6rem 0.4rem;
    gap: 0;
  }
  
  .tab-btn span:last-child {
    display: none;
  }
}

/* Accessibility */
.tab-btn:focus-visible {
  outline: 2px solid #60a5fa;
  outline-offset: -2px;
}
</style>