<template>
  <header class="sticky top-0 z-50 bg-white border-b border-gray-200 shadow-sm">
    <div class="max-w-md mx-auto px-4 py-2">
      <!-- Compact Header Layout -->
      <div class="flex items-center justify-between gap-3">
        <!-- Logo & Branding (Compact) -->
        <a href="#" class="flex items-center gap-2 flex-shrink-0 group">
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
            <span class="font-bold text-sm text-gray-900 leading-none">Deaf</span>
            <span class="text-xs text-gray-500 leading-none">услуги</span>
          </div>
        </a>

        <!-- Right Actions -->
        <div class="flex items-center gap-2">
          <!-- Status Indicator (optional online status) -->
          <div class="hidden sm:flex items-center gap-1 px-2 py-1 rounded-full bg-green-50 border border-green-200">
            <span class="w-2 h-2 bg-green-500 rounded-full animate-pulse"></span>
            <span class="text-xs text-green-700 font-medium">Онлайн</span>
          </div>

          <!-- Profile Quick Access -->
          <button
            v-if="userData?.username"
            class="flex items-center justify-center w-9 h-9 rounded-full bg-gradient-to-br from-blue-500 to-blue-600 text-white text-xs font-bold hover:shadow-md transition-shadow active:scale-95"
            :title="userData.first_name"
            aria-label="Профиль"
          >
            {{ getUserInitials(userData.first_name) }}
          </button>

          <!-- Settings Icon (compact) -->
          <button
            class="flex items-center justify-center w-9 h-9 rounded-lg text-gray-600 hover:bg-gray-100 transition-colors active:scale-95"
            aria-label="Настройки"
          >
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none">
              <circle cx="12" cy="12" r="3" stroke="currentColor" stroke-width="2"/>
              <path d="M12 1V3M12 21V23M4.22 4.22L5.64 5.64M18.36 18.36L19.78 19.78M1 12H3M21 12H23M4.22 19.78L5.64 18.36M19.78 4.22L18.36 5.64" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
            </svg>
          </button>
        </div>
      </div>
    </div>
  </header>
</template>

<script setup lang="ts">
interface Props {
  userData?: {
    first_name?: string
    id?: string | number
    username?: string
  }
}

defineProps<Props>()

const getUserInitials = (name?: string): string => {
  if (!name) return '?'
  return name
    .split(' ')
    .map(word => word[0])
    .join('')
    .toUpperCase()
    .slice(0, 2)
}
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
