/**
 * Profile Types for WDEAF TMA
 * Centralized type definitions for profile-related components
 */

export interface User {
  id: string | number
  first_name?: string
  username?: string
  photo_url?: string
}

export interface ProfileStats {
  ordersCount: number
  rating: number
  reviewsCount?: number
  completedOrders?: number
}

export interface ServiceAvailability {
  weekdays: boolean
  weekends: boolean
  evenings: boolean
}

export interface ServiceImage {
  file?: File
  preview?: string
  url?: string
}

export interface Service {
  id: string
  serviceName: string
  name?: string
  description: string
  category: ServiceCategory
  price: number
  timezone?: string
  images?: ServiceImage[]
  availability?: ServiceAvailability
  rating?: number
  reviewsCount?: number
  providerId?: string
  createdAt?: string
  updatedAt?: string
}

export type ServiceCategory = 
  | 'repair' 
  | 'business' 
  | 'fashion' 
  | 'education' 
  | 'design' 
  | 'it'

export interface ProviderFormData {
  serviceName: string
  description: string
  category: string
  price: number
  timezone: string
  availability: ServiceAvailability
  images: ServiceImage[]
}

export interface ProviderProfile {
  userId: string
  services: Service[]
  rating: number
  completedOrders: number
  reviewsCount: number
  joinedAt: string
}

// Event emits types
export interface ProfileEmits {
  'open-settings': []
  'show-toast': [message: string]
}

export interface ProfileActionsEmits {
  'open-become-provider': []
  'open-provider-dashboard': []
  'open-settings': []
}

export interface ServiceDetailsEmits {
  'close': []
  'delete': []
  'edit': []
}

export interface BecomeProviderModalEmits {
  'close': []
  'submit': [data: ProviderFormData]
}

export interface ProviderServicesListEmits {
  'select-service': [service: Service]
  'add-service': []
}
