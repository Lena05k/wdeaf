import { ApiClient } from '@/utils/api'

interface ServiceFilters {
    category?: string
    search?: string
    page?: number
    limit?: number
    sort?: 'price' | 'rating' | 'reviews'
}

interface ServiceResponse {
    id: number
    name: string
    provider: string
    category: string
    description: string
    fullDescription: string
    price: number
    reviews: number
    response_time: string
    providerRating: number
    images: string[]
}

const apiClient = new ApiClient(
    import.meta.env.VITE_API_URL || 'https://api.wdeaf.app'
)

export const servicesApi = {
    list: async (filters: ServiceFilters = {}): Promise<ServiceResponse[]> => {
        const params = new URLSearchParams()
        if (filters.category) params.append('category', filters.category)
        if (filters.search) params.append('search', filters.search)
        if (filters.page) params.append('page', filters.page.toString())
        if (filters.limit) params.append('limit', filters.limit.toString())
        if (filters.sort) params.append('sort', filters.sort)

        return apiClient.get(`/services?${params.toString()}`)
    },

    getById: async (id: number): Promise<ServiceResponse> => {
        return apiClient.get(`/services/${id}`)
    },

    getByProvider: async (providerId: number): Promise<ServiceResponse[]> => {
        return apiClient.get(`/services/provider/${providerId}`)
    },

    search: async (query: string): Promise<ServiceResponse[]> => {
        return apiClient.get('/services/search', {
            headers: { 'X-Search-Query': query }
        })
    }
}
