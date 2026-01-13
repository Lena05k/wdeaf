<template>
  <AuthLayout>
    <form @submit.prevent="handleForgotPassword" class="space-y-4">
      <h2 class="text-2xl font-bold text-center mb-2">Восстановление пароля</h2>
      <p class="text-center text-sm text-gray-400 mb-6">
        Введите email, и мы отправим ссылку для восстановления пароля
      </p>

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

      <!-- Success Message -->
      <div v-if="successMessage" class="p-3 rounded-lg bg-green-900 border border-green-500 text-green-300 text-sm">
        {{ successMessage }}
      </div>

      <!-- Submit Button -->
      <button
        type="submit"
        :disabled="loading"
        class="w-full py-2 px-4 bg-blue-600 hover:bg-blue-500 disabled:bg-gray-600 text-white font-semibold rounded-lg transition"
      >
        {{ loading ? 'Отправка...' : 'Отправить ссылку' }}
      </button>

      <!-- Back Link -->
      <div class="text-center">
        <router-link to="/login" class="text-blue-400 hover:text-blue-300 text-sm">
          ← Вернуться к входу
        </router-link>
      </div>
    </form>
  </AuthLayout>
</template>

<script>
import AuthLayout from '@/components/layout/AuthLayout.vue'

export default {
  name: 'ForgotPasswordPage',
  components: {
    AuthLayout
  },
  data() {
    return {
      form: {
        email: ''
      },
      loading: false,
      successMessage: '',
      error: ''
    }
  },
  methods: {
    async handleForgotPassword() {
      this.loading = true;
      this.error = '';
      this.successMessage = '';

      try {
        // Имитация API запроса
        await new Promise(resolve => setTimeout(resolve, 1500));

        // Показать сообщение об успехе
        this.successMessage = `Ссылка для восстановления пароля отправлена на ${this.form.email}`;

        // Очистить форму
        this.form.email = '';

        // Редирект на логин после 3 секунд
        setTimeout(() => {
          this.$router.push({ name: 'login' });
        }, 3000);
      } catch (err) {
        this.error = 'Ошибка при отправке. Попробуйте снова.';
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
