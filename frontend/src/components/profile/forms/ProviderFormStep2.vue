<template>
  <div>
    <h3 class="text-lg font-semibold text-blue-400 mb-4">📎 Медиа</h3>
    <p class="text-sm text-gray-400 mb-4">Не обязательно! Добавьте фото, чтобы обовы были более привлекательными</p>

    <!-- Image Preview -->
    <div class="space-y-2 mb-3">
      <div
          v-for="(image, index) in formData.images"
          :key="index"
          class="relative bg-slate-700 border border-blue-900 rounded-lg overflow-hidden flex items-center gap-2 p-2 h-16 group"
      >
        <img
            :src="image.preview"
            :alt="'Service image ' + (index + 1)"
            class="w-14 h-14 object-cover rounded"
        />
        <span class="text-xs text-gray-300 flex-1">Вид {{ index + 1 }}</span>
        <button
            @click="removeImage(index)"
            class="bg-red-600 text-white rounded-full p-1 opacity-0 group-hover:opacity-100 hover:bg-red-700 transition flex-shrink-0"
        >
          ✕
        </button>
      </div>

      <!-- Add Image Button - Paperclip style -->
      <div v-if="formData.images.length < 5">
        <label class="flex items-center justify-center gap-2 bg-slate-700/50 border border-dashed border-blue-900 rounded-lg py-4 px-3 cursor-pointer hover:border-blue-500 hover:bg-slate-700 transition group">
          <span class="text-2xl group-hover:scale-110 transition">📎</span>
          <div class="text-center flex-1">
            <p class="text-sm font-semibold text-gray-300 group-hover:text-blue-400 transition">{{ formData.images.length > 0 ? 'Добавить ещё' : 'Положите фото' }}</p>
            <p class="text-xs text-gray-500">{{ 5 - formData.images.length }} ром осталось</p>
          </div>
          <input
              type="file"
              accept="image/*"
              multiple
              class="hidden"
              @change="handleImageUpload"
          />
        </label>
      </div>
    </div>

    <!-- Empty State - only if no images added -->
    <div v-if="formData.images.length === 0" class="text-center py-8 bg-slate-700/30 border border-dashed border-slate-600 rounded-lg">
      <p class="text-3xl mb-2">🖼️</p>
      <p class="text-gray-400 text-sm mb-2">Не добавлены фото</p>
      <p class="text-xs text-gray-500">Используйте скрепку выше, чтобы добавить</p>
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
    // Оптимизация для Telegram: не болюше 5МБ
    if (file.size > 5 * 1024 * 1024) {
      alert('Файл слишком большой (макс 5 МБ)')
      return
    }

    // Оптимизация: конвертируем в WebP или сжимаем
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