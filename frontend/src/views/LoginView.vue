<template>
  <div class="min-h-screen flex items-center justify-center px-4" :style="{ backgroundColor: bgColor }">
    <div class="w-full max-w-md">
      <!-- Logo/Header -->
      <div class="text-center mb-8">
        <h1 class="text-3xl font-bold mb-2" :style="{ color: textColor }">WDEAF</n        <p class="text-sm" :style="{ color: hintColor }}>Сервис поиска исполнителей</p>
      </div>

      <!-- Auth Card -->
      <div class="rounded-2xl p-6 mb-6" :style="{ backgroundColor: surfaceColor }">
        <!-- Tabs -->
        <div class="flex gap-4 mb-6 border-b" :style="{ borderColor: borderColor }">
          <button
            @click="authTab = 'telegram'"
            :class="[
              'flex-1 pb-3 font-medium transition-colors',
              authTab === 'telegram'
                ? 'border-b-2'
                : 'opacity-60 hover:opacity-80'
            ]"
            :style="{
              color: authTab === 'telegram' ? buttonColor : hintColor,
              borderColor: authTab === 'telegram' ? buttonColor : 'transparent'
            }"
          >
            Telegram
          </button>
          <button
            @click="authTab = 'phone'"
            :class="[
              'flex-1 pb-3 font-medium transition-colors',
              authTab === 'phone'
                ? 'border-b-2'
                : 'opacity-60 hover:opacity-80'
            ]"
            :style="{
              color: authTab === 'phone' ? buttonColor : hintColor,
              borderColor: authTab === 'phone' ? buttonColor : 'transparent'
            }"
          >
            Телефон
          </button>
        </div>

        <!-- Telegram Auth Tab -->
        <div v-if="authTab === 'telegram'" class="space-y-4">
          <p class="text-sm text-center" :style="{ color: hintColor }}>
            Используйте Telegram для быстрой авторизации
          </p>
          <button
            @click="handleTelegramAuth"
            :disabled="loading"
            class="w-full py-3 px-4 rounded-lg font-semibold flex items-center justify-center gap-2 transition-all disabled:opacity-50"
            :style={" backgroundColor: buttonColor, color: '#ffffff' }"
          >
            <svg v-if="!loading" class="w-5 h-5" viewBox="0 0 24 24" fill="currentColor">
              <path d="M12 0C5.373 0 0 5.373 0 12s5.373 12 12 12 12-5.373 12-12S18.627 0 12 0zm5.894 8.221l-1.97 9.28c-.145.658-.537.818-1.084.508l-3-2.21-1.446 1.394c-.16.16-.295.295-.605.295-.417 0-.335-.149-.471-.524l-1.052-3.459-2.923-.876c-.635-.194-.639-.535.134-.804l11.384-4.392c.535-.196 1.017.131.832.941z"/>
            </svg>
            <span v-if="loading">Загрузка...</span>
            <span v-else>Войти через Telegram</span>
          </button>
        </div>

        <!-- Phone Auth Tab -->
        <form v-else-if="authTab === 'phone'" @submit.prevent="handlePhoneAuth" class="space-y-4">
          <!-- Phone Input -->
          <div class="form-group">
            <label class="block text-sm font-medium mb-2" :style="{ color: textColor }}>Номер телефона</label>
            <input
              v-model="formData.phone"
              type="tel"
              placeholder="+7 (999) 999-99-99"
              class="w-full px-4 py-3 rounded-lg border transition-colors focus:outline-none"
              :style="{
                backgroundColor: bgColor,
                borderColor: formData.phone && !isPhoneValid ? '#ef4444' : borderColor,
                color: textColor
              }"
              @input="formatPhoneNumber"
            />
            <p v-if="formData.phone && !isPhoneValid" class="text-xs mt-1" style="color: #ef4444;">
              Некорректный номер телефона
            </p>
          </div>

          <!-- Name Input -->
          <div class="form-group">
            <label class="block text-sm font-medium mb-2" :style="{ color: textColor }">Имя</label>
            <input
              v-model="formData.first_name"
              type="text"
              placeholder="Иван"
              class="w-full px-4 py-3 rounded-lg border transition-colors focus:outline-none"
              :style="{
                backgroundColor: bgColor,
                borderColor: borderColor,
                color: textColor
              }"
            />
          </div>

          <!-- Telegram Username Input -->
          <div class="form-group">
            <label class="block text-sm font-medium mb-2" :style="{ color: textColor }">Имя пользователя Telegram (опционально)</label>
            <div class="flex items-center" :style="{ backgroundColor: bgColor }" class="px-4 py-3 rounded-lg border" :style="{ borderColor }">
              <span :style="{ color: hintColor }}">@</span>
              <input
                v-model="formData.username"
                type="text"
                placeholder="your_telegram_name"
                class="flex-1 bg-transparent ml-1 focus:outline-none"
                :style="{ color: textColor }"
              />
            </div>
          </div>

          <!-- Submit Button -->
          <button
            type="submit"
            :disabled="loading || !isFormValid"
            class="w-full py-3 px-4 rounded-lg font-semibold transition-all disabled:opacity-50"
            :style="{ backgroundColor: buttonColor, color: '#ffffff' }"
          >
            <span v-if="loading">Загрузка...</span>
            <span v-else>Продолжить</span>
          </button>
        </form>
      </div>

      <!-- Error Message -->
      <div v-if="errorMessage" class="p-4 rounded-lg mb-4" style="backgroundColor: rgba(239, 68, 68, 0.1); color: #ef4444;">
        <p class="text-sm font-medium">{{ errorMessage }}</p>
      </div>

      <!-- Terms -->
      <p class="text-xs text-center" :style="{ color: hintColor }}>
        Продолжая, вы соглашаетесь с нашей
        <a href="#" class="underline" :style="{ color: buttonColor }">Политикой конфиденциальности</a>
      </p>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useUserStore } from '@/stores/userStore'
