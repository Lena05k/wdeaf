<template>
  <div class="p-4 space-y-4">
    <!-- Profile Info Card -->
    <div class="provider-card">
      <h2 class="text-lg font-bold mb-4">Мой профиль</h2>
      
      <div class="space-y-3">
        <ProfileRow label="ID" :value="userData.id" />
        <ProfileRow label="Username" :value="`@${userData.username || 'N/A'}`" />
        <ProfileRow label="Заказов" :value="String(ordersCount)" />
        <ProfileRow 
          label="Рейтинг" 
          :value="`★★★★☆ (4.8)`" 
          class="text-yellow-400"
        />
      </div>
    </div>

    <!-- Actions Card -->
    <div class="provider-card">
      <h3 class="font-bold mb-3">Действия</h3>
      
      <button 
        @click="$emit('become-provider')"
        class="w-full btn-primary py-2 rounded-lg font-semibold text-sm mb-2"
      >
        📝 Стать исполнителем
      </button>
      
      <button 
        @click="$emit('open-settings')"
        class="w-full btn-secondary py-2 rounded-lg font-semibold text-sm"
      >
        ⚙️ Настройки
      </button>
    </div>

    <!-- Additional Info -->
    <div class="provider-card">
      <h3 class="font-bold mb-3">О платформе</h3>
      <p class="text-sm text-gray-400">WDEAF - платформа для поиска и заказа услуг</p>
      <p class="text-xs text-gray-500 mt-2">Версия 1.0.0</p>
    </div>
  </div>
</template>

<script>
export default {
  name: 'ProfileView',
  props: {
    userData: {
      type: Object,
      required: true
    },
    ordersCount: {
      type: Number,
      default: 0
    }
  },
  emits: ['become-provider', 'open-settings'],
  components: {
    ProfileRow: {
      props: {
        label: String,
        value: String
      },
      template: `
        <div class="flex justify-between py-2 border-b border-blue-900">
          <span class="text-gray-400">{{ label }}:</span>
          <span class="font-semibold">{{ value }}</span>
        </div>
      `
    }
  }
}
</script>

<style scoped>
</style>
