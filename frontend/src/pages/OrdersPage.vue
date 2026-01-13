<template>
  <div class="orders-page">
    <Header :userData="userData" class="sticky top-0 z-50" />
    
    <main class="max-w-md mx-auto pb-20">
      <OrdersView 
        :userOrders="userOrders"
        @browse-services="goToHome"
        @cancel-order="handleCancelOrder"
      />
    </main>

    <Toast v-if="showToast" :message="toastMessage" />
  </div>
</template>

<script>
import OrdersView from '@/views/OrdersView.vue'
import Header from '../components/layout/Header.vue'
import Toast from '../components/shared/Toast.vue'

export default {
  name: 'OrdersPage',
  components: {
    Header,
    OrdersView,
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
    goToHome() {
      this.$router.push({ name: 'home' });
    },
    handleCancelOrder(orderId) {
      this.userOrders = this.userOrders.filter(order => order.id !== orderId);
      this.showToast = true;
      this.toastMessage = '✓ Заказ отменен';
      setTimeout(() => {
        this.showToast = false;
      }, 3000);
    }
  }
}
</script>

<style scoped>
</style>
