<template>
  <div 
    @click="$emit('select')"
    class="service-card rounded-lg overflow-hidden cursor-pointer"
  >
    <!-- Image Carousel -->
    <div class="image-carousel">
      <img 
        :src="service.images[service.currentImageIndex || 0]" 
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
          :class="['dot', { 'active': (service.currentImageIndex || 0) === idx }]"
          @click.stop="selectImage(idx)"
        ></div>
      </div>
    </div>
    
    <!-- Card Content -->
    <div class="p-4">
      <div class="flex justify-between items-start mb-2">
        <div class="flex-1">
          <h3 class="font-bold">{{ service.name }}</h3>
          <p class="text-xs text-gray-400 mt-1">{{ service.provider }}</p>
        </div>
        <div class="badge-category">{{ service.category }}</div>
      </div>
      
      <p class="text-sm text-gray-400 mb-3 line-clamp-2">{{ service.description }}</p>

      <div class="flex items-center justify-between mb-3">
        <div class="flex items-center gap-1">
          <span class="rating-stars">★★★★★</span>
          <span class="text-xs text-gray-600">({{ service.reviews }})</span>
        </div>
        <span class="font-bold text-blue-400">{{ service.price }}₽</span>
      </div>

      <button 
        @click.stop="$emit('order')"
        class="btn-primary w-full py-2 rounded-lg font-semibold text-sm"
      >
        Заказать
      </button>
    </div>
  </div>
</template>

<script>
export default {
  name: 'ServiceCard',
  props: {
    service: {
      type: Object,
      required: true
    }
  },
  emits: ['select', 'order', 'next-image', 'prev-image'],
  methods: {
    selectImage(idx) {
      this.service.currentImageIndex = idx;
    }
  }
}
</script>

<style scoped>
.service-card {
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  background: #1a1f2e;
  border: 1px solid #0055FF;
}

.service-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 12px 24px rgba(0, 85, 255, 0.3);
  border-color: #0055FF;
}

.image-carousel {
  position: relative;
  width: 100%;
  height: 200px;
  background: #0F1319;
  overflow: hidden;
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

.badge-category {
  display: inline-block;
  padding: 4px 12px;
  border-radius: 20px;
  font-size: 12px;
  font-weight: 500;
  background: rgba(0, 85, 255, 0.15);
  color: #0055FF;
  border: 1px solid #0055FF;
}

.rating-stars {
  color: #FFD700;
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

.text-gray-400 { color: #999999; }
.text-gray-600 { color: #666666; }
</style>
