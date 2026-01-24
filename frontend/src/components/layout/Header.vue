<template>
  <header class="sticky top-0 z-50 bg-white border-b border-gray-200 shadow-sm" :style="headerStyle">
    <div class="max-w-md mx-auto px-4 py-2">
      <!-- Compact Header Layout -->
      <div class="flex items-center justify-between gap-3">
        <!-- Logo & Branding (Compact) -->
        <a href="#" @click.prevent="goHome" class="flex items-center gap-2 flex-shrink-0 group">
          <!-- Logo SVG (Smaller) -->
          <div class="w-10 h-10 flex-shrink-0 transition-transform group-hover:scale-105">
            <svg
              viewBox="0 0 220 220"
              fill="none"
              xmlns="http://www.w3.org/2000/svg"
            >
              <g clip-path="url(#clip0_4001_20)">
                <path d="M1.52588e-05 47.2652C1.52588e-05 21.1613 21.1614 0 47.2652 0L173.306 1.81017e-10C199.41 2.08283e-10 220.571 21.1613 220.571 47.2652L220.571 173.306C220.571 199.41 199.41 220.571 173.306 220.571L47.2652 220.571C21.1614 220.571 1.5259e-05 199.41 1.5259e-05 173.306L1.52588e-05 47.2652Z" fill="#0E1117"/>
                <mask id="mask0_4001_20" style="mask-type:alpha" maskUnits="userSpaceOnUse" x="0" y="0" width="221" height="221">
                  <path d="M1.52588e-05 47.2652C1.52588e-05 21.1613 21.1614 -1.52588e-05 47.2652 -1.52587e-05L173.306 -1.52586e-05C199.41 -1.52586e-05 220.571 21.1613 220.571 47.2652L220.571 173.306C220.571 199.409 199.41 220.571 173.306 220.571L47.2652 220.571C21.1614 220.571 1.5259e-05 199.409 1.5259e-05 173.306L1.52588e-05 47.2652Z" fill="#4747A6"/>
                </mask>
                <g mask="url(#mask0_4001_20)">
                  <path d="M114.697 114.224C51.3516 114.224 3.4062e-05 62.8727 2.02174e-05 -0.472626L1.52589e-05 -23.1599C1.41428e-06 -86.5052 51.3516 -137.857 114.697 -137.857L168.894 -137.857C232.24 -137.857 283.591 -86.5053 283.591 -23.1599L283.591 -0.472687C283.591 62.8726 232.24 114.224 168.894 114.224L114.697 114.224Z" fill="#155DFC"/>
                  <path d="M88.3104 181.183C85.198 181.183 82.4546 179.127 81.5624 176.126L43.6266 48.5098C42.2747 43.962 45.6584 39.3877 50.3745 39.3877L83.7892 39.3877C87.0614 39.3877 89.9027 41.6561 90.6477 44.8633L102.578 96.2214C104.251 103.427 114.396 103.557 116.252 96.3963L129.649 44.6883C130.458 41.5662 133.259 39.3877 136.464 39.3877L172.51 39.3877C175.723 39.3877 178.529 41.5761 179.331 44.7076L192.477 96.0354C194.317 103.222 204.502 103.092 206.16 95.8601L217.85 44.8829C218.587 41.6662 221.433 39.3876 224.713 39.3876L256.849 39.3876C261.565 39.3876 264.949 43.9619 263.597 48.5098L225.661 176.126C224.769 179.127 222.026 181.183 218.913 181.183L181.333 181.183C178.155 181.183 175.37 179.041 174.536 175.954L160.36 123.484C158.47 116.491 148.606 116.52 146.756 123.523L132.918 175.915C132.098 179.021 129.304 181.183 126.111 181.183L88.3104 181.183Z" fill="white"/>
                </g>
              </g>
              <defs>
                <clipPath id="clip0_4001_20">
                  <rect width="220.571" height="220.571" fill="white" transform="translate(1.52588e-05 220.571) rotate(-90)"/>
                </clipPath>
              </defs>
            </svg>
          </div>

          <!-- Brand Text (Inline) -->
          <div class="flex flex-col gap-0.5">
            <span class="font-bold text-sm leading-none" :style="{ color: textColor }">Deaf</span>
            <span class="text-xs leading-none" :style="{ color: hintColor }">услуги</span>
          </div>
        </a>

        <!-- Right Actions -->
        <div class="flex items-center gap-2">
          <!-- Status Indicator (optional online status) -->
          <div class="hidden sm:flex items-center gap-1 px-2 py-1 rounded-full border" :style="statusStyle">
            <span class="w-2 h-2 bg-green-500 rounded-full animate-pulse"></span>
            <span class="text-xs font-medium">Онлайн</span>
          </div>

          <!-- Theme Toggle Button (Telegram-aware) -->
          <button
            @click="toggleTheme"
            class="flex items-center justify-center w-9 h-9 rounded-lg hover:shadow-md transition-all active:scale-95"
            :style="themeButtonStyle"
            title="Переключить тему"
            aria-label="Переключить тему"
          >
            <!-- Sun icon (light mode) -->
            <svg v-if="isDarkMode" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <circle cx="12" cy="12" r="5"></circle>
              <line x1="12" y1="1" x2="12" y2="3"></line>
              <line x1="12" y1="21" x2="12" y2="23"></line>
              <line x1="4.22" y1="4.22" x2="5.64" y2="5.64"></line>
              <line x1="18.36" y1="18.36" x2="19.78" y2="19.78"></line>
              <line x1="1" y1="12" x2="3" y2="12"></line>
              <line x1="21" y1="12" x2="23" y2="12"></line>
              <line x1="4.22" y1="19.78" x2="5.64" y2="18.36"></line>
              <line x1="18.36" y1="5.64" x2="19.78" y2="4.22"></line>
            </svg>
            <!-- Moon icon (dark mode) -->
            <svg v-else width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"></path>
            </svg>
          </button>

          <!-- Profile Quick Access -->
          <button
            v-if="userData?.username"
            @click="goToProfile"
            class="flex items-center justify-center w-9 h-9 rounded-full text-white text-xs font-bold hover:shadow-md transition-all active:scale-95"
            :style="avatarStyle"
            :title="userData.first_name"
            aria-label="Перейти в профиль"
          >
            {{ getUserInitials(userData.first_name) }}
          </button>
        </div>
      </div>
    </div>
  </header>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'

