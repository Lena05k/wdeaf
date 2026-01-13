<template>
  <div class="profile-page">
    <Header :userData="userData" class="sticky top-0 z-50" />
    
    <main class="max-w-md mx-auto pb-20">
      <ProfileView 
        :userData="userData"
        :ordersCount="userOrders.length"
        @become-provider="handleBecomeProvider"
        @open-settings="handleOpenSettings"
      />
    </main>

    <Toast v-if="showToast" :message="toastMessage" />
  </div>
</template>

<script>
import Header from '../components/layout/Header.vue'
import ProfileView from '../views/ProfileView.vue'
import Toast from '../components/shared/Toast.vue'

export default {
  name: 'ProfilePage',
  components: {
    Header,
    ProfileView,
    Toast
  },
  data() {
    return {
      userData: {
        first_name: 'Иван',
        id: '123456789',
        username: 'ivan_user'
      },
      userOrders: [
        {
          id: 1,
          service: 'Уроки английского',
          provider: 'Джон Д.',
          status: 'active',
          price: 1500,
          date: 'сегодня 15:00'
        },
        {
          id: 2,
          service: 'Консультация бухгалтера',
          provider: 'Мария С.',
          status: 'pending',
          price: 3000,
          date: 'завтра 10:00'
        }
      ],
      showToast: false,
      toastMessage: ''
    }
  },
  methods: {
    handleBecomeProvider() {
      this.showToast = true;
      this.toastMessage = 'Скоро вы сможете стать исполнителем!';
      setTimeout(() => {
        this.showToast = false;
      }, 3000);
    },
    handleOpenSettings() {
      this.showToast = true;
      this.toastMessage = 'Настройки откроются вскоре';
      setTimeout(() => {
        this.showToast = false;
      }, 3000);
    }
  }
}
</script>

<style scoped>
</style>
