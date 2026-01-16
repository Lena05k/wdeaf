<template>
  <div class="modal-overlay fixed inset-0 bg-black/50 flex items-end z-50 animate-fade-in">
    <div class="modal-content bg-slate-800 w-full max-w-md rounded-t-2xl border-t border-blue-900 max-h-[90vh] overflow-y-auto animate-slide-up">
      <!-- Header -->
      <div class="sticky top-0 bg-slate-800 border-b border-blue-900 p-4 flex justify-between items-center">
        <h2 class="text-xl font-bold">✏️ Редактировать услугу</h2>
        <button
          @click="$emit('close')"
          class="text-gray-400 hover:text-white text-2xl"
        >
          ✕
        </button>
      </div>

      <!-- Content -->
      <div class="p-4 space-y-4">
        <!-- Service Name -->
        <div>
          <label class="block text-sm font-semibold mb-2">Название услуги</label>
          <input
            v-model="editData.serviceName"
            type="text"
            class="w-full bg-slate-700 border border-blue-900 rounded-lg px-4 py-2 text-white focus:outline-none focus:border-blue-500"
          />
        </div>

        <!-- Description -->
        <div>
          <label class="block text-sm font-semibold mb-2">Описание</label>
          <textarea
            v-model="editData.description"
            rows="4"
            class="w-full bg-slate-700 border border-blue-900 rounded-lg px-4 py-2 text-white focus:outline-none focus:border-blue-500 resize-none"
          />
        </div>

        <!-- Category -->
        <div>
          <label class="block text-sm font-semibold mb-2">Категория</label>
          <select
            v-model="editData.category"
            class="w-full bg-slate-700 border border-blue-900 rounded-lg px-4 py-2 text-white focus:outline-none focus:border-blue-500"
          >
            <option value="languages">🗣️ Языки</option>
            <option value="music">🎵 Музыка</option>
            <option value="design">🎨 Дизайн</option>
            <option value="programming">💻 Программирование</option>
            <option value="fitness">💪 Фитнес</option>
            <option value="other">📦 Другое</option>
          </select>
        </div>

        <!-- Price -->
        <div>
          <label class="block text-sm font-semibold mb-2">Цена (₽)</label>
          <input
            v-model="editData.price"
            type="number"
            class="w-full bg-slate-700 border border-blue-900 rounded-lg px-4 py-2 text-white focus:outline-none focus:border-blue-500"
          />
        </div>

        <!-- Max Concurrent Orders -->
        <div>
          <label class="block text-sm font-semibold mb-2">Макс. одновременных заказов</label>
          <input
            v-model="editData.maxConcurrentOrders"
            type="number"
            class="w-full bg-slate-700 border border-blue-900 rounded-lg px-4 py-2 text-white focus:outline-none focus:border-blue-500"
          />
        </div>

        <!-- Availability -->
        <div>
          <label class="block text-sm font-semibold mb-3">Доступность</label>
          <div class="space-y-2 bg-slate-700 rounded-lg p-3 border border-blue-900">
            <label class="flex items-center gap-2 cursor-pointer">
              <input
                v-model="editData.availability.weekdays"
                type="checkbox"
                class="w-4 h-4"
              />
              <span class="text-sm">Будни (Пн-Пт)</span>
            </label>
            <label class="flex items-center gap-2 cursor-pointer">
              <input
                v-model="editData.availability.weekends"
                type="checkbox"
                class="w-4 h-4"
              />
              <span class="text-sm">Выходные (Сб-Вс)</span>
            </label>
            <label class="flex items-center gap-2 cursor-pointer">
              <input
                v-model="editData.availability.evenings"
                type="checkbox"
                class="w-4 h-4"
              />
              <span class="text-sm">Вечерние часы (18:00-23:00)</span>
            </label>
          </div>
        </div>

        <!-- Timezone -->
        <div>
          <label class="block text-sm font-semibold mb-2">Часовой пояс</label>
          <select
            v-model="editData.timezone"
            class="w-full bg-slate-700 border border-blue-900 rounded-lg px-4 py-2 text-white focus:outline-none focus:border-blue-500"
          >
            <option value="UTC+3">UTC+3 (Москва)</option>
            <option value="UTC+4">UTC+4 (Казань)</option>
            <option value="UTC+5">UTC+5 (Екатеринбург)</option>
            <option value="UTC+8">UTC+8 (Владивосток)</option>
          </select>
        </div>
      </div>

      <!-- Footer -->
      <div class="sticky bottom-0 bg-slate-800 border-t border-blue-900 p-4 flex gap-2">
        <button
          @click="$emit('close')"
          class="flex-1 bg-slate-700 hover:bg-slate-600 text-white font-semibold py-2 rounded-lg transition"
        >
          Отмена
        </button>
        <button
          @click="saveChanges"
          class="flex-1 bg-blue-600 hover:bg-blue-500 text-white font-semibold py-2 rounded-lg transition"
        >
          ✓ Сохранить
        </button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, watch } from 'vue'

const props = defineProps({
  provider: Object
})

const emit = defineEmits(['close', 'save'])

const editData = reactive({
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
  maxConcurrentOrders: 5
})

// Инициализация данных при загрузке
watch(
  () => props.provider,
  (newProvider) => {
    if (newProvider) {
      Object.assign(editData, newProvider)
    }
  },
  { immediate: true }
)

const saveChanges = () => {
  emit('save', editData)
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
