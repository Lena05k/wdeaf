<template>
  <div class="profile-content">
    <!-- Avatar Section -->
    <div class="profile-header">
      <div class="avatar-circle">Л</div>
      <h2 class="profile-name">Лена</h2>
      <p class="profile-username">@lena_user</p>
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
      <button class="btn btn-primary">Редактировать профиль</button>
      <button class="btn btn-secondary">Настройки</button>
    </div>

    <!-- Divider -->
    <div class="divider"></div>

    <!-- Additional Info -->
    <div class="info-section">
      <h3 class="section-title">О мне</h3>
      <p class="info-text">Профессиональный веб-дизайнер с опытом 5+ лет</p>
    </div>

    <!-- Logout -->
    <button class="btn btn-danger">Выход</button>
  </div>
</template>

<script setup lang="ts">
import { defineProps } from 'vue'

defineProps<{
  isProvider: boolean
}>()
</script>

<style scoped>
.profile-content {
  padding: 1.5rem 1rem;
  space-y: 1.5rem;
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

.btn-primary:active {
  background: #1d4ed8;
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

/* Divider */
.divider {
  height: 1px;
  background: rgba(148, 163, 184, 0.1);
  margin: 1rem 0;
}

/* Info Section */
.info-section {
  margin-bottom: 1.5rem;
}

.section-title {
  font-size: 0.875rem;
  font-weight: 600;
  color: #a0aec0;
  text-transform: uppercase;
  letter-spacing: 0.02em;
  margin: 0 0 0.75rem;
}

.info-text {
  color: #cbd5e1;
  font-size: 0.875rem;
  line-height: 1.5;
  margin: 0;
}
</style>