import { authService } from '@/api/authService'

const router = useRouter()
const userStore = useUserStore()

const authTab = ref<'telegram' | 'phone'>('telegram')
const loading = ref(false)
const errorMessage = ref('')

const formData = ref({
  phone: '',
  first_name: '',
  username: ''
})

const isPhoneValid = computed(() => {
  if (!formData.value.phone) return true
  // Простая валидация: телефон должен содержать минимум 10 цифр
  const digits = formData.value.phone.replace(/\D/g, '')
  return digits.length >= 10
})

const isFormValid = computed(() => {
  return (
    formData.value.phone &&
    formData.value.first_name.trim() &&
    isPhoneValid.value
  )
})

const getTelegramThemeParams = () => {
  if (!window.Telegram?.WebApp?.themeParams) {
    return {
      bg_color: '#ffffff',
      text_color: '#000000',
      hint_color: '#6b7280',
      button_color: '#2563eb',
      secondary_bg_color: '#f9fafb'
    }
  }
  return window.Telegram.WebApp.themeParams
}

const themeParams = computed(() => getTelegramThemeParams())

const textColor = computed(() => themeParams.value.text_color || '#000000')
const hintColor = computed(() => themeParams.value.hint_color || '#6b7280')
const bgColor = computed(() => themeParams.value.bg_color || '#ffffff')
const buttonColor = computed(() => themeParams.value.button_color || '#2563eb')
const surfaceColor = computed(() => themeParams.value.secondary_bg_color || '#f9fafb')
const borderColor = computed(() => {
  // Вычисляем цвет границы на основе bg и hint colors
  return textColor.value === '#ffffff' ? 'rgba(255, 255, 255, 0.2)' : 'rgba(0, 0, 0, 0.1)'
})

const formatPhoneNumber = () => {
  // Простое форматирование: удаляем все кроме цифр и +
  const value = formData.value.phone
  const digits = value.replace(/\D/g, '')
  
  if (digits.length === 0) {
    formData.value.phone = ''
  } else if (digits.length <= 2) {
    formData.value.phone = '+' + digits
  } else if (digits.length <= 5) {
    formData.value.phone = '+' + digits.slice(0, 1) + ' (' + digits.slice(1)
  } else if (digits.length <= 7) {
    formData.value.phone = '+' + digits.slice(0, 1) + ' (' + digits.slice(1, 4) + ') ' + digits.slice(4)
  } else {
    formData.value.phone = '+' + digits.slice(0, 1) + ' (' + digits.slice(1, 4) + ') ' + digits.slice(4, 7) + '-' + digits.slice(7, 9) + '-' + digits.slice(9, 11)
  }
}

/**
 * Telegram Auth Handler
 * Использует Telegram Web Apps API для получения данных пользователя
 */
const handleTelegramAuth = async () => {
  try {
    loading.value = true
    errorMessage.value = ''
    
    // Инициализируем Telegram WebApp если ещё не инициализирован
    if (window.Telegram?.WebApp) {
      const tg = window.Telegram.WebApp
      tg.ready()
      
      // Получаем initData для отправки на бэкенд
      const initData = tg.initData
      
      if (!initData) {
        throw new Error('Не удалось получить данные от Telegram')
      }
      
      // Отправляем initData на бэкенд для валидации подписи
      const response = await authService.loginWithTelegram(initData)
      
      // Сохраняем токен
      if (response.access_token) {
        authService.setToken(response.access_token)
      }
      
      // Обновляем store
      userStore.setUser(response.user)
      
      // Редиректим на главную страницу
      await router.push('/')
    } else {
      throw new Error('Telegram Web App недоступен')
    }
  } catch (error: any) {
    console.error('Telegram auth error:', error)
    errorMessage.value = error.message || 'Ошибка авторизации через Telegram'
  } finally {
    loading.value = false
  }
}

/**
 * Phone Auth Handler
 * Авторизация по номеру телефона + имя + ник Telegram
 */
const handlePhoneAuth = async () => {
  try {
    loading.value = true
    errorMessage.value = ''
    
    if (!isFormValid.value) {
      throw new Error('Заполните все обязательные поля')
    }
    
    // Очищаем номер телефона от форматирования
    const phoneDigits = formData.value.phone.replace(/\D/g, '')
    
    // Отправляем запрос на регистрацию
    const response = await authService.loginWithPhone({
      phone: '+' + phoneDigits,
      first_name: formData.value.first_name,
      username: formData.value.username || undefined
    })
    
    // Сохраняем токен
    if (response.access_token) {
      authService.setToken(response.access_token)
    }
    
    // Обновляем store
    userStore.setUser(response.user)
    
    // Редиректим на главную страницу
    await router.push('/')
  } catch (error: any) {
    console.error('Phone auth error:', error)
    errorMessage.value = error.message || 'Ошибка авторизации'
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  // Инициализируем Telegram WebApp при загрузке
  if (window.Telegram?.WebApp) {
    const tg = window.Telegram.WebApp
    tg.ready()
    // Скрываем главную кнопку при авторизации
    tg.MainButton?.hide()
    tg.BackButton?.hide()
  }
})
</script>

<style scoped>
.form-group {
  width: 100%;
}
</style>