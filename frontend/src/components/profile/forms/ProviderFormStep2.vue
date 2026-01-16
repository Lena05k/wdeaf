<template>
  <div>
    <h3 class="text-lg font-semibold text-blue-400 mb-4">Фотографии услуги</h3>
    <p class="text-sm text-gray-400 mb-3">Добавьте до 5 фотографий (макс 5 МБ каждая)</p>

    <!-- Image Preview -->
    <div class="space-y-2">
      <div
          v-for="(image, index) in formData.images"
          :key="index"
          class="relative bg-slate-700 border border-blue-900 rounded-lg overflow-hidden"
      >
        <img
            :src="image.preview"
            :alt="'Service image ' + (index + 1)"
            class="w-full h-32 object-cover"
        />
        <button
            @click="removeImage(index)"
            class="absolute top-1 right-1 bg-red-600 text-white rounded-full p-1 hover:bg-red-700"
        >
          ✕
        </button>
      </div>

      <!-- Add Image Button -->
      <div v-if="formData.images.length < 5">
        <label class="flex items-center justify-center gap-2 bg-slate-700 border border-dashed border-blue-900 rounded-lg py-6 cursor-pointer hover:border-blue-500 transition">
          <span class="text-2xl">📸</span>
          <span class="text-sm font-semibold">Добавить фото</span>
          <input
              type="file"
              accept="image/*"
              class="hidden"
              @change="handleImageUpload"
          />
        </label>
      </div>
    </div>

    <div v-if="formData.images.length === 0" class="text-center py-6 text-gray-400">
      <p class="text-4xl mb-2">📷</p>
      <p>Добавьте минимум одну фотографию</p>
    </div>
  </div>
</template>

<script setup lang="ts">
interface FormData {
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
  formData: FormData
}

const props = defineProps<Props>()

const emit = defineEmits<{
  'update:formData': [data: FormData]
}>()

const handleImageUpload = (event: Event) => {
  const target = event.target as HTMLInputElement
  const files = target.files
  if (!files) return

  Array.from(files).forEach(file => {
    if (file.size > 5 * 1024 * 1024) {
      alert('Файл слишком большой (макс 5 МБ)')
      return
    }

    const reader = new FileReader()
    reader.onload = (e) => {
      if (props.formData.images.length < 5 && e.target?.result) {
        const newImages = [...props.formData.images, {
          file,
          preview: e.target.result as string
        }]
        emit('update:formData', { ...props.formData, images: newImages })
      }
    }
    reader.readAsDataURL(file)
  })
  target.value = ''
}

const removeImage = (index: number) => {
  const newImages = props.formData.images.filter((_, i) => i !== index)
  emit('update:formData', { ...props.formData, images: newImages })
}
</script>

<style scoped></style>
