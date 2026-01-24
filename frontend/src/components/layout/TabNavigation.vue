<template>
  <nav class="sticky top-14 z-40 bg-white border-b border-gray-200" :style="navStyle">
    <div class="max-w-md mx-auto flex h-12">
      <button
        v-for="tab in tabs"
        :key="tab.id"
        @click="emit('update:currentTab', tab.id)"
        :class="[
          'flex-1 flex flex-col items-center justify-center text-xs font-medium transition-all',
          currentTab === tab.id
            ? 'border-b-2 border-blue-600'
            : 'border-b-2 border-transparent hover:border-gray-300'
        ]"
        :style="currentTab === tab.id ? activeTabStyle : inactiveTabStyle"
        :title="tab.label"
        :aria-label="tab.label"
      >
        <!-- SVG Icons instead of emojis -->
        <svg 
          v-if="tab.id === 'browse'" 
          width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" class="mb-1"
        >
          <circle cx="11" cy="11" r="8"></circle>
          <path d="m21 21-4.35-4.35"></path>
        </svg>
        
        <svg 
          v-else-if="tab.id === 'catalog'" 
          width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" class="mb-1"
        >
          <path d="M22 19a2 2 0 0 1-2 2H4a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h5l2 3h9a2 2 0 0 1 2 2z"></path>
        </svg>
        
        <svg 
          v-else-if="tab.id === 'orders'" 
          width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" class="mb-1"
        >
          <path d="M6 2h12a2 2 0 0 1 2 2v16a2 2 0 0 1-2 2H6a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2z"></path>
          <line x1="6" y1="6" x2="18" y2="6"></line>
          <line x1="6" y1="10" x2="18" y2="10"></line>
          <line x1="6" y1="14" x2="18" y2="14"></line>
        </svg>
        
        <span class="text-xs mt-0.5 font-medium leading-none">{{ tab.label }}</span>
      </button>
    </div>
  </nav>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'

interface Tab {
  id: string
  label: string
}

interface Props {
  currentTab: string
}

defineProps<Props>()

const emit = defineEmits<{
  'update:currentTab': [value: string]
}>()

const isDarkMode = ref(false)

const tabs: Tab[] = [
  { id: 'browse', label: 'Обзор' },
  { id: 'catalog', label: 'Каталог' },
  { id: 'orders', label: 'Заказы' }
]

const getTelegramThemeParams = () => {
  if (!window.Telegram?.WebApp?.themeParams) {
    return {
      text_color: '#000000',
      hint_color: '#6b7280',
      bg_color: '#ffffff'
    }
  }
  return window.Telegram.WebApp.themeParams
}

const themeParams = computed(() => getTelegramThemeParams())

const navStyle = computed(() => ({
  backgroundColor: themeParams.value.bg_color || '#ffffff',
  borderColor: isDarkMode.value ? '#374151' : '#e5e5e5'
}))

const activeTabStyle = computed(() => ({
  color: '#2563eb',
  fontWeight: '600'
}))

const inactiveTabStyle = computed(() => ({
  color: themeParams.value.hint_color || '#6b7280',
  fontWeight: '500'
}))

onMounted(() => {
  // Sync with Telegram theme
  if (window.Telegram?.WebApp) {
    isDarkMode.value = window.Telegram.WebApp.colorScheme === 'dark'
    
    // Listen for theme changes
    window.Telegram.WebApp.onEvent('themeChanged', () => {
      isDarkMode.value = window.Telegram.WebApp.colorScheme === 'dark'
    })
  }
})
</script>

<style scoped>
/* Smooth transitions */
button {
  transition: all 0.2s cubic-bezier(0.16, 1, 0.3, 1);
  color: inherit;
}

button:hover {
  opacity: 0.8;
}

button:active {
  transform: scale(0.98);
}

/* Focus states */
button:focus-visible {
  outline: 2px solid #3b82f6;
  outline-offset: -2px;
}

/* SVG icon styling */
svg {
  stroke-linecap: round;
  stroke-linejoin: round;
}
</style>
