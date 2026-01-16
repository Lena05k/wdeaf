<template>
  <AuthLayout>
    <form @submit.prevent="handleLogin" class="space-y-4">
      <h2 class="text-2xl font-bold text-center mb-6">Вход в аккаунт</h2>

      <!-- Email Input -->
      <div class="form-group">
        <label for="email" class="block text-sm font-medium text-gray-300 mb-2">
          Email или username
        </label>
        <input
          id="email"
          v-model="form.email"
          type="text"
          placeholder="user@example.com"
          class="form-input w-full px-4 py-2 rounded-lg bg-slate-700 border border-blue-500 text-white placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-blue-400"
          required
        >
      </div>

      <!-- Password Input -->
      <div class="form-group">
        <label for="password" class="block text-sm font-medium text-gray-300 mb-2">
          Пароль
        </label>
        <input
          id="password"
          v-model="form.password"
          type="password"
          placeholder="••••••••"
          class="form-input w-full px-4 py-2 rounded-lg bg-slate-700 border border-blue-500 text-white placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-blue-400"
          required
        >
      </div>

      <!-- Remember Me -->
      <div class="flex items-center">
        <input
          id="remember"
          v-model="form.remember"
          type="checkbox"
          class="w-4 h-4 rounded border-blue-500 cursor-pointer"
        >
        <label for="remember" class="ml-2 text-sm text-gray-400 cursor-pointer">
          Запомнить меня
        </label>
      </div>

      <!-- Submit Button -->
      <button
        type="submit"
        :disabled="loading"
        class="w-full py-2 px-4 bg-blue-600 hover:bg-blue-500 disabled:bg-gray-600 text-white font-semibold rounded-lg transition"
      >
        {{ loading ? 'Загрузка...' : 'Вход' }}
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

<script>
import AuthLayout from '../../components/layout/AuthLayout.vue'

export default {
  name: 'LoginPage',
  components: {
    AuthLayout
  },
  data() {
    return {
      form: {
        email: '',
        password: '',
        remember: false
      },
      loading: false,
      error: ''
    }
  },
  methods: {
    async handleLogin() {
      this.loading = true;
      this.error = '';

      try {
        // Имитация API запроса
        await new Promise(resolve => setTimeout(resolve, 1500));

        // Сохранить токен
        localStorage.setItem('authToken', 'mock-token-' + Date.now());
        localStorage.setItem('user', JSON.stringify({
          email: this.form.email,
          id: '123456789',
          first_name: 'Иван'
        }));

        // Редирект на главную
        this.$router.push({ name: 'home' });
      } catch (err) {
        this.error = 'Ошибка при входе. Попробуйте снова.';
      } finally {
        this.loading = false;
      }
    }
  }
}
</script>

<style scoped>
.form-group {
  margin-bottom: 1rem;
}

.form-input {
  transition: all 0.3s ease;
}

.form-input:focus {
  border-color: #0055FF;
  box-shadow: 0 0 0 3px rgba(0, 85, 255, 0.1);
}
</style>
