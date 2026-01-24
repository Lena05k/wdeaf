<template>
  <div class="user-header">
    <!-- Hero Section: Avatar + Name (iOS 18 style) -->
    <div class="hero-section">
      <!-- Avatar -->
      <div class="avatar-container">
        <div class="w-24 h-24 bg-gradient-to-br from-blue-500 to-blue-600 rounded-full flex items-center justify-center text-5xl font-bold text-white shadow-lg">
          {{ user?.first_name?.charAt(0)?.toUpperCase() || '?' }}
        </div>
      </div>

      <!-- Name & Username -->
      <div class="user-info-center">
        <h1 class="text-2xl font-bold text-white">{{ user?.first_name || 'Пользователь' }}</h1>
        <p class="text-sm text-gray-400">@{{ user?.username || 'user' }}</p>
        <p v-if="isProvider" class="text-xs text-blue-400 mt-1.5">✓ Исполнитель</p>
      </div>
    </div>

    <!-- Settings Sections (iOS 18 style) -->
    <div class="settings-container">
      <!-- For Regular User -->
      <template v-if="!isProvider">
        <!-- Orders History Section -->
        <div class="settings-section">
          <h2 class="settings-section-title">ИСТОРИЯ</h2>
          
          <div class="settings-cell-group">
            <button 
              @click="$emit('show-orders')"
              class="settings-cell border-b border-slate-700"
            >
              <div class="cell-icon bg-blue-500">📋</div>
              <div class="cell-content">
                <p class="cell-label">Мои заказы</p>
                <p class="cell-value">{{ ordersCount }} активных</p>
              </div>
              <svg class="w-5 h-5 text-gray-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7" />
              </svg>
            </button>

            <!-- Reviews -->
            <button 
              @click="$emit('show-reviews')"
              class="settings-cell border-b border-slate-700"
            >
              <div class="cell-icon bg-yellow-500">⭐</div>
              <div class="cell-content">
                <p class="cell-label">Оставленные отзывы</p>
                <p class="cell-value">{{ reviewsCount }} отзывов</p>
              </div>
              <svg class="w-5 h-5 text-gray-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7" />
              </svg>
            </button>

            <!-- Saved Services -->
            <button 
              @click="$emit('show-saved')"
              class="settings-cell"
            >
              <div class="cell-icon bg-red-500">❤️</div>
              <div class="cell-content">
                <p class="cell-label">Сохраненные услуги</p>
                <p class="cell-value">{{ savedCount }} услуг</p>
              </div>
              <svg class="w-5 h-5 text-gray-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7" />
              </svg>
            </button>
          </div>
        </div>

        <!-- Become Provider Section -->
        <div class="settings-section">
          <h2 class="settings-section-title">ВОЗМОЖНОсТИ</h2>
          
          <div class="settings-cell-group">
            <button 
              @click="$emit('become-provider')"
              class="settings-cell-provider"
            >
              <div class="cell-icon bg-gradient-to-br from-purple-500 to-purple-600">🚀</div>
              <div class="cell-content">
                <p class="cell-label-provider">Стать исполнителем</p>
                <p class="cell-value">Создавайте услуги и зарабатывайте</p>
              </div>
              <svg class="w-5 h-5 text-purple-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7" />
              </svg>
            </button>
          </div>
        </div>
      </template>

      <!-- For Provider -->
      <template v-else>
        <!-- My Services Section -->
        <div class="settings-section">
          <div class="flex items-center justify-between mb-3">
            <h2 class="settings-section-title">МОИ УСЛУГИ</h2>
            <button 
              @click="$emit('add-service')"
              class="text-blue-400 hover:text-blue-300 text-sm font-semibold transition"
            >
              + Добавить
            </button>
          </div>
          
          <div class="settings-cell-group">
            <button 
              v-if="services.length === 0"
              @click="$emit('add-service')"
              class="settings-cell-empty"
            >
              <div class="cell-icon bg-slate-700">➕</div>
              <div class="cell-content">
                <p class="cell-label">Добавить первую услугу</p>
                <p class="cell-value">Начните предлагать услуги</p>
              </div>
            </button>

            <div v-for="(service, index) in services" :key="service.id">
              <button 
                v-if="index < 3"
                class="settings-cell border-b border-slate-700 group"
                @click="$emit('edit-service', service)"
              >
                <div class="cell-icon bg-blue-500">📌</div>
                <div class="cell-content">
                  <p class="cell-label">{{ service.name }}</p>
                  <p class="cell-value">{{ formatPrice(service.price) }} ₽</p>
                </div>
                <div class="flex gap-2 opacity-0 group-hover:opacity-100 transition">
                  <button 
                    @click.stop="$emit('delete-service', service.id)"
                    class="text-red-400 hover:text-red-300 text-sm"
                  >
                    🗑
                  </button>
                </div>
              </button>
            </div>

            <button 
              v-if="services.length > 3"
              @click="$emit('show-all-services')"
              class="settings-cell text-blue-400"
            >
              <div class="cell-icon bg-slate-700">📂</div>
              <div class="cell-content">
                <p class="cell-label">Еще услуг</p>
                <p class="cell-value">{{ services.length - 3 }} услуги</p>
              </div>
              <svg class="w-5 h-5 text-gray-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7" />
              </svg>
            </button>
          </div>
        </div>

        <!-- Provider Stats Section -->
        <div class="settings-section">
          <h2 class="settings-section-title">СТАТИСТИКА</h2>
          
          <div class="settings-cell-group">
            <button 
              @click="$emit('show-provider-orders')"
              class="settings-cell border-b border-slate-700"
            >
              <div class="cell-icon bg-green-500">✅</div>
              <div class="cell-content">
                <p class="cell-label">Выполненные заказы</p>
                <p class="cell-value">{{ completedOrders }} заказов</p>
              </div>
              <svg class="w-5 h-5 text-gray-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7" />
              </svg>
            </button>

            <button 
              @click="$emit('show-provider-reviews')"
              class="settings-cell border-b border-slate-700"
            >
              <div class="cell-icon bg-yellow-500">⭐</div>
              <div class="cell-content">
                <p class="cell-label">Рейтинг</p>
                <p class="cell-value">{{ providerRating }}/5.0 ({{ providerReviews }} отзывов)</p>
              </div>
              <svg class="w-5 h-5 text-gray-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7" />
              </svg>
            </button>

            <button 
              @click="$emit('show-analytics')"
              class="settings-cell"
            >
              <div class="cell-icon bg-purple-500">💰</div>
              <div class="cell-content">
                <p class="cell-label">Общий доход</p>
                <p class="cell-value">{{ formatPrice(totalEarnings) }} ₽</p>
              </div>
              <svg class="w-5 h-5 text-gray-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7" />
              </svg>
            </button>
          </div>
        </div>
      </template>

      <!-- Common Settings Section -->
      <div class="settings-section">
        <h2 class="settings-section-title">ПРОФИЛЬ</h2>
        
        <div class="settings-cell-group">
          <button 
            @click="$emit('edit-profile')"
            class="settings-cell border-b border-slate-700"
          >
            <div class="cell-icon bg-blue-500">✏️</div>
            <div class="cell-content">
              <p class="cell-label">Редактировать профиль</p>
              <p class="cell-value">{{ user?.first_name }}</p>
            </div>
            <svg class="w-5 h-5 text-gray-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7" />
            </svg>
          </button>

          <button 
            @click="$emit('show-notifications')"
            class="settings-cell"
          >
            <div class="cell-icon bg-orange-500">🔔</div>
            <div class="cell-content">
              <p class="cell-label">Уведомления</p>
              <p class="cell-value">Включены</p>
            </div>
            <svg class="w-5 h-5 text-gray-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7" />
            </svg>
          </button>
        </div>
      </div>

      <!-- Danger Zone -->
      <div class="settings-section">
        <div class="settings-cell-group">
          <button 
            @click="$emit('logout')"
            class="settings-cell-danger"
          >
            <div class="cell-icon-danger">🚪</div>
            <div class="cell-content">
              <p class="cell-label-danger">Выйти из аккаунта</p>
            </div>
          </button>
        </div>
        <p class="section-footer">Вы выдете из своего аккаунта на этом устройстве</p>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
