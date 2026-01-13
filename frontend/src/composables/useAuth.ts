import { ref, computed } from 'vue'

interface TelegramUser {
    id: number
    first_name: string
    username?: string
    photo_url?: string
    is_premium?: boolean
}

interface UserData {
    id: number | null
    first_name: string
    username: string | null
    is_provider: boolean
    photo_url: string | null
}

export function useAuth() {
    const userData = ref<UserData>({
        id: null,
        first_name: 'Гость',
        username: null,
        is_provider: false,
        photo_url: null
    })

    const isAuthenticated = computed(() => userData.value.id !== null)

    const initAuth = async () => {
        if (window.Telegram?.WebApp) {
            const tg = window.Telegram.WebApp
            const user = tg.initDataUnsafe?.user as TelegramUser | undefined

            if (user) {
                const storedProvider = localStorage.getItem(`provider_${user.id}`)
                userData.value = {
                    id: user.id,
                    first_name: user.first_name,
                    username: user.username || null,
                    is_provider: storedProvider === 'true',
                    photo_url: user.photo_url || null
                }
            }

            tg.ready()
        }
    }

    const becomeProvider = async (): Promise<void> => {
        if (userData.value.id) {
            localStorage.setItem(`provider_${userData.value.id}`, 'true')
            userData.value.is_provider = true
        }
    }

    return {
        userData,
        isAuthenticated,
        initAuth,
        becomeProvider
    }
}
