import { createRouter, createWebHistory, RouteRecordRaw } from 'vue-router'

import HomePage from '../pages/HomePage.vue'
import CatalogPage from '../pages/CatalogPage.vue'
import OrdersPage from '../pages/OrdersPage.vue'
import ProfilePage from '../pages/ProfilePage.vue'
import ServiceDetailPage from '../pages/ServiceDetailPage.vue'
import ProviderProfilePage from '../pages/ProviderProfilePage.vue'
import ProviderDashboardPage from '../pages/ProviderDashboardPage.vue'
import LoginPage from '../pages/auth/LoginPage.vue'
import SignupPage from '../pages/auth/SignupPage.vue'
import ForgotPasswordPage from '../pages/auth/ForgotPasswordPage.vue'
import NotFoundPage from '../pages/NotFoundPage.vue'

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
    path: '/provider-dashboard',
    name: 'provider-dashboard',
    component: () => {
      console.log('📊 Loading ProviderDashboard component')
      return import('../pages/ProviderDashboardPage.vue')
          .then(module => {
            console.log('✅ ProviderDashboard loaded successfully!', module)
            return module
          })
          .catch(error => {
            console.error('❌ Failed to load ProviderDashboard:', error)
            throw error
          })
    }
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

// Логирование всех навигаций
router.beforeEach((to, from, next) => {
  console.log(`🔄 Navigating from "${from.name || 'initial'}" to "${to.name}"`)
  console.log('📍 Available routes:', routes.map(r => ({ name: r.name, path: r.path })))
  next()
})

router.afterEach((to) => {
  console.log(`✅ Successfully navigated to "${to.name}"`)
  console.log('Current URL:', window.location.href)
})

router.onError((error) => {
  console.error('❌ Router error:', error)
  console.error('Stack:', error.stack)
})


export default router
