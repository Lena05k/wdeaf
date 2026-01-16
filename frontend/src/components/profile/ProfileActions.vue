<template>
  <div class="space-y-2 mt-6">
    <p class="text-sm font-semibold text-gray-400 px-2">Действия</p>

    <!-- Become Provider Button -->
    <button
        v-if="!isProvider"
        @click="emit('open-become-provider')"
        class="w-full bg-gradient-to-r from-blue-600 to-blue-500 hover:from-blue-500 hover:to-blue-400 text-white font-semibold py-3 rounded-lg transition flex items-center justify-center gap-2"
    >
      📝 Стать исполнителем
    </button>

    <!-- Provider Dashboard Button -->
    <button
        v-else
        @click="emit('open-provider-dashboard')"
        class="w-full bg-gradient-to-r from-green-600 to-green-500 hover:from-green-500 hover:to-green-400 text-white font-semibold py-3 rounded-lg transition flex items-center justify-center gap-2"
    >
      📋 Мои услуги ({{ servicesCount }})
    </button>

    <!-- Settings Button -->
    <button
        @click="emit('open-settings')"
        class="w-full bg-slate-800 hover:bg-slate-700 border border-blue-900 text-white font-semibold py-3 rounded-lg transition flex items-center justify-center gap-2"
    >
      ⚙️ Настройки
    </button>
  </div>
</template>

<script setup lang="ts">
interface Props {
  isProvider: boolean
  servicesCount: number
}

defineProps<Props>()

const emit = defineEmits<{
  'open-become-provider': []
  'open-provider-dashboard': []
  'open-settings': []
}>()
</script>

<style scoped></style>
