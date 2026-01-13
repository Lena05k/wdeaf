interface RequestConfig {
    method?: 'GET' | 'POST' | 'PUT' | 'DELETE' | 'PATCH'
    headers?: Record<string, string>
    body?: any
    timeout?: number
}

export class ApiClient {
    private baseURL: string
    private timeout: number = 10000

    constructor(baseURL: string) {
        this.baseURL = baseURL
    }

    async request<T = any>(
        endpoint: string,
        config: RequestConfig = {}
    ): Promise<T> {
        const url = `${this.baseURL}${endpoint}`
        const method = config.method || 'GET'
        const headers: Record<string, string> = {
            'Content-Type': 'application/json',
            ...config.headers
        }

        const token = localStorage.getItem('auth_token')
        if (token) {
            headers['Authorization'] = `Bearer ${token}`
        }

        const options: RequestInit = {
            method,
            headers
        }

        if (config.body) {
            options.body = JSON.stringify(config.body)
        }

        try {
            const controller = new AbortController()
            const timeout = setTimeout(
                () => controller.abort(),
                config.timeout || this.timeout
            )

            const response = await fetch(url, {
                ...options,
                signal: controller.signal
            })

            clearTimeout(timeout)

            if (!response.ok) {
                throw new Error(`HTTP ${response.status}: ${response.statusText}`)
            }

            return await response.json()
        } catch (error) {
            if (error instanceof Error) {
                throw new Error(`API Error: ${error.message}`)
            }
            throw error
        }
    }

    get<T = any>(endpoint: string, config?: RequestConfig): Promise<T> {
        return this.request<T>(endpoint, { ...config, method: 'GET' })
    }

    post<T = any>(endpoint: string, body: any, config?: RequestConfig): Promise<T> {
        return this.request<T>(endpoint, { ...config, method: 'POST', body })
    }

    put<T = any>(endpoint: string, body: any, config?: RequestConfig): Promise<T> {
        return this.request<T>(endpoint, { ...config, method: 'PUT', body })
    }

    delete<T = any>(endpoint: string, config?: RequestConfig): Promise<T> {
        return this.request<T>(endpoint, { ...config, method: 'DELETE' })
    }
}
