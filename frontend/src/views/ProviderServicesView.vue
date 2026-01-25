<template>
  <div class="provider-services-view">
    <!-- Header -->
    <div class="view-header">
      <button @click="handleBack" class="back-button">
        <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <polyline points="15 18 9 12 15 6"></polyline>
        </svg>
      </button>
      <h1 class="page-title">📦 Мои услуги</h1>
      <div class="header-spacer"></div>
    </div>

    <!-- Services Section -->
    <div class="view-content">
      <ProviderServicesSection
        :services="services"
        @add-service="openAddService"
        @edit-service="openEditService"
        @delete-service="handleDeleteService"
        @service-click="openServiceDetail"
      />
    </div>

    <!-- Add/Edit Service Modal -->
    <ServiceModal
      v-if="showServiceModal"
      :service="currentService"
      :is-editing="isEditingService"
      @submit="submitService"
      @close="closeServiceModal"
    />

    <!-- Service Detail Modal -->
    <ServiceDetailModal
      :is-open="showServiceDetail"
      :service="selectedServiceDetail"
      :is-provider-mode="true"
      @close="closeServiceDetail"
      @edit="handleEditFromDetail"
      @delete="handleDeleteFromDetail"
    />
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import { useRouter } from 'vue-router'
import ProviderServicesSection from '@/components/profile/ProviderServicesSection.vue'
import ServiceModal from '@/components/profile/modals/ServiceModal.vue'
import ServiceDetailModal from '@/components/modals/ServiceDetailModal.vue'

interface Service {
  id: string | number
  name: string
  price: number
  category?: string
  description?: string
  orders?: number
  rating?: number
  images?: string[]
  fullDescription?: string
}

const router = useRouter()

// State
const showServiceModal = ref(false)
const isEditingService = ref(false)
const currentService = ref<Service | null>(null)
const showServiceDetail = ref(false)
const selectedServiceDetail = ref<Service | null>(null)

// Services Data
const services = ref<Service[]>([
  {
    id: 1,
    name: 'Web-дизайн сайта',
    price: 15000,
    description: 'Профессиональный дизайн сайта',
    category: 'Дизайн',
    orders: 12,
    rating: 4.9,
    images: ['https://via.placeholder.com/400x300?text=Service+1'],
    fullDescription: 'Полный дизайн веб-сайта с учетом всех современных тенденций. Включает макеты, прототипы и дизайн-систему.'
  },
  {
    id: 2,
    name: 'Дизайн логотипа',
    price: 3000,
    description: 'Креативные логотипы',
    category: 'Дизайн',
    orders: 28,
    rating: 5,
    images: ['https://via.placeholder.com/400x300?text=Service+2'],
    fullDescription: 'Создание уникального логотипа для вашего бренда. Включает несколько вариантов и итерации.'
  },
  {
    id: 3,
    name: 'Мокеты и прототипы',
    price: 8000,
    description: 'Прототипы и макеты интерфейсов',
    category: 'Дизайн',
    orders: 8,
    rating: 4.8,
    images: ['https://via.placeholder.com/400x300?text=Service+3'],
    fullDescription: 'Интерактивные макеты и прототипы приложений. Готовы к передаче разработчикам.'
  },
  {
    id: 4,
    name: 'Дизайн интерфейса приложения',
    price: 20000,
    description: 'UI/UX дизайн для мобильных и веб-приложений',
    category: 'Дизайн',
    orders: 5,
    rating: 4.9,
    images: ['https://via.placeholder.com/400x300?text=Service+4'],
    fullDescription: 'Полный дизайн пользовательского интерфейса приложения с учетом UX best practices.'
  },
  {
    id: 5,
    name: 'Переразработка дизайна',
    price: 12000,
    description: 'Обновление существующего дизайна',
    category: 'Дизайн',
    orders: 3,
    rating: 4.7,
    images: ['https://via.placeholder.com/400x300?text=Service+5'],
    fullDescription: 'Модернизация и переразработка существующего дизайна с учетом современных трендов.'
  }
])

// Methods
const handleBack = () => {
  router.back()
}

const openAddService = () => {
  isEditingService.value = false
  currentService.value = null
  showServiceModal.value = true
}

const openEditService = (service: Service) => {
  isEditingService.value = true
  currentService.value = JSON.parse(JSON.stringify(service))
  showServiceModal.value = true
}

const closeServiceModal = () => {
  showServiceModal.value = false
  currentService.value = null
  isEditingService.value = false
}

const submitService = (service: Service) => {
  if (isEditingService.value && currentService.value) {
    const index = services.value.findIndex(s => s.id === currentService.value!.id)
    if (index !== -1) {
      services.value[index] = { ...services.value[index], ...service }
    }
  } else {
    services.value.push({
      ...service,
      id: Date.now(),
      orders: 0,
      rating: 0
    })
  }
  closeServiceModal()
}

const handleDeleteService = (serviceId: string | number) => {
  services.value = services.value.filter(s => s.id !== serviceId)
}

const openServiceDetail = (service: Service) => {
  selectedServiceDetail.value = service
  showServiceDetail.value = true
}

const closeServiceDetail = () => {
  showServiceDetail.value = false
  selectedServiceDetail.value = null
}

const handleEditFromDetail = (editedService: Service) => {
  const index = services.value.findIndex(s => s.id === editedService.id)
  if (index !== -1) {
    services.value[index] = editedService
  }
  closeServiceDetail()
}

const handleDeleteFromDetail = (serviceId: string | number) => {
  services.value = services.value.filter(s => s.id !== serviceId)
  closeServiceDetail()
}
</script>

<style scoped>
.provider-services-view {
  min-height: 100vh;
  background: linear-gradient(to bottom, #0f172a, #0f1319);
}

/* Header */
.view-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 16px;
  background: linear-gradient(to bottom, #1e293b, #0f172a);
  border-bottom: 1px solid rgba(148, 163, 184, 0.1);
  position: sticky;
  top: 0;
  z-index: 10;
}

.back-button {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 40px;
  height: 40px;
  background: rgba(148, 163, 184, 0.1);
  border: 1px solid rgba(148, 163, 184, 0.2);
  color: #e2e8f0;
  border-radius: 10px;
  cursor: pointer;
  transition: all 0.2s ease;
  flex-shrink: 0;
}

.back-button:hover {
  background: rgba(148, 163, 184, 0.2);
  border-color: rgba(148, 163, 184, 0.4);
}

.back-button:active {
  transform: scale(0.95);
}

.back-button svg {
  width: 24px;
  height: 24px;
}

.page-title {
  margin: 0;
  font-size: 1.25rem;
  font-weight: 700;
  color: white;
  flex: 1;
  text-align: center;
}

.header-spacer {
  width: 40px;
  flex-shrink: 0;
}

/* Content */
.view-content {
  padding: 20px;
  max-width: 1200px;
  margin: 0 auto;
}

/* Responsive */
@media (max-width: 768px) {
  .view-header {
    padding: 12px;
  }

  .page-title {
    font-size: 1.1rem;
  }

  .view-content {
    padding: 16px;
  }
}

@media (max-width: 480px) {
  .view-header {
    padding: 12px 12px;
  }

  .page-title {
    font-size: 1rem;
  }

  .view-content {
    padding: 12px;
  }
}
</style>
