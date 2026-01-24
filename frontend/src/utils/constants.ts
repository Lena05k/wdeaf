export const CATEGORIES = [
    { id: 1, name: 'Ремонт', slug: 'repair', icon: '🔧' },
    { id: 2, name: 'Бизнес', slug: 'business', icon: '📊' },
    { id: 3, name: 'Мода', slug: 'fashion', icon: '✂️' },
    { id: 4, name: 'Обучение', slug: 'education', icon: '📖' },
    { id: 5, name: 'Дизайн', slug: 'design', icon: '🎭' },
    { id: 6, name: 'IT', slug: 'it', icon: '💻' }
] as const

export const PAGINATION = {
    pageSize: 20,
    preloadPages: 2
} as const

export const CACHE_TTL = {
    services: 3600, // 1 hour
    reviews: 1800, // 30 min
    provider: 1800, // 30 min
    user: 300 // 5 min
} as const

export const TOAST_DURATION = 3000

export const ORDER_STATUSES = {
    pending: 'В ожидании',
    active: 'Активен',
    completed: 'Завершен',
    cancelled: 'Отменен'
} as const

export const API_ENDPOINTS = {
    services: '/services',
    providers: '/providers',
    orders: '/orders',
    users: '/users'
} as const
