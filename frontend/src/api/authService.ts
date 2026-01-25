/**
 * Authentication Service
 * Handles login/signup for both Telegram Web Apps and phone-based auth
 */

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'

interface User {
  id: string | number
  first_name: string
  last_name?: string
  username?: string
  phone?: string
}

interface AuthResponse {
  access_token: string
  token_type: string
  user: User
}

interface PhoneAuthPayload {
  phone: string
  first_name: string
  username?: string
}

/**
 * Telegram Web Apps Integration
 * Based on: https://core.telegram.org/bots/webapps
 */
class AuthService {
  private tokenKey = 'wdeaf_auth_token'
  private userKey = 'wdeaf_user_data'

  /**
   * Initialize Telegram Web App
   * Call this once when app loads
   */
  initTelegramWebApp(): void {
    if (!window.Telegram?.WebApp) {
      console.warn('Telegram Web App SDK not available')
      return
    }

    const tg = window.Telegram.WebApp
    
    // Инициализируем приложение
    tg.ready()
    
    // Устанавливаем цвет header по цвету Telegram
    const headerColor = tg.themeParams?.bg_color || '#FFFFFF'
    tg.setHeaderColor(headerColor)
    
    console.log('✅ Telegram Web App initialized')
  }

  /**
   * Login with Telegram
   * @param initData - Telegram initData from window.Telegram.WebApp.initData
   */
  async loginWithTelegram(initData: string): Promise<AuthResponse> {
    try {
      const response = await fetch(`${API_BASE_URL}/api/auth/telegram`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ init_data: initData }),
      })

      if (!response.ok) {
        const error = await response.json()
        throw new Error(error.detail || 'Telegram auth failed')
      }

      const data = await response.json() as AuthResponse
      return data
    } catch (error) {
      console.error('Telegram auth error:', error)
      throw error
    }
  }

  /**
   * Login with phone number
   * @param payload - Phone, name, and optional Telegram username
   */
  async loginWithPhone(payload: PhoneAuthPayload): Promise<AuthResponse> {
    try {
      const response = await fetch(`${API_BASE_URL}/api/auth/phone`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(payload),
      })

      if (!response.ok) {
        const error = await response.json()
        throw new Error(error.detail || 'Phone auth failed')
      }

      const data = await response.json() as AuthResponse
      return data
    } catch (error) {
      console.error('Phone auth error:', error)
      throw error
    }
  }

  /**
   * Refresh access token
   * @param refreshToken - Refresh token from previous auth
   */
  async refreshToken(refreshToken: string): Promise<AuthResponse> {
    try {
      const response = await fetch(`${API_BASE_URL}/api/auth/refresh`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ refresh_token: refreshToken }),
      })

      if (!response.ok) {
        throw new Error('Token refresh failed')
      }

      const data = await response.json() as AuthResponse
      return data
    } catch (error) {
      console.error('Token refresh error:', error)
      throw error
    }
  }

  /**
   * Store auth token
   */
  setToken(token: string): void {
    localStorage.setItem(this.tokenKey, token)
  }

  /**
   * Get stored auth token
   */
  getToken(): string | null {
    return localStorage.getItem(this.tokenKey)
  }

  /**
   * Remove auth token
   */
  removeToken(): void {
    localStorage.removeItem(this.tokenKey)
  }

  /**
   * Store user data
   */
  setUser(user: User): void {
    localStorage.setItem(this.userKey, JSON.stringify(user))
  }

  /**
   * Get stored user data
   */
  getUser(): User | null {
    const data = localStorage.getItem(this.userKey)
    return data ? JSON.parse(data) : null
  }

  /**
   * Check if user is authenticated
   */
  isAuthenticated(): boolean {
    return !!this.getToken()
  }

  /**
   * Logout - clear all stored data
   */
  logout(): void {
    this.removeToken()
    localStorage.removeItem(this.userKey)
  }
}

export const authService = new AuthService()

/**
 * Fetch wrapper with auth token
 * Use this instead of fetch to automatically include auth header
 */
export async function fetchWithAuth(
  url: string,
  options: RequestInit = {}
): Promise<Response> {
  const token = authService.getToken()
  const headers = {
    'Content-Type': 'application/json',
    ...options.headers,
  } as Record<string, string>

  if (token) {
    headers['Authorization'] = `Bearer ${token}`
  }

  return fetch(url, {
    ...options,
    headers,
  })
}