<template>
  <Teleport to="body">
    <div class="toast" :class="`toast--${type}`" @animationend="emit('close')">
      <div class="toast-icon">{{ icons[type] }}</div>
      <p class="toast-message">{{ message }}</p>
    </div>
  </Teleport>
</template>

<script setup lang="ts">
import { defineProps, defineEmits } from 'vue'

type ToastType = 'success' | 'error' | 'info'

defineProps<{
  message: string
  type?: ToastType
}>()

defineEmits<{
  close: []
}>()

const icons: Record<ToastType, string> = {
  success: '✓',
  error: '✕',
  info: 'ℹ'
}
</script>

<style scoped>
.toast {
  position: fixed;
  bottom: 80px;
  left: 16px;
  right: 16px;
  max-width: 400px;
  margin: 0 auto;
  padding: 12px 16px;
  border-radius: 8px;
  display: flex;
  align-items: center;
  gap: 12px;
  z-index: 2000;
  animation: slideInUp 0.3s ease forwards, slideOutDown 0.3s ease 2.7s forwards;
  font-weight: 500;
}

@keyframes slideInUp {
  from {
    transform: translateY(100%);
    opacity: 0;
  }
  to {
    transform: translateY(0);
    opacity: 1;
  }
}

@keyframes slideOutDown {
  from {
    transform: translateY(0);
    opacity: 1;
  }
  to {
    transform: translateY(100%);
    opacity: 0;
  }
}

.toast--success {
  background: #059669;
  color: #ffffff;
  border: 1px solid #10b981;
}

.toast--error {
  background: #dc2626;
  color: #ffffff;
  border: 1px solid #ef4444;
}

.toast--info {
  background: #0055ff;
  color: #ffffff;
  border: 1px solid #0055ff;
}

.toast-icon {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 20px;
  height: 20px;
  font-size: 14px;
  font-weight: 700;
}

.toast-message {
  margin: 0;
  font-size: 14px;
  flex: 1;
}
</style>
