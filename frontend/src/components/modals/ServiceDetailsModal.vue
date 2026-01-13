<template>
  <div v-if="service" class="fixed inset-0 modal-overlay z-50 flex items-end">
    <div class="modal-content w-full rounded-t-2xl p-4 max-w-md animate-slide-up">
      <div class="flex justify-between items-center mb-4">
        <h2 class="text-lg font-bold">{{ service.name }}</h2>
        <button @click="$emit('close')" class="text-2xl text-gray-400">✕</button>
      </div>

      <!-- Image Carousel -->
      <div v-if="service.images" class="image-carousel mb-4">
        <img
            :src="service.images[modalImageIndex]"
            class="carousel-image"
            :alt="service.name"
        >
        <button
            v-if="service.images.length > 1"
            @click.stop="$emit('prev-image')"
            class="carousel-nav prev"
        >
          ‹
        </button>
        <button
            v-if="service.images.length > 1"
            @click.stop="$emit('next-image')"
            class="carousel-nav next"
        >
          ›
        </button>
        <div class="carousel-dots" v-if="service.images.length > 1">
          <div
              v-for="(img, idx) in service.images"
              :key="idx"
              :class="['dot', { 'active': modalImageIndex === idx }]"
              @click.stop="selectImage(idx)"
          ></div>
        </div>
      </div>

      <div class="space-y-4 mb-4 max-h-80 overflow-y-auto">
        <!-- Full Description -->
        <div>
          <p class="text-sm text-gray-400 mb-1">Полное описание</p>
          <p class="text-gray-300">{{ service.fullDescription || service.description }}</p>
        </div>

        <!-- Provider Profile -->
        <div
            @click="$emit('view-provider', service.provider)"
            class="bg-blue-900 bg-opacity-30 rounded-lg p-3 border border-blue-700 cursor-pointer hover:bg-opacity-50 transition"
        >
          <p class="text-sm text-gray-400 mb-2">👤 Профиль исполнителя</p>
          <div class="flex items-center justify-between">
            <p class="font-semibold">{{ service.provider }}</p>
            <span class="text-yellow-400">⭐ {{ service.providerRating || 4.8 }}</span>
          </div>
        </div>

        <div class="grid grid-cols-2 gap-4">
          <div>
            <p class="text-sm text-gray-400 mb-1">Рейтинг</p>
            <p class="font-semibold">⭐ {{ service.providerRating || 4.8 }} ({{ service.reviews }} отзывов)</p>
          </div>
          <div>
            <p class="text-sm text-gray-400 mb-1">Цена</p>
            <p class="font-bold text-blue-400 text-lg">{{ service.price }}₽</p>
          </div>
        </div>

        <div>
          <p class="text-sm text-gray-400 mb-1">Время ответа</p>
          <p class="text-gray-300">{{ service.response_time }}</p>
        </div>

        <!-- Reviews Section -->
        <div v-if="service.reviews > 0" class="reviews-section">
          <p class="text-sm font-semibold text-blue-400 mb-3">💬 Последние отзывы:</p>
          <div class="review-item">
            <p class="text-sm font-semibold mb-1">{{ service.provider }}</p>
            <p class="text-xs text-gray-400">⭐ 5.0</p>
            <p class="text-sm text-gray-300 mt-1">Отличная работа! Очень доволен качеством и скоростью выполнения.</p>
          </div>
          <div class="review-item">
            <p class="text-sm font-semibold mb-1">Клиент</p>
            <p class="text-xs text-gray-400">⭐ 4.8</p>
            <p class="text-sm text-gray-300 mt-1">Профессионал своего дела, рекомендую!</p>
          </div>
        </div>
      </div>

      <button
          @click="$emit('order-confirm')"
          class="btn-primary w-full py-3 rounded-lg font-bold text-lg mb-2"
      >
        Заказать услугу
      </button>
      <button
          @click="$emit('close')"
          class="btn-secondary w-full py-3 rounded-lg font-semibold"
      >
        Отмена
      </button>
    </div>
  </div>
</template>

<script>
export default {
  name: 'ServiceDetailsModal',
  props: {
    service: {
      type: Object,
      default: null
    },
    modalImageIndex: {
      type: Number,
      default: 0
    }
  },
  emits: ['close', 'order-confirm', 'view-provider', 'next-image', 'prev-image'],
  methods: {
    selectImage(idx) {
      this.$emit('update:modalImageIndex', idx);
    }
  }
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

.image-carousel {
  position: relative;
  width: 100%;
  height: 200px;
  background: #0F1319;
  overflow: hidden;
  border-radius: 8px;
}

.carousel-image {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: opacity 0.3s ease;
}

.carousel-nav {
  position: absolute;
  top: 50%;
  transform: translateY(-50%);
  background: rgba(0, 85, 255, 0.8);
  color: white;
  border: none;
  width: 36px;
  height: 36px;
  border-radius: 50%;
  cursor: pointer;
  z-index: 10;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: background 0.3s;
}

.carousel-nav:hover {
  background: #0055FF;
}

.carousel-nav.prev { left: 8px; }
.carousel-nav.next { right: 8px; }

.carousel-dots {
  position: absolute;
  bottom: 8px;
  left: 50%;
  transform: translateX(-50%);
  display: flex;
  gap: 6px;
  z-index: 10;
}

.dot {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background: rgba(255, 255, 255, 0.5);
  cursor: pointer;
  transition: background 0.3s;
}

.dot.active {
  background: #0055FF;
}

.reviews-section {
  background: #0F1319;
  border-radius: 8px;
  padding: 12px;
  border-left: 3px solid #0055FF;
}

.review-item {
  background: #1a1f2e;
  padding: 12px;
  border-radius: 8px;
  margin-bottom: 10px;
  border: 1px solid rgba(0, 85, 255, 0.2);
}

.btn-primary {
  background: #0055FF;
  color: #FFFFFF;
  transition: all 0.3s ease;
  border: none;
  cursor: pointer;
}

.btn-primary:hover {
  background: #0044CC;
  box-shadow: 0 8px 16px rgba(0, 85, 255, 0.4);
  transform: translateY(-2px);
}

.btn-primary:active {
  transform: translateY(0);
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

.text-gray-300 { color: #CCCCCC; }
.text-gray-400 { color: #999999; }

@keyframes slideUp {
  from { transform: translateY(100%); }
  to { transform: translateY(0); }
}

.animate-slide-up {
  animation: slideUp 0.3s ease-out;
}
</style>
