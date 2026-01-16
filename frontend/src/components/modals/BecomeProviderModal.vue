<template>
  <div v-if="isOpen" class="modal-overlay fixed inset-0 bg-black/50 flex items-end z-50">
    <div class="modal-content bg-slate-800 w-full max-w-md rounded-t-2xl border-t border-blue-900 max-h-[90vh] overflow-y-auto">
      <!-- Header -->
      <div class="sticky top-0 bg-slate-800 border-b border-blue-900 p-3 flex justify-between items-center">
        <h2 class="text-lg font-bold">📝 Новая услуга</h2>
        <button
            @click="emit('close')"
            class="text-gray-400 hover:text-white text-2xl"
        >
          ✕
        </button>
      </div>

      <!-- Progress Bar -->
      <div class="px-4 pt-3 pb-2 flex gap-2">
        <div
            v-for="step in 2"
            :key="step"
            :class="[
              'flex-1 h-1 rounded-full transition-all',
              currentStep >= step ? 'bg-blue-500' : 'bg-slate-700'
            ]"
        />
      </div>

      <!-- Content -->
      <div class="p-4 space-y-4">
        <!-- Step 1: Basic Info -->
        <div v-if="currentStep === 1" class="space-y-3 animate-fadeIn">
          <div>
            <label class="block text-xs font-semibold text-gray-400 mb-1">НАЗВАНИЕ УСЛУГИ</label>
            <input
                v-model="formData.serviceName"
                type="text"
                placeholder=""
                class="w-full bg-slate-700 border border-blue-900 rounded-lg px-3 py-2 text-sm text-white placeholder-gray-500 focus:outline-none focus:border-blue-500"
            />
          </div>

          <div>
            <label class="block text-xs font-semibold text-gray-400 mb-1">ОПИСАНИЕ</label>
            <textarea
                v-model="formData.description"
                placeholder="Что вы делаете?"
                rows="3"
                class="w-full bg-slate-700 border border-blue-900 rounded-lg px-3 py-2 text-sm text-white placeholder-gray-500 focus:outline-none focus:border-blue-500 resize-none"
            />
          </div>

          <div class="grid grid-cols-2 gap-2">
            <div>
              <label class="block text-xs font-semibold text-gray-400 mb-1">КАТЕГОРИЯ</label>
              <select
                  v-model="formData.category"
                  class="w-full bg-slate-700 border border-blue-900 rounded-lg px-3 py-2 text-sm text-white focus:outline-none focus:border-blue-500"
              >
                <option value="" disabled>Выберите</option>
                <option value="repair">🏠 Ремонт</option>
                <option value="business">💼 Бизнес</option>
                <option value="fashion">👗 Мода</option>
                <option value="education">📚 Обучение</option>
                <option value="design">🎨 Дизайн</option>
                <option value="it">💻 IT</option>
              </select>
            </div>
            <div>
              <label class="block text-xs font-semibold text-gray-400 mb-1">ЦЕНА (₽)</label>
              <input
                  v-model.number="formData.price"
                  type="number"
                  placeholder="500"
                  class="w-full bg-slate-700 border border-blue-900 rounded-lg px-3 py-2 text-sm text-white placeholder-gray-500 focus:outline-none focus:border-blue-500"
              />
            </div>
          </div>
        </div>

        <!-- Step 2: Photos & Schedule -->
        <div v-if="currentStep === 2" class="space-y-4 animate-fadeIn">
          <!-- Photos Section (Optional) -->
          <div>
            <div class="flex items-center gap-2 mb-2">
              <span class="text-sm font-semibold text-blue-400">📎 Фото</span>
              <span class="text-xs text-gray-500">(опционально)</span>
            </div>

            <!-- Current Images -->
            <div v-if="formData.images && formData.images.length > 0" class="space-y-2 mb-2">
              <div
                  v-for="(image, index) in formData.images"
                  :key="index"
                  class="relative bg-slate-700 border border-blue-900 rounded-lg overflow-hidden group"
              >
                <img
                    :src="image.preview || image"
                    :alt="'Image ' + (index + 1)"
                    class="w-full h-20 object-cover"
                />
                <button
                    @click="removeImage(index)"
                    class="absolute top-1 right-1 bg-red-600 text-white rounded-full p-1 opacity-0 group-hover:opacity-100 hover:bg-red-700 transition"
                >
                  ✕
                </button>
              </div>
            </div>

            <!-- Add Photos Button -->
            <label v-if="!formData.images || formData.images.length < 5" class="flex items-center justify-center gap-2 bg-slate-700 border border-dashed border-slate-600 rounded-lg py-3 cursor-pointer hover:border-blue-500 hover:bg-slate-700/80 transition text-sm font-medium text-gray-400 hover:text-blue-400">
              <span class="text-lg">📎</span>
              <span>Добавить фото</span>
              <input
                  type="file"
                  accept="image/*"
                  multiple
                  class="hidden"
                  @change="handleAddImage"
              />
            </label>
          </div>

          <!-- Schedule & Timezone -->
          <div>
            <h3 class="text-sm font-semibold text-blue-400 mb-2">⏰ Время работы</h3>

            <!-- Timezone -->
            <div class="mb-3">
              <label class="block text-xs font-semibold text-gray-400 mb-1">ЧАСОВОЙ ПОЯС</label>
              <select
                  v-model="formData.timezone"
                  class="w-full bg-slate-700 border border-blue-900 rounded-lg px-3 py-2 text-sm text-white focus:outline-none focus:border-blue-500"
              >
                <option value="UTC+3">UTC+3 (Москва)</option>
                <option value="UTC+4">UTC+4 (Казань)</option>
                <option value="UTC+5">UTC+5 (Екатеринбург)</option>
                <option value="UTC+8">UTC+8 (Владивосток)</option>
              </select>
            </div>

            <!-- Availability Checkboxes -->
            <div class="space-y-2 bg-slate-700/50 rounded-lg p-3 border border-slate-700">
              <label class="flex items-center gap-2 cursor-pointer hover:text-blue-400 transition">
                <input
                    v-model="formData.availability.weekdays"
                    type="checkbox"
                    class="w-4 h-4 cursor-pointer accent-blue-500"
                />
                <span class="text-sm">Будни (Пн-Пт)</span>
              </label>
              <label class="flex items-center gap-2 cursor-pointer hover:text-blue-400 transition">
                <input
                    v-model="formData.availability.weekends"
                    type="checkbox"
                    class="w-4 h-4 cursor-pointer accent-blue-500"
                />
                <span class="text-sm">Выходные (Сб-Вс)</span>
              </label>
              <label class="flex items-center gap-2 cursor-pointer hover:text-blue-400 transition">
                <input
                    v-model="formData.availability.evenings"
                    type="checkbox"
                    class="w-4 h-4 cursor-pointer accent-blue-500"
                />
                <span class="text-sm">Вечера (18:00-23:00)</span>
              </label>
            </div>
          </div>
        </div>
      </div>

      <!-- Footer Buttons -->
      <div class="sticky bottom-0 bg-slate-800 border-t border-blue-900 p-3 flex gap-2">
        <button
            v-if="currentStep > 1"
            @click="currentStep--"
            class="flex-1 bg-slate-700 hover:bg-slate-600 text-white font-semibold py-2 text-sm rounded-lg transition"
        >
          ← Назад
        </button>
        <button
            v-if="currentStep < 2"
            @click="handleNextStep"
            :disabled="!isStep1Valid"
            :class="[
              'flex-1 font-semibold py-2 text-sm rounded-lg transition',
              isStep1Valid
                ? 'bg-blue-600 hover:bg-blue-500 text-white'
                : 'bg-gray-700 text-gray-400 cursor-not-allowed'
            ]"
        >
          Далее →
        </button>
        <button
            v-else
            @click="handleSubmit"
            :disabled="!isStep2Valid"
            :class="[
              'flex-1 font-semibold py-2 text-sm rounded-lg transition',
              isStep2Valid
                ? 'bg-green-600 hover:bg-green-500 text-white'
                : 'bg-gray-700 text-gray-400 cursor-not-allowed'
            ]"
        >
          ✅ Готово
        </button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed, ref } from 'vue'

