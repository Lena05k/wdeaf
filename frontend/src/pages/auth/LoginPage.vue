<template>
  <AuthLayout>
    <form @submit.prevent="handleLogin" class="space-y-4">
      <h2 class="text-2xl font-bold text-center mb-6">Вход в аккаунт</h2>

      <!-- Error -->
      <div
        v-if="authStore.error"
        class="p-3 rounded-lg bg-red-900/30 border border-red-500/50 text-red-300 text-sm"
      >
        {{ authStore.error }}
      </div>

      <!-- Email Input -->
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

      <!-- Password Input -->
      <div>
        <label for="password" class="block text-sm font-medium text-gray-300 mb-2">
          Пароль
        </label>
        <input
          id="password"
          v-model="form.password"
          type="password"
          placeholder="••••••••"
          autocomplete="current-password"
          class="w-full px-4 py-3 rounded-lg bg-slate-700 border border-slate-600 text-white placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-blue-400 focus:border-transparent transition"
          required
        />
      </div>

      <!-- Submit -->
      <button
        type="submit"
        :disabled="authStore.loading"
        class="w-full py-3 px-4 bg-blue-600 hover:bg-blue-500 disabled:bg-gray-600 disabled:cursor-not-allowed text-white font-semibold rounded-lg transition"
      >
        {{ authStore.loading ? 'Загрузка...' : 'Войти' }}
      </button>

      <!-- Links -->
      <div class="text-center space-y-2 text-sm">
        <router-link to="/forgot-password" class="block text-blue-400 hover:text-blue-300">
          Забыли пароль?
        </router-link>
        <p class="text-gray-400">
          Нет аккаунта?
          <router-link to="/signup" class="text-blue-400 hover:text-blue-300">
            Зарегистрируйтесь
          </router-link>
        </p>
      </div>
    </form>
  </AuthLayout>
</template>

<script setup lang="ts">
import { reactive } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../../stores/authStore'
import AuthLayout from '../../components/layout/AuthLayout.vue'

const router = useRouter()
const authStore = useAuthStore()

const form = reactive({
  email: '',
  password: '',
})

async function handleLogin(): Promise<void> {
  const success = await authStore.login({
    email: form.email,
    password: form.password,
  })
  if (success) {
    router.push({ name: 'catalog' })
  }
}
</script>
