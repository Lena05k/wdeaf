<template>
  <div
      class="app"
      :data-theme="themeStore.isDark ? 'dark' : 'light'"
      :style="themeStyles"
  >
    <MainLayout>
      <component :is="currentView" />
    </MainLayout>

    <Toast v-if="toastStore.show" />
  </div>
</template>

<script setup>
import { computed, onMounted } from 'vue'
import { useThemeStore } from '@/stores/themeStore'
import { useAuthStore } from '@/stores/userStore'
import MainLayout from '@/components/layout/MainLayout.vue'
import Toast from '@/components/shared/Toast.vue'
import { useRoute } from 'vue-router'

const route = useRoute()
const themeStore = useThemeStore()
const authStore = useAuthStore()

const currentView = computed(() => {
  const views = {
    'browse': () => import('@/views/BrowseServices.vue'),
    'catalog': () => import('@/views/Catalog.vue'),
    'orders': () => import('@/views/Orders.vue'),
    'profile': () => import('@/views/Profile.vue')
  }
  return views[route.params.tab || 'browse']
})

const themeStyles = computed(() => ({
  '--color-primary': themeStore.colors.primary,
  '--color-bg-primary': themeStore.colors.bg.primary,
  '--color-text-primary': themeStore.colors.text.primary
}))

onMounted(async () => {
  themeStore.initTheme()
  await authStore.initAuth()
})
</script>

<style scoped>
.app {
  min-height: 100vh;
  background: var(--color-bg-primary);
  color: var(--color-text-primary);
  transition: background 0.3s, color 0.3s;
}
</style>
