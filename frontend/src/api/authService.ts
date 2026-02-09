/**
 * Authentication Service for WDEAF
 * Supports: Email/Password, Phone (Telegram auth coming soon)
 */

import { apiRequest } from './client'
import type { AuthResponse, LoginPayload, SignupPayload, PhoneAuthPayload, User } from '../types/auth'

const TOKEN_KEY = 'wdeaf_auth_token'
const REFRESH_KEY = 'wdeaf_refresh_token'
const USER_KEY = 'wdeaf_user_data'

export const authApi = {
  async login(payload: LoginPayload): Promise<AuthResponse> {
    return apiRequest<AuthResponse>('/api/auth/login', {
      method: 'POST',
      body: JSON.stringify(payload),
    })
  },

  async signup(payload: SignupPayload): Promise<AuthResponse> {
    return apiRequest<AuthResponse>('/api/auth/signup', {
      method: 'POST',
      body: JSON.stringify(payload),
    })
  },

  async loginPhone(payload: PhoneAuthPayload): Promise<AuthResponse> {
    return apiRequest<AuthResponse>('/api/auth/phone', {
      method: 'POST',
      body: JSON.stringify(payload),
    })
  },

  async refreshToken(refreshToken: string): Promise<AuthResponse> {
    return apiRequest<AuthResponse>('/api/auth/refresh', {
      method: 'POST',
      body: JSON.stringify({ refresh_token: refreshToken }),
    })
  },

  async getMe(): Promise<User> {
    return apiRequest<User>('/api/auth/me')
  },
}

export const tokenStorage = {
  setTokens(access: string, refresh: string): void {
    localStorage.setItem(TOKEN_KEY, access)
    localStorage.setItem(REFRESH_KEY, refresh)
  },

  getAccessToken(): string | null {
    return localStorage.getItem(TOKEN_KEY)
  },

  getRefreshToken(): string | null {
    return localStorage.getItem(REFRESH_KEY)
  },

  setUser(user: User): void {
    localStorage.setItem(USER_KEY, JSON.stringify(user))
  },

  getUser(): User | null {
    const raw = localStorage.getItem(USER_KEY)
    return raw ? JSON.parse(raw) : null
  },

  clear(): void {
    localStorage.removeItem(TOKEN_KEY)
    localStorage.removeItem(REFRESH_KEY)
    localStorage.removeItem(USER_KEY)
  },
}
