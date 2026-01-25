import { defineStore } from 'pinia'
import { ref, computed } from 'vue'

interface User {
  id: string | number
  first_name: string
  last_name?: string
  username?: string
  email?: string
  phone?: string
}

interface Service {
  id: string | number
  serviceName: string
  name?: string
  description: string
  category: string
  price: number
  timezone: string
  availability: {
    weekdays: boolean
    weekends: boolean
    evenings: boolean
  }
  images?: any[]
  maxConcurrentOrders?: number
  rating?: number
  reviews?: number
}

interface ProviderInfo {
  serviceName: string
  description: string
  category: string
  categories?: string[]
  price: number
  timezone: string
  availability: {
    weekdays: boolean
    weekends: boolean
    evenings: boolean
  }
  maxConcurrentOrders: number
  rating?: number
  reviews?: number
}

export const useUserStore = defineStore('user', () => {
  // ← НОВОЕ: Функция для получения данных из Telegram
  const getTelegramUser = (): User => {
    // Пытаемся получить данные из Telegram Mini App
    if (window.Telegram?.WebApp?.initDataUnsafe?.user) {
      const telegramUser = window.Telegram.WebApp.initDataUnsafe.user
      console.log('👤 Loaded user from Telegram:', telegramUser)
      return {
        id: telegramUser.id,
        first_name: telegramUser.first_name,
        last_name: telegramUser.last_name,
        username: telegramUser.username
      }
    }

    // Fallback если Telegram недоступен (для разработки)
    console.warn('⚠️ Telegram not available, using default user data')
    return {
      id: '123456789',
      first_name: 'Иван',
      username: 'ivan_user'
    }
  }

  // Инициализируем с данными из Telegram или fallback
  const user = ref<User>(getTelegramUser())
  const authToken = ref<string | null>('authenticated')
  const providerInfo = ref<ProviderInfo | null>(null)
  const providerServices = ref<Service[]>([])

  const isAuthenticated = computed(() => !!authToken.value || !!user.value)
  // ✅ ИСПРАВЛЕНО: Исполнитель создан только если есть providerInfo (профиль создан)
  const isProvider = computed(() => providerInfo.value !== null)

  // Инициализация из Telegram (может вызвать повторно если нужно)
  const initFromTelegram = () => {
    user.value = getTelegramUser()
  }

  // Установить юзера
  const setUser = (userData: User) => {
    user.value = userData
    if (userData) {
      authToken.value = 'authenticated'
    }
  }

  // Установить информацию исполнителя
  const setProviderInfo = (provider: ProviderInfo) => {
    providerInfo.value = provider
    console.log('✅ Provider profile created:', provider)
  }

  // Получить информацию исполнителя
  const getProviderInfo = () => {
    return providerInfo.value
  }

  // Обновить профиль исполнителя
  const updateProviderInfo = (updates: Partial<ProviderInfo>) => {
    if (providerInfo.value) {
      providerInfo.value = { ...providerInfo.value, ...updates }
      console.log('✏️ Provider profile updated:', providerInfo.value)
    }
  }

  // Добавить услугу
  const addService = (service: Omit<Service, 'id'>) => {
    const newService = {
      id: Date.now(),
      ...service
    } as Service
    providerServices.value.push(newService)
    console.log('✅ Service added:', newService)
  }

  // Обновить услугу
  const updateService = (serviceId: string | number, updates: Partial<Service>) => {
    const service = providerServices.value.find(s => s.id === serviceId)
    if (service) {
      Object.assign(service, updates)
      console.log('✏️ Service updated:', serviceId, updates)
    } else {
      console.warn('⚠️ Service not found:', serviceId)
    }
  }

  // Удалить услугу
  const deleteService = (serviceId: string | number) => {
    const initialLength = providerServices.value.length
    providerServices.value = providerServices.value.filter(s => s.id !== serviceId)
    if (providerServices.value.length < initialLength) {
      console.log('🗑️ Service deleted:', serviceId)
    }
  }

  // Установить статус провайдера
  const setProviderStatus = (status: boolean) => {
    if (!status) {
      providerServices.value = []
      providerInfo.value = null
    }
  }

  // 🔥 НОВОЕ: Убрать роль исполнителя (остаться обычным клиентом)
  const removeProviderRole = () => {
    providerInfo.value = null
    providerServices.value = []
    console.log('🚪 Provider role removed, now regular customer')
  }

  // Выход
  const logout = () => {
    // Сбрасываем к дефолтному или телеграмм юзеру
    user.value = getTelegramUser()
    authToken.value = null
    providerInfo.value = null
    providerServices.value = []
  }

  // Получить полное имя
  const fullName = computed(() => {
    if (!user.value) return ''
    const { first_name, last_name } = user.value
    return last_name ? `${first_name} ${last_name}` : first_name
  })

  // Получить ID пользователя
  const userId = computed(() => user.value?.id)

  return {
    // State
    user,
    authToken,
    providerInfo,
    providerServices,

    // Computed
    isAuthenticated,
    isProvider,
    fullName,
    userId,

    // Methods
    initFromTelegram,
    setUser,
    setProviderInfo,
    getProviderInfo,
    updateProviderInfo,
    addService,
    updateService,
    deleteService,
    setProviderStatus,
    removeProviderRole,
    logout
  }
})
