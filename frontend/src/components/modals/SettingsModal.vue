<template>
  <div class="modal-overlay fixed inset-0 bg-black/50 flex items-end z-50 animate-fade-in">
    <div class="modal-content bg-slate-800 w-full max-w-md rounded-t-2xl border-t border-blue-900 max-h-[90vh] overflow-y-auto animate-slide-up">
      <!-- Header -->
      <div class="sticky top-0 bg-slate-800 border-b border-blue-900 p-4 flex justify-between items-center">
        <h2 class="text-xl font-bold">⚙️ Настройки</h2>
        <button
          @click="$emit('close')"
          class="text-gray-400 hover:text-white text-2xl"
        >
          ✕
        </button>
      </div>

      <!-- Content -->
      <div class="p-4 space-y-4">
        <!-- Account Section -->
        <div>
          <h3 class="text-sm font-semibold text-gray-400 mb-3">Аккаунт</h3>
          <div class="space-y-3 bg-slate-700 rounded-lg p-3 border border-blue-900">
            <div>
              <label class="block text-sm font-semibold mb-1">Имя</label>
              <input
                v-model="settings.firstName"
                type="text"
                class="w-full bg-slate-600 border border-blue-900 rounded px-3 py-2 text-white focus:outline-none focus:border-blue-500"
              />
            </div>
            <div>
              <label class="block text-sm font-semibold mb-1">Фамилия</label>
              <input
                v-model="settings.lastName"
                type="text"
                class="w-full bg-slate-600 border border-blue-900 rounded px-3 py-2 text-white focus:outline-none focus:border-blue-500"
              />
            </div>
            <div>
              <label class="block text-sm font-semibold mb-1">Email</label>
              <input
                v-model="settings.email"
                type="email"
                class="w-full bg-slate-600 border border-blue-900 rounded px-3 py-2 text-white focus:outline-none focus:border-blue-500"
              />
            </div>
            <div>
              <label class="block text-sm font-semibold mb-1">Телефон</label>
              <input
                v-model="settings.phone"
                type="tel"
                placeholder="+7 (999) 999-99-99"
                class="w-full bg-slate-600 border border-blue-900 rounded px-3 py-2 text-white focus:outline-none focus:border-blue-500"
              />
            </div>
          </div>
        </div>

        <!-- Notifications Section -->
        <div>
          <h3 class="text-sm font-semibold text-gray-400 mb-3">Уведомления</h3>
          <div class="space-y-2 bg-slate-700 rounded-lg p-3 border border-blue-900">
            <label class="flex items-center gap-2 cursor-pointer">
              <input
                v-model="settings.notifications.orders"
                type="checkbox"
                class="w-4 h-4"
              />
              <span class="text-sm">Новые заказы</span>
            </label>
            <label class="flex items-center gap-2 cursor-pointer">
              <input
                v-model="settings.notifications.messages"
                type="checkbox"
                class="w-4 h-4"
              />
              <span class="text-sm">Новые сообщения</span>
            </label>
            <label class="flex items-center gap-2 cursor-pointer">
              <input
                v-model="settings.notifications.reviews"
                type="checkbox"
                class="w-4 h-4"
              />
              <span class="text-sm">Новые отзывы</span>
            </label>
            <label class="flex items-center gap-2 cursor-pointer">
              <input
                v-model="settings.notifications.promotions"
                type="checkbox"
                class="w-4 h-4"
              />
              <span class="text-sm">Промо и новости</span>
            </label>
          </div>
        </div>

        <!-- Privacy Section -->
        <div>
          <h3 class="text-sm font-semibold text-gray-400 mb-3">Приватность</h3>
          <div class="space-y-2 bg-slate-700 rounded-lg p-3 border border-blue-900">
            <label class="flex items-center gap-2 cursor-pointer">
              <input
                v-model="settings.privacy.showProfile"
                type="checkbox"
                class="w-4 h-4"
              />
              <span class="text-sm">Показывать профиль в поиске</span>
            </label>
            <label class="flex items-center gap-2 cursor-pointer">
              <input
                v-model="settings.privacy.showPhone"
                type="checkbox"
                class="w-4 h-4"
              />
              <span class="text-sm">Показывать телефон в профиле</span>
            </label>
            <label class="flex items-center gap-2 cursor-pointer">
              <input
                v-model="settings.privacy.allowMessages"
                type="checkbox"
                class="w-4 h-4"
              />
              <span class="text-sm">Разрешить сообщения от незнакомых</span>
            </label>
          </div>
        </div>

        <!-- Danger Zone -->
        <div>
          <h3 class="text-sm font-semibold text-red-400 mb-3">Опасная зона</h3>
          <div class="space-y-2">
            <button
              @click="showChangePasswordModal = true"
              class="w-full bg-slate-700 hover:bg-slate-600 border border-yellow-900 text-yellow-400 font-semibold py-2 rounded-lg transition"
            >
              🔑 Изменить пароль
            </button>
            <button
              @click="showDeleteConfirm = true"
              class="w-full bg-slate-700 hover:bg-red-900 border border-red-900 text-red-400 font-semibold py-2 rounded-lg transition"
            >
              🗑️ Удалить аккаунт
            </button>
          </div>
        </div>

        <!-- Delete Confirmation -->
        <div v-if="showDeleteConfirm" class="bg-red-900/20 border border-red-900 rounded-lg p-3 space-y-2">
          <p class="text-sm font-semibold text-red-400">⚠️ Это необратимое действие!</p>
          <p class="text-xs text-gray-400">Ваш аккаунт и все данные будут удалены</p>
          <div class="flex gap-2">
            <button
              @click="showDeleteConfirm = false"
              class="flex-1 bg-slate-600 text-white py-2 rounded text-sm"
            >
              Отмена
            </button>
            <button
              @click="deleteAccount"
              class="flex-1 bg-red-600 text-white py-2 rounded text-sm hover:bg-red-700"
            >
              Удалить
            </button>
          </div>
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
          @click="saveSettings"
          class="flex-1 bg-blue-600 hover:bg-blue-500 text-white font-semibold py-2 rounded-lg transition"
        >
          ✓ Сохранить
        </button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive } from 'vue'

const props = defineProps({
  userData: Object
})

const emit = defineEmits(['close', 'save'])

const showDeleteConfirm = ref(false)
const showChangePasswordModal = ref(false)

const settings = reactive({
  firstName: props.userData?.first_name || '',
  lastName: '',
  email: '',
  phone: '',
  notifications: {
    orders: true,
    messages: true,
    reviews: true,
    promotions: false
  },
  privacy: {
    showProfile: true,
    showPhone: false,
    allowMessages: true
  }
})

const saveSettings = () => {
  emit('save', settings)
}

const deleteAccount = () => {
  console.log('Account deletion initiated')
  // TODO: Запрос на удаление аккаунта
  showDeleteConfirm.value = false
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
