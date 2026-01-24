<template>
  <div class="profile-page">
    <!-- UserHeader contains everything now -->
    <UserHeader />
  </div>
</template>

<script setup lang="ts">
import { onMounted } from 'vue'
import { useUserStore } from '@/stores/userStore'
import UserHeader from '@/components/profile/UserHeader.vue'

const userStore = useUserStore()

onMounted(() => {
  userStore.initFromTelegram()
})
</script>

<style scoped>
.profile-page {
  background: linear-gradient(135deg, #0f1319 0%, #1a1f2e 100%);
  width: 100%;
  height: 100%;
}
</style>