export interface ProviderFormData {
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
  isOpen: boolean
}

defineProps<Props>()

const emit = defineEmits<{
  'close': []
  'submit': [data: ProviderFormData]
}>()

const currentStep = ref(1)
const formData = ref<ProviderFormData>({
  serviceName: '',
  description: '',
  category: '',
  price: 0,
  timezone: 'UTC+3',
  availability: {
    weekdays: true,
    weekends: false,
    evenings: true
  },
  images: []
})

// ЩАГ 1: Основная информация
const isStep1Valid = computed(() => {
  return (
    formData.value.serviceName.trim().length > 0 &&
    formData.value.description.trim().length > 5 &&
    formData.value.category.length > 0 &&
    formData.value.price > 0
  )
})

// ЩАГ 2: Фото и график (все опционально)
const isStep2Valid = computed(() => {
  return Object.values(formData.value.availability).some(v => v)
})

const handleNextStep = () => {
  if (isStep1Valid.value) {
    currentStep.value = 2
  }
}

const handleAddImage = (event: Event) => {
  const target = event.target as HTMLInputElement
  const files = target.files
  if (!files) return

  Array.from(files).forEach(file => {
    if (file.size > 5 * 1024 * 1024) {
      alert('Файл слишком большой (макс 5 МБ)')
      return
    }

    const reader = new FileReader()
    reader.onload = (e) => {
      if (formData.value.images && formData.value.images.length < 5 && e.target?.result) {
        formData.value.images.push({
          file,
          preview: e.target.result as string
        })
      }
    }
    reader.readAsDataURL(file)
  })
  target.value = ''
}

const removeImage = (index: number) => {
  if (formData.value.images) {
    formData.value.images.splice(index, 1)
  }
}

const handleSubmit = () => {
  if (isStep2Valid.value) {
    emit('submit', formData.value)
    // Reset form
    currentStep.value = 1
    formData.value = {
      serviceName: '',
      description: '',
      category: '',
      price: 0,
      timezone: 'UTC+3',
      availability: {
        weekdays: true,
        weekends: false,
        evenings: true
      },
      images: []
    }
  }
}
</script>

<style scoped>
.modal-overlay {
  animation: fadeIn 0.3s ease-out;
}

.modal-content {
  animation: slideUp 0.3s ease-out;
}

.animate-fadeIn {
  animation: fadeIn 0.3s ease-out;
}

@keyframes fadeIn {
  from {
    opacity: 0;
  }
  to {
    opacity: 1;
  }
}

@keyframes slideUp {
  from {
    transform: translateY(100%);
  }
  to {
    transform: translateY(0);
  }
}
</style>
