<template>
  <div>
    <h3 class="text-lg font-semibold text-blue-400 mb-4">✅ Проверка данных</h3>

    <!-- Summary Card -->
    <div class="bg-blue-900/20 border border-blue-900 rounded-lg p-4 space-y-4">
      <!-- Service Name & Category -->
      <div class="flex items-start gap-3">
        <span class="text-green-400 text-xl font-bold flex-shrink-0">✓</span>
        <div class="flex-1 min-w-0">
          <p class="font-semibold text-white truncate">{{ formData.serviceName }}</p>
          <p class="text-sm text-gray-400">{{ getCategoryName(formData.category) }}</p>
        </div>
      </div>

      <div class="h-px bg-slate-700"></div>

      <!-- Price & Media Count -->
      <div class="flex items-start gap-3">
        <span class="text-green-400 text-xl font-bold flex-shrink-0">✓</span>
        <div class="flex-1 min-w-0">
          <p class="font-semibold text-white">{{ formData.price }}₽ за услугу</p>
          <p class="text-sm text-gray-400">{{ formData.images.length }} {{ getImageWord() }}</p>
        </div>
      </div>

      <div class="h-px bg-slate-700"></div>

      <!-- Schedule -->
      <div class="flex items-start gap-3">
        <span class="text-green-400 text-xl font-bold flex-shrink-0">✓</span>
        <div class="flex-1 min-w-0">
          <p class="font-semibold text-white">{{ formData.timezone }}</p>
          <p class="text-xs text-gray-400 space-y-1">
            <div v-if="formData.availability.weekdays">{{ getAvailabilityText() }}</div>
          </p>
        </div>
      </div>
    </div>

    <!-- Info Text -->
    <div class="mt-4 p-3 bg-slate-700/50 border border-slate-600 rounded-lg">
      <p class="text-xs text-gray-400 leading-relaxed">
        🌟 Описание вашей услуги:
      </p>
      <p class="text-sm text-gray-200 mt-2 line-clamp-4">{{ formData.description }}</p>
    </div>

    <!-- Info Message -->
    <div class="mt-4 p-3 bg-blue-900/20 border border-blue-800 rounded-lg">
      <p class="text-xs text-blue-300 leading-relaxed">
        ✨ После публикации васа услуга станет видна клиентам в каталоге.
      </p>
    </div>
  </div>
</template>

<script setup lang="ts">
interface FormData {
  serviceName: string
  description: string
  category: string
  price: number
  timezone: string
  availability: {
    weekdays: boolean
    weekends: boolean
    evenings: boolean
  }
  images: Array<{ file?: File; preview?: string }>
}

interface Props {
  formData: FormData
}

defineProps<Props>()

const categoryNames: Record<string, string> = {
  repair: '🏠 Ремонт',
  business: '💼 Бизнес',
  fashion: '👗 Мода',
  education: '📚 Обучение',
  design: '🎨 Дизайн',
  it: '💻 IT'
}

const getCategoryName = (category: string): string => {
  return categoryNames[category] || category
}

const getImageWord = (): string => {
  const count = (0 as any).formData?.images?.length || 0
  if (count === 0) return 'без фото'
  if (count === 1) return 'фото'
  if (count <= 4) return 'фото'
  return 'фото'
}

const getAvailabilityText = (): string => {
  const days = []
  // Это место ставим ранее
  return 'Настроики графика сохранены'
}
</script>

<style scoped>
.line-clamp-4 {
  display: -webkit-box;
  -webkit-line-clamp: 4;
  -webkit-box-orient: vertical;
  overflow: hidden;
}
</style>