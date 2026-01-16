<template>
  <div>
    <h3 class="text-lg font-semibold text-blue-400 mb-4">Основная информация</h3>

    <div class="space-y-3">
      <div>
        <label class="block text-sm font-semibold mb-2">Название услуги</label>
        <input
            :value="formData.serviceName"
            @input="updateField('serviceName', ($event.target as HTMLInputElement).value)"
            type="text"
            placeholder="Например: Уроки английского онлайн"
            class="w-full bg-slate-700 border border-blue-900 rounded-lg px-4 py-2 text-white placeholder-gray-500 focus:outline-none focus:border-blue-500"
        />
      </div>

      <div>
        <label class="block text-sm font-semibold mb-2">Описание услуги</label>
        <textarea
            :value="formData.description"
            @input="updateField('description', ($event.target as HTMLTextAreaElement).value)"
            placeholder="Подробное описание того, что вы предлагаете"
            rows="4"
            class="w-full bg-slate-700 border border-blue-900 rounded-lg px-4 py-2 text-white placeholder-gray-500 focus:outline-none focus:border-blue-500 resize-none"
        />
      </div>

      <div>
        <label class="block text-sm font-semibold mb-2">Категория</label>
        <select
            :value="formData.category"
            @change="updateField('category', ($event.target as HTMLSelectElement).value)"
            class="w-full bg-slate-700 border border-blue-900 rounded-lg px-4 py-2 text-white focus:outline-none focus:border-blue-500"
        >
          <option value="">Выберите категорию</option>
          <option value="repair">🏠 Ремонт</option>
          <option value="business">💼 Бизнес</option>
          <option value="fashion">👗 Мода</option>
          <option value="education">📚 Обучение</option>
          <option value="design">🎨 Дизайн</option>
          <option value="it">💻 IT</option>
        </select>
      </div>

      <div>
        <label class="block text-sm font-semibold mb-2">Цена за услугу (₽)</label>
        <input
            :value="formData.price"
            @input="updateField('price', Number(($event.target as HTMLInputElement).value))"
            type="number"
            placeholder="500"
            class="w-full bg-slate-700 border border-blue-900 rounded-lg px-4 py-2 text-white placeholder-gray-500 focus:outline-none focus:border-blue-500"
        />
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
</script>

<style scoped></style>
