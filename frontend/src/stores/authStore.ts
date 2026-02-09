import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { authApi, tokenStorage } from '../api/authService'
import type { User, LoginPayload, SignupPayload } from '../types/auth'

export const useAuthStore = defineStore('auth', () => {
  const user = ref<User | null>(tokenStorage.getUser())
  const loading = ref(false)
  const error = ref<string | null>(null)

  const isAuthenticated = computed(() => !!user.value && !!tokenStorage.getAccessToken())
  const isProvider = computed(() => user.value?.is_provider ?? false)
  const fullName = computed(() => {
    if (!user.value) return ''
    return user.value.last_name
      ? `${user.value.first_name} ${user.value.last_name}`
      : user.value.first_name
  })

  function handleAuthResponse(data: { access_token: string; refresh_token: string; user: User }): void {
    tokenStorage.setTokens(data.access_token, data.refresh_token)
    tokenStorage.setUser(data.user)
    user.value = data.user
    error.value = null
  }

  async function login(payload: LoginPayload): Promise<boolean> {
    loading.value = true
    error.value = null

    try {
      const data = await authApi.login(payload)
      handleAuthResponse(data)
      return true
    } catch (e) {
      error.value = e instanceof Error ? e.message : 'Login failed'
      return false
    } finally {
      loading.value = false
    }
  }

  async function signup(payload: SignupPayload): Promise<boolean> {
    loading.value = true
    error.value = null

    try {
      const data = await authApi.signup(payload)
      handleAuthResponse(data)
      return true
    } catch (e) {
      error.value = e instanceof Error ? e.message : 'Registration failed'
      return false
    } finally {
      loading.value = false
    }
  }

  async function refreshSession(): Promise<boolean> {
    const refreshToken = tokenStorage.getRefreshToken()
    if (!refreshToken) return false

    try {
      const data = await authApi.refreshToken(refreshToken)
      handleAuthResponse(data)
      return true
    } catch {
      logout()
      return false
    }
  }

  async function fetchUser(): Promise<void> {
    try {
      const me = await authApi.getMe()
      user.value = me
      tokenStorage.setUser(me)
    } catch {
      logout()
    }
  }

  function logout(): void {
    tokenStorage.clear()
    user.value = null
    error.value = null
  }

  return {
    user,
    loading,
    error,
    isAuthenticated,
    isProvider,
    fullName,
    login,
    signup,
    refreshSession,
    fetchUser,
    logout,
  }
})
