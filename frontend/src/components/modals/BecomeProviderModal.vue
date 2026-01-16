<template>
  <div class="modal-overlay fixed inset-0 bg-black/50 flex items-end z-50 animate-fade-in">
    <div class="modal-content bg-slate-800 w-full max-w-md rounded-t-2xl border-t border-blue-900 max-h-[90vh] overflow-y-auto animate-slide-up">
      <!-- Header -->
      <div class="sticky top-0 bg-slate-800 border-b border-blue-900 p-4 flex justify-between items-center">
        <h2 class="text-xl font-bold">📝 Стать исполнителем</h2>
        <button
          @click="$emit('close')"
          class="text-gray-400 hover:text-white text-2xl"
        >
          ✕
        </button>
      </div>

      <!-- Content -->
      <div class="p-4 space-y-4">
        <!-- Step Indicator -->
        <div class="flex gap-2">
          <div
            v-for="step in steps"
            :key="step"
            :class="[
              'flex-1 h-1 rounded-full transition',
              currentStep >= step ? 'bg-blue-500' : 'bg-slate-700'
            ]"
          />
        </div>

        <!-- Step 1: Basic Info -->
        <div v-if="currentStep === 1" class="space-y-4">
          <h3 class="text-lg font-semibold text-blue-400">Основная информация</h3>
          
          <div>
            <label class="block text-sm font-semibold mb-2">Название услуги</label>
            <input
              v-model="formData.serviceName"
              type="text"
              placeholder="Например: Уроки английского онлайн"
              class="w-full bg-slate-700 border border-blue-900 rounded-lg px-4 py-2 text-white placeholder-gray-500 focus:outline-none focus:border-blue-500"
            />
          </div>

          <div>
            <label class="block text-sm font-semibold mb-2">Описание услуги</label>
            <textarea
              v-model="formData.description"
              placeholder="Подробное описание того, что вы предлагаете"
              rows="4"
              class="w-full bg-slate-700 border border-blue-900 rounded-lg px-4 py-2 text-white placeholder-gray-500 focus:outline-none focus:border-blue-500 resize-none"
            />
          </div>

          <div>
            <label class="block text-sm font-semibold mb-2">Категория</label>
            <select
              v-model="formData.category"
              class="w-full bg-slate-700 border border-blue-900 rounded-lg px-4 py-2 text-white focus:outline-none focus:border-blue-500"
            >
              <option value="">Выберите категорию</option>
              <option value="languages">🗣️ Языки</option>
              <option value="music">🎵 Музыка</option>
              <option value="design">🎨 Дизайн</option>
              <option value="programming">💻 Программирование</option>
              <option value="fitness">💪 Фитнес</option>
              <option value="other">📦 Другое</option>
            </select>
          </div>

          <div>
            <label class="block text-sm font-semibold mb-2">Цена за услугу (₽)</label>
            <input
              v-model="formData.price"
              type="number"
              placeholder="500"
              class="w-full bg-slate-700 border border-blue-900 rounded-lg px-4 py-2 text-white placeholder-gray-500 focus:outline-none focus:border-blue-500"
            />
          </div>
        </div>

        <!-- Step 2: Images -->
        <div v-if="currentStep === 2" class="space-y-4">
          <h3 class="text-lg font-semibold text-blue-400">Фотографии услуги</h3>
          <p class="text-sm text-gray-400">Добавьте до 5 фотографий (макс 5 МБ каждая)</p>

          <!-- Image Upload -->
          <div class="space-y-2">
            <div
              v-for="(image, index) in formData.images"
              :key="index"
              class="relative bg-slate-700 border border-blue-900 rounded-lg overflow-hidden"
            >
              <img
                :src="image.preview"
                :alt="'Service image ' + (index + 1)"
                class="w-full h-32 object-cover"
              />
              <button
                @click="removeImage(index)"
                class="absolute top-1 right-1 bg-red-600 text-white rounded-full p-1 hover:bg-red-700"
              >
                ✕
              </button>
            </div>

            <!-- Add Image Button -->
            <div v-if="formData.images.length < 5">
              <label class="flex items-center justify-center gap-2 bg-slate-700 border border-dashed border-blue-900 rounded-lg py-6 cursor-pointer hover:border-blue-500 transition">
                <span class="text-2xl">📸</span>
                <span class="text-sm font-semibold">Добавить фото</span>
                <input
                  type="file"
                  accept="image/*"
                  class="hidden"
                  @change="handleImageUpload"
                />
              </label>
            </div>
          </div>

          <div v-if="formData.images.length === 0" class="text-center py-6 text-gray-400">
            <p class="text-4xl mb-2">📷</p>
            <p>Добавьте минимум одну фотографию</p>
          </div>
        </div>

        <!-- Step 3: Schedule -->
        <div v-if="currentStep === 3" class="space-y-4">
          <h3 class="text-lg font-semibold text-blue-400">График работы</h3>

          <div>
            <label class="block text-sm font-semibold mb-2">Часовой пояс</label>
            <select
              v-model="formData.timezone"
              class="w-full bg-slate-700 border border-blue-900 rounded-lg px-4 py-2 text-white focus:outline-none focus:border-blue-500"
            >
              <option value="UTC+3">UTC+3 (Москва)</option>
              <option value="UTC+4">UTC+4 (Казань)</option>
              <option value="UTC+5">UTC+5 (Екатеринбург)</option>
              <option value="UTC+8">UTC+8 (Владивосток)</option>
            </select>
          </div>

          <div>
            <label class="block text-sm font-semibold mb-2">Доступность</label>
            <div class="space-y-2">
              <label class="flex items-center gap-2 cursor-pointer">
                <input
                  v-model="formData.availability.weekdays"
                  type="checkbox"
                  class="w-4 h-4"
                />
                <span class="text-sm">Будни (Пн-Пт)</span>
              </label>
              <label class="flex items-center gap-2 cursor-pointer">
                <input
                  v-model="formData.availability.weekends"
                  type="checkbox"
                  class="w-4 h-4"
                />
                <span class="text-sm">Выходные (Сб-Вс)</span>
              </label>
              <label class="flex items-center gap-2 cursor-pointer">
                <input
                  v-model="formData.availability.evenings"
                  type="checkbox"
                  class="w-4 h-4"
                />
                <span class="text-sm">Вечерние часы (18:00-23:00)</span>
              </label>
            </div>
          </div>

          <div>
            <label class="block text-sm font-semibold mb-2">Макс. одновременных заказов</label>
            <input
              v-model="formData.maxConcurrentOrders"
              type="number"
              placeholder="5"
              class="w-full bg-slate-700 border border-blue-900 rounded-lg px-4 py-2 text-white placeholder-gray-500 focus:outline-none focus:border-blue-500"
            />
          </div>
        </div>

        <!-- Step 4: Verification -->
        <div v-if="currentStep === 4" class="space-y-4">
          <h3 class="text-lg font-semibold text-blue-400">Проверка</h3>

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

          <p class="text-xs text-gray-400">
            После отправки ваш профиль исполнителя будет создан и опубликован. Клиенты смогут найти вашу услугу в каталоге.
          </p>
        </div>
      </div>

      <!-- Footer Buttons -->
      <div class="sticky bottom-0 bg-slate-800 border-t border-blue-900 p-4 flex gap-2">
        <button
          v-if="currentStep > 1"
          @click="previousStep"
          class="flex-1 bg-slate-700 hover:bg-slate-600 text-white font-semibold py-2 rounded-lg transition"
        >
          ← Назад
        </button>
        <button
          v-if="currentStep < steps"
          @click="nextStep"
          :disabled="!isStepValid"
          :class="[
            'flex-1 font-semibold py-2 rounded-lg transition',
            isStepValid
              ? 'bg-blue-600 hover:bg-blue-500 text-white'
              : 'bg-gray-700 text-gray-400 cursor-not-allowed'
          ]"
        >
          Далее →
        </button>
        <button
          v-else
          @click="submitForm"
          class="flex-1 bg-green-600 hover:bg-green-500 text-white font-semibold py-2 rounded-lg transition"
        >
          ✓ Создать профиль
        </button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'

