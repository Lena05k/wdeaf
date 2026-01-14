// src/stores/userStore.ts
import { defineStore } from 'pinia'
import { ref, computed } from 'vue'

interface TelegramUser {
  id: number
  is_bot: boolean
  first_name: string
  last_name?: string
  username?: string
  language_code?: string
  is_premium?: boolean
  added_to_attachment_menu?: boolean
  allows_user_initiated_voice_chats?: boolean
  allows_user_initiated_video_chats?: boolean
}

interface User extends TelegramUser {
  authToken?: string
  email?: string
}

export const useUserStore = defineStore('user', () => {
  const user = ref<User | null>(null)
  const isAuthenticated = ref(false)
  const loading = ref(false)

  const setUser = (userData: User) => {
    user.value = userData
    isAuthenticated.value = !!userData.authToken
  }

  const logout = () => {
    user.value = null
    isAuthenticated.value = false
    localStorage.removeItem('authToken')
  }

  const getTelegramUser = (): TelegramUser | null => {
    try {
      if (window.telegramUser) {
        return window.telegramUser
      }
      if (window.Telegram?.WebApp?.initData) {
        const params = new URLSearchParams(window.Telegram.WebApp.initData)
        const userData = params.get('user')
        return userData ? JSON.parse(userData) : null
      }
    } catch (e) {
      console.error('Error getting Telegram user:', e)
    }
    return null
  }

  const initFromTelegram = () => {
    const tgUser = getTelegramUser()
    if (tgUser) {
      setUser({
        ...tgUser,
        authToken: localStorage.getItem('authToken') || undefined,
        email: localStorage.getItem('userEmail') || undefined
      })
    }
  }

  const firstName = computed(() => user.value?.first_name || '')
  const lastName = computed(() => user.value?.last_name || '')
  const fullName = computed(() => 
    `${user.value?.first_name || ''} ${user.value?.last_name || ''}`.trim()
  )
  const username = computed(() => user.value?.username || '')
  const userId = computed(() => user.value?.id || null)

  return {
    // State
    user,
    isAuthenticated,
    loading,
    
    // Actions
    setUser,
    logout,
    getTelegramUser,
    initFromTelegram,
    
    // Computed
    firstName,
    lastName,
    fullName,
    username,
    userId
  }
})
