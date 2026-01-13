import { ApiClient } from '@/utils/api'

interface ProviderProfile {
    id: number
    name: string
    rating: number
    reviews_count: number
    response_time: string
    photo_url?: string
    bio?: string
    services_count: number
    joined_date: string
}

interface ProviderReview {
    id: number
    author: string
    rating: number
    text: string
    date: string
}

interface ProviderPortfolio {
    id: number
    image_url: string
    title: string
    description: string
}

const apiClient = new ApiClient(
    import.meta.env.VITE_API_URL || 'https://api.wdeaf.app'
)

export const providersApi = {
    getProfile: async (providerId: number): Promise<ProviderProfile> => {
        return apiClient.get(`/providers/${providerId}`)
    },

    getReviews: async (providerId: number, page: number = 1): Promise<ProviderReview[]> => {
        return apiClient.get(`/providers/${providerId}/reviews?page=${page}`)
    },

    getPortfolio: async (providerId: number): Promise<ProviderPortfolio[]> => {
        return apiClient.get(`/providers/${providerId}/portfolio`)
    },

    searchProviders: async (query: string): Promise<ProviderProfile[]> => {
        return apiClient.get(`/providers/search?q=${encodeURIComponent(query)}`)
    }
}
