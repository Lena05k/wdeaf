<template>
  <div>
    <h3 class="text-lg font-semibold text-blue-400 mb-4">График работы</h3>

    <div class="space-y-4">
      <div>
        <label class="block text-sm font-semibold mb-2">Часовой пояс</label>
        <select
            :value="formData.timezone"
            @change="updateField('timezone', ($event.target as HTMLSelectElement).value)"
            class="w-full bg-slate-700 border border-blue-900 rounded-lg px-4 py-2 text-white focus:outline-none focus:border-blue-500"
        >
          <option value="UTC+3">UTC+3 (Москва)</option>
          <option value="UTC+4">UTC+4 (Казань)</option>
          <option value="UTC+5">UTC+5 (Екатеринбург)</option>
          <option value="UTC+8">UTC+8 (Владивосток)</option>
        </select>
      </div>

      <div>
        <label class="block text-sm font-semibold mb-3">Доступность</label>
        <div class="space-y-2 bg-slate-700 rounded-lg p-3 border border-blue-900">
          <label class="flex items-center gap-2 cursor-pointer">
            <input
                :checked="formData.availability.weekdays"
                @change="updateAvailability('weekdays', ($event.target as HTMLInputElement).checked)"
                type="checkbox"
                class="w-4 h-4"
            />
            <span class="text-sm">Будни (Пн-Пт)</span>
          </label>
          <label class="flex items-center gap-2 cursor-pointer">
            <input
                :checked="formData.availability.weekends"
                @change="updateAvailability('weekends', ($event.target as HTMLInputElement).checked)"
                type="checkbox"
                class="w-4 h-4"
            />
            <span class="text-sm">Выходные (Сб-Вс)</span>
          </label>
          <label class="flex items-center gap-2 cursor-pointer">
            <input
                :checked="formData.availability.evenings"
                @change="updateAvailability('evenings', ($event.target as HTMLInputElement).checked)"
                type="checkbox"
                class="w-4 h-4"
            />
            <span class="text-sm">Вечерние часы (18:00-23:00)</span>
          </label>
        </div>
      </div>
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

const updateField = (field: keyof FormData, value: any) => {
  emit('update:formData', { ...props.formData, [field]: value })
}

const updateAvailability = (field: keyof FormData['availability'], value: boolean) => {
  emit('update:formData', {
    ...props.formData,
    availability: { ...props.formData.availability, [field]: value }
  })
}
</script>

<style scoped></style>
