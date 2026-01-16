import { ref } from 'vue'
import { useUserStore } from '@/stores/userStore'
import type { ProviderFormData } from '@/components/modals/BecomeProviderModal.vue'

export const useProfile = () => {
  const userStore = useUserStore()
  const showBecomeProviderModal = ref(false)
  const selectedServiceForEdit = ref<any>(null)

  const openBecomeProviderModal = () => {
    showBecomeProviderModal.value = true
  }

  const closeBecomeProviderModal = () => {
    showBecomeProviderModal.value = false
  }

  const submitProvider = (data: ProviderFormData) => {
    userStore.addService({
      serviceName: data.serviceName,
      name: data.serviceName,
      description: data.description,
      category: data.category,
      price: data.price,
      images: data.images,
      availability: data.availability,
      timezone: data.timezone
    })

    closeBecomeProviderModal()
    return '✅ Профиль исполнителя создан!'
  }

  const selectServiceForEdit = (service: any) => {
    selectedServiceForEdit.value = service
  }

  const closeServiceDetails = () => {
    selectedServiceForEdit.value = null
  }

  const deleteService = (serviceId: string) => {
    if (confirm('Вы уверены? Услуга будет удалена.')) {
      userStore.deleteService(serviceId)
      closeServiceDetails()
      return '🗑️ Услуга удалена'
    }
    return null
  }

  const editService = () => {
    // TODO: Implement edit functionality
    console.log('✏️ Editing service:', selectedServiceForEdit.value)
    closeServiceDetails()
  }

  const openProviderDashboard = () => {
    console.log('📋 Opening provider dashboard')
    return '👤 Профиль исполнителя открыт'
  }

  return {
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
  }
}
