<template>
  <div class="layout">
    <Header :user-data="userData" />
    <TabNavigation :current-tab="currentTab" @update:current-tab="currentTab = $event" />
    <main class="main-content max-w-md mx-auto pb-20">
      <slot />
    </main>
    <Toast v-if="showToast" :message="toastMessage" :type="toastType" />
  </div>
</template>

<script setup lang="ts">
import { ref, provide, onMounted } from 'vue'
import Header from './Header.vue'
import TabNavigation from './TabNavigation.vue'
import Toast from '../shared/Toast.vue'
import { useAuth } from '@/composables/useAuth'
import { useTheme } from '@/composables/useTheme'

const currentTab = ref<string>('browse')
const showToast = ref(false)
const toastMessage = ref('')
const toastType = ref<'success' | 'error' | 'info'>('success')

const { userData, initAuth } = useAuth()
const { initTheme, colors, isDark } = useTheme()

// Предоставляем в дочерние компоненты
provide('currentTab', currentTab)
provide('showToast', (message: string, type: 'success' | 'error' | 'info' = 'success') => {
  toastMessage.value = message
  toastType.value = type
  showToast.value = true
  setTimeout(() => {
    showToast.value = false
  }, 3000)
})

onMounted(async () => {
  initTheme()
  await initAuth()
})
</script>

<style scoped>
.layout {
  min-height: 100vh;
  background: var(--color-bg-primary);
  color: var(--color-text-primary);
  transition: all 0.3s ease;
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
}

.main-content {
  padding: 16px;
}
</style>
