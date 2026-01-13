declare global {
    interface Window {
        Telegram?: {
            WebApp: {
                ready(): void
                close(): void
                sendData(data: string): void
                onEvent(eventType: string, callback: () => void): void
                offEvent(eventType: string, callback: () => void): void
                setHeaderColor(color: string): void
                colorScheme: 'light' | 'dark'
                initDataUnsafe: {
                    user?: {
                        id: number
                        is_bot: boolean
                        first_name: string
                        last_name?: string
                        username?: string
                        language_code?: string
                        is_premium?: boolean
                        photo_url?: string
                    }
                    auth_date: number
                    hash: string
                }
            }
        }
    }
}

export {}
