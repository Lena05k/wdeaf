<template>
  <AuthLayout>
    <form @submit.prevent="handleSignup" class="space-y-4">
      <h2 class="text-2xl font-bold text-center mb-6">Создать аккаунт</h2>

      <!-- Error -->
      <div
        v-if="authStore.error"
        class="p-3 rounded-lg bg-red-900/30 border border-red-500/50 text-red-300 text-sm"
      >
        {{ authStore.error }}
      </div>

      <!-- First Name -->
      <div>
        <label for="firstName" class="block text-sm font-medium text-gray-300 mb-2">
          Имя
        </label>
        <input
          id="firstName"
          v-model="form.firstName"
          type="text"
          placeholder="Иван"
          autocomplete="given-name"
          class="w-full px-4 py-3 rounded-lg bg-slate-700 border border-slate-600 text-white placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-blue-400 focus:border-transparent transition"
          required
        />
      </div>

      <!-- Last Name -->
      <div>
        <label for="lastName" class="block text-sm font-medium text-gray-300 mb-2">
          Фамилия <span class="text-gray-500">(необязательно)</span>
        </label>
        <input
          id="lastName"
          v-model="form.lastName"
          type="text"
          placeholder="Иванов"
          autocomplete="family-name"
          class="w-full px-4 py-3 rounded-lg bg-slate-700 border border-slate-600 text-white placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-blue-400 focus:border-transparent transition"
        />
      </div>

      <!-- Email -->
      <div>
        <label for="email" class="block text-sm font-medium text-gray-300 mb-2">
          Email
        </label>
        <input
          id="email"
          v-model="form.email"
          type="email"
          placeholder="user@example.com"
          autocomplete="email"
          class="w-full px-4 py-3 rounded-lg bg-slate-700 border border-slate-600 text-white placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-blue-400 focus:border-transparent transition"
          required
        />
      </div>

      <!-- Password -->
      <div>
        <label for="password" class="block text-sm font-medium text-gray-300 mb-2">
          Пароль
        </label>
        <input
          id="password"
          v-model="form.password"
          type="password"
          placeholder="••••••••"
          autocomplete="new-password"
          class="w-full px-4 py-3 rounded-lg bg-slate-700 border border-slate-600 text-white placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-blue-400 focus:border-transparent transition"
          required
        />
        <p class="text-xs text-gray-400 mt-1">Минимум 8 символов, хотя бы 1 цифра</p>
      </div>

      <!-- Confirm Password -->
      <div>
        <label for="confirmPassword" class="block text-sm font-medium text-gray-300 mb-2">
          Подтверждение пароля
        </label>
        <input
          id="confirmPassword"
          v-model="form.confirmPassword"
          type="password"
          placeholder="••••••••"
          autocomplete="new-password"
          class="w-full px-4 py-3 rounded-lg bg-slate-700 border border-slate-600 text-white placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-blue-400 focus:border-transparent transition"
          required
        />
        <p v-if="passwordMismatch" class="text-xs text-red-400 mt-1">
          Пароли не совпадают
        </p>
      </div>

      <!-- Terms -->
      <div class="flex items-start">
        <input
          id="terms"
          v-model="form.terms"
          type="checkbox"
          class="w-4 h-4 rounded border-blue-500 cursor-pointer mt-1"
          required
        />
        <label for="terms" class="ml-2 text-sm text-gray-400 cursor-pointer">
          Я согласен с
          <router-link to="#" class="text-blue-400 hover:text-blue-300">
            условиями использования
          </router-link>
        </label>
      </div>

      <!-- Submit -->
      <button
        type="submit"
        :disabled="authStore.loading || passwordMismatch"
        class="w-full py-3 px-4 bg-blue-600 hover:bg-blue-500 disabled:bg-gray-600 disabled:cursor-not-allowed text-white font-semibold rounded-lg transition"
      >
        {{ authStore.loading ? 'Загрузка...' : 'Зарегистрироваться' }}
      </button>

      <!-- Links -->
      <p class="text-center text-sm text-gray-400">
        Уже есть аккаунт?
        <router-link to="/login" class="text-blue-400 hover:text-blue-300">
          Войти
        </router-link>
      </p>
    </form>
  </AuthLayout>
</template>

<script setup lang="ts">
import { reactive, computed } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../../stores/authStore'
import AuthLayout from '../../components/layout/AuthLayout.vue'

const router = useRouter()
const authStore = useAuthStore()

const form = reactive({
  firstName: '',
  lastName: '',
  email: '',
  password: '',
  confirmPassword: '',
  terms: false,
})

const passwordMismatch = computed(
  () => form.confirmPassword.length > 0 && form.password !== form.confirmPassword,
)

async function handleSignup(): Promise<void> {
  if (form.password !== form.confirmPassword) return

  const success = await authStore.signup({
    email: form.email,
    password: form.password,
    first_name: form.firstName,
    last_name: form.lastName || undefined,
  })

  if (success) {
    router.push({ name: 'catalog' })
  }
}
</script>
