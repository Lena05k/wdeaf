import { defineStore } from 'pinia'
import { ref, watch, computed } from 'vue'

type Theme = 'light' | 'dark' | 'auto'

export const useThemeStore = defineStore('theme', () => {
    const currentTheme = ref<Theme>('dark')
    const prefersDark = ref(
        window.matchMedia('(prefers-color-scheme: dark)').matches
    )

    // Определить активную тему
    const activeTheme = computed(() => {
        if (currentTheme.value === 'auto') {
            return prefersDark.value ? 'dark' : 'light'
        }
        return currentTheme.value
    })

    // Инициализация из localStorage
    const initTheme = () => {
        const saved = localStorage.getItem('theme') as Theme | null
        if (saved && ['light', 'dark', 'auto'].includes(saved)) {
            currentTheme.value = saved
        }

        // Слушаем системные изменения
        const mediaQuery = window.matchMedia('(prefers-color-scheme: dark)')
        mediaQuery.addEventListener('change', (e) => {
            prefersDark.value = e.matches
            applyTheme()
        })

        applyTheme()
    }

    // Применить тему к DOM
    const applyTheme = () => {
        const html = document.documentElement
        const theme = activeTheme.value

        if (theme === 'dark') {
            html.setAttribute('data-color-scheme', 'dark')
            html.classList.add('dark')
            html.classList.remove('light')
        } else {
            html.setAttribute('data-color-scheme', 'light')
            html.classList.add('light')
            html.classList.remove('dark')
        }
    }

    // Смена темы
    const setTheme = (theme: Theme) => {
        currentTheme.value = theme
        localStorage.setItem('theme', theme)
        applyTheme()
    }

    // Переключение между light/dark
    const toggleTheme = () => {
        if (activeTheme.value === 'dark') {
            setTheme('light')
        } else {
            setTheme('dark')
        }
    }

    // Автоматическая тема (система)
    const setAutoTheme = () => {
        setTheme('auto')
    }

    // Следить за изменениями темы
    watch(() => currentTheme.value, () => {
        applyTheme()
    })

    return {
        currentTheme,
        activeTheme,
        prefersDark,
        initTheme,
        setTheme,
        toggleTheme,
        setAutoTheme
    }
})
