<template>
  <div class="service-card" @click="emit('select', service)">
    <ImageCarousel
        :images="service.images"
        @update:index="currentImageIndex = $event"
    />

    <div class="p-4">
      <div class="flex justify-between items-start mb-2">
        <div class="flex-1">
          <h3 class="font-bold">{{ service.name }}</h3>
          <p class="text-xs text-secondary">{{ service.provider }}</p>
        </div>
        <span class="badge-category">{{ service.category }}</span>
      </div>

      <p class="text-sm text-secondary mb-3 line-clamp-2">
        {{ service.description }}
      </p>

      <div class="flex justify-between mb-3">
        <span class="text-yellow-400">⭐ {{ service.providerRating }}</span>
        <span class="font-bold text-primary">{{ formatters.price(service.price) }}</span>
      </div>

      <button
          class="btn-primary w-full"
          @click.stop="emit('select', service)"
      >
        Подробности
      </button>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import ImageCarousel from './ImageCarousel.vue'
import { Formatters } from '@/utils/formatters'

const props = defineProps({
  service: Object,
  required: true
})

const emit = defineEmits(['select', 'order'])
const currentImageIndex = ref(0)
const formatters = Formatters
</script>

<style scoped>
.service-card {
  border: 1px solid var(--color-border);
  border-radius: 8px;
  overflow: hidden;
  cursor: pointer;
  transition: all 0.3s;
}

.service-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 12px 24px var(--color-shadow);
}
</style>