import { defineStore } from 'pinia'
import { ref, computed } from 'vue'

export interface Order {
    id: string | number
    service_id: number
    service: string
    provider: string
    provider_id: string
    status: 'pending' | 'active' | 'completed' | 'cancelled'
    price: number
    date: string
    scheduled_date?: string
    notes?: string
    created_at: string
    updated_at: string
}

export const useOrderStore = defineStore('order', () => {
    const orders = ref<Order[]>([
        {
            id: 1,
            service_id: 4,
            service: 'Уроки английского',
            provider: 'Джон Д.',
            provider_id: 'provider_4',
            status: 'active',
            price: 1500,
            date: 'сегодня 15:00',
            created_at: new Date().toISOString(),
            updated_at: new Date().toISOString()
        },
        {
            id: 2,
            service_id: 2,
            service: 'Консультация бухгалтера',
            provider: 'Мария С.',
            provider_id: 'provider_2',
            status: 'pending',
            price: 3000,
            date: 'завтра 10:00',
            created_at: new Date().toISOString(),
            updated_at: new Date().toISOString()
        }
    ])

    const isLoading = ref(false)
    const error = ref<string | null>(null)

    // Computed
    const activeOrders = computed(() => {
        return orders.value.filter(o => o.status === 'active' || o.status === 'pending')
    })

    const completedOrders = computed(() => {
        return orders.value.filter(o => o.status === 'completed')
    })

    const totalSpent = computed(() => {
        return orders.value
            .filter(o => o.status !== 'cancelled')
            .reduce((sum, o) => sum + o.price, 0)
    })

    // Methods
    const fetchOrders = async () => {
        isLoading.value = true
        error.value = null

        try {
            // const response = await apiClient.get('/orders')
            // orders.value = response.data
        } catch (e) {
            error.value = 'Ошибка загрузки заказов'
        } finally {
            isLoading.value = false
        }
    }

    const createOrder = async (serviceId: number, serviceName: string, provider: string, price: number, notes?: string, scheduledDate?: string) => {
        isLoading.value = true
        error.value = null

        try {
            // const response = await apiClient.post('/orders', {
            //   service_id: serviceId,
            //   notes,
            //   scheduled_date: scheduledDate
            // })

            const newOrder: Order = {
                id: Date.now(),
                service_id: serviceId,
                service: serviceName,
                provider: provider,
                provider_id: `provider_${serviceId}`,
                status: 'pending',
                price: price,
                date: scheduledDate || new Date().toLocaleString('ru-RU'),
                notes: notes,
                created_at: new Date().toISOString(),
                updated_at: new Date().toISOString()
            }

            orders.value.unshift(newOrder)
            return newOrder
        } catch (e) {
            error.value = 'Ошибка создания заказа'
            throw e
        } finally {
            isLoading.value = false
        }
    }

    const getOrderById = (id: string | number) => {
        return orders.value.find(o => o.id === id)
    }

    const cancelOrder = async (id: string | number) => {
        isLoading.value = true
        error.value = null

        try {
            // await apiClient.patch(`/orders/${id}`, { status: 'cancelled' })

            const order = orders.value.find(o => o.id === id)
            if (order) {
                order.status = 'cancelled'
                order.updated_at = new Date().toISOString()
            }
        } catch (e) {
            error.value = 'Ошибка отмены заказа'
            throw e
        } finally {
            isLoading.value = false
        }
    }

    const updateOrderStatus = async (id: string | number, status: Order['status']) => {
        isLoading.value = true
        error.value = null

        try {
            // await apiClient.patch(`/orders/${id}`, { status })

            const order = orders.value.find(o => o.id === id)
            if (order) {
                order.status = status
                order.updated_at = new Date().toISOString()
            }
        } catch (e) {
            error.value = 'Ошибка обновления статуса'
            throw e
        } finally {
            isLoading.value = false
        }
    }

    return {
        // State
        orders,
        isLoading,
        error,

        // Computed
        activeOrders,
        completedOrders,
        totalSpent,

        // Methods
        fetchOrders,
        createOrder,
        getOrderById,
        cancelOrder,
        updateOrderStatus
    }
})
