<template>
  <div v-if="providerInfo" class="space-y-4 pb-4">
    <!-- Profile Card -->
    <div class="bg-gradient-to-br from-blue-900/30 to-blue-800/20 border border-blue-700 rounded-xl p-4 space-y-4">
      <!-- Header with Edit -->
      <div class="flex items-center justify-between">
        <h3 class="text-lg font-bold text-blue-300 flex items-center gap-2">
          <span>👤</span> Профиль исполнителя
        </h3>
        <button
          @click="$emit('edit')"
          class="text-blue-400 hover:text-blue-300 text-xl transition"
        >
          ✍️
        </button>
      </div>

      <!-- Info Grid -->
      <div class="space-y-3">
        <!-- Name -->
        <div>
          <p class="text-xs text-gray-400 mb-1">ИМЕ</p>
          <p class="font-semibold text-white">{{ providerInfo.serviceName }}</p>
        </div>

        <!-- Description -->
        <div>
          <p class="text-xs text-gray-400 mb-1">О сЕБЕ</p>
          <p class="text-sm text-gray-300 line-clamp-3">{{ providerInfo.description }}</p>
        </div>

        <!-- Categories -->
        <div>
          <p class="text-xs text-gray-400 mb-2">КАТЕГОРИИ</p>
          <div class="flex flex-wrap gap-2">
            <span
              v-for="cat in providerInfo.categories"
              :key="cat"
              class="bg-blue-600 text-white px-3 py-1 rounded-full text-xs font-semibold"
            >
              {{ cat }}
            </span>
          </div>
        </div>

        <!-- Timezone -->
        <div>
          <p class="text-xs text-gray-400 mb-1">ЧАСОВОЙ ПОЯС</p>
          <p class="font-semibold text-white">{{ providerInfo.timezone }}</p>
        </div>

        <!-- Availability -->
        <div>
          <p class="text-xs text-gray-400 mb-2">ДОСТУПНОСТЬ</p>
          <div class="space-y-1">
            <p v-if="providerInfo.availability?.weekdays" class="text-sm text-green-400 flex items-center gap-2">
              <span>✓</span> Будни (Пн-Пт)
            </p>
            <p v-if="providerInfo.availability?.weekends" class="text-sm text-green-400 flex items-center gap-2">
              <span>✓</span> Выходные (Сб-Вс)
            </p>
            <p v-if="providerInfo.availability?.evenings" class="text-sm text-green-400 flex items-center gap-2">
              <span>✓</span> Вечерние (18:00-23:00)
            </p>
          </div>
        </div>
      </div>
    </div>

    <!-- Stats -->
    <div class="grid grid-cols-2 gap-3">
      <div class="bg-slate-800 border border-slate-700 rounded-xl p-3 text-center">
        <p class="text-2xl font-bold text-yellow-400">4.8</p>
        <p class="text-xs text-gray-400 mt-1">⭐ Рейтинг</p>
      </div>
      <div class="bg-slate-800 border border-slate-700 rounded-xl p-3 text-center">
        <p class="text-2xl font-bold text-blue-400">24</p>
        <p class="text-xs text-gray-400 mt-1">💬 Отзывы</p>
      </div>
    </div>
  </div>

  <!-- Empty State -->
  <div v-else class="text-center py-12 text-gray-400">
    <p class="text-3xl mb-2👤</p>
    <p class="text-sm">Профиль не загружен</p>
  </div>
</template>

<script setup lang="ts">
interface ProviderInfo {
  serviceName?: string
  description?: string
  categories?: string[]
  timezone?: string
  availability?: {
    weekdays: boolean
    weekends: boolean
    evenings: boolean
  }
}

defineProps<{
  providerInfo?: ProviderInfo
}>()

defineEmits<{
  edit: []
}>()
</script>
