import { ApiClient } from '@/utils/api'

export interface Order {
    id: number
    service_id: number
    service_name: string
    provider_id: number
    provider_name: string
    status: 'pending' | 'active' | 'completed' | 'cancelled'
    price: number
    created_at: string
    scheduled_date?: string
    notes?: string
}

export interface CreateOrderPayload {
    service_id: number
    scheduled_date?: string
    notes?: string
}

const apiClient = new ApiClient(
    import.meta.env.VITE_API_URL || 'https://api.wdeaf.app'
)

export const ordersApi = {
    list: async (status?: string): Promise<Order[]> => {
        const query = status ? `?status=${status}` : ''
        return apiClient.get(`/orders/my${query}`)
    },

    getById: async (orderId: number): Promise<Order> => {
        return apiClient.get(`/orders/${orderId}`)
    },

    create: async (payload: CreateOrderPayload): Promise<Order> => {
        return apiClient.post('/orders/create', payload)
    },

    cancel: async (orderId: number): Promise<{ success: boolean }> => {
        return apiClient.post(`/orders/${orderId}/cancel`, {})
    },

    updateStatus: async (orderId: number, status: string): Promise<Order> => {
        return apiClient.put(`/orders/${orderId}/status`, { status })
    }
}
