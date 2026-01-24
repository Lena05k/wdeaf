<template>
  <div class="profile-view">
    <!-- User Header (iOS 18 Settings Style) -->
    <UserHeader :user="userStore.user" :is-provider="userStore.isProvider" />
  </div>
</template>

<script setup lang="ts">
import { useUserStore } from '@/stores/userStore'
import UserHeader from '@/components/profile/UserHeader.vue'

const userStore = useUserStore()
</script>

<style scoped>
.profile-view {
  background: linear-gradient(to bottom, #0f172a, #0f1319);
  min-height: 100vh;
  padding-bottom: 80px;
}
</style>