<template>
  <div class="provider-profile-section">
    <div class="bg-slate-800 border border-slate-700 rounded-xl p-6 space-y-6">
      <!-- Profile Header -->
      <div class="flex items-start justify-between pb-4 border-b border-slate-700">
        <div>
          <h3 class="text-2xl font-bold text-white">{{ providerInfo?.name ?? 'Профиль' }}</h3>
          <p class="text-gray-400 mt-1">
            🌟 {{ ((providerInfo?.rating as number) ?? 0).toFixed(1) }} рейтинг · {{ (providerInfo?.reviews as number) ?? 0 }} отзывов
          </p>
        </div>
        <button
          @click="editProfile"
          class="bg-blue-600 hover:bg-blue-500 text-white font-semibold px-4 py-2 rounded-lg transition active:scale-95 flex items-center gap-2"
        >
          ✍️ Отредактировать
        </button>
      </div>

      <!-- Bio -->
      <div>
        <label class="block text-sm font-semibold text-gray-300 mb-2">📝 О себе</label>
        <p class="text-gray-400 leading-relaxed">
          {{ providerInfo?.bio ?? 'Ни с чем еще не направялось. Напишите детально о себе!' }}
        </p>
      </div>

      <!-- Location -->
      <div>
        <label class="block text-sm font-semibold text-gray-300 mb-2">📍 Местонахождение</label>
        <p class="text-gray-400">
          {{ providerInfo?.location ?? 'Не указано' }}
        </p>
      </div>

      <!-- Specializations -->
      <div>
        <label class="block text-sm font-semibold text-gray-300 mb-3">🌟 Специализация</label>
        <div class="flex flex-wrap gap-2">
          <span
            v-if="(providerInfo?.specializations as string[])?.length"
            v-for="spec in (providerInfo?.specializations as string[])"
            :key="spec"
            class="bg-blue-900 text-blue-300 px-3 py-1 rounded-full text-sm font-medium"
          >
            {{ spec }}
          </span>
          <span v-else class="text-gray-400 text-sm">Не указано</span>
        </div>
      </div>

      <!-- Experience -->
      <div>
        <label class="block text-sm font-semibold text-gray-300 mb-2">🎤 Основной эксперимент</label>
        <p class="text-gray-400">
          {{ providerInfo?.experience ?? 'Не указано' }}
        </p>
      </div>

      <!-- Contact Info -->
      <div class="border-t border-slate-700 pt-4 space-y-3">
        <label class="block text-sm font-semibold text-gray-300">📞 Контактные данные</label>
        <div>
          <p class="text-xs text-gray-500 mb-1">Email</p>
          <p class="text-gray-300 font-mono text-sm">
            {{ providerInfo?.email ?? 'Не указано' }}
          </p>
        </div>
        <div>
          <p class="text-xs text-gray-500 mb-1">Телефон</p>
          <p class="text-gray-300 font-mono text-sm">
            {{ providerInfo?.phone ?? 'Не указано' }}
          </p>
        </div>
      </div>

      <!-- Stats -->
      <div class="grid grid-cols-3 gap-3 border-t border-slate-700 pt-4">
        <div class="text-center">
          <p class="text-2xl font-bold text-blue-400">
            {{ (providerInfo?.completedOrders as number) ?? 0 }}
          </p>
          <p class="text-xs text-gray-400 mt-1">Заказов</p>
        </div>
        <div class="text-center">
          <p class="text-2xl font-bold text-yellow-400">
            {{ ((providerInfo?.rating as number) ?? 0).toFixed(1) }}
          </p>
          <p class="text-xs text-gray-400 mt-1">Рейтинг</p>
        </div>
        <div class="text-center">
          <p class="text-2xl font-bold text-green-400">
            {{ (providerInfo?.reviews as number) ?? 0 }}
          </p>
          <p class="text-xs text-gray-400 mt-1">Отзывов</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
interface ProviderInfo {
  id?: string | number
  name?: string
  bio?: string
  location?: string
  experience?: string
  specializations?: string[]
  email?: string
  phone?: string
  rating?: number
  reviews?: number
  completedOrders?: number
  [key: string]: any
}

defineProps<{
  providerInfo?: ProviderInfo | null
}>()

const emit = defineEmits<{
  edit: []
}>()

const editProfile = () => {
  emit('edit')
}
</script>
