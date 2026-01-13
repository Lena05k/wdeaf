<template>
  <span class="badge" :class="[`badge--${variant}`, `badge--${size}`]">
    {{ text }}
  </span>
</template>

<script setup lang="ts">
import { withDefaults, defineProps } from 'vue'

type BadgeVariant = 'primary' | 'secondary' | 'success' | 'warning' | 'error'
type BadgeSize = 'sm' | 'md' | 'lg'

withDefaults(
    defineProps<{
      text: string
      variant?: BadgeVariant
      size?: BadgeSize
    }>(),
    {
      variant: 'primary',
      size: 'md'
    }
)
</script>

<style scoped>
.badge {
  display: inline-block;
  border-radius: 20px;
  font-weight: 600;
  white-space: nowrap;
}

/* Variants */
.badge--primary {
  background: rgba(0, 85, 255, 0.15);
  color: #0055ff;
  border: 1px solid #0055ff;
}

.badge--secondary {
  background: rgba(153, 153, 153, 0.15);
  color: #999999;
  border: 1px solid #999999;
}

.badge--success {
  background: rgba(16, 185, 129, 0.15);
  color: #10b981;
  border: 1px solid #10b981;
}

.badge--warning {
  background: rgba(245, 158, 11, 0.15);
  color: #f59e0b;
  border: 1px solid #f59e0b;
}

.badge--error {
  background: rgba(239, 68, 68, 0.15);
  color: #ef4444;
  border: 1px solid #ef4444;
}

/* Sizes */
.badge--sm {
  padding: 4px 8px;
  font-size: 12px;
}

.badge--md {
  padding: 6px 12px;
  font-size: 13px;
}

.badge--lg {
  padding: 8px 16px;
  font-size: 14px;
}
</style>
