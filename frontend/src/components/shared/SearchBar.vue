<template>
  <div class="space-y-3">
    <input
        :value="searchQuery"
        @input="$emit('update:searchQuery', $event.target.value)"
        type="text"
        placeholder="🔍 Поиск услуг..."
        class="search-input w-full px-4 py-2 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
    >

    <div class="flex gap-2 overflow-x-auto pb-2">
      <button
          v-for="cat in categories"
          :key="cat"
          @click="toggleCategory(cat)"
          :class="['catalog-btn', selectedCategory === cat ? 'active' : '']"
      >
        {{ cat }}
      </button>
    </div>
  </div>
</template>

<script>
export default {
  name: 'SearchBar',
  props: {
    searchQuery: {
      type: String,
      default: ''
    },
    selectedCategory: {
      type: String,
      default: ''
    },
    categories: {
      type: Array,
      required: true
    }
  },
  emits: ['update:searchQuery', 'update:selectedCategory'],
  methods: {
    toggleCategory(cat) {
      const newCategory = this.selectedCategory === cat ? '' : cat;
      this.$emit('update:selectedCategory', newCategory);
    }
  }
}
</script>

<style scoped>
.search-input {
  background: rgba(255, 255, 255, 0.1);
  color: #FFFFFF;
  border: 1px solid #0055FF;
}

.search-input::placeholder {
  color: rgba(255, 255, 255, 0.5);
}

.catalog-btn {
  padding: 8px 16px;
  border-radius: 20px;
  font-size: 13px;
  font-weight: 500;
  border: 1px solid #0055FF;
  background: transparent;
  color: #0055FF;
  cursor: pointer;
  white-space: nowrap;
  transition: all 0.3s;
}

.catalog-btn.active {
  background: #0055FF;
  color: #FFFFFF;
}

.catalog-btn:hover {
  background: rgba(0, 85, 255, 0.15);
}
</style>
