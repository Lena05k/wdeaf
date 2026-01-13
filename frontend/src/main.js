import { createApp } from 'vue'
import { createPinia } from 'pinia'
import App from './App.vue'
import router from './router'

// Импортируем stores для инициализации
import { useThemeStore } from '../src/stores/themeStore.js'
import { useAuthStore } from '../src/stores/userStore'
import { useServiceStore } from '../src/stores/servicesStore.js'

const app = createApp(App)

const pinia = createPinia()
app.use(pinia)

const themeStore = useThemeStore()
themeStore.initTheme()

const authStore = useAuthStore()
authStore.initAuth()

const serviceStore = useServiceStore()
serviceStore.loadFavorites()

app.use(router)
app.mount('#app')
