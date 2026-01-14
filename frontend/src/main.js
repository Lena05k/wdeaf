import { createApp } from 'vue'
import { createPinia } from 'pinia'
import App from './App.vue'
import router from './router'


// Initialize app
const app = createApp(App)

// Use Pinia store
const pinia = createPinia()
app.use(pinia)

// Use router
app.use(router)

// Initialize Telegram WebApp
if (window.Telegram?.WebApp) {
    const tg = window.Telegram.WebApp

    // Ready the app
    tg.ready()

    // Expand to full height
    tg.expand()

    // Set header color
    tg.setHeaderColor('#0F1319')

    // Disable vertical swipe
    tg.disableVerticalSwipes()

    // Enable closing confirmation
    tg.enableClosingConfirmation()

    // Store user data from Telegram in global
    if (tg.initData) {
        try {
            const params = new URLSearchParams(tg.initData)
            const userData = params.get('user')
            if (userData) {
                window.telegramUser = JSON.parse(userData)
            }
        } catch (e) {
            console.error('Error parsing Telegram user:', e)
        }
    }
}

// Handle back button
if (window.Telegram?.WebApp) {
    const tg = window.Telegram.WebApp

    tg.onEvent('backButtonClicked', () => {
        router.back()
    })

    // Show/hide back button based on route
    router.afterEach((to) => {
        if (to.name === 'login' || to.name === 'signup' || to.name === 'home') {
            tg.BackButton.hide()
        } else {
            tg.BackButton.show()
        }
    })
}

app.mount('#app')