<template>
  <div class="fixed inset-0 bg-black/50 flex items-end z-50 animate-in" @click="$emit('close')">
    <div class="bg-slate-800 w-full rounded-t-3xl border-t border-slate-700 max-h-[90vh] overflow-y-auto" @click.stop>
      <!-- Header -->
      <div class="sticky top-0 bg-gradient-to-b from-slate-800 to-slate-900 border-b border-slate-700 p-4 flex justify-between items-center">
        <h2 class="text-xl font-bold text-white flex items-center gap-2">
          <span>📋</span> Стать исполнителем
        </h2>
        <button @click="$emit('close')" class="text-gray-400 hover:text-white text-2xl">
          ✕
        </button>
      </div>

      <!-- Progress Indicator -->
      <div class="px-4 pt-4 flex gap-2">
        <div 
          v-for="step in 2" 
          :key="step"
          :class="[
            'flex-1 h-1 rounded-full transition',
            currentStep >= step ? 'bg-blue-500' : 'bg-slate-700'
          ]"
        />
      </div>

      <!-- Content -->
      <div class="p-4 space-y-4">
        <!-- Step 1: Personal Info -->
        <div v-if="currentStep === 1" class="space-y-4">
          <h3 class="text-lg font-semibold text-blue-400">Расскажите о себе</h3>

          <div class="space-y-3">
            <div>
              <label class="block text-sm font-semibold mb-2 text-gray-300">Ваше имя</label>
              <input
                v-model="form.name"
                type="text"
                placeholder="Например: Иван Петров"
                class="w-full bg-slate-700 border border-slate-600 rounded-lg px-4 py-2 text-white placeholder-gray-500 focus:outline-none focus:border-blue-500 focus:ring-2 focus:ring-blue-500/30"
              />
              <p v-if="errors.name" class="text-xs text-red-500 mt-1">{{ errors.name }}</p>
            </div>

            <div>
              <label class="block text-sm font-semibold mb-2 text-gray-300">О себе и вашем опыте</label>
              <textarea
                v-model="form.description"
                placeholder="Расскажите о вашем опыте, навыках и специализации"
                rows="4"
                class="w-full bg-slate-700 border border-slate-600 rounded-lg px-4 py-2 text-white placeholder-gray-500 focus:outline-none focus:border-blue-500 focus:ring-2 focus:ring-blue-500/30 resize-none"
              />
              <p v-if="errors.description" class="text-xs text-red-500 mt-1">{{ errors.description }}</p>
              <p class="text-xs text-gray-500 mt-1">Мин. 20 символов</p>
            </div>

            <div>
              <label class="block text-sm font-semibold mb-3 text-gray-300">Категории работ</label>
              <div class="space-y-2 bg-slate-700/50 rounded-lg p-3 border border-slate-600 max-h-48 overflow-y-auto">
                <label
                  v-for="cat in categories"
                  :key="cat"
                  class="flex items-center gap-3 cursor-pointer p-2 rounded hover:bg-slate-600 transition"
                >
                  <input
                    :checked="form.categories.includes(cat)"
                    type="checkbox"
                    @change="toggleCategory(cat)"
                    class="w-4 h-4 accent-blue-500"
                  />
                  <span class="text-sm">{{ cat }}</span>
                </label>
              </div>
              <p v-if="errors.categories" class="text-xs text-red-500 mt-1">{{ errors.categories }}</p>
              <p class="text-xs text-gray-500 mt-1">Выберите минимум 1</p>
            </div>
          </div>
        </div>

        <!-- Step 2: Schedule -->
        <div v-if="currentStep === 2" class="space-y-4">
          <h3 class="text-lg font-semibold text-blue-400">График работы</h3>

          <div class="space-y-4">
            <div>
              <label class="block text-sm font-semibold mb-2 text-gray-300">Часовой пояс</label>
              <select
                v-model="form.timezone"
                class="w-full bg-slate-700 border border-slate-600 rounded-lg px-4 py-2 text-white focus:outline-none focus:border-blue-500"
              >
                <option value="UTC+3">UTC+3 (Москва)</option>
                <option value="UTC+4">UTC+4 (Казань)</option>
                <option value="UTC+5">UTC+5 (Екатеринбург)</option>
                <option value="UTC+8">UTC+8 (Владивосток)</option>
              </select>
            </div>

            <div>
              <label class="block text-sm font-semibold mb-3 text-gray-300">Доступность</label>
              <div class="space-y-2 bg-slate-700/50 rounded-lg p-3 border border-slate-600">
                <label class="flex items-center gap-3 cursor-pointer p-2 rounded hover:bg-slate-600 transition">
                  <input
                    v-model="form.availability.weekdays"
                    type="checkbox"
                    class="w-4 h-4 accent-green-500"
                  />
                  <span class="text-sm">Будни (Пн-Пт)</span>
                </label>
                <label class="flex items-center gap-3 cursor-pointer p-2 rounded hover:bg-slate-600 transition">
                  <input
                    v-model="form.availability.weekends"
                    type="checkbox"
                    class="w-4 h-4 accent-green-500"
                  />
                  <span class="text-sm">Выходные (Сб-Вс)</span>
                </label>
                <label class="flex items-center gap-3 cursor-pointer p-2 rounded hover:bg-slate-600 transition">
                  <input
                    v-model="form.availability.evenings"
                    type="checkbox"
                    class="w-4 h-4 accent-green-500"
                  />
                  <span class="text-sm">Вечерние часы (18:00-23:00)</span>
                </label>
              </div>
              <p v-if="errors.availability" class="text-xs text-red-500 mt-1">{{ errors.availability }}</p>
              <p class="text-xs text-gray-500 mt-1">Выберите минимум 1</p>
            </div>

            <!-- Data Processing Consent -->
            <div class="bg-blue-900/30 border border-blue-700 rounded-lg p-4 space-y-2">
              <h4 class="font-semibold text-blue-300 text-sm">✓ Обработка данных</h4>
              <label class="flex items-start gap-3 cursor-pointer">
                <input
                  v-model="form.agreeDataProcessing"
                  type="checkbox"
                  class="w-4 h-4 accent-blue-500 mt-1 flex-shrink-0"
                />
                <span class="text-xs text-gray-300">
                  Я согласен на обработку моих персональных данных в соответствии с
                  <span class="text-blue-400">Федеральным законом №152-ФЗ</span>
                  и полностью ознаком с политикой конфиденциальности
                </span>
              </label>
              <p v-if="errors.agreeDataProcessing" class="text-xs text-red-500">{{ errors.agreeDataProcessing }}</p>
            </div>
          </div>
        </div>
      </div>

      <!-- Footer -->
      <div class="sticky bottom-0 bg-gradient-to-t from-slate-800 to-slate-900 border-t border-slate-700 p-4 flex gap-2">
        <button
          v-if="currentStep > 1"
          @click="currentStep--"
          class="flex-1 bg-slate-700 hover:bg-slate-600 text-white font-semibold py-3 rounded-lg transition active:scale-95"
        >
          ← Назад
        </button>
        <button
          v-if="currentStep < 2"
          @click="currentStep++"
          :disabled="!isStep1Valid"
          :class="[
            'flex-1 font-semibold py-3 rounded-lg transition active:scale-95',
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
            'flex-1 font-semibold py-3 rounded-lg transition active:scale-95',
            isStep2Valid
              ? 'bg-green-600 hover:bg-green-500 text-white'
              : 'bg-gray-700 text-gray-400 cursor-not-allowed'
          ]"
        >
          ✓ Создать профиль
        </button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'

