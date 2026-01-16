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
        @select-service="selectServiceForDetails"
        @add-service="openBecomeProviderModal"
    />

    <!-- Service Details Modal -->
    <ServiceDetailsModal
        :service="selectedServiceForDetails"
        @close="closeServiceDetails"
        @delete="handleDeleteService"
        @edit="openEditModal"
    />

    <!-- Edit Service Modal -->
    <EditProviderModal
        :service="selectedServiceForEdit"
        @close="closeEditModal"
        @save="handleSaveEdited"
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
import EditProviderModal from '@/components/modals/EditProviderModal.vue'
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
  showEditProviderModal,
  selectedServiceForEdit,
  selectedServiceForDetails,
  openBecomeProviderModal,
  closeBecomeProviderModal,
  openEditProviderModal,
  closeEditProviderModal,
  submitProvider,
  saveEditedService,
  selectServiceForDetails,
  closeServiceDetails,
  deleteService,
  openProviderDashboard
} = useProfile()

const handleSubmitProvider = (data: ProviderFormData) => {
  const message = submitProvider(data)
  emit('show-toast', message)
}

const handleDeleteService = () => {
  if (!selectedServiceForDetails.value) return
  const message = deleteService(selectedServiceForDetails.value.id)
  if (message) {
    emit('show-toast', message)
  }
}

const handleProviderDashboard = () => {
  const message = openProviderDashboard()
  emit('show-toast', message)
}

const openEditModal = (service: any) => {
  openEditProviderModal(service)
  closeServiceDetails()
}

const closeEditModal = () => {
  closeEditProviderModal()
}

const handleSaveEdited = (service: any) => {
  const message = saveEditedService(service)
  emit('show-toast', message)
}
</script>

<style scoped>
.profile-view {
  max-width: 400px;
  margin: 0 auto;
}
</style>
