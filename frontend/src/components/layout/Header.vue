<template>
  <header class="sticky top-0 z-50 bg-white border-b border-gray-200" :style="headerStyle">
    <!-- Logo Row -->
    <div class="max-w-md mx-auto px-4 py-3 border-b border-gray-200">
      <div class="flex items-center justify-between">
        <!-- Logo -->
        <button
          @click="goHome"
          @keydown.enter="goHome"
          @keydown.space="goHome"
          class="logo-btn flex items-center flex-shrink-0 group"
          title="На главную"
          aria-label="WDEAF Главная"
        >
          <!-- SVG Logo -->
          <div class="w-9 h-9 flex-shrink-0 transition-transform group-hover:scale-110 group-focus-visible:scale-110">
            <svg
              viewBox="0 0 220 220"
              fill="none"
              xmlns="http://www.w3.org/2000/svg"
              class="w-full h-full"
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
        </button>

        <!-- Spacer -->
        <div class="flex-1"></div>

        <!-- Profile Avatar -->
        <button
          v-if="userInitials"
          @click="openProfile"
          @keydown.enter="openProfile"
          class="profile-avatar"
          :title="`Профиль ${userName}`"
          :aria-label="`Профиль пользователя ${userName}`"
          :style="avatarStyle"
        >
          <span class="font-bold text-sm">{{ userInitials }}</span>
        </button>
      </div>
    </div>

    <!-- Tab Navigation -->
    <nav class="max-w-md mx-auto flex h-12" role="tablist">
      <button
        v-for="tab in tabs"
        :key="tab.id"
        role="tab"
        :aria-selected="currentTab === tab.id"
        :aria-controls="`panel-${tab.id}`"
        @click="updateTab(tab.id)"
        :class="[
          'flex-1 flex flex-col items-center justify-center text-xs font-medium transition-all',
          currentTab === tab.id
            ? 'border-b-2 border-blue-600'
            : 'border-b-2 border-transparent hover:border-gray-300'
        ]"
        :style="currentTab === tab.id ? activeTabStyle : inactiveTabStyle"
        :title="tab.label"
      >
        <!-- SVG Icons -->
        <svg
          v-if="tab.id === 'browse'"
          width="20"
          height="20"
          viewBox="0 0 24 24"
          fill="none"
          stroke="currentColor"
          stroke-width="2"
          class="mb-1"
        >
          <circle cx="11" cy="11" r="8"></circle>
          <path d="m21 21-4.35-4.35"></path>
        </svg>

        <svg
          v-else-if="tab.id === 'catalog'"
          width="20"
          height="20"
          viewBox="0 0 24 24"
          fill="none"
          stroke="currentColor"
          stroke-width="2"
          class="mb-1"
        >
          <path d="M22 19a2 2 0 0 1-2 2H4a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h5l2 3h9a2 2 0 0 1 2 2z"></path>
        </svg>

        <svg
          v-else-if="tab.id === 'orders'"
          width="20"
          height="20"
          viewBox="0 0 24 24"
          fill="none"
          stroke="currentColor"
          stroke-width="2"
          class="mb-1"
        >
          <path d="M6 2h12a2 2 0 0 1 2 2v16a2 2 0 0 1-2 2H6a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2z"></path>
          <line x1="6" y1="6" x2="18" y2="6"></line>
          <line x1="6" y1="10" x2="18" y2="10"></line>
          <line x1="6" y1="14" x2="18" y2="14"></line>
        </svg>

        <span class="text-xs mt-0.5 font-medium leading-none">{{ tab.label }}</span>
      </button>
    </nav>
  </header>
</template>

<script setup lang="ts">
import { computed, onMounted, ref } from 'vue'

interface Tab {
  id: string
  label: string
}

interface Props {
  userName?: string
  userInitials?: string
  buttonColor?: string
  currentTab?: string
}

const props = withDefaults(defineProps<Props>(), {
  userName: 'User',
  userInitials: 'U',
  buttonColor: '#2563eb',
  currentTab: 'browse'
})

const emit = defineEmits<{
  'open-profile': []
  'go-home': []
  'update:current-tab': [value: string]
}>()

