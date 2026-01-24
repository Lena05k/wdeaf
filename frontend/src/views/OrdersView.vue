<template>
  <div class="orders-view">
    <!-- Empty State -->
    <div v-if="userOrders.length === 0" class="empty-state">
      <p class="empty-icon">📠</p>
      <p class="empty-title">Нет активных заказов</p>
      <button 
        @click="emit('browse-services')"
        class="btn-primary"
      >
        Найти услугу
      </button>
    </div>

    <!-- Orders List -->
    <div v-else class="orders-list">
      <OrderCard 
        v-for="order in userOrders"
        :key="order.id"
        :order="order"
        @select="selectOrder(order)"
      />
    </div>

    <!-- Order Detail Modal -->
    <OrderDetailModal
      :is-open="showOrderModal"
      :order="selectedOrder"
      @close="closeOrderModal"
      @cancel="handleCancelOrder"
      @message="handleMessage"
    />
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import OrderCard from '@/components/shared/OrderCard.vue'
import OrderDetailModal from '@/components/modals/OrderDetailModal.vue'

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
  userOrders: Order[]
}

const props = defineProps<Props>()

const emit = defineEmits<{
  'browse-services': []
  'cancel-order': [orderId: string | number]
}>()

const showOrderModal = ref(false)
const selectedOrder = ref<Order | null>(null)

const selectOrder = (order: Order) => {
  selectedOrder.value = order
  showOrderModal.value = true
}

const closeOrderModal = () => {
  showOrderModal.value = false
  selectedOrder.value = null
}

const handleCancelOrder = (order: Order) => {
  emit('cancel-order', order.id)
  closeOrderModal()
}

const handleMessage = (order: Order) => {
  console.log('Написание сообщения исполнителю:', order)
  closeOrderModal()
}
</script>

<style scoped>
.orders-view {
  padding: 16px;
}

.empty-state {
  text-align: center;
  padding: 48px 0;
}

.empty-icon {
  font-size: 3rem;
  margin-bottom: 12px;
}

.empty-title {
  font-size: 1rem;
  color: #6b7280;
  margin-bottom: 24px;
  margin-top: 0;
}

.btn-primary {
  background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%);
  color: white;
  border: none;
  padding: 12px 24px;
  border-radius: 12px;
  font-weight: 600;
  font-size: 0.95rem;
  cursor: pointer;
  transition: all 0.3s cubic-bezier(0.16, 1, 0.3, 1);
  box-shadow: 0 8px 24px rgba(37, 99, 235, 0.3);
}

.btn-primary:hover {
  transform: translateY(-2px);
  box-shadow: 0 12px 32px rgba(37, 99, 235, 0.4);
}

.btn-primary:active {
  transform: scale(0.98);
}

.orders-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

/* Dark Mode */
@media (prefers-color-scheme: dark) {
  .empty-title {
    color: #d1d5db;
  }
}
</style>