<template>
  <div
    class="order-card"
    @click="emit('select')"
  >
    <div class="order-header">
      <div>
        <h3 class="order-service">{{ order.service }}</h3>
        <p class="order-provider">{{ order.provider }}</p>
      </div>
      <span :class="['status-badge', `status-${order.status}`]">
        {{ getStatusLabel(order.status) }}
      </span>
    </div>

    <div class="order-details">
      <div class="detail-item">
        <span class="detail-label">Дата</span>
        <span class="detail-value">{{ formatDate(order.date) }}</span>
      </div>
      <div class="detail-item">
        <span class="detail-label">Цена</span>
        <span class="detail-value detail-price">{{ formatPrice(order.price) }}</span>
      </div>
    </div>

    <!-- Description Preview -->
    <p v-if="order.description" class="description-preview">
      {{ order.description }}
    </p>
  </div>
</template>

<script setup lang="ts">
interface Order {
  id: string | number
  service: string
  provider: string
  status: 'active' | 'pending' | 'completed' | 'cancelled'
  price: number
  date: string | Date
  deadline?: string | Date
  description?: string
  category?: string
}

interface Props {
  order: Order
}

defineProps<Props>()

const emit = defineEmits<{
  'select': []
}>()

const getStatusLabel = (status: string): string => {
  const labels: Record<string, string> = {
    'active': 'Активен',
    'pending': 'Ожидание',
    'completed': 'Завершено',
    'cancelled': 'Отменено'
  }
  return labels[status] || 'Неизвестно'
}

const formatDate = (date: string | Date | undefined): string => {
  if (!date) return 'Не указано'
  const d = new Date(date)
  const options: Intl.DateTimeFormatOptions = {
    month: 'short',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit'
  }
  return d.toLocaleDateString('ru-RU', options)
}

const formatPrice = (price: number | undefined): string => {
  if (!price) return 'Не указано'
  return new Intl.NumberFormat('ru-RU', {
    style: 'currency',
    currency: 'RUB',
    minimumFractionDigits: 0
  }).format(price)
}
</script>

<style scoped>
.order-card {
  background: linear-gradient(135deg, #ffffff 0%, #f8f9fa 100%);
  border: 1px solid rgba(229, 231, 235, 0.8);
  border-radius: 16px;
  padding: 16px;
  margin-bottom: 12px;
  cursor: pointer;
  transition: all 0.3s cubic-bezier(0.16, 1, 0.3, 1);
}

.order-card:hover {
  border-color: rgba(37, 99, 235, 0.5);
  box-shadow: 0 8px 24px rgba(37, 99, 235, 0.15);
  transform: translateY(-2px);
}

.order-card:active {
  transform: scale(0.98);
}

.order-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 12px;
  gap: 12px;
}

.order-service {
  font-size: 1rem;
  font-weight: 700;
  color: #111827;
  margin: 0 0 4px 0;
}

.order-provider {
  font-size: 0.8rem;
  color: #6b7280;
  margin: 0;
}

.status-badge {
  display: inline-block;
  padding: 6px 12px;
  border-radius: 12px;
  font-size: 0.75rem;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  white-space: nowrap;
  flex-shrink: 0;
}

.status-active {
  background: rgba(34, 197, 94, 0.1);
  color: #22c55e;
  border: 1px solid rgba(34, 197, 94, 0.3);
}

.status-pending {
  background: rgba(245, 158, 11, 0.1);
  color: #f59e0b;
  border: 1px solid rgba(245, 158, 11, 0.3);
}

.status-completed {
  background: rgba(34, 197, 94, 0.1);
  color: #22c55e;
  border: 1px solid rgba(34, 197, 94, 0.3);
}

.status-cancelled {
  background: rgba(239, 68, 68, 0.1);
  color: #ef4444;
  border: 1px solid rgba(239, 68, 68, 0.3);
}

.order-details {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 12px;
  margin-bottom: 12px;
}

.detail-item {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.detail-label {
  font-size: 0.7rem;
  color: #6b7280;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.detail-value {
  font-size: 0.9rem;
  font-weight: 600;
  color: #111827;
}

.detail-price {
  color: #2563eb;
  font-size: 1rem;
}

.description-preview {
  font-size: 0.8rem;
  color: #6b7280;
  line-height: 1.4;
  margin: 0;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

/* Dark Mode */
@media (prefers-color-scheme: dark) {
  .order-card {
    background: linear-gradient(135deg, #1f2937 0%, #111827 100%);
    border-color: rgba(75, 85, 99, 0.3);
  }

  .order-card:hover {
    border-color: rgba(59, 130, 246, 0.5);
    box-shadow: 0 8px 24px rgba(59, 130, 246, 0.2);
  }

  .order-service {
    color: #f3f4f6;
  }

  .order-provider,
  .detail-label,
  .description-preview {
    color: #d1d5db;
  }

  .detail-value {
    color: #f3f4f6;
  }
}
</style>