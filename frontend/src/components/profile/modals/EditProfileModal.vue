<template>
  <div class="fixed inset-0 bg-black/50 flex items-end z-50 animate-in" @click="$emit('close')">
    <div class="bg-slate-800 w-full rounded-t-3xl border-t border-slate-700 max-h-[90vh] overflow-y-auto" @click.stop>
      <!-- Header -->
      <div class="sticky top-0 bg-gradient-to-b from-slate-800 to-slate-900 border-b border-slate-700 p-4 flex justify-between items-center">
        <h2 class="text-xl font-bold text-white flex items-center gap-2">
          <span>✏️</span> Редактировать профиль
        </h2>
        <button @click="$emit('close')" class="text-gray-400 hover:text-white text-2xl">
          ✕
        </button>
      </div>

      <!-- Content -->
      <div class="p-4 space-y-4">
        <!-- First Name -->
        <div>
          <label class="block text-sm font-semibold mb-2 text-gray-300">Имя</label>
          <input
            v-model="form.first_name"
            type="text"
            placeholder="Ваше имя"
            class="w-full bg-slate-700 border border-slate-600 rounded-lg px-4 py-2 text-white placeholder-gray-500 focus:outline-none focus:border-blue-500 focus:ring-2 focus:ring-blue-500/30"
          />
          <p v-if="errors.first_name" class="text-xs text-red-500 mt-1">{{ errors.first_name }}</p>
        </div>

        <!-- Last Name (Optional) -->
        <div>
          <label class="block text-sm font-semibold mb-2 text-gray-300">Фамилия (опционально)</label>
          <input
            v-model="form.last_name"
            type="text"
            placeholder="Ваша фамилия"
            class="w-full bg-slate-700 border border-slate-600 rounded-lg px-4 py-2 text-white placeholder-gray-500 focus:outline-none focus:border-blue-500 focus:ring-2 focus:ring-blue-500/30"
          />
        </div>

        <!-- Username -->
        <div>
          <label class="block text-sm font-semibold mb-2 text-gray-300">Юзернейм</label>
          <input
            v-model="form.username"
            type="text"
            placeholder="ваш_юзернейм"
            class="w-full bg-slate-700 border border-slate-600 rounded-lg px-4 py-2 text-white placeholder-gray-500 focus:outline-none focus:border-blue-500 focus:ring-2 focus:ring-blue-500/30"
          />
          <p v-if="errors.username" class="text-xs text-red-500 mt-1">{{ errors.username }}</p>
          <p class="text-xs text-gray-500 mt-1">Минимум 3 символа, без пробелов</p>
        </div>

        <!-- Email (Optional) -->
        <div>
          <label class="block text-sm font-semibold mb-2 text-gray-300">Email (опционально)</label>
          <input
            v-model="form.email"
            type="email"
            placeholder="your@email.com"
            class="w-full bg-slate-700 border border-slate-600 rounded-lg px-4 py-2 text-white placeholder-gray-500 focus:outline-none focus:border-blue-500 focus:ring-2 focus:ring-blue-500/30"
          />
          <p v-if="errors.email" class="text-xs text-red-500 mt-1">{{ errors.email }}</p>
        </div>

        <!-- Phone (Optional) -->
        <div>
          <label class="block text-sm font-semibold mb-2 text-gray-300">Телефон (опционально)</label>
          <input
            v-model="form.phone"
            type="tel"
            placeholder="+7 (XXX) XXX-XX-XX"
            class="w-full bg-slate-700 border border-slate-600 rounded-lg px-4 py-2 text-white placeholder-gray-500 focus:outline-none focus:border-blue-500 focus:ring-2 focus:ring-blue-500/30"
          />
          <p v-if="errors.phone" class="text-xs text-red-500 mt-1">{{ errors.phone }}</p>
        </div>
      </div>

      <!-- Footer -->
      <div class="sticky bottom-0 bg-gradient-to-t from-slate-800 to-slate-900 border-t border-slate-700 p-4 flex gap-2">
        <button
          @click="$emit('close')"
          class="flex-1 bg-slate-700 hover:bg-slate-600 text-white font-semibold py-3 rounded-lg transition active:scale-95"
        >
          Отмена
        </button>
        <button
          @click="handleSubmit"
          :disabled="!isFormValid"
          :class="[
            'flex-1 font-semibold py-3 rounded-lg transition active:scale-95',
            isFormValid
              ? 'bg-blue-600 hover:bg-blue-500 text-white'
              : 'bg-gray-700 text-gray-400 cursor-not-allowed'
          ]"
        >
          ✓ Сохранить
        </button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'

interface User {
  id: string | number
  first_name: string
  last_name?: string
  username?: string
  email?: string
  phone?: string
}

interface Props {
  user: User
}

const props = defineProps<Props>()

const emit = defineEmits<{
  submit: [data: User]
  close: []
}>()

// Form state
const form = ref<User>({
  id: props.user.id,
  first_name: props.user.first_name,
  last_name: props.user.last_name || '',
  username: props.user.username || '',
  email: props.user.email || '',
  phone: props.user.phone || ''
})

const errors = ref<Record<string, string>>({})

// Validation
const validateForm = () => {
  errors.value = {}

  // First name required
  if (!form.value.first_name.trim()) {
    errors.value.first_name = 'Имя обязательно'
  } else if (form.value.first_name.trim().length < 2) {
    errors.value.first_name = 'Имя должно быть не менее 2 символов'
  }

  // Username validation (if provided)
  if (form.value.username) {
    if (form.value.username.length < 3) {
      errors.value.username = 'Юзернейм должен быть не менее 3 символов'
    } else if (!/^[a-zA-Z0-9_]+$/.test(form.value.username)) {
      errors.value.username = 'Юзернейм может содержать только буквы, цифры и подчеркивание'
    }
  }

  // Email validation (if provided)
  if (form.value.email) {
    if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(form.value.email)) {
      errors.value.email = 'Некорректный email'
    }
  }

  return Object.keys(errors.value).length === 0
}

const isFormValid = computed(() => {
  return form.value.first_name.trim().length >= 2
})

const handleSubmit = () => {
  if (!validateForm()) return

  emit('submit', {
    id: form.value.id,
    first_name: form.value.first_name,
    last_name: form.value.last_name || undefined,
    username: form.value.username || undefined,
    email: form.value.email || undefined,
    phone: form.value.phone || undefined
  })
}
</script>

<style scoped>
@keyframes fadeIn {
  from {
    opacity: 0;
  }
  to {
    opacity: 1;
  }
}

.animate-in {
  animation: fadeIn 0.3s ease-out;
}
</style>