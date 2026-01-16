import { ref } from 'vue'
import { useUserStore } from '@/stores/userStore'
import type { ProviderFormData } from '@/components/modals/BecomeProviderModal.vue'

export const useProfile = () => {
  const userStore = useUserStore()
  const showBecomeProviderModal = ref(false)
  const showEditProviderModal = ref(false)
  const selectedServiceForEdit = ref<any>(null)
  const selectedServiceForDetails = ref<any>(null)

  const openBecomeProviderModal = () => {
    showBecomeProviderModal.value = true
  }

  const closeBecomeProviderModal = () => {
    showBecomeProviderModal.value = false
  }

  const openEditProviderModal = (service: any) => {
    selectedServiceForEdit.value = { ...service }
    showEditProviderModal.value = true
  }

  const closeEditProviderModal = () => {
    showEditProviderModal.value = false
    selectedServiceForEdit.value = null
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

  const saveEditedService = (service: any) => {
    // Update service in store
    userStore.updateService(service.id, {
      serviceName: service.serviceName,
      name: service.serviceName,
      description: service.description,
      category: service.category,
      price: service.price,
      images: service.images,
      availability: service.availability,
      timezone: service.timezone
    })

    closeEditProviderModal()
    return '✅ Услуга обновлена!'
  }

  const selectServiceForDetails = (service: any) => {
    selectedServiceForDetails.value = service
  }

  const closeServiceDetails = () => {
    selectedServiceForDetails.value = null
  }

  const deleteService = (serviceId: string) => {
    if (confirm('Вы уверены? Услуга будет удалена.')) {
      userStore.deleteService(serviceId)
      closeServiceDetails()
      return '🗑️ Услуга удалена'
    }
    return null
  }

  const openProviderDashboard = () => {
    console.log('📊 Открытие дашборда исполнителя')
    return '👤 Профиль исполнителя открыт'
  }

  return {
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
  }
}
