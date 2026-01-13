<template>
  <div
      @click="selectCategory"
      class="bg-gradient-to-br from-blue-600 to-blue-500 rounded-lg p-4 cursor-pointer hover:shadow-lg transition text-white text-center"
  >
    <p class="text-3xl mb-2">{{ category.icon }}</p>
    <p class="font-semibold text-sm">{{ category.name }}</p>
    <p class="text-xs mt-1 opacity-80">{{ category.count }} услуг</p>
  </div>
</template>

<script>
export default {
  name: 'CategoryCard',
  props: {
    category: {
      type: Object,
      required: true,
      validator: (obj) => obj.id && obj.name && obj.icon && typeof obj.count === 'number'
    }
  },
  emits: ['select'],
  methods: {
    selectCategory() {
      this.$emit('select', this.category);
    }
  }
}
</script>

<style scoped>
</style>
