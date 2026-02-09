export interface User {
  id: number
  telegram_id?: number | null
  email?: string | null
  first_name: string
  last_name?: string | null
  username?: string | null
  phone?: string | null
  is_provider: boolean
  auth_provider: string
}

export interface AuthResponse {
  access_token: string
  refresh_token: string
  token_type: string
  user: User
}

export interface LoginPayload {
  email: string
  password: string
}

export interface SignupPayload {
  email: string
  password: string
  first_name: string
  last_name?: string
}

export interface PhoneAuthPayload {
  phone: string
  first_name: string
  last_name?: string
  username?: string
}
