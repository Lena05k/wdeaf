<template>
  <Modal
      :is-open="isOpen"
      title="Профиль исполнителя"
      large
      @close="emit('close')"
  >
    <template v-if="provider">
      <!-- Provider Header -->
      <div class="provider-header">
        <Avatar :name="provider.name" size="lg" />
        <div class="provider-info">
          <h3 class="provider-name">{{ provider.name }}</h3>
          <Rating :value="provider.rating" :show-value="true" :review-count="provider.reviews_count" />
          <p class="response-time">⏱️ Ответ в течение {{ provider.response_time }}</p>
        </div>
      </div>

      <div class="space-y-4 mb-4 max-h-96 overflow-y-auto">
        <!-- Bio -->
        <div v-if="provider.bio">
          <label class="label-small">О себе</label>
          <p class="text-secondary">{{ provider.bio }}</p>
        </div>

        <!-- Portfolio -->
        <div>
          <label class="label-small">📸 Портфолио ({{ portfolio.length }} фото)</label>
          <div class="portfolio-grid">
            <img
                v-for="(item, idx) in portfolio"
                :key="idx"
                :src="item.image_url"
                :alt="item.title"
                class="portfolio-image"
                @click="selectedPortfolioIndex = idx"
            />
          </div>
        </div>

        <!-- Services -->
        <div>
          <label class="label-small">📋 Услуги исполнителя ({{ services.length }})</label>
          <div class="services-list">
            <div
                v-for="service in services"
                :key="service.id"
                class="service-item"
            >
              <p class="service-name">{{ service.name }}</p>
              <p class="service-price">{{ formatters.price(service.price) }}</p>
            </div>
          </div>
        </div>

        <!-- Reviews -->
        <ReviewsSection
            v-if="provider.reviews_count > 0"
            :reviews="reviews"
            :provider-name="provider.name"
        />
      </div>

      <!-- Action Buttons -->
      <template #footer>
        <Button
            variant="primary"
            size="lg"
            @click="emit('contact')"
            class="flex-1"
        >
          💬 Написать сообщение
        </Button>
        <Button
            variant="outline"
            size="lg"
            @click="emit('close')"
            class="flex-1"
        >
          Закрыть
        </Button>
      </template>
    </template>

    <!-- Portfolio Lightbox -->
    <PortfolioLightbox
        v-if="selectedPortfolioIndex !== null"
        :images="portfolio"
        :current-index="selectedPortfolioIndex"
        @close="selectedPortfolioIndex = null"
        @prev="selectedPortfolioIndex = Math.max(0, selectedPortfolioIndex - 1)"
        @next="selectedPortfolioIndex = Math.min(portfolio.length - 1, selectedPortfolioIndex + 1)"
    />
  </Modal>
</template>

<script setup lang="ts">
import { defineProps, defineEmits, ref } from 'vue'
import Modal from '@/components/shared/Modal.vue'
import Button from '@/components/shared/Button.vue'
import Rating from '@/components/shared/Rating.vue'
import Avatar from '@/components/shared/Avatar.vue'
import ReviewsSection from '@/components/shared/ReviewsSection.vue'
import PortfolioLightbox from '@/components/shared/PortfolioLightbox.vue'
import { Formatters } from '@/utils/formatters'

interface Provider {
  id: number
  name: string
  rating: number
  reviews_count: number
  response_time: string
  photo_url?: string
  bio?: string
  services_count: number
  joined_date: string
}

interface PortfolioItem {
  id: number
  image_url: string
  title: string
  description: string
}

interface Service {
  id: number
  name: string
  price: number
}

interface Review {
  id: number
  author: string
  rating: number
  text: string
  date: string
}

defineProps<{
  isOpen: boolean
  provider: Provider | null
  portfolio?: PortfolioItem[]
  services?: Service[]
  reviews?: Review[]
}>()

const emit = defineEmits<{
  close: []
  contact: []
}>()

const selectedPortfolioIndex = ref<number | null>(null)
const formatters = Formatters

const portfolio = ref<PortfolioItem[]>([
  {
    id: 1,
    image_url: 'https://via.placeholder.com/300x300?text=Portfolio+1',
    title: 'Проект 1',
    description: 'Описание проекта'
  },
  {
    id: 2,
    image_url: 'https://via.placeholder.com/300x300?text=Portfolio+2',
    title: 'Проект 2',
    description: 'Описание проекта'
  },
  {
    id: 3,
    image_url: 'https://via.placeholder.com/300x300?text=Portfolio+3',
    title: 'Проект 3',
    description: 'Описание проекта'
  }
])

const services = ref<Service[]>([
  { id: 1, name: 'Услуга сантехника', price: 2500 },
  { id: 2, name: 'Обслуживание ПК', price: 1800 }
])

const reviews = ref<Review[]>([
  {
    id: 1,
    author: 'Клиент 1',
    rating: 5.0,
    text: 'Отличная работа!',
    date: '2 дня назад'
  },
  {
    id: 2,
    author: 'Клиент 2',
    rating: 4.8,
    text: 'Спасибо за качество!',
    date: '1 неделю назад'
  }
])
</script>

<style scoped>
.provider-header {
  display: flex;
  gap: 16px;
  padding: 16px;
  background: var(--color-bg-secondary);
  border-radius: 8px;
  margin-bottom: 16px;
}

.provider-info {
  flex: 1;
  display: flex;
  flex-direction: column;
  justify-content: center;
  gap: 8px;
}

.provider-name {
  margin: 0;
  font-size: 18px;
  font-weight: 700;
  color: var(--color-text-primary);
}

.response-time {
  margin: 0;
  font-size: 13px;
  color: var(--color-text-secondary);
}

.label-small {
  display: block;
  font-size: 12px;
  font-weight: 600;
  color: var(--color-text-secondary);
  margin-bottom: 8px;
}

.text-secondary {
  color: var(--color-text-secondary);
  font-size: 13px;
  line-height: 1.5;
}

.portfolio-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 8px;
}

.portfolio-image {
  width: 100%;
  aspect-ratio: 1;
  object-fit: cover;
  border-radius: 8px;
  cursor: pointer;
  transition: transform 0.3s;
}

.portfolio-image:hover {
  transform: scale(1.05);
}

.services-list {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.service-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 12px;
  background: var(--color-bg-secondary);
  border-left: 3px solid var(--color-primary);
  border-radius: 6px;
}

.service-name {
  margin: 0;
  font-weight: 600;
  color: var(--color-text-primary);
  font-size: 14px;
}

.service-price {
  margin: 0;
  font-size: 13px;
  color: var(--color-text-secondary);
}
</style>
