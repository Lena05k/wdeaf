<template>
  <div v-if="service" class="modal-overlay fixed inset-0 bg-black/50 flex items-end z-50">
    <div class="modal-content bg-slate-800 w-full max-w-md rounded-t-2xl border-t border-blue-900 max-h-[90vh] overflow-y-auto">
      <!-- Header -->
      <div class="sticky top-0 bg-slate-800 border-b border-blue-900 p-3 flex justify-between items-center">
        <h2 class="text-lg font-bold">✏️ Редактировать</h2>
        <button
            @click="emit('close')"
            class="text-gray-400 hover:text-white text-2xl"
        >
          ✕
        </button>
      </div>

      <!-- Content -->
      <div class="p-4 space-y-4">
        <!-- Basic Info Section -->
        <div class="space-y-3">
          <!-- Название -->
          <div>
            <label class="block text-xs font-semibold text-gray-400 mb-1">НАЗВАНИЕ</label>
            <input
                v-model="editedService.serviceName"
                type="text"
                placeholder="Название услуги"
                class="w-full bg-slate-700 border border-blue-900 rounded-lg px-3 py-2 text-sm text-white placeholder-gray-500 focus:outline-none focus:border-blue-500"
            />
          </div>

          <!-- Описание -->
          <div>
            <label class="block text-xs font-semibold text-gray-400 mb-1">ОПИСАНИЕ</label>
            <textarea
                v-model="editedService.description"
                placeholder="Что вы делаете?"
                rows="3"
                class="w-full bg-slate-700 border border-blue-900 rounded-lg px-3 py-2 text-sm text-white placeholder-gray-500 focus:outline-none focus:border-blue-500 resize-none"
            />
          </div>

          <!-- Категория и Цена (в один ряд для TMA) -->
          <div class="grid grid-cols-2 gap-2">
            <div>
              <label class="block text-xs font-semibold text-gray-400 mb-1">КАТЕГОРИЯ</label>
              <select
                  v-model="editedService.category"
                  class="w-full bg-slate-700 border border-blue-900 rounded-lg px-3 py-2 text-sm text-white focus:outline-none focus:border-blue-500"
              >
                <option value="repair">Ремонт</option>
                <option value="business">Бизнес</option>
                <option value="fashion">Мода</option>
                <option value="education">Обучение</option>
                <option value="design">Дизайн</option>
                <option value="it">IT</option>
              </select>
            </div>
            <div>
              <label class="block text-xs font-semibold text-gray-400 mb-1">ЦЕНА (₽)</label>
              <input
                  v-model.number="editedService.price"
                  type="number"
                  placeholder="500"
                  class="w-full bg-slate-700 border border-blue-900 rounded-lg px-3 py-2 text-sm text-white placeholder-gray-500 focus:outline-none focus:border-blue-500"
              />
            </div>
          </div>
        </div>

        <!-- Divider -->
        <div class="h-px bg-slate-700"></div>

        <!-- Images Section - Optional with Paper Clip -->
        <div>
          <div class="flex items-center gap-2 mb-3">
            <span class="text-sm font-semibold text-blue-400">📎 Фото и файлы</span>
            <span class="text-xs text-gray-500">(опционально)</span>
          </div>

          <!-- Current Attachments -->
          <div v-if="editedService.images && editedService.images.length > 0" class="space-y-2 mb-3">
            <div
                v-for="(image, index) in editedService.images"
                :key="`existing-${index}`"
                class="relative bg-slate-700 border border-blue-900 rounded-lg overflow-hidden group flex items-center gap-2 p-2 h-16"
            >
              <img
                  :src="image.preview || image"
                  :alt="'Image ' + (index + 1)"
                  class="w-14 h-14 object-cover rounded"
              />
              <span class="text-xs text-gray-300 truncate flex-1">{{ `Image ${index + 1}` }}</span>
              <button
                  @click="removeImage(index)"
                  class="bg-red-600 text-white rounded-full p-1 opacity-0 group-hover:opacity-100 hover:bg-red-700 transition flex-shrink-0"
              >
                ✕
              </button>
            </div>
          </div>

          <!-- Add Attachments Button (Paper Clip Style) -->
          <label v-if="!editedService.images || editedService.images.length < 5" class="flex items-center justify-center gap-2 bg-slate-700 border border-dashed border-slate-600 rounded-lg py-3 px-2 cursor-pointer hover:border-blue-500 hover:bg-slate-700/80 transition text-sm font-medium text-gray-400 hover:text-blue-400">
            <span class="text-lg">📎</span>
            <span>{{ editedService.images && editedService.images.length > 0 ? 'Добавить ещё' : 'Добавить' }}</span>
            <input
                type="file"
                accept="image/*"
                multiple
                class="hidden"
                @change="handleAddImage"
            />
          </label>
        </div>

        <!-- Divider -->
        <div class="h-px bg-slate-700"></div>

        <!-- Schedule Section -->
        <div>
          <h3 class="text-sm font-semibold text-blue-400 mb-2">⏰ Время работы</h3>

          <!-- Timezone -->
          <div class="mb-3">
            <label class="block text-xs font-semibold text-gray-400 mb-1">ЧАСОВОЙ ПОЯС</label>
            <select
                v-model="editedService.timezone"
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
                  v-model="editedService.availability.weekdays"
                  type="checkbox"
                  class="w-4 h-4 cursor-pointer accent-blue-500"
              />
              <span class="text-sm">Будни (Пн-Пт)</span>
            </label>
            <label class="flex items-center gap-2 cursor-pointer hover:text-blue-400 transition">
              <input
                  v-model="editedService.availability.weekends"
                  type="checkbox"
                  class="w-4 h-4 cursor-pointer accent-blue-500"
              />
              <span class="text-sm">Выходные (Сб-Вс)</span>
            </label>
            <label class="flex items-center gap-2 cursor-pointer hover:text-blue-400 transition">
              <input
                  v-model="editedService.availability.evenings"
                  type="checkbox"
                  class="w-4 h-4 cursor-pointer accent-blue-500"
              />
              <span class="text-sm">Вечера (18:00-23:00)</span>
            </label>
          </div>
        </div>
      </div>

      <!-- Footer Buttons -->
      <div class="sticky bottom-0 bg-slate-800 border-t border-blue-900 p-3 flex gap-2">
        <button
            @click="emit('close')"
            class="flex-1 bg-slate-700 hover:bg-slate-600 text-white font-semibold py-2 text-sm rounded-lg transition"
        >
          ✕ Отмена
        </button>
        <button
            @click="handleSave"
            :disabled="!isFormValid"
            :class="[
              'flex-1 font-semibold py-2 text-sm rounded-lg transition',
              isFormValid
                ? 'bg-green-600 hover:bg-green-500 text-white'
                : 'bg-gray-700 text-gray-400 cursor-not-allowed'
            ]"
        >
          💾 Сохранить
        </button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed, reactive, watch } from 'vue'

