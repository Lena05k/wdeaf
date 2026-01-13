<template>
  <div class="auth-layout min-h-screen bg-gradient-to-br from-slate-900 via-slate-800 to-slate-900 flex items-center justify-center p-4">
    <div class="auth-container max-w-md w-full">
      <!-- Header -->
      <div class="text-center mb-8">
        <h1 class="text-4xl font-bold text-blue-400 mb-2">WDEAF</h1>
        <p class="text-gray-400">Платформа услуг и сервисов</p>
      </div>

      <!-- Content Slot -->
      <div class="auth-content bg-slate-800 rounded-lg border border-blue-500 p-6 shadow-lg">
        <slot></slot>
      </div>

      <!-- Footer -->
      <div class="text-center mt-6 text-xs text-gray-500">
        <p>
          <slot name="footer">
            © 2026 WDEAF. Все права защищены.
          </slot>
        </p>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'AuthLayout'
}
</script>

<style scoped>
.auth-layout {
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
}

.auth-container {
  animation: fadeIn 0.3s ease-out;
}

.auth-content {
  backdrop-filter: blur(10px);
}

@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

/* Responsive */
@media (max-width: 640px) {
  .auth-container {
    padding: 16px;
  }
}
</style>
