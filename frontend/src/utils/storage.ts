interface CacheItem<T = any> {
    value: T
    timestamp: number
    ttl: number | null
}

export class StorageManager {
    private static readonly DB_NAME = 'wdeaf_cache'
    private static readonly STORE_NAME = 'cache'

    static async setItem<T = any>(
        key: string,
        value: T,
        ttl: number | null = null
    ): Promise<void> {
        const data: CacheItem<T> = {
            value,
            timestamp: Date.now(),
            ttl
        }
        localStorage.setItem(key, JSON.stringify(data))
    }

    static async getItem<T = any>(key: string): Promise<T | null> {
        const stored = localStorage.getItem(key)
        if (!stored) return null

        try {
            const { value, timestamp, ttl } = JSON.parse(stored) as CacheItem<T>

            if (ttl && Date.now() - timestamp > ttl) {
                localStorage.removeItem(key)
                return null
            }

            return value
        } catch {
            return null
        }
    }

    static async removeItem(key: string): Promise<void> {
        localStorage.removeItem(key)
    }

    static async clear(): Promise<void> {
        localStorage.clear()
    }

    static async getCacheSize(): Promise<number> {
        let size = 0
        for (let key in localStorage) {
            if (localStorage.hasOwnProperty(key)) {
                size += localStorage[key].length + key.length
            }
        }
        return size
    }

    static async clearExpiredItems(): Promise<void> {
        const keys = Object.keys(localStorage)
        keys.forEach(key => {
            const stored = localStorage.getItem(key)
            if (stored) {
                try {
                    const { timestamp, ttl } = JSON.parse(stored) as CacheItem
                    if (ttl && Date.now() - timestamp > ttl) {
                        localStorage.removeItem(key)
                    }
                } catch {
                    // Ignore parse errors
                }
            }
        })
    }
}
