<template>
  <div class="user-header">
    <!-- Sticky Header Only (No Tabs) -->
    <div class="header-sticky">
      <!-- Logo -->
      <div class="logo-section">
        <div class="logo">W</div>
      </div>

      <!-- Brand Text -->
      <div class="brand-text">
        <span class="brand-name">Деаф</span>
        <span class="brand-hint">услуги</span>
      </div>

      <!-- Profile Button -->
      <button class="profile-btn" @click="toggleProfile">
        {{ userInitial }}
      </button>
    </div>

    <!-- Profile Modal -->
    <Modal v-if="showProfileModal" title="👤 Мой профиль" @close="toggleProfile">
      <div class="profile-modal-content">
        <!-- Avatar Section -->
        <div class="profile-header">
          <div class="avatar-circle">{{ userInitial }}</div>
          <h2 class="profile-name">{{ userData.first_name }}</h2>
          <p class="profile-username">@{{ userData.username }}</p>
          <p v-if="isProvider" class="profile-badge">✓ Исполнитель</p>
        </div>

        <!-- Stats -->
        <div class="stats-grid">
          <div class="stat-card">
            <p class="stat-value">4.9</p>
            <p class="stat-label">Рейтинг</p>
          </div>
          <div class="stat-card">
            <p class="stat-value">28</p>
            <p class="stat-label">Заказов</p>
          </div>
          <div class="stat-card">
            <p class="stat-value">124</p>
            <p class="stat-label">Отзывов</p>
          </div>
        </div>

        <!-- Action Buttons -->
        <div class="action-buttons">
          <button class="btn btn-primary">Редактировать</button>
          <button class="btn btn-secondary">Настройки</button>
        </div>

        <!-- Logout -->
        <button class="btn btn-danger">Выход</button>
      </div>
    </Modal>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import Modal from '@/components/common/Modal.vue'

const isProvider = ref(true)
const showProfileModal = ref(false)

const userData = ref({
  first_name: 'Лена',
  username: 'lena_user'
})

const userInitial = computed(() => userData.value.first_name.charAt(0).toUpperCase())

// Functions
const toggleProfile = () => {
  showProfileModal.value = !showProfileModal.value
}
</script>

<style scoped>
.user-header {
  background: linear-gradient(to bottom, #0f1319, #0f1319);
}

/* Header Sticky */
.header-sticky {
  position: sticky;
  top: 0;
  z-index: 40;
  display: flex;
  align-items: center;
  gap: 0.75rem;
  padding: 0.75rem 1rem;
  background: #ffffff;
  border-bottom: 1px solid #e5e7eb;
  max-width: 768px;
  margin: 0 auto;
  width: 100%;
  box-sizing: border-box;
}

.logo-section {
  display: flex;
  align-items: center;
  flex-shrink: 0;
}

.logo {
  width: 2.5rem;
  height: 2.5rem;
  background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%);
  color: white;
  border-radius: 0.5rem;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: bold;
  font-size: 1.25rem;
}

/* Brand Text */
.brand-text {
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
  flex-shrink: 0;
}

.brand-name {
  font-size: 0.875rem;
  font-weight: 600;
  color: #000000;
  line-height: 1;
}

.brand-hint {
  font-size: 0.75rem;
  color: #6b7280;
  line-height: 1;
}

/* Profile Button */
.profile-btn {
  width: 2.5rem;
  height: 2.5rem;
  border-radius: 50%;
  background: #3b82f6;
  color: white;
  border: none;
  cursor: pointer;
  font-weight: bold;
  font-size: 1rem;
  transition: all 0.2s ease;
  flex-shrink: 0;
  margin-left: auto;
}

.profile-btn:hover {
  background: #2563eb;
}

.profile-btn:active {
  background: #1d4ed8;
}

/* Profile Modal Content */
.profile-modal-content {
  padding: 1rem 0;
}

.profile-header {
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
  padding: 1.5rem 0;
  border-bottom: 1px solid rgba(148, 163, 184, 0.1);
  margin-bottom: 1.5rem;
}

.avatar-circle {
  width: 4rem;
  height: 4rem;
  border-radius: 50%;
  background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.5rem;
  font-weight: bold;
  color: white;
  margin-bottom: 1rem;
}

.profile-name {
  font-size: 1.5rem;
  font-weight: bold;
  color: white;
  margin: 0.5rem 0 0.25rem;
}

.profile-username {
  color: #a0aec0;
  font-size: 0.875rem;
  margin: 0.25rem 0;
}

.profile-badge {
  color: #3b82f6;
  font-size: 0.875rem;
  font-weight: 500;
  margin-top: 0.5rem;
}

/* Stats Grid */
.stats-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 0.75rem;
  margin-bottom: 1.5rem;
}

.stat-card {
  background: rgba(30, 41, 59, 0.5);
  border: 1px solid rgba(148, 163, 184, 0.1);
  border-radius: 0.75rem;
  padding: 1rem;
  text-align: center;
}

.stat-value {
  font-size: 1.25rem;
  font-weight: bold;
  color: #3b82f6;
  margin: 0 0 0.25rem;
}

.stat-label {
  font-size: 0.75rem;
  color: #a0aec0;
  margin: 0;
  text-transform: uppercase;
  letter-spacing: 0.02em;
}

/* Action Buttons */
.action-buttons {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
  margin-bottom: 1.5rem;
}

.btn {
  padding: 0.75rem 1rem;
  border-radius: 0.75rem;
  border: none;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s ease;
  font-size: 0.875rem;
}

.btn-primary {
  background: #3b82f6;
  color: white;
}

.btn-primary:hover {
  background: #2563eb;
}

.btn-secondary {
  background: rgba(148, 163, 184, 0.1);
  color: #e2e8f0;
  border: 1px solid rgba(148, 163, 184, 0.2);
}

.btn-secondary:hover {
  background: rgba(148, 163, 184, 0.15);
}

.btn-danger {
  background: rgba(239, 68, 68, 0.1);
  color: #ef4444;
  border: 1px solid rgba(239, 68, 68, 0.2);
}

.btn-danger:hover {
  background: rgba(239, 68, 68, 0.15);
}
</style>