interface User {
  id?: string | number
  first_name?: string
  last_name?: string
  username?: string
}

interface Service {
  id: string | number
  name: string
  price: number
  description?: string
}

interface Props {
  user?: User
  isProvider: boolean
  services?: Service[]
  ordersCount?: number
  reviewsCount?: number
  savedCount?: number
  completedOrders?: number
  providerRating?: number
  providerReviews?: number
  totalEarnings?: number
}

const props = withDefaults(defineProps<Props>(), {
  services: () => [],
  ordersCount: 0,
  reviewsCount: 0,
  savedCount: 0,
  completedOrders: 0,
  providerRating: 0,
  providerReviews: 0,
  totalEarnings: 0
})

defineEmits<{
  'show-orders': []
  'show-reviews': []
  'show-saved': []
  'show-all-services': []
  'show-provider-orders': []
  'show-provider-reviews': []
  'show-analytics': []
  'show-notifications': []
  'become-provider': []
  'add-service': []
  'edit-service': [service: Service]
  'delete-service': [id: string | number]
  'edit-profile': []
  'logout': []
}>()

// Форматирование цены
const formatPrice = (price: number): string => {
  return new Intl.NumberFormat('ru-RU').format(price)
}
</script>

<style scoped>
.user-header {
  background: linear-gradient(to bottom, #0f1319, #0f1319);
  min-height: 100vh;
  padding-bottom: 40px;
}

/* Hero Section */
.hero-section {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 1rem;
  padding: 2rem 1rem 1.5rem;
  border-bottom: 1px solid rgba(148, 163, 184, 0.1);
}

.avatar-container {
  display: flex;
  align-items: center;
  justify-content: center;
}

.user-info-center {
  text-align: center;
}

/* Settings Container */
.settings-container {
  padding: 1.5rem 1rem;
  display: flex;
  flex-direction: column;
  gap: 2rem;
}

/* Section Title (iOS 18 style) */
.settings-section-title {
  font-size: 0.8125rem;
  font-weight: 600;
  letter-spacing: 0.05em;
  color: rgba(148, 163, 184, 0.6);
  margin-bottom: 0.75rem;
  padding: 0 0.5rem;
  text-transform: uppercase;
}

/* Section */
.settings-section {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}

/* Cell Group (iOS 18 style) */
.settings-cell-group {
  background: rgba(30, 41, 59, 0.5);
  border: 1px solid rgba(148, 163, 184, 0.1);
  border-radius: 0.875rem;
  overflow: hidden;
  backdrop-filter: blur(10px);
}

/* Settings Cell */
.settings-cell {
  display: flex;
  align-items: center;
  gap: 1rem;
  width: 100%;
  padding: 1rem;
  background: transparent;
  border: none;
  cursor: pointer;
  transition: all 0.2s ease;
}

.settings-cell:hover {
  background: rgba(59, 130, 246, 0.05);
}

.settings-cell:active {
  background: rgba(59, 130, 246, 0.1);
}

/* Empty State Cell */
.settings-cell-empty {
  display: flex;
  align-items: center;
  gap: 1rem;
  width: 100%;
  padding: 1rem;
  background: transparent;
  border: none;
  cursor: pointer;
  transition: all 0.2s ease;
}

.settings-cell-empty:hover {
  background: rgba(167, 139, 250, 0.05);
}

/* Provider Highlight Cell */
.settings-cell-provider {
  display: flex;
  align-items: center;
  gap: 1rem;
  width: 100%;
  padding: 1rem;
  background: rgba(147, 51, 234, 0.1);
  border: none;
  cursor: pointer;
  transition: all 0.2s ease;
}

.settings-cell-provider:hover {
  background: rgba(147, 51, 234, 0.15);
}

.settings-cell-provider:active {
  background: rgba(147, 51, 234, 0.2);
}

.cell-label-provider {
  font-size: 0.9375rem;
  font-weight: 600;
  color: #a78bfa;
  margin: 0;
}

/* Cell Icon */
.cell-icon {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 2.5rem;
  height: 2.5rem;
  border-radius: 0.625rem;
  font-size: 1.25rem;
  flex-shrink: 0;
}

/* Cell Content */
.cell-content {
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
  flex: 1;
  text-align: left;
}

.cell-label {
  font-size: 0.9375rem;
  font-weight: 500;
  color: #ffffff;
  margin: 0;
}

.cell-value {
  font-size: 0.8125rem;
  color: rgba(148, 163, 184, 0.7);
  margin: 0;
}

/* Danger Zone */
.settings-cell-danger {
  display: flex;
  align-items: center;
  gap: 1rem;
  width: 100%;
  padding: 1rem;
  background: transparent;
  border: none;
  cursor: pointer;
  transition: all 0.2s ease;
}

.settings-cell-danger:hover {
  background: rgba(239, 68, 68, 0.05);
}

.settings-cell-danger:active {
  background: rgba(239, 68, 68, 0.1);
}

.cell-icon-danger {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 2.5rem;
  height: 2.5rem;
  border-radius: 0.625rem;
  font-size: 1.25rem;
  background: rgba(239, 68, 68, 0.2);
  flex-shrink: 0;
}

.cell-label-danger {
  font-size: 0.9375rem;
  font-weight: 500;
  color: #ef4444;
  margin: 0;
}

/* Section Footer */
.section-footer {
  font-size: 0.75rem;
  color: rgba(148, 163, 184, 0.5);
  padding: 0.5rem 1rem;
  text-align: center;
  margin-top: -0.5rem;
}

/* Responsive */
@media (max-width: 640px) {
  .settings-container {
    padding: 1rem 0.75rem;
    gap: 1.5rem;
  }

  .settings-cell,
  .settings-cell-empty,
  .settings-cell-provider,
  .settings-cell-danger {
    padding: 0.875rem;
  }

  .cell-icon {
    width: 2.25rem;
    height: 2.25rem;
    font-size: 1rem;
  }
}
</style>