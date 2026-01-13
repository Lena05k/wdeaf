import { ref, computed } from 'vue'

export interface Service {
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
    currentImageIndex?: number
}

export function useSearch(services: Service[]) {
    const searchQuery = ref<string>('')
    const selectedCategory = ref<string>('')

    const filteredServices = computed((): Service[] => {
        return services.filter(service => {
            const matchesSearch =
                service.name.toLowerCase().includes(searchQuery.value.toLowerCase()) ||
                service.provider.toLowerCase().includes(searchQuery.value.toLowerCase()) ||
                service.description.toLowerCase().includes(searchQuery.value.toLowerCase())

            const matchesCategory = !selectedCategory.value ||
                service.category === selectedCategory.value

            return matchesSearch && matchesCategory
        })
    })

    const resetFilters = (): void => {
        searchQuery.value = ''
        selectedCategory.value = ''
    }

    return {
        searchQuery,
        selectedCategory,
        filteredServices,
        resetFilters
    }
}
