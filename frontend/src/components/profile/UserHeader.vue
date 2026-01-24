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
      <!-- Profile Section -->
      <div class="settings-section">
        <h2 class="settings-section-title">ПРОФИЛЬ</h2>
        
        <!-- Profile Cell -->
        <div class="settings-cell-group">
          <button class="settings-cell">
            <div class="cell-icon bg-blue-500">👤</div>
            <div class="cell-content">
              <p class="cell-label">Обновить профиль</p>
              <p class="cell-value">{{ user?.first_name }}</p>
            </div>
            <svg class="w-5 h-5 text-gray-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7" />
            </svg>
          </button>
        </div>
      </div>

      <!-- Account Section -->
      <div class="settings-section">
        <h2 class="settings-section-title">АККАУНТ</h2>
        
        <div class="settings-cell-group">
          <!-- Email Cell -->
          <button class="settings-cell border-b border-slate-700">
            <div class="cell-icon bg-red-500">📧</div>
            <div class="cell-content">
              <p class="cell-label">Почта</p>
              <p class="cell-value">user@example.com</p>
            </div>
            <svg class="w-5 h-5 text-gray-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7" />
            </svg>
          </button>

          <!-- Phone Cell -->
          <button class="settings-cell border-b border-slate-700">
            <div class="cell-icon bg-green-500">📱</div>
            <div class="cell-content">
              <p class="cell-label">Номер телефона</p>
              <p class="cell-value">+7 (999) 123-45-67</p>
            </div>
            <svg class="w-5 h-5 text-gray-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7" />
            </svg>
          </button>

          <!-- Location Cell -->
          <button class="settings-cell">
            <div class="cell-icon bg-purple-500">📍</div>
            <div class="cell-content">
              <p class="cell-label">Место расположения</p>
              <p class="cell-value">Москва, Россия</p>
            </div>
            <svg class="w-5 h-5 text-gray-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7" />
            </svg>
          </button>
        </div>
      </div>

      <!-- Privacy & Security Section -->
      <div class="settings-section">
        <h2 class="settings-section-title">БЕЗОПАСНОСТЬ</h2>
        
        <div class="settings-cell-group">
          <!-- Privacy Cell -->
          <button class="settings-cell border-b border-slate-700">
            <div class="cell-icon bg-blue-600">🔒</div>
            <div class="cell-content">
              <p class="cell-label">Приватность</p>
              <p class="cell-value">Увидим для всех</p>
            </div>
            <svg class="w-5 h-5 text-gray-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7" />
            </svg>
          </button>

          <!-- Notifications Cell -->
          <button class="settings-cell">
            <div class="cell-icon bg-orange-500">🔔</div>
            <div class="cell-content">
              <p class="cell-label">Нотификации</p>
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
          <button class="settings-cell-danger">
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

defineProps<{
  user?: User
  isProvider: boolean
}>()
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
  border-radius: 0.875rem;
}

.settings-cell:hover {
  background: rgba(59, 130, 246, 0.05);
}

.settings-cell:active {
  background: rgba(59, 130, 246, 0.1);
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
  border-radius: 0.875rem;
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

  .settings-cell {
    padding: 0.875rem;
  }

  .cell-icon {
    width: 2.25rem;
    height: 2.25rem;
    font-size: 1rem;
  }
}
</style>