const isDarkMode = ref(false)
const currentTabLocal = ref(props.currentTab)

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
      bg_color: '#ffffff',
      button_color: '#2563eb'
    }
  }
  return window.Telegram.WebApp.themeParams
}

const themeParams = computed(() => getTelegramThemeParams())

const headerStyle = computed(() => ({
  backgroundColor: themeParams.value.bg_color || '#ffffff',
  color: themeParams.value.text_color || '#000000',
  borderColor: isDarkMode.value ? '#374151' : '#e5e5e5'
}))

const avatarStyle = computed(() => ({
  backgroundColor: props.buttonColor || themeParams.value.button_color || '#2563eb',
  borderColor: props.buttonColor || themeParams.value.button_color || '#2563eb'
}))

const activeTabStyle = computed(() => ({
  color: '#2563eb',
  fontWeight: '600'
}))

const inactiveTabStyle = computed(() => ({
  color: themeParams.value.hint_color || '#6b7280',
  fontWeight: '500'
}))

const currentTab = computed(() => props.currentTab)

const updateTab = (tabId: string) => {
  currentTabLocal.value = tabId
  emit('update:current-tab', tabId)
}

const goHome = () => {
  emit('go-home')
}

const openProfile = () => {
  emit('open-profile')
}

onMounted(() => {
  if (window.Telegram?.WebApp) {
    isDarkMode.value = window.Telegram.WebApp.colorScheme === 'dark'

    window.Telegram.WebApp.onEvent('themeChanged', () => {
      isDarkMode.value = window.Telegram.WebApp.colorScheme === 'dark'
    })
  }
})
</script>

<style scoped>
/* Logo Button */
.logo-btn {
  background: none;
  border: none;
  padding: 0.25rem;
  cursor: pointer;
  border-radius: 8px;
  transition: background-color 0.2s ease-out;
  display: flex;
  align-items: center;
  position: relative;
}

.logo-btn:hover {
  background-color: rgba(0, 0, 0, 0.04);
}

.logo-btn:focus-visible {
  outline: 2px solid #3b82f6;
  outline-offset: 2px;
}

/* Profile Avatar - Circular */
.profile-avatar {
  width: 2.25rem;
  height: 2.25rem;
  border-radius: 50%;
  color: white;
  border: 2px solid currentColor;
  cursor: pointer;
  font-weight: 700;
  font-size: 0.875rem;
  transition: all 0.2s cubic-bezier(0.16, 1, 0.3, 1);
  flex-shrink: 0;
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.15);
  position: relative;
}

.profile-avatar::before {
  content: '';
  position: absolute;
  inset: 0;
  border-radius: 50%;
  background: linear-gradient(135deg, rgba(255, 255, 255, 0.2) 0%, rgba(255, 255, 255, 0) 100%);
  pointer-events: none;
}

.profile-avatar:hover {
  transform: translateY(-2px) scale(1.08);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
}

.profile-avatar:active {
  transform: translateY(0) scale(0.95);
  box-shadow: 0 1px 4px rgba(0, 0, 0, 0.15);
}

.profile-avatar:focus-visible {
  outline: 2px solid white;
  outline-offset: 2px;
}

/* Tab Navigation */
nav button {
  transition: all 0.2s cubic-bezier(0.16, 1, 0.3, 1);
  color: inherit;
  border: none;
  background: none;
  font-family: inherit;
  font-size: inherit;
  cursor: pointer;
}

nav button:hover {
  opacity: 0.8;
}

nav button:active {
  transform: scale(0.98);
}

/* Focus states */
nav button:focus-visible {
  outline: 2px solid #3b82f6;
  outline-offset: -2px;
}

/* SVG Icon styling */
svg {
  stroke-linecap: round;
  stroke-linejoin: round;
}

/* Responsive */
@media (max-width: 640px) {
  .logo-btn {
    padding: 0.25rem;
  }
}

/* High contrast mode support */
@media (prefers-contrast: more) {
  .profile-avatar {
    border-width: 3px;
  }
}

/* Reduced motion support */
@media (prefers-reduced-motion: reduce) {
  * {
    animation-duration: 0.01ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: 0.01ms !important;
  }
}
</style>