interface Props {
  userData?: {
    first_name?: string
    id?: string | number
    username?: string
  }
}

const emit = defineEmits<{
  'update:currentTab': [value: string]
}>()

const props = defineProps<Props>()

const isDarkMode = ref(false)

const getUserInitials = (name?: string): string => {
  if (!name) return '?'
  return name
    .split(' ')
    .map(word => word[0])
    .join('')
    .toUpperCase()
    .slice(0, 2)
}

const goHome = () => {
  console.log('Going to home (browse tab)')
  emit('update:currentTab', 'browse')
}

const goToProfile = () => {
  console.log('Going to profile tab')
  emit('update:currentTab', 'profile')
}

const toggleTheme = () => {
  isDarkMode.value = !isDarkMode.value
  applyTheme()
}

const applyTheme = () => {
  // Sync with Telegram theme if available
  if (window.Telegram?.WebApp) {
    const colorScheme = window.Telegram.WebApp.colorScheme
    isDarkMode.value = colorScheme === 'dark'
  }
  
  // Apply to document
  document.documentElement.setAttribute('data-theme', isDarkMode.value ? 'dark' : 'light')
}

const getTelegramThemeParams = () => {
  if (!window.Telegram?.WebApp?.themeParams) {
    return {
      bg_color: '#ffffff',
      text_color: '#000000',
      hint_color: '#6b7280',
      secondary_bg_color: '#f3f4f6',
      button_color: '#2563eb'
    }
  }
  return window.Telegram.WebApp.themeParams
}

const themeParams = computed(() => getTelegramThemeParams())

const textColor = computed(() => themeParams.value.text_color || '#000000')
const hintColor = computed(() => themeParams.value.hint_color || '#6b7280')
const bgColor = computed(() => themeParams.value.bg_color || '#ffffff')
const buttonColor = computed(() => themeParams.value.button_color || '#2563eb')

const headerStyle = computed(() => ({
  backgroundColor: bgColor.value,
  color: textColor.value,
  borderColor: isDarkMode.value ? '#374151' : '#e5e5e5'
}))

const statusStyle = computed(() => ({
  backgroundColor: isDarkMode.value ? 'rgba(34, 197, 94, 0.1)' : 'rgba(34, 197, 94, 0.08)',
  borderColor: isDarkMode.value ? '#22c55e' : '#86efac',
  color: isDarkMode.value ? '#86efac' : '#16a34a'
}))

const themeButtonStyle = computed(() => ({
  backgroundColor: isDarkMode.value ? '#374151' : '#f3f4f6',
  color: textColor.value
}))

const avatarStyle = computed(() => ({
  background: `linear-gradient(135deg, ${buttonColor.value} 0%, rgba(37, 99, 235, 0.8) 100%)`
}))

onMounted(() => {
  // Initialize Telegram WebApp
  if (window.Telegram?.WebApp) {
    window.Telegram.WebApp.ready()
    
    // Apply initial theme
    applyTheme()
    
    // Listen for theme changes
    window.Telegram.WebApp.onEvent('themeChanged', () => {
      applyTheme()
    })
  }
})
</script>

<style scoped>
/* Smooth animations */
@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(-2px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

header {
  animation: fadeIn 0.3s ease-out;
}

/* Focus states for accessibility */
button:focus-visible {
  outline: 2px solid #0055ff;
  outline-offset: 2px;
}

/* Smooth hover transitions */
button {
  transition: all 0.2s ease;
}

button:active {
  transition: transform 0.1s ease;
}

/* Pulse animation for online indicator */
@keyframes pulse {
  0%, 100% {
    opacity: 1;
  }
  50% {
    opacity: 0.5;
  }
}

.animate-pulse {
  animation: pulse 2s cubic-bezier(0.4, 0, 0.6, 1) infinite;
}
</style>
