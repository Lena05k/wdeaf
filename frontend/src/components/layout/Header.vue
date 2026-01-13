<template>
  <header class="header sticky top-0 z-50">
    <div class="max-w-md mx-auto px-4 py-3 flex items-center justify-between">
      <div>
        <h1 class="text-xl font-bold">WDEAF</h1>
        <p class="text-xs text-secondary">Платформа услуг</p>
      </div>
      <div class="text-right">
        <p class="text-sm font-semibold">{{ userData.first_name || 'Гость' }}</p>
        <p class="text-xs text-secondary">@{{ userData.username || 'user' }}</p>
      </div>
    </div>
  </header>
</template>

<script setup lang="ts">
import { defineProps } from 'vue'

interface User {
  first_name: string
  username: string | null
}

defineProps<{
  userData: User
}>()
</script>

<style scoped>
.header {
  background: var(--color-bg-secondary);
  border-bottom: 1px solid var(--color-primary);
  box-shadow: 0 2px 8px var(--color-shadow);
}

.header h1 {
  color: var(--color-primary);
  margin: 0;
}

.text-secondary {
  color: var(--color-text-secondary);
}
</style>
