import { defineStore } from 'pinia'
import { ref, computed } from 'vue'

export interface Service {
    id: number
    name: string
    provider: string
    provider_id: string
    category: string
    description: string
    fullDescription: string
    price: number
    reviews: number
    response_time: string
    providerRating: number
    images: string[]
    currentImageIndex?: number
    created_at: string
    is_favorite?: boolean
}

export const useServiceStore = defineStore('service', () => {
    const services = ref<Service[]>([
        {
            id: 1,
            name: 'Услуга сантехника',
            provider: 'Олег М.',
            provider_id: 'provider_1',
            category: '🏠 Ремонт',
            description: 'Профессиональный ремонт и монтаж сантехники',
            fullDescription: 'Профессиональный ремонт и монтаж сантехники с гарантией. Выполняю любые работы: замену кранов, чистку труб, установку полотенцесушителей. 10 лет опыта, работаю быстро и аккуратно.',
            price: 2500,
            reviews: 156,
            response_time: '< 1 часа',
            providerRating: 4.9,
            images: [
                'https://via.placeholder.com/300x200?text=Сантехника+1',
                'https://via.placeholder.com/300x200?text=Сантехника+2',
                'https://via.placeholder.com/300x200?text=Сантехника+3'
            ],
            created_at: new Date().toISOString()
        },
        {
            id: 2,
            name: 'Консультация бухгалтера',
            provider: 'Мария С.',
            provider_id: 'provider_2',
            category: '💼 Бизнес',
            description: 'Налоговое планирование и бухгалтерская отчетность',
            fullDescription: 'Профессиональная консультация по налоговому планированию, ведение бухгалтерского учета, подготовка отчетности. Помогу оптимизировать налоги и разобраться в законодательстве.',
            price: 3000,
            reviews: 89,
            response_time: '< 2 часов',
            providerRating: 4.7,
            images: [
                'https://via.placeholder.com/300x200?text=Бухгалтер+1',
                'https://via.placeholder.com/300x200?text=Бухгалтер+2'
            ],
            created_at: new Date().toISOString()
        }
    ])

    const searchQuery = ref('')
    const selectedCategory = ref('')
    const favorites = ref<number[]>([])
    const isLoading = ref(false)
    const error = ref<string | null>(null)

    // Computed
    const filteredServices = computed(() => {
        return services.value.filter(service => {
            const matchesSearch = service.name.toLowerCase().includes(searchQuery.value.toLowerCase()) ||
                service.provider.toLowerCase().includes(searchQuery.value.toLowerCase()) ||
                service.description.toLowerCase().includes(searchQuery.value.toLowerCase())
            const matchesCategory = !selectedCategory.value || service.category === selectedCategory.value
            return matchesSearch && matchesCategory
        })
    })

    const categories = computed(() => {
        const cats = new Set(services.value.map(s => s.category))
        return Array.from(cats).sort()
    })

    const favoriteServices = computed(() => {
        return services.value.filter(s => favorites.value.includes(s.id))
    })

    // Methods
    const fetchServices = async (category?: string, search?: string) => {
        isLoading.value = true
        error.value = null

        try {
            // const response = await apiClient.get('/services', {
            //   params: { category, search }
            // })
            // services.value = response.data

            // Mock - услуги уже инициализированы
            if (search) searchQuery.value = search
            if (category) selectedCategory.value = category
        } catch (e) {
            error.value = 'Ошибка загрузки услуг'
        } finally {
            isLoading.value = false
        }
    }

    const getServiceById = (id: number) => {
        return services.value.find(s => s.id === id)
    }

    const toggleFavorite = (serviceId: number) => {
        const index = favorites.value.indexOf(serviceId)
        if (index > -1) {
            favorites.value.splice(index, 1)
        } else {
            favorites.value.push(serviceId)
        }
        localStorage.setItem('favorites', JSON.stringify(favorites.value))
    }

    const isFavorite = (serviceId: number) => {
        return favorites.value.includes(serviceId)
    }

    const setSearchQuery = (query: string) => {
        searchQuery.value = query
    }

    const setSelectedCategory = (category: string) => {
        selectedCategory.value = category
    }

    const loadFavorites = () => {
        const saved = localStorage.getItem('favorites')
        if (saved) {
            try {
                favorites.value = JSON.parse(saved)
            } catch (e) {
                favorites.value = []
            }
        }
    }

    return {
        // State
        services,
        searchQuery,
        selectedCategory,
        favorites,
        isLoading,
        error,

        // Computed
        filteredServices,
        categories,
        favoriteServices,

        // Methods
        fetchServices,
        getServiceById,
        toggleFavorite,
        isFavorite,
        setSearchQuery,
        setSelectedCategory,
        loadFavorites
    }
})
