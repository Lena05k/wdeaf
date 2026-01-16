<template>
  <div class="w-full max-w-2xl mx-auto">
    <!-- Progress Bar -->
    <div class="mb-6">
      <div class="flex items-center justify-between mb-2">
        <span class="text-sm font-semibold text-blue-400">Step {{ currentStep }} of 3</span>
        <span class="text-xs text-gray-400">{{ getProgressPercentage }}%</span>
      </div>
      <div class="w-full h-2 bg-slate-700 rounded-full overflow-hidden border border-blue-900">
        <div 
          :style="{ width: `${getProgressPercentage}%` }"
          class="h-full bg-gradient-to-r from-blue-500 to-blue-400 transition-all duration-300"
        ></div>
      </div>
    </div>

    <!-- Step Content -->
    <div class="bg-slate-800 rounded-lg border border-blue-900 p-6 mb-6 min-h-96">
      <!-- Step 1: Info + Schedule -->
      <Transition name="fade" mode="out-in">
        <div v-if="currentStep === 1" key="step1">
          <ProviderFormStep1 
            :form-data="formData" 
            @update:formData="updateFormData"
          />
        </div>

        <!-- Step 2: Optional Photos -->
        <div v-else-if="currentStep === 2" key="step2">
          <ProviderFormStep2 
            :form-data="formData" 
            @update:formData="updateFormData"
          />
        </div>

        <!-- Step 3: Review & Confirm -->
        <div v-else-if="currentStep === 3" key="step3">
          <ProviderFormStep3 :form-data="formData" />
        </div>
      </Transition>
    </div>

    <!-- Navigation Buttons -->
    <div class="flex gap-3">
      <!-- Back Button -->
      <button
        v-if="currentStep > 1"
        @click="goToPreviousStep"
        class="flex-1 py-3 px-4 bg-slate-700 hover:bg-slate-600 text-white font-semibold rounded-lg transition flex items-center justify-center gap-2"
      >
        <span>←</span>
        <span>{{ $t('back', 'Back') }}</span>
      </button>

      <!-- Next Button -->
      <button
        v-if="currentStep < 3"
        @click="goToNextStep"
        :disabled="!canProceedToNextStep"
        :class="[
          'flex-1 py-3 px-4 font-semibold rounded-lg transition flex items-center justify-center gap-2',
          canProceedToNextStep
            ? 'bg-blue-600 hover:bg-blue-500 text-white cursor-pointer'
            : 'bg-gray-700 text-gray-400 cursor-not-allowed opacity-50'
        ]"
      >
        <span>{{ $t('next', 'Next') }}</span>
        <span>→</span>
      </button>

      <!-- Publish Button -->
      <button
        v-if="currentStep === 3"
        @click="handlePublish"
        :disabled="isPublishing"
        :class="[
          'flex-1 py-3 px-4 font-semibold rounded-lg transition flex items-center justify-center gap-2',
          isPublishing
            ? 'bg-gray-700 text-gray-400 cursor-not-allowed opacity-50'
            : 'bg-green-600 hover:bg-green-500 text-white cursor-pointer'
        ]"
      >
        <span v-if="!isPublishing">✓</span>
        <span v-if="isPublishing" class="animate-spin">⚡</span>
        <span>{{ isPublishing ? $t('publishing', 'Publishing...') : $t('publish', 'Publish') }}</span>
      </button>
    </div>

    <!-- Validation Messages -->
    <div v-if="validationError" class="mt-4 p-3 bg-red-600/20 border border-red-600 rounded-lg">
      <p class="text-sm text-red-300">{{ validationError }}</p>
    </div>

    <!-- Info Messages -->
    <div v-if="currentStep === 2" class="mt-4 p-3 bg-blue-900/20 border border-blue-800 rounded-lg">
      <p class="text-xs text-blue-300">
        📋 Примечание: Вы можете пропустить эту u041dнстру - она опциональна. Но фото делают вашу услугу более атрактивной для клиентов.
      </p>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, reactive } from 'vue'
import ProviderFormStep1 from './ProviderFormStep1.vue'
import ProviderFormStep2 from './ProviderFormStep2.vue'
import ProviderFormStep3 from './ProviderFormStep3.vue'

interface FormDataType {
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

const currentStep = ref(1)
const isPublishing = ref(false)
const validationError = ref('')

const formData = reactive<FormDataType>({
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

// Validators
const isStep1Valid = computed(() => {
  return (
    formData.serviceName.trim().length > 0 &&
    formData.description.trim().length > 5 &&
    formData.category.length > 0 &&
    formData.price > 0
  )
})

// Step 2 is always valid (photos are optional)
const isStep2Valid = computed(() => true)

const canProceedToNextStep = computed(() => {
  if (currentStep.value === 1) return isStep1Valid.value
  if (currentStep.value === 2) return isStep2Valid.value
  return false
})

const getProgressPercentage = computed(() => {
  return Math.round((currentStep.value / 3) * 100)
})

const updateFormData = (newData: Partial<FormDataType>) => {
  Object.assign(formData, newData)
  validationError.value = ''
}

const goToNextStep = () => {
  validationError.value = ''

  if (currentStep.value === 1 && !isStep1Valid.value) {
    validationError.value = 'Пожалуйста, заполните все обязательные поля'
    return
  }

  if (currentStep.value < 3) {
    currentStep.value++
    // Trigger haptic feedback in Telegram
    if (typeof window !== 'undefined' && (window as any).Telegram?.WebApp?.HapticFeedback) {
      (window as any).Telegram.WebApp.HapticFeedback.impactOccurred('light')
    }
  }
}

const goToPreviousStep = () => {
  if (currentStep.value > 1) {
    currentStep.value--
    validationError.value = ''
  }
}

const handlePublish = async () => {
  try {
    isPublishing.value = true
    validationError.value = ''

    // Create FormData for multipart upload
    const submitData = new FormData()
    submitData.append('serviceName', formData.serviceName)
    submitData.append('description', formData.description)
    submitData.append('category', formData.category)
    submitData.append('price', formData.price.toString())
    submitData.append('timezone', formData.timezone)
    submitData.append('availability', JSON.stringify(formData.availability))

    // Add images if present
    formData.images.forEach((image, index) => {
      if (image.file) {
        submitData.append(`images[${index}]`, image.file)
      }
    })

    // Send to API
    const response = await fetch('/api/services', {
      method: 'POST',
      body: submitData
    })

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`)
    }

    const result = await response.json()

    // Success feedback
    if (typeof window !== 'undefined' && (window as any).Telegram?.WebApp?.HapticFeedback) {
      (window as any).Telegram.WebApp.HapticFeedback.impactOccurred('medium')
    }

    // Emit success event or navigate
    emit('success', result)
  } catch (error) {
    console.error('Error publishing service:', error)
    validationError.value = 'Ошибка при вы бние услуги. Попытайте ещё раз.'
  } finally {
    isPublishing.value = false
  }
}

const emit = defineEmits<{
  'success': [data: any]
}>()
</script>

<style scoped>
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.3s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}
</style>