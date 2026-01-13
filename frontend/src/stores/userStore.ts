import { defineStore } from 'pinia'
import { ref, computed } from 'vue'

export interface User {
    id: string
    username: string
    first_name: string
    last_name?: string
    photo_url?: string
    is_premium: boolean
    is_provider: boolean
    rating: number
    reviews_count: number
    joined_date: string
    bio?: string
}

export interface AuthState {
    user: User | null
    token: string | null
    isAuthenticated: boolean
    isLoading: boolean
    error: string | null
}

export const useAuthStore = defineStore('auth', () => {
    // State
    const user = ref<User | null>(null)
    const token = ref<string | null>(null)
    const isLoading = ref(false)
    const error = ref<string | null>(null)

    // Computed
    const isAuthenticated = computed(() => !!user.value && !!token.value)

    const userDisplayName = computed(() => {
        if (!user.value) return 'Гость'
        return user.value.first_name || user.value.username
    })

    const userInitials = computed(() => {
        if (!user.value) return '?'
        const parts = [user.value.first_name, user.value.last_name].filter(Boolean)
        return parts.map(p => p[0].toUpperCase()).join('')
    })

    // Methods
    const initAuth = () => {
        // Восстановить сессию из localStorage
        const savedUser = localStorage.getItem('user')
        const savedToken = localStorage.getItem('token')

        if (savedUser && savedToken) {
            try {
                user.value = JSON.parse(savedUser)
                token.value = savedToken
            } catch (e) {
                clearAuth()
            }
        }

        // Если есть Telegram WebApp, использовать данные оттуда
        if (window.Telegram?.WebApp?.initDataUnsafe?.user) {
            const tgUser = window.Telegram.WebApp.initDataUnsafe.user
            setUserFromTelegram(tgUser)
        }
    }

    const setUserFromTelegram = (tgUser: any) => {
        user.value = {
            id: String(tgUser.id),
            username: tgUser.username || `user_${tgUser.id}`,
            first_name: tgUser.first_name || 'User',
            last_name: tgUser.last_name,
            photo_url: tgUser.photo_url,
            is_premium: tgUser.is_premium || false,
            is_provider: false,
            rating: 4.8,
            reviews_count: 0,
            joined_date: new Date().toISOString()
        }
        token.value = `telegram_${tgUser.id}_${Date.now()}`
        saveSession()
    }

    const login = async (username: string, password: string) => {
        isLoading.value = true
        error.value = null

        try {
            // Имитация API запроса
            // const response = await apiClient.post('/auth/login', { username, password })

            // Mock данные
            user.value = {
                id: '123456789',
                username: username,
                first_name: 'Иван',
                last_name: 'Петров',
                is_premium: false,
                is_provider: false,
                rating: 4.8,
                reviews_count: 0,
                joined_date: new Date().toISOString()
            }
            token.value = `token_${Date.now()}`

            saveSession()
            return true
        } catch (e) {
            error.value = 'Ошибка входа. Проверьте учетные данные.'
            return false
        } finally {
            isLoading.value = false
        }
    }

    const signup = async (username: string, firstName: string, password: string) => {
        isLoading.value = true
        error.value = null

        try {
            // const response = await apiClient.post('/auth/signup', {
            //   username,
            //   first_name: firstName,
            //   password
            // })

            user.value = {
                id: `${Date.now()}`,
                username: username,
                first_name: firstName,
                is_premium: false,
                is_provider: false,
                rating: 5.0,
                reviews_count: 0,
                joined_date: new Date().toISOString()
            }
            token.value = `token_${Date.now()}`

            saveSession()
            return true
        } catch (e) {
            error.value = 'Ошибка регистрации. Попробуйте позже.'
            return false
        } finally {
            isLoading.value = false
        }
    }

    const logout = () => {
        clearAuth()
    }

    const updateProfile = async (updates: Partial<User>) => {
        if (!user.value) return false

        isLoading.value = true
        error.value = null

        try {
            // const response = await apiClient.put(`/users/${user.value.id}`, updates)

            user.value = {
                ...user.value,
                ...updates
            }
            saveSession()
            return true
        } catch (e) {
            error.value = 'Ошибка обновления профиля.'
            return false
        } finally {
            isLoading.value = false
        }
    }

    const becomeProvider = async () => {
        if (!user.value) return false

        isLoading.value = true
        error.value = null

        try {
            // const response = await apiClient.post(`/users/${user.value.id}/become-provider`)

            user.value.is_provider = true
            saveSession()
            return true
        } catch (e) {
            error.value = 'Ошибка активации режима исполнителя.'
            return false
        } finally {
            isLoading.value = false
        }
    }

    const saveSession = () => {
        if (user.value) {
            localStorage.setItem('user', JSON.stringify(user.value))
        }
        if (token.value) {
            localStorage.setItem('token', token.value)
        }
    }

    const clearAuth = () => {
        user.value = null
        token.value = null
        error.value = null
        localStorage.removeItem('user')
        localStorage.removeItem('token')
    }

    return {
        // State
        user,
        token,
        isLoading,
        error,

        // Computed
        isAuthenticated,
        userDisplayName,
        userInitials,

        // Methods
        initAuth,
        login,
        signup,
        logout,
        updateProfile,
        becomeProvider,
        setUserFromTelegram
    }
})
