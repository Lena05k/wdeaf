<template>
  <div class="skeleton" :style="{ width, height }" :class="`skeleton--${variant}`"></div>
</template>

<script setup lang="ts">
import { withDefaults, defineProps } from 'vue'

type SkeletonVariant = 'text' | 'circle' | 'rect'

withDefaults(
    defineProps<{
      width?: string
      height?: string
      variant?: SkeletonVariant
    }>(),
    {
      width: '100%',
      height: '20px',
      variant: 'text'
    }
)
</script>

<style scoped>
.skeleton {
  background: linear-gradient(
      90deg,
      var(--color-text-secondary) 25%,
      rgba(255, 255, 255, 0.1) 50%,
      var(--color-text-secondary) 75%
  );
  background-size: 200% 100%;
  animation: loading 1.5s infinite;
  border-radius: 4px;
}

.skeleton--circle {
  border-radius: 50%;
}

.skeleton--rect {
  border-radius: 8px;
}

@keyframes loading {
  0% {
    background-position: 200% 0;
  }
  100% {
    background-position: -200% 0;
  }
}
</style>