interface ServiceImage {
  file?: File
  preview?: string
  url?: string
}

interface Service {
  id: string
  serviceName: string
  name?: string
  description: string
  category: string
  price: number
  timezone?: string
  images?: (ServiceImage | string)[]
  availability?: {
    weekdays: boolean
    weekends: boolean
    evenings: boolean
  }
  rating?: number
  reviewsCount?: number
}

interface Props {
  service: Service | null
}

const props = defineProps<Props>()

const emit = defineEmits<{
  'close': []
  'save': [service: Service]
}>()

const editedService = reactive<Service>({
  id: '',
  serviceName: '',
  description: '',
  category: 'repair',
  price: 0,
  timezone: 'UTC+3',
  images: [],
  availability: {
    weekdays: true,
    weekends: false,
    evenings: true
  }
})

// Watch for prop changes and update editedService - СОХРАНЯЕМ ДАННЫЕ КАК ЕСТЬ
watch(() => props.service, (newService) => {
  if (newService) {
    // Копируем все данные точно как есть
    const copy = JSON.parse(JSON.stringify(newService))
    Object.assign(editedService, copy)
    // Гарантируем структуру availability
    if (!editedService.availability) {
      editedService.availability = {
        weekdays: true,
        weekends: false,
        evenings: true
      }
    }
  }
}, { immediate: true, deep: true })

// Валидация: ФОТО ТЕПЕРЬ ОПЦИОНАЛЬНО
const isFormValid = computed(() => {
  return (
    editedService.serviceName.trim().length > 0 &&
    editedService.description.trim().length > 5 &&
    editedService.category.length > 0 &&
    editedService.price > 0
  )
})

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
      if (editedService.images && editedService.images.length < 5 && e.target?.result) {
        editedService.images.push({
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
  if (editedService.images) {
    editedService.images.splice(index, 1)
  }
}

const handleSave = () => {
  if (isFormValid.value) {
    emit('save', { ...editedService })
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