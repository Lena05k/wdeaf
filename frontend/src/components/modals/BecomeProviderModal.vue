<template>
  <div v-if="isOpen" class="modal-overlay fixed inset-0 bg-black/50 flex items-end z-50">
    <div class="modal-content bg-slate-800 w-full max-w-md rounded-t-2xl border-t border-blue-900 max-h-[90vh] overflow-y-auto">
      <!-- Header -->
      <div class="sticky top-0 bg-slate-800 border-b border-blue-900 p-4 flex justify-between items-center">
        <h2 class="text-xl font-bold">📝 Стать исполнителем</h2>
        <button
            @click="emit('close')"
            class="text-gray-400 hover:text-white text-2xl"
        >
          ✕
        </button>
      </div>

      <!-- Step Indicator -->
      <div class="px-4 pt-4 flex gap-2">
        <div
            v-for="step in 4"
            :key="step"
            :class="[
              'flex-1 h-1 rounded-full transition',
              currentStep >= step ? 'bg-blue-500' : 'bg-slate-700'
            ]"
        />
      </div>

      <!-- Content -->
      <div class="p-4 space-y-4">
        <!-- Step 1: Basic Info -->
        <ProviderFormStep1 v-if="currentStep === 1" :form-data="formData" @update:form-data="formData = $event" />

        <!-- Step 2: Images -->
        <ProviderFormStep2 v-if="currentStep === 2" :form-data="formData" @update:form-data="formData = $event" />

        <!-- Step 3: Schedule -->
        <ProviderFormStep3 v-if="currentStep === 3" :form-data="formData" @update:form-data="formData = $event" />

        <!-- Step 4: Verification -->
        <ProviderFormStep4 v-if="currentStep === 4" :form-data="formData" />
      </div>

      <!-- Footer Buttons -->
      <div class="sticky bottom-0 bg-slate-800 border-t border-blue-900 p-4 flex gap-2">
        <button
            v-if="currentStep > 1"
            @click="currentStep--"
            class="flex-1 bg-slate-700 hover:bg-slate-600 text-white font-semibold py-2 rounded-lg transition"
        >
          ← Назад
        </button>
        <button
            v-if="currentStep < 4"
            @click="currentStep++"
            :disabled="!isStepValid"
            :class="[
              'flex-1 font-semibold py-2 rounded-lg transition',
              isStepValid
                ? 'bg-blue-600 hover:bg-blue-500 text-white'
                : 'bg-gray-700 text-gray-400 cursor-not-allowed'
            ]"
        >
          Далее →
        </button>
        <button
            v-else
            @click="emit('submit')"
            class="flex-1 bg-green-600 hover:bg-green-500 text-white font-semibold py-2 rounded-lg transition"
        >
          ✓ Нарегистрируть
        </button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed, ref } from 'vue'
import ProviderFormStep1 from '@/components/profile/forms/ProviderFormStep1.vue'
import ProviderFormStep2 from '@/components/profile/forms/ProviderFormStep2.vue'
import ProviderFormStep3 from '@/components/profile/forms/ProviderFormStep3.vue'
import ProviderFormStep4 from '@/components/profile/forms/ProviderFormStep4.vue'

export interface ProviderFormData {
  serviceName: string
  description: string
  category: string
  price: number
  timezone: string
  availability: {
    weekdays: boolean
    weekends: boolean
    evenings: boolean
  }
  images: Array<{ file?: File; preview?: string }>
}

interface Props {
  isOpen: boolean
}

defineProps<Props>()

const emit = defineEmits<{
  'close': []
  'submit': [data: ProviderFormData]
}>()

const currentStep = ref(1)
const formData = ref<ProviderFormData>({
  serviceName: '',
  description: '',
  category: '',
  price: 0,
  timezone: 'UTC+3',
  availability: {
    weekdays: true,
    weekends: false,
    evenings: true
  },
  images: []
})

const isStepValid = computed(() => {
  switch (currentStep.value) {
    case 1:
      return (
        formData.value.serviceName.trim().length > 0 &&
        formData.value.description.trim().length > 10 &&
        formData.value.category.length > 0 &&
        formData.value.price > 0
      )
    case 2:
      return formData.value.images.length > 0
    case 3:
      return Object.values(formData.value.availability).some(v => v)
    case 4:
      return true
    default:
      return false
  }
})
</script>

<style scoped>
.modal-overlay {
  animation: fadeIn 0.3s ease-out;
}

.modal-content {
  animation: slideUp 0.3s ease-out;
}

@keyframes fadeIn {
  from {
    opacity: 0;
  }
  to {
    opacity: 1;
  }
}

@keyframes slideUp {
  from {
    transform: translateY(100%);
  }
  to {
    transform: translateY(0);
  }
}
</style>