interface ProviderForm {
  name: string
  description: string
  categories: string[]
  timezone: string
  availability: {
    weekdays: boolean
    weekends: boolean
    evenings: boolean
  }
  agreeDataProcessing: boolean
}

const currentStep = ref(1)

const categories = [
  'Ремонт',
  'Бизнес',
  'Мода',
  'Обучение',
  'Дизайн',
  'IT',
  'Консультация',
  'Творчество'
]

const form = ref<ProviderForm>({
  name: '',
  description: '',
  categories: [],
  timezone: 'UTC+3',
  availability: {
    weekdays: true,
    weekends: false,
    evenings: true
  },
  agreeDataProcessing: false
})

const errors = ref<Record<string, string>>({})

// Validation for Step 1
const validateStep1 = (): boolean => {
  errors.value = {}

  if (!form.value.name.trim()) {
    errors.value.name = 'Имя обязательно'
  } else if (form.value.name.trim().length < 2) {
    errors.value.name = 'Имя должно быть не менее 2 символов'
  }

  if (!form.value.description.trim()) {
    errors.value.description = 'Описание обязательно'
  } else if (form.value.description.trim().length < 20) {
    errors.value.description = 'Описание должно быть минимум 20 символов'
  }

  if (form.value.categories.length === 0) {
    errors.value.categories = 'Выберите хотя бы одну категорию'
  }

  return Object.keys(errors.value).length === 0
}

// Validation for Step 2
const validateStep2 = (): boolean => {
  errors.value = {}

  const hasAvailability = Object.values(form.value.availability).some(v => v)
  if (!hasAvailability) {
    errors.value.availability = 'Выберите хотя бы один день/время'
  }

  if (!form.value.agreeDataProcessing) {
    errors.value.agreeDataProcessing = 'Необходимо согласие на обработку данных'
  }

  return Object.keys(errors.value).length === 0
}

const isStep1Valid = computed(() => {
  return (
    form.value.name.trim().length > 2 &&
    form.value.description.trim().length >= 20 &&
    form.value.categories.length > 0
  )
})

const isStep2Valid = computed(() => {
  const hasAvailability = Object.values(form.value.availability).some(v => v)
  return hasAvailability && form.value.agreeDataProcessing
})

const toggleCategory = (category: string) => {
  const index = form.value.categories.indexOf(category)
  if (index === -1) {
    form.value.categories.push(category)
  } else {
    form.value.categories.splice(index, 1)
  }
}

const handleSubmit = () => {
  // Validate step 2
  if (!validateStep2()) {
    return
  }

  // Emit form data to parent
  emit('submit', form.value)
}

defineEmits<{
  submit: [data: ProviderForm]
  close: []
}>()
</script>

<style scoped>
@keyframes fadeIn {
  from {
    opacity: 0;
  }
  to {
    opacity: 1;
  }
}

.animate-in {
  animation: fadeIn 0.3s ease-out;
}
</style>