<template>
  <AuthLayout>
    <form @submit.prevent="handleSignup" class="space-y-4">
      <h2 class="text-2xl font-bold text-center mb-6">Создать аккаунт</h2>

      <!-- First Name Input -->
      <div class="form-group">
        <label for="firstName" class="block text-sm font-medium text-gray-300 mb-2">
          Имя
        </label>
        <input
          id="firstName"
          v-model="form.firstName"
          type="text"
          placeholder="Иван"
          class="form-input w-full px-4 py-2 rounded-lg bg-slate-700 border border-blue-500 text-white placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-blue-400"
          required
        >
      </div>

      <!-- Email Input -->
      <div class="form-group">
        <label for="email" class="block text-sm font-medium text-gray-300 mb-2">
          Email
        </label>
        <input
          id="email"
          v-model="form.email"
          type="email"
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
        <p class="text-xs text-gray-400 mt-1">Минимум 8 символов</p>
      </div>

      <!-- Confirm Password Input -->
      <div class="form-group">
        <label for="confirmPassword" class="block text-sm font-medium text-gray-300 mb-2">
          Подтверждение пароля
        </label>
        <input
          id="confirmPassword"
          v-model="form.confirmPassword"
          type="password"
          placeholder="••••••••"
          class="form-input w-full px-4 py-2 rounded-lg bg-slate-700 border border-blue-500 text-white placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-blue-400"
          required
        >
      </div>

      <!-- Terms Checkbox -->
      <div class="flex items-start">
        <input
          id="terms"
          v-model="form.terms"
          type="checkbox"
          class="w-4 h-4 rounded border-blue-500 cursor-pointer mt-1"
          required
        >
        <label for="terms" class="ml-2 text-sm text-gray-400 cursor-pointer">
          Я согласен с
          <router-link to="#" class="text-blue-400 hover:text-blue-300">
            условиями использования
          </router-link>
        </label>
      </div>

      <!-- Submit Button -->
      <button
        type="submit"
        :disabled="loading"
        class="w-full py-2 px-4 bg-blue-600 hover:bg-blue-500 disabled:bg-gray-600 text-white font-semibold rounded-lg transition"
      >
        {{ loading ? 'Загрузка...' : 'Зарегистрироваться' }}
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

<script>
import AuthLayout from '@/components/layout/AuthLayout.vue'

export default {
  name: 'SignupPage',
  components: {
    AuthLayout
  },
  data() {
    return {
      form: {
        firstName: '',
        email: '',
        password: '',
        confirmPassword: '',
        terms: false
      },
      loading: false,
      error: ''
    }
  },
  methods: {
    async handleSignup() {
      // Валидация
      if (this.form.password !== this.form.confirmPassword) {
        this.error = 'Пароли не совпадают';
        return;
      }

      if (this.form.password.length < 8) {
        this.error = 'Пароль должен быть минимум 8 символов';
        return;
      }

      this.loading = true;
      this.error = '';

      try {
        // Имитация API запроса
        await new Promise(resolve => setTimeout(resolve, 1500));

        // Сохранить данные пользователя
        localStorage.setItem('authToken', 'mock-token-' + Date.now());
        localStorage.setItem('user', JSON.stringify({
          email: this.form.email,
          firstName: this.form.firstName,
          id: '123456789'
        }));

        // Редирект на главную
        this.$router.push({ name: 'home' });
      } catch (err) {
        this.error = 'Ошибка при регистрации. Попробуйте снова.';
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
