<template>
  <nav class="tab-nav sticky top-16 z-40">
    <div class="max-w-md mx-auto px-4 flex gap-6 overflow-x-auto">
      <button
          v-for="tab in tabs"
          :key="tab.id"
          @click="emit('update:current-tab', tab.id)"
          :class="['tab-btn', { active: currentTab === tab.id }]"
      >
        {{ tab.icon }} {{ tab.label }}
      </button>
    </div>
  </nav>
</template>

<script setup lang="ts">
import { defineProps, defineEmits } from 'vue'

interface Tab {
  id: string
  label: string
  icon: string
}

defineProps<{
  currentTab: string
}>()

defineEmits<{
  'update:current-tab': [tab: string]
}>()

const tabs: Tab[] = [
  { id: 'browse', label: 'Услуги', icon: '🔍' },
  { id: 'catalog', label: 'Каталог', icon: '📂' },
  { id: 'orders', label: 'Заказы', icon: '📋' },
  { id: 'profile', label: 'Профиль', icon: '👤' }
]
</script>

<style scoped>
.tab-nav {
  background: var(--color-bg-secondary);
  border-bottom: 1px solid var(--color-primary);
}

.tab-btn {
  padding: 12px 8px;
  font-weight: 600;
  font-size: 14px;
  color: var(--color-text-secondary);
  background: transparent;
  border: none;
  cursor: pointer;
  transition: all 0.3s ease;
  white-space: nowrap;
  border-bottom: 3px solid transparent;
}

.tab-btn:hover {
  color: var(--color-primary);
}

.tab-btn.active {
  border-bottom-color: var(--color-primary);
  color: var(--color-primary);
}
</style>
