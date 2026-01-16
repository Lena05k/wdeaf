<template>
  <div>
    <h3 class="text-lg font-semibold text-blue-400 mb-4">Проверка</h3>

    <div class="bg-blue-900/20 border border-blue-900 rounded-lg p-4 space-y-3">
      <div class="flex items-start gap-2">
        <span class="text-green-400 font-bold">✓</span>
        <div class="text-sm">
          <p class="font-semibold">{{ formData.serviceName }}</p>
          <p class="text-gray-400">{{ formData.category }}</p>
        </div>
      </div>

      <div class="flex items-start gap-2">
        <span class="text-green-400 font-bold">✓</span>
        <div class="text-sm">
          <p class="font-semibold">{{ formData.price }}₽ за услугу</p>
          <p class="text-gray-400">{{ formData.images.length }} фотографий</p>
        </div>
      </div>

      <div class="flex items-start gap-2">
        <span class="text-green-400 font-bold">✓</span>
        <div class="text-sm">
          <p class="font-semibold">{{ formData.timezone }}</p>
          <p class="text-gray-400">Данные готовы к отправке</p>
        </div>
      </div>
    </div>

    <p class="text-xs text-gray-400 mt-4">
      После отправки ваш профиль исполнителя будет создан и опубликован. Клиенты смогут найти вашу услугу в каталоге.
    </p>
  </div>
</template>

<script setup lang="ts">
import type { ProviderFormData } from '@/components/modals/BecomeProviderModal.vue'

interface Props {
  formData: ProviderFormData
}

defineProps<Props>()
</script>

<style scoped></style>
