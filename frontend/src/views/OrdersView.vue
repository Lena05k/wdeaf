<template>
  <div class="p-4 space-y-3">
    <!-- Empty State -->
    <div v-if="userOrders.length === 0" class="text-center py-12">
      <p class="text-2xl mb-2">📭</p>
      <p class="text-gray-400">Нет активных заказов</p>
      <button 
        @click="$emit('browse-services')"
        class="btn-primary mt-4 px-6 py-2 rounded-lg text-sm font-semibold"
      >
        Найти услугу
      </button>
    </div>

    <!-- Orders List -->
    <div v-else class="space-y-3">
      <OrderCard 
        v-for="order in userOrders"
        :key="order.id"
        :order="order"
        @cancel="cancelOrder(order.id)"
      />
    </div>
  </div>
</template>

<script>
import OrderCard from '../components/shared/OrderCard.vue';

export default {
  name: 'OrdersView',
  components: {
    OrderCard
  },
  props: {
    userOrders: {
      type: Array,
      required: true
    }
  },
  emits: ['browse-services', 'cancel-order'],
  methods: {
    cancelOrder(orderId) {
      this.$emit('cancel-order', orderId)
    }
  }
}
</script>

<style scoped>
.btn-primary {
  background: #0055FF;
  color: white;
  border: 1px solid #0055FF;
  transition: all 0.3s;
  cursor: pointer;
}

.btn-primary:hover {
  background: #0044cc;
  border-color: #0044cc;
}
</style>