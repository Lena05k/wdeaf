<template>
  <div class="fixed inset-0 bg-black/80 backdrop-blur-sm z-50 flex items-center justify-center p-4 animate-fadeIn">
    <div class="bg-slate-800 border border-slate-700 rounded-2xl w-full max-w-md max-h-[90vh] overflow-y-auto animate-slideUp">
      <!-- Header -->
      <div class="sticky top-0 bg-slate-800 border-b border-slate-700 p-6 flex items-center justify-between">
        <h2 class="text-2xl font-bold text-white">
          {{ isEditing ? 'Отредактировать' : 'Новая' }} услуга
        </h2>
        <button
          @click="close"
          class="text-gray-400 hover:text-white text-2xl transition"
        >
          ×
        </button>
      </div>

      <!-- Form -->
      <form @submit.prevent="submit" class="p-6 space-y-4">
        <!-- Service Name -->
        <div class="form-group">
          <label class="form-label">💯 Название услуги *</label>
          <input
            v-model="formData.serviceName"
            type="text"
            placeholder="напр. Web-дизайн"
            class="form-control"
            required
          />
        </div>

        <!-- Category -->
        <div class="form-group">
          <label class="form-label">🌟 Категория *</label>
          <select v-model="formData.category" class="form-control" required>
            <option value="">-- Выберите --</option>
            <option value="design">Дизайн</option>
            <option value="development">Разработка</option>
            <option value="marketing">Маркетинг</option>
            <option value="consulting">Консултирование</option>
            <option value="other">Прочее</option>
          </select>
        </div>

        <!-- Description -->
        <div class="form-group">
          <label class="form-label">📝 Описание *</label>
          <textarea
            v-model="formData.description"
            placeholder="Описание вашей услуги..."
            class="form-control h-24"
            required
          ></textarea>
        </div>

        <!-- Price -->
        <div class="form-group">
          <label class="form-label">💵 Цена (руб.) *</label>
          <input
            v-model.number="formData.price"
            type="number"
            min="0"
            step="100"
            placeholder="5000"
            class="form-control"
            required
          />
        </div>

        <!-- Availability -->
        <div class="form-group">
          <label class="form-label">📅 Надоступность</label>
          <div class="space-y-2">
            <label class="flex items-center gap-2 cursor-pointer">
              <input
                v-model="formData.availability.weekdays"
                type="checkbox"
                class="w-4 h-4 rounded"
              />
              <span class="text-gray-300">Пн-Пт (Рабочие дни)</span>
            </label>
            <label class="flex items-center gap-2 cursor-pointer">
              <input
                v-model="formData.availability.weekends"
                type="checkbox"
                class="w-4 h-4 rounded"
              />
              <span class="text-gray-300">Сб-Вс (Выходные)</span>
            </label>
            <label class="flex items-center gap-2 cursor-pointer">
              <input
                v-model="formData.availability.evenings"
                type="checkbox"
                class="w-4 h-4 rounded"
              />
              <span class="text-gray-300">🌙 Вечерами</span>
            </label>
          </div>
        </div>

        <!-- Divider -->
        <div class="border-t border-slate-700 my-4"></div>

        <!-- Action Buttons -->
        <div class="flex gap-2">
          <button
            type="button"
            @click="close"
            class="flex-1 bg-slate-700 hover:bg-slate-600 text-white font-semibold py-3 rounded-lg transition active:scale-95"
          >
            Отмена
          </button>
          <button
            type="submit"
            class="flex-1 bg-green-600 hover:bg-green-500 text-white font-semibold py-3 rounded-lg transition active:scale-95 flex items-center justify-center gap-2"
          >
            <span>✅</span> {{ isEditing ? 'Сохранить' : 'Создать' }}
          </button>
        </div>
      </form>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, watch } from 'vue'

interface Service {
  id?: string | number
  serviceName: string
  category: string
  description: string
  price: number
  availability: {
    weekdays: boolean
    weekends: boolean
    evenings: boolean
  }
  images?: string[]
}

interface Props {
  service?: Service
  isEditing?: boolean
}

const props = withDefaults(defineProps<Props>(), {
  isEditing: false
})

const emit = defineEmits<{
  submit: [data: Service]
  close: []
}>()

const formData = ref<Service>({
  serviceName: '',
  category: '',
  description: '',
  price: 0,
  availability: {
    weekdays: true,
    weekends: false,
    evenings: true
  }
})

// Initialize form with existing data
watch(
  () => props.service,
  (service) => {
    if (service) {
      formData.value = JSON.parse(JSON.stringify(service))
    }
  },
  { immediate: true }
)

const submit = () => {
  if (!formData.value.serviceName || !formData.value.category || !formData.value.description || !formData.value.price) {
    alert('Пожалуйста, заполните все обязательные поля')
    return
  }
  emit('submit', formData.value)
}

const close = () => {
  emit('close')
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
    transform: translateY(20px);
    opacity: 0;
  }
  to {
    transform: translateY(0);
    opacity: 1;
  }
}

.animate-fadeIn {
  animation: fadeIn 0.3s ease-out;
}

.animate-slideUp {
  animation: slideUp 0.3s ease-out;
}
</style>
