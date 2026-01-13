<template>
  <button
      :class="['btn', `btn--${variant}`, `btn--${size}`, { 'btn--loading': loading }]"
      :disabled="disabled || loading"
      v-bind="$attrs"
  >
    <span v-if="loading" class="btn-spinner"></span>
    <slot />
  </button>
</template>

<script setup lang="ts">
import { defineProps, withDefaults } from 'vue'

type ButtonVariant = 'primary' | 'secondary' | 'outline'
type ButtonSize = 'sm' | 'md' | 'lg'

withDefaults(
    defineProps<{
      variant?: ButtonVariant
      size?: ButtonSize
      loading?: boolean
      disabled?: boolean
    }>(),
    {
      variant: 'primary',
      size: 'md',
      loading: false,
      disabled: false
    }
)
</script>

<style scoped>
.btn {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  font-weight: 600;
  border-radius: 8px;
  border: none;
  cursor: pointer;
  transition: all 0.3s ease;
  white-space: nowrap;
}

/* Variants */
.btn--primary {
  background: var(--color-primary);
  color: #ffffff;
}

.btn--primary:hover:not(:disabled) {
  background: #0044cc;
  box-shadow: 0 8px 16px rgba(0, 85, 255, 0.4);
  transform: translateY(-2px);
}

.btn--secondary {
  background: transparent;
  color: var(--color-primary);
  border: 1px solid var(--color-primary);
}

.btn--secondary:hover:not(:disabled) {
  background: rgba(0, 85, 255, 0.1);
}

.btn--outline {
  background: transparent;
  color: var(--color-text-primary);
  border: 1px solid var(--color-text-secondary);
}

.btn--outline:hover:not(:disabled) {
  border-color: var(--color-text-primary);
  background: var(--color-bg-secondary);
}

/* Sizes */
.btn--sm {
  padding: 6px 12px;
  font-size: 12px;
}

.btn--md {
  padding: 10px 16px;
  font-size: 14px;
}

.btn--lg {
  padding: 14px 24px;
  font-size: 16px;
  width: 100%;
}

/* States */
.btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.btn--loading {
  position: relative;
}

.btn-spinner {
  display: inline-block;
  width: 14px;
  height: 14px;
  border: 2px solid currentColor;
  border-right-color: transparent;
  border-radius: 50%;
  animation: spin 0.6s linear infinite;
}

@keyframes spin {
  to {
    transform: rotate(360deg);
  }
}
</style>
