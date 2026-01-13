<template>
  <div class="avatar" :class="`avatar--${size}`">
    <img v-if="photoUrl" :src="photoUrl" :alt="name" class="avatar-image" />
    <div v-else class="avatar-initials">
      {{ initials }}
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed, defineProps, withDefaults } from 'vue'

withDefaults(
    defineProps<{
      name: string
      photoUrl?: string
      size?: 'sm' | 'md' | 'lg'
    }>(),
    {
      size: 'md'
    }
)

const initials = computed(() => {
  return name
      .split(' ')
      .map(n => n[0])
      .join('')
      .toUpperCase()
      .slice(0, 2)
})
</script>

<style scoped>
.avatar {
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 50%;
  background: linear-gradient(135deg, var(--color-primary), #0044cc);
  color: #ffffff;
  font-weight: 700;
  overflow: hidden;
}

.avatar--sm {
  width: 32px;
  height: 32px;
  font-size: 12px;
}

.avatar--md {
  width: 48px;
  height: 48px;
  font-size: 16px;
}

.avatar--lg {
  width: 64px;
  height: 64px;
  font-size: 20px;
}

.avatar-image {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.avatar-initials {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 100%;
  height: 100%;
}
</style>
