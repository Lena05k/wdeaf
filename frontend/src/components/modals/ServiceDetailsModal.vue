<template>
  <Modal
      :is-open="isOpen"
      title="Детали услуги"
      large
      @close="emit('close')"
  >
    <template v-if="service">
      <!-- Full Images Gallery -->
      <ImageCarousel
          :images="service.images"
          class="mb-4"
          @update:index="currentImageIndex = $event"
      />

      <div class="space-y-4 mb-4 max-h-96 overflow-y-auto">
        <!-- Full Description -->
        <div>
          <label class="label-small">Полное описание</label>
          <p class="text-primary">{{ service.fullDescription || service.description }}</p>
        </div>

        <!-- Provider Profile Button -->
        <button
            @click="emit('view-provider', service.provider)"
            class="provider-button"
        >
          <span>👤 Профиль исполнителя</span>
          <Rating :value="service.providerRating || 4.8" :show-value="false" />
        </button>

        <!-- Stats Grid -->
        <div class="grid grid-cols-2 gap-4">
          <div class="stat-item">
            <label class="label-small">Рейтинг</label>
            <Rating :value="service.providerRating || 4.8" :review-count="service.reviews" />
          </div>
          <div class="stat-item">
            <label class="label-small">Цена</label>
            <p class="price-text">{{ formatters.price(service.price) }}</p>
          </div>
        </div>

        <!-- Response Time -->
        <div class="stat-item">
          <label class="label-small">Время ответа</label>
          <p class="text-primary">{{ service.response_time }}</p>
        </div>

        <!-- Reviews Section -->
        <ReviewsSection
            v-if="service.reviews > 0"
            :reviews="mockReviews"
            :provider-name="service.provider"
        />
      </div>

      <!-- Action Buttons -->
      <template #footer>
        <Button
            variant="primary"
            size="lg"
            @click="emit('order')"
            class="flex-1"
        >
          Заказать услугу
        </Button>
        <Button
            variant="outline"
            size="lg"
            @click="emit('close')"
            class="flex-1"
        >
          Отмена
        </Button>
      </template>
    </template>
  </Modal>
</template>

<script setup lang="ts">
import { defineProps, defineEmits, ref } from 'vue'
import Modal from '@/components/shared/Modal.vue'
import ImageCarousel from '@/components/shared/ImageCarousel.vue'
import Button from '@/components/shared/Button.vue'
import Rating from '@/components/shared/Rating.vue'
import ReviewsSection from '@/components/shared/ReviewsSection.vue'
import { Formatters } from '@/utils/formatters'

interface Service {
  id: number
  name: string
  provider: string
  category: string
  description: string
  fullDescription: string
  price: number
  reviews: number
  response_time: string
  providerRating: number
  images: string[]
}

interface Review {
  author: string
  rating: number
  text: string
  date?: string
}

defineProps<{
  isOpen: boolean
  service: Service | null
}>()

const emit = defineEmits<{
  close: []
  order: []
  'view-provider': [provider: string]
}>()

const currentImageIndex = ref(0)
const formatters = Formatters

const mockReviews: Review[] = [
  {
    author: 'Иван П.',
    rating: 5.0,
    text: 'Отличная работа! Очень доволен качеством и скоростью выполнения.',
    date: '2 дня назад'
  },
  {
    author: 'Мария К.',
    rating: 4.8,
    text: 'Профессионал своего дела, рекомендую!',
    date: '1 неделю назад'
  }
]
</script>

<style scoped>
.label-small {
  display: block;
  font-size: 12px;
  font-weight: 600;
  color: var(--color-text-secondary);
  margin-bottom: 8px;
}

.text-primary {
  color: var(--color-text-primary);
  font-size: 14px;
  line-height: 1.5;
}

.provider-button {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 12px;
  background: rgba(0, 85, 255, 0.1);
  border: 1px solid var(--color-primary);
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.3s;
  color: var(--color-text-primary);
  font-weight: 600;
  width: 100%;
}

.provider-button:hover {
  background: rgba(0, 85, 255, 0.2);
}

.stat-item {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.price-text {
  font-size: 16px;
  font-weight: 700;
  color: var(--color-primary);
  margin: 0;
}
</style>
