<template>
  <div class="provider-orders-section">
    <!-- Header -->
    <h3 class="text-xl font-bold text-white mb-4">{{ orders?.length ?? 0 }} заказов</h3>

    <!-- Empty State -->
    <div v-if="!orders || orders.length === 0" class="text-center py-12 bg-slate-800 rounded-xl">
      <p class="text-5xl mb-4">💼</p>
      <p class="text-gray-400 text-lg">Нет активных заказов</p>
      <p class="text-gray-500 text-sm mt-2">Ожидаются последовательные заказы</p>
    </div>

    <!-- Orders List -->
    <div v-else class="space-y-3">
      <div
        v-for="order in orders"
        :key="order.id"
        class="bg-slate-800 border border-slate-700 rounded-xl p-4 hover:border-blue-500 transition group"
      >
        <!-- Order Header -->
        <div class="flex items-start justify-between mb-3">
          <div>
            <h4 class="font-bold text-white group-hover:text-blue-300 transition">
              {{ order.serviceName }}
            </h4>
            <p class="text-sm text-gray-400 mt-1">
              👤 {{ order.clientName }}
            </p>
          </div>
          <div class="text-right">
            <p class="text-lg font-bold text-green-400">
              {{ formatPrice(order.price) }}
            </p>
            <span :class="['text-xs font-semibold px-2 py-1 rounded', getStatusColor(order.status)]">
              {{ getStatusLabel(order.status) }}
            </span>
          </div>
        </div>

        <!-- Order Details -->
        <div class="text-xs text-gray-400 mb-4 space-y-1">
          <p>📅 {{ formatDate(order.date) }}</p>
          <p>Order ID: #{{ order.id }}</p>
        </div>

        <!-- Actions -->
        <div class="flex gap-2">
          <button
            v-if="order.status === 'pending'"
            @click="acceptOrder(order.id)"
            class="flex-1 bg-green-600 hover:bg-green-500 text-white font-semibold py-2 rounded-lg transition active:scale-95"
          >
            ✅ Принять
          </button>
          <button
            v-if="order.status === 'in_progress'"
            @click="completeOrder(order.id)"
            class="flex-1 bg-blue-600 hover:bg-blue-500 text-white font-semibold py-2 rounded-lg transition active:scale-95"
          >
            ✔️ Окончить
          </button>
          <button
            @click="viewOrder(order.id)"
            class="flex-1 bg-slate-700 hover:bg-slate-600 text-white font-semibold py-2 rounded-lg transition active:scale-95"
          >
            👀 Детали
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
interface Order {
  id: string | number
  clientName: string
  serviceName: string
  date: string
  status: 'pending' | 'in_progress' | 'completed'
  price: number
}

defineProps<{
  orders?: Order[]
}>()

const emit = defineEmits<{
  accept: [id: string | number]
  complete: [id: string | number]
  view: [id: string | number]
}>()

const formatPrice = (price: number): string => {
  return new Intl.NumberFormat('ru-RU', {
    style: 'currency',
    currency: 'RUB',
    minimumFractionDigits: 0
  }).format(price)
}

const formatDate = (dateStr: string): string => {
  try {
    const date = new Date(dateStr)
    return new Intl.DateTimeFormat('ru-RU', {
      year: 'numeric',
      month: 'short',
      day: 'numeric'
    }).format(date)
  } catch {
    return dateStr
  }
}

const getStatusLabel = (status: string): string => {
  const labels: Record<string, string> = {
    pending: 'Ожидание',
    in_progress: 'В процессе',
    completed: 'Завершён'
  }
  return labels[status] || status
}

const getStatusColor = (status: string): string => {
  const colors: Record<string, string> = {
    pending: 'bg-yellow-900 text-yellow-300',
    in_progress: 'bg-blue-900 text-blue-300',
    completed: 'bg-green-900 text-green-300'
  }
  return colors[status] || 'bg-gray-900 text-gray-300'
}

const acceptOrder = (id: string | number) => {
  emit('accept', id)
}

const completeOrder = (id: string | number) => {
  emit('complete', id)
}

const viewOrder = (id: string | number) => {
  emit('view', id)
}
</script>
