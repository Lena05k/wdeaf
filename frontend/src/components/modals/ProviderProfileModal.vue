<template>
  <div v-if="providerName" class="fixed inset-0 modal-overlay z-50 flex items-end">
    <div class="modal-content w-full rounded-t-2xl p-4 max-w-md animate-slide-up max-h-96 overflow-y-auto">
      <div class="flex justify-between items-center mb-4">
        <h2 class="text-lg font-bold">Профиль исполнителя</h2>
        <button @click="$emit('close')" class="text-2xl text-gray-400">✕</button>
      </div>

      <div class="flex items-center gap-3 mb-4 pb-4 border-b border-blue-900">
        <div class="provider-avatar">{{ providerName.charAt(0) }}</div>
        <div class="flex-1">
          <p class="font-bold text-lg">{{ providerName }}</p>
          <p class="text-yellow-400">⭐ 4.8 (156 отзывов)</p>
          <p class="text-sm text-gray-400 mt-1">Ответ в течение 1 часа</p>
        </div>
      </div>

      <div class="space-y-3 mb-4">
        <!-- Portfolio Section -->
        <div>
          <p class="text-sm text-gray-400 mb-2">📸 Портфолио (3 фото)</p>
          <div class="grid grid-cols-3 gap-2">
            <img 
              src="https://via.placeholder.com/100" 
              class="rounded-lg w-full aspect-square object-cover" 
              alt="portfolio 1"
            >
            <img 
              src="https://via.placeholder.com/100" 
              class="rounded-lg w-full aspect-square object-cover" 
              alt="portfolio 2"
            >
            <img 
              src="https://via.placeholder.com/100" 
              class="rounded-lg w-full aspect-square object-cover" 
              alt="portfolio 3"
            >
          </div>
        </div>

        <!-- Services Section -->
        <div>
          <p class="text-sm text-gray-400 mb-2">📋 Услуги исполнителя (5)</p>
          <div class="space-y-2">
            <div class="bg-blue-900 bg-opacity-20 rounded p-2 text-sm border-l-2 border-blue-500">
              <p class="font-semibold">Услуга сантехника</p>
              <p class="text-gray-400">2500₽</p>
            </div>
            <div class="bg-blue-900 bg-opacity-20 rounded p-2 text-sm border-l-2 border-blue-500">
              <p class="font-semibold">Обслуживание ПК</p>
              <p class="text-gray-400">1800₽</p>
            </div>
          </div>
        </div>
      </div>

      <button 
        @click="$emit('close')" 
        class="btn-secondary w-full py-3 rounded-lg font-semibold"
      >
        Закрыть
      </button>
    </div>
  </div>
</template>

<script>
export default {
  name: 'ProviderProfileModal',
  props: {
    providerName: {
      type: String,
      default: ''
    }
  },
  emits: ['close']
}
</script>

<style scoped>
.modal-overlay {
  background: rgba(0, 0, 0, 0.7);
}

.modal-content {
  background: #1a1f2e;
  color: #FFFFFF;
  border: 1px solid #0055FF;
}

.provider-avatar {
  width: 70px;
  height: 70px;
  min-width: 70px;
  border-radius: 50%;
  background: linear-gradient(135deg, #0055FF, #0044CC);
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  font-weight: bold;
  font-size: 28px;
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

@keyframes slideUp {
  from { transform: translateY(100%); }
  to { transform: translateY(0); }
}

.animate-slide-up {
  animation: slideUp 0.3s ease-out;
}
</style>