const emit = defineEmits(['close', 'confirm'])

const currentStep = ref(1)
const steps = 4

const formData = ref({
  serviceName: '',
  description: '',
  category: '',
  price: '',
  images: [] as Array<{ file: File; preview: string }>,
  timezone: 'UTC+3',
  availability: {
    weekdays: true,
    weekends: false,
    evenings: true
  },
  maxConcurrentOrders: '5'
})

const isStepValid = computed(() => {
  switch (currentStep.value) {
    case 1:
      return (
        formData.value.serviceName.trim().length > 0 &&
        formData.value.description.trim().length > 10 &&
        formData.value.category.length > 0 &&
        formData.value.price > 0
      )
    case 2:
      return formData.value.images.length > 0
    case 3:
      return (
        Object.values(formData.value.availability).some(v => v) &&
        formData.value.maxConcurrentOrders > 0
      )
    case 4:
      return true
    default:
      return false
  }
})

const nextStep = () => {
  if (isStepValid.value && currentStep.value < steps) {
    currentStep.value++
  }
}

const previousStep = () => {
  if (currentStep.value > 1) {
    currentStep.value--
  }
}

const handleImageUpload = (event: Event) => {
  const input = event.target as HTMLInputElement
  const files = input.files

  if (files) {
    Array.from(files).forEach(file => {
      // Проверка размера
      if (file.size > 5 * 1024 * 1024) {
        alert('Файл слишком большой (макс 5 МБ)')
        return
      }

      // Создание preview
      const reader = new FileReader()
      reader.onload = (e) => {
        if (formData.value.images.length < 5) {
          formData.value.images.push({
            file,
            preview: e.target?.result as string
          })
        }
      }
      reader.readAsDataURL(file)
    })
  }

  // Reset input
  input.value = ''
}

const removeImage = (index: number) => {
  formData.value.images.splice(index, 1)
}

const submitForm = () => {
  // Подготовка данных для отправки
  const providerData = {
    serviceName: formData.value.serviceName,
    description: formData.value.description,
    category: formData.value.category,
    price: parseFloat(formData.value.price as any),
    images: formData.value.images.map(img => img.file),
    timezone: formData.value.timezone,
    availability: formData.value.availability,
    maxConcurrentOrders: parseInt(formData.value.maxConcurrentOrders as any)
  }

  emit('confirm', providerData)
}
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

@keyframes slideUp {
  from {
    transform: translateY(100%);
  }
  to {
    transform: translateY(0);
  }
}

.animate-fade-in {
  animation: fadeIn 0.3s ease-out;
}

.animate-slide-up {
  animation: slideUp 0.3s ease-out;
}
</style>
