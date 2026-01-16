<template>
  <div>
    <h3 class="text-lg font-semibold text-blue-400 mb-4">📝 Основная информация</h3>

    <div class="space-y-3">
      <div>
        <label class="block text-xs font-semibold text-gray-400 mb-1">Название услуги</label>
        <input
            :value="formData.serviceName"
            @input="updateField('serviceName', ($event.target as HTMLInputElement).value)"
            type="text"
            placeholder="Например: Уроки английского онлайн"
            class="w-full bg-slate-700 border border-blue-900 rounded-lg px-4 py-2 text-white placeholder-gray-500 focus:outline-none focus:border-blue-500"
        />
      </div>

      <div>
        <label class="block text-xs font-semibold text-gray-400 mb-1">Описание услуги</label>
        <textarea
            :value="formData.description"
            @input="updateField('description', ($event.target as HTMLTextAreaElement).value)"
            placeholder="Подробное описание того, что вы предлагаете"
            rows="3"
            class="w-full bg-slate-700 border border-blue-900 rounded-lg px-4 py-2 text-white placeholder-gray-500 focus:outline-none focus:border-blue-500 resize-none"
        />
      </div>

      <div class="grid grid-cols-2 gap-2">
        <div>
          <label class="block text-xs font-semibold text-gray-400 mb-1">Категория</label>
          <select
              :value="formData.category"
              @change="updateField('category', ($event.target as HTMLSelectElement).value)"
              class="w-full bg-slate-700 border border-blue-900 rounded-lg px-4 py-2 text-white focus:outline-none focus:border-blue-500"
          >
            <option value="">Выберите</option>
            <option value="repair">🏠 Ремонт</option>
            <option value="business">💼 Бизнес</option>
            <option value="fashion">👗 Мода</option>
            <option value="education">📚 Обучение</option>
            <option value="design">🎨 Дизайн</option>
            <option value="it">💻 IT</option>
          </select>
        </div>
        <div>
          <label class="block text-xs font-semibold text-gray-400 mb-1">Цена (₽)</label>
          <input
              :value="formData.price"
              @input="updateField('price', Number(($event.target as HTMLInputElement).value))"
              type="number"
              placeholder="500"
              class="w-full bg-slate-700 border border-blue-900 rounded-lg px-4 py-2 text-white placeholder-gray-500 focus:outline-none focus:border-blue-500"
          />
        </div>
      </div>

      <!-- Schedule Section - Moved here to reduce steps -->
      <div class="mt-4 pt-4 border-t border-slate-700">
        <h4 class="text-sm font-semibold text-blue-400 mb-3">⏰ Когда вы работаете?</h4>
        
        <div class="mb-3">
          <label class="block text-xs font-semibold text-gray-400 mb-1">Часовой пояс</label>
          <select
              :value="formData.timezone"
              @change="updateField('timezone', ($event.target as HTMLSelectElement).value)"
              class="w-full bg-slate-700 border border-blue-900 rounded-lg px-4 py-2 text-sm text-white focus:outline-none focus:border-blue-500"
          >
            <option value="UTC+3">UTC+3 (Москва)</option>
            <option value="UTC+4">UTC+4 (Казань)</option>
            <option value="UTC+5">UTC+5 (Екатеринбург)</option>
            <option value="UTC+8">UTC+8 (Владивосток)</option>
          </select>
        </div>

        <div class="space-y-2 bg-slate-700/50 rounded-lg p-3 border border-slate-700">
          <label class="flex items-center gap-2 cursor-pointer">
            <input
                :checked="formData.availability.weekdays"
                @change="updateAvailability('weekdays', ($event.target as HTMLInputElement).checked)"
                type="checkbox"
                class="w-4 h-4 cursor-pointer accent-blue-500"
            />
            <span class="text-sm">Будни (Пн-Пт)</span>
          </label>
          <label class="flex items-center gap-2 cursor-pointer">
            <input
                :checked="formData.availability.weekends"
                @change="updateAvailability('weekends', ($event.target as HTMLInputElement).checked)"
                type="checkbox"
                class="w-4 h-4 cursor-pointer accent-blue-500"
            />
            <span class="text-sm">Выходные (Сб-Вс)</span>
          </label>
          <label class="flex items-center gap-2 cursor-pointer">
            <input
                :checked="formData.availability.evenings"
                @change="updateAvailability('evenings', ($event.target as HTMLInputElement).checked)"
                type="checkbox"
                class="w-4 h-4 cursor-pointer accent-blue-500"
            />
            <span class="text-sm">Вечера (18:00-23:00)</span>
          </label>
        </div>
      </div>
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

const props = defineProps<Props>()

const emit = defineEmits<{
  'update:formData': [data: FormData]
}>()

const updateField = (field: keyof FormData, value: any) => {
  emit('update:formData', { ...props.formData, [field]: value })
}

const updateAvailability = (field: keyof FormData['availability'], value: boolean) => {
  emit('update:formData', {
    ...props.formData,
    availability: { ...props.formData.availability, [field]: value }
  })
}
</script>

<style scoped></style>