<template>
  <div class="not-found-page min-h-screen bg-gradient-to-br from-slate-900 via-slate-800 to-slate-900 flex items-center justify-center p-4">
    <div class="text-center max-w-md">
      <h1 class="text-6xl font-bold text-blue-400 mb-4">404</h1>
      <h2 class="text-2xl font-bold text-white mb-2">Страница не найдена</h2>
      <p class="text-gray-400 mb-8">
        Похоже, страница, которую вы ищете, не существует или была удалена.
      </p>

      <div class="space-y-3">
        <router-link
          to="/"
          class="block py-2 px-4 bg-blue-600 hover:bg-blue-500 text-white font-semibold rounded-lg transition"
        >
          На главную страницу
        </router-link>
        <button
          @click="goBack"
          class="w-full py-2 px-4 bg-slate-700 hover:bg-slate-600 text-white font-semibold rounded-lg transition"
        >
          Назад
        </button>
      </div>

      <!-- Logo -->
      <div class="mt-12">
        <h3 class="text-3xl font-bold text-blue-400">WDEAF</h3>
        <p class="text-gray-500 text-sm">Платформа услуг и сервисов</p>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'NotFoundPage',
  methods: {
    goBack() {
      this.$router.back();
    }
  }
}
</script>

<style scoped>
</style>
