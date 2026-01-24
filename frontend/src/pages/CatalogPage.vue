<template>
  <div class="catalog-page">
    <Header :userData="userData" class="sticky top-0 z-50" />
    
    <main class="max-w-md mx-auto pb-20">
      <CatalogView 
        :catalogCategories="catalogCategories"
        @category-selected="handleCategorySelect"
      />
    </main>

    <Toast v-if="showToast" :message="toastMessage" />
  </div>
</template>

<script>
import Header from '../components/layout/Header.vue'
import Toast from '../components/shared/Toast.vue'
import CatalogView from '@/views/CatalogView.vue'

export default {
  name: 'CatalogPage',
  components: {
    Header,
    CatalogView,
    Toast
  },
  data() {
    return {
      userData: {
        first_name: 'Иван',
        id: '123456789',
        username: 'ivan_user'
      },
      catalogCategories: [
        { id: 1, name: 'Ремонт', icon: '🔧', count: 23 },
        { id: 2, name: 'Бизнес', icon: '📊', count: 18 },
        { id: 3, name: 'Мода', icon: '✂️', count: 34 },
        { id: 4, name: 'Обучение', icon: '📖', count: 45 },
        { id: 5, name: 'Дизайн', icon: '🎭', count: 29 },
        { id: 6, name: 'IT', icon: '💻', count: 56 }
      ],
      showToast: false,
      toastMessage: ''
    }
  },
  methods: {
    handleCategorySelect(category) {
      this.$router.push({
        name: 'home',
        query: { category: category.name }
      });
    }
  }
}
</script>

<style scoped>
</style>
