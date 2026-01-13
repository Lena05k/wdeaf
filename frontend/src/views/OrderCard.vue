<template>
  <div class="provider-card">
    <div class="flex justify-between items-start mb-2">
      <h3 class="font-bold">{{ order.service }}</h3>
      <span :class="['text-xs font-semibold px-3 py-1 rounded-full', 
        order.status === 'active' ? 'bg-green-900 text-green-300' : 'bg-blue-900 text-blue-300']">
        {{ order.status === 'active' ? '✓ Активен' : '⏳ В ожидании' }}
      </span>
    </div>
    
    <p class="text-sm text-gray-400 mb-2">Исполнитель: {{ order.provider }}</p>
    
    <div class="flex justify-between items-center mb-3">
      <span class="text-sm text-gray-500">{{ order.date }}</span>
      <span class="font-bold text-blue-400">{{ order.price }}₽</span>
    </div>

    <button 
      v-if="order.status === 'pending'"
      @click="$emit('cancel')"
      class="btn-secondary w-full py-1 rounded text-xs font-semibold"
    >
      Отменить заказ
    </button>
  </div>
</template>

<script>
export default {
  name: 'OrderCard',
  props: {
    order: {
      type: Object,
      required: true,
      validator: (obj) => obj.id && obj.service && obj.provider && obj.status && obj.price && obj.date
    }
  },
  emits: ['cancel']
}
</script>

<style scoped>
.provider-card {
  background: #1a1f2e;
  border: 1px solid #0055FF;
  border-radius: 12px;
  padding: 16px;
  margin-bottom: 16px;
}

.btn-secondary {
  background: transparent;
  color: #0055FF;
  border: 1px solid #0055FF;
  transition: all 0.3s;
  cursor: pointer;
}

.btn-secondary:hover {
  background: rgba(0, 85, 255, 0.1);
}

.text-gray-400 { color: #999999; }
.text-gray-500 { color: #777777; }
</style>
