<template>
  <div class="profile-view p-4 space-y-4">
    <!-- User Info Section -->
    <ProfileHeader />

    <!-- Stats -->
    <ProfileStats :orders-count="ordersCount" />

    <!-- Actions Section -->
    <ProfileActions
        :is-provider="userStore.isProvider"
        :services-count="userStore.providerServices.length"
        @open-become-provider="openBecomeProviderModal"
        @open-provider-dashboard="handleProviderDashboard"
        @open-settings="emit('open-settings')"
    />

    <!-- Provider Services (if provider) -->
    <ProviderServicesList
        v-if="userStore.isProvider"
        :services="userStore.providerServices"
        @select-service="selectServiceForEdit"
        @add-service="openBecomeProviderModal"
    />

    <!-- Service Details Modal -->
    <ServiceDetailsModal
        :service="selectedServiceForEdit"
        @close="closeServiceDetails"
        @delete="handleDeleteService"
        @edit="editService"
    />

    <!-- Become Provider Modal -->
    <BecomeProviderModal
        :is-open="showBecomeProviderModal"
        @close="closeBecomeProviderModal"
        @submit="handleSubmitProvider"
    />
  </div>
</template>

<script setup lang="ts">
import { useProfile } from '@/composables/useProfile'
import ProfileHeader from '@/components/profile/ProfileHeader.vue'
import ProfileStats from '@/components/profile/ProfileStats.vue'
import ProfileActions from '@/components/profile/ProfileActions.vue'
import ProviderServicesList from '@/components/profile/ProviderServicesList.vue'
import ServiceDetailsModal from '@/components/modals/ServiceDetailsModal.vue'
import BecomeProviderModal from '@/components/modals/BecomeProviderModal.vue'
import type { ProviderFormData } from '@/components/modals/BecomeProviderModal.vue'

interface Props {
  userData?: Record<string, any>
  ordersCount: number
}

defineProps<Props>()

const emit = defineEmits<{
  'open-settings': []
  'show-toast': [message: string]
}>()

const {
  userStore,
  showBecomeProviderModal,
  selectedServiceForEdit,
  openBecomeProviderModal,
  closeBecomeProviderModal,
  submitProvider,
  selectServiceForEdit,
  closeServiceDetails,
  deleteService,
  editService,
  openProviderDashboard
} = useProfile()

const handleSubmitProvider = (data: ProviderFormData) => {
  const message = submitProvider(data)
  emit('show-toast', message)
}

const handleDeleteService = () => {
  if (!selectedServiceForEdit.value) return
  const message = deleteService(selectedServiceForEdit.value.id)
  if (message) {
    emit('show-toast', message)
  }
}

const handleProviderDashboard = () => {
  const message = openProviderDashboard()
  emit('show-toast', message)
}
</script>

<style scoped>
.profile-view {
  max-width: 400px;
  margin: 0 auto;
}
</style>
