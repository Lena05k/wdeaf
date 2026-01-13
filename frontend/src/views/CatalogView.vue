<template>
  <div class="p-4 space-y-4">
    <h2 class="text-lg font-bold mb-4">Категории услуг</h2>
    
    <div class="grid grid-cols-2 gap-3">
      <CategoryCard 
        v-for="cat in catalogCategories"
        :key="cat.id"
        :category="cat"
        @select="selectCategory(cat)"
      />
    </div>
  </div>
</template>

<script>
import CategoryCard from '../components/shared/CategoryCard.vue'

export default {
  name: 'CatalogView',
  components: {
    CategoryCard
  },
  props: {
    catalogCategories: {
      type: Array,
      required: true
    }
  },
  emits: ['category-selected'],
  methods: {
    selectCategory(category) {
      this.$emit('category-selected', category);
    }
  }
}
</script>

<style scoped>
</style>
