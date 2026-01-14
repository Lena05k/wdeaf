import { createRouter, createWebHistory, RouteRecordRaw } from 'vue-router'

// Pages
import HomePage from '@/pages/HomePage.vue'
import CatalogPage from '@/pages/CatalogPage.vue'
import OrdersPage from '@/pages/OrdersPage.vue'
import ProfilePage from '@/pages/ProfilePage.vue'
import ServiceDetailPage from '@/pages/ServiceDetailPage.vue'
import ProviderProfilePage from '@/pages/ProviderProfilePage.vue'
import LoginPage from '@/pages/LoginPage.vue'
import SignupPage from '@/pages/SignupPage.vue'
import ForgotPasswordPage from '@/pages/ForgotPasswordPage.vue'
import NotFoundPage from '@/pages/NotFoundPage.vue'

const routes: Array<RouteRecordRaw> = [
  {
    path: '/',
    name: 'home',
    component: HomePage
  },
  {
    path: '/catalog',
    name: 'catalog',
    component: CatalogPage
  },
  {
    path: '/orders',
    name: 'orders',
    component: OrdersPage
  },
  {
    path: '/profile',
    name: 'profile',
    component: ProfilePage
  },
  {
    path: '/service/:id',
    name: 'service-detail',
    component: ServiceDetailPage
  },
  {
    path: '/provider/:name',
    name: 'provider-profile',
    component: ProviderProfilePage
  },
  {
    path: '/login',
    name: 'login',
    component: LoginPage
  },
  {
    path: '/signup',
    name: 'signup',
    component: SignupPage
  },
  {
    path: '/forgot-password',
    name: 'forgot-password',
    component: ForgotPasswordPage
  },
  {
    path: '/:pathMatch(.*)*',
    name: 'not-found',
    component: NotFoundPage
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

// ⏸️ Аутентификация временно отключена
// Раскомментируйте когда нужна проверка прав доступа

export default router
