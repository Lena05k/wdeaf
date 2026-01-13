import { ref, computed, onMounted } from 'vue'

const COLOR_SCHEME = {
    light: {
        primary: '#0055FF',
        white: '#FFFFFF',
        bg: { primary: '#FFFFFF', secondary: '#F5F5F5' },
        text: { primary: '#0F1319', secondary: '#666666' },
        border: '#DDDDDD'
    },
    dark: {
        primary: '#0055FF',
        white: '#FFFFFF',
        bg: { primary: '#0F1319', secondary: '#1a1f2e' },
        text: { primary: '#FFFFFF', secondary: '#CCCCCC' },
        border: '#0055FF'
    }
}

export function useTheme() {
    const theme = ref('light')
    const colors = ref(COLOR_SCHEME.light)

    const initTheme = () => {
        if (window.Telegram?.WebApp) {
            const tg = window.Telegram.WebApp
            const isDark = tg.colorScheme === 'dark'

            theme.value = isDark ? 'dark' : 'light'
            colors.value = isDark ? COLOR_SCHEME.dark : COLOR_SCHEME.light

            // Слушаем изменения в реальном времени
            tg.onEvent('themeChanged', () => {
                const newIsDark = tg.colorScheme === 'dark'
                theme.value = newIsDark ? 'dark' : 'light'
                colors.value = newIsDark ? COLOR_SCHEME.dark : COLOR_SCHEME.light
            })
        }
    }

    return {
        theme,
        colors,
        isDark: computed(() => theme.value === 'dark'),
        initTheme
    }
}
