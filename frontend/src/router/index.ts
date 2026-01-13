import { createRouter, createWebHistory, RouteRecordRaw } from 'vue-router'
import { useAuthStore } from '../stores/userStore'

// Layouts
import MainLayout from '@/layouts/MainLayout.vue'
import AuthLayout from '@/layouts/AuthLayout.vue'

// Pages
import HomePage from '@/pages/HomePage.vue'
import CatalogPage from '@/pages/CatalogPage.vue'
import OrdersPage from '@/pages/OrdersPage.vue'
import ProfilePage from '@/pages/ProfilePage.vue'
import ServiceDetailPage from '@/pages/ServiceDetailPage.vue'
import ProviderProfilePage from '@/pages/ProviderProfilePage.vue'
import LoginPage from '@/pages/auth/LoginPage.vue'
import SignupPage from '@/pages/auth/SignupPage.vue'
import ForgotPasswordPage from '@/pages/auth/ForgotPasswordPage.vue'
import NotFoundPage from '@/pages/NotFoundPage.vue'

const routes: RouteRecordRaw[] = [
    // Auth Routes
    {
        path: '/auth',
        component: AuthLayout,
        meta: { requiresGuest: true },
        children: [
            {
                path: 'login',
                name: 'Login',
                component: LoginPage,
                meta: {
                    title: 'Вход - WDEAF',
                    description: 'Войдите в свой аккаунт'
                }
            },
            {
                path: 'signup',
                name: 'Signup',
                component: SignupPage,
                meta: {
                    title: 'Регистрация - WDEAF',
                    description: 'Создайте новый аккаунт'
                }
            },
            {
                path: 'forgot-password',
                name: 'ForgotPassword',
                component: ForgotPasswordPage,
                meta: {
                    title: 'Восстановление пароля - WDEAF'
                }
            }
        ]
    },

    // Main App Routes
    {
        path: '/',
        component: MainLayout,
        meta: { requiresAuth: true },
        children: [
            {
                path: '',
                name: 'Home',
                component: HomePage,
                meta: {
                    title: 'WDEAF - Платформа услуг',
                    description: 'Найдите нужную услугу быстро и легко',
                    tab: 'browse'
                }
            },
            {
                path: 'catalog',
                name: 'Catalog',
                component: CatalogPage,
                meta: {
                    title: 'Каталог услуг - WDEAF',
                    description: 'Просмотрите все категории услуг',
                    tab: 'catalog'
                }
            },
            {
                path: 'orders',
                name: 'Orders',
                component: OrdersPage,
                meta: {
                    title: 'Мои заказы - WDEAF',
                    description: 'Управляйте своими заказами',
                    tab: 'orders'
                }
            },
            {
                path: 'profile',
                name: 'Profile',
                component: ProfilePage,
                meta: {
                    title: 'Мой профиль - WDEAF',
                    description: 'Управляйте профилем',
                    tab: 'profile'
                }
            },
            {
                path: 'service/:id',
                name: 'ServiceDetail',
                component: ServiceDetailPage,
                meta: {
                    title: 'Детали услуги - WDEAF'
                }
            },
            {
                path: 'provider/:id',
                name: 'ProviderProfile',
                component: ProviderProfilePage,
                meta: {
                    title: 'Профиль исполнителя - WDEAF'
                }
            }
        ]
    },

    // 404 Not Found
    {
        path: '/:pathMatch(.*)*',
        name: 'NotFound',
        component: NotFoundPage,
        meta: {
            title: 'Страница не найдена - WDEAF'
        }
    }
]

const router = createRouter({
    history: createWebHistory(import.meta.env.BASE_URL),
    routes,
    scrollBehavior(to, from, savedPosition) {
        if (savedPosition) {
            return savedPosition
        } else {
            return { top: 0 }
        }
    }
})

// Navigation Guards
router.beforeEach((to, from, next) => {
    const authStore = useAuthStore()

    // Установить title
    if (to.meta.title) {
        document.title = to.meta.title as string
    }

    // Проверка требуемой аутентификации
    if (to.meta.requiresAuth && !authStore.isAuthenticated) {
        next({ name: 'Login', query: { redirect: to.fullPath } })
        return
    }

    // Проверка для гостей (redirect если уже авторизирован)
    if (to.meta.requiresGuest && authStore.isAuthenticated) {
        next({ name: 'Home' })
        return
    }

    next()
})

router.afterEach((to) => {
    // Отправить аналитику или обновить метатеги
    if (to.meta.description) {
        const metaDescription = document.querySelector('meta[name="description"]')
        if (metaDescription) {
            metaDescription.setAttribute('content', to.meta.description as string)
        }
    }
})

export default router
