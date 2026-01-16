<template>
  <div class="space-y-3">
    <!-- Search Input -->
    <input
        :value="searchQuery"
        @input="$emit('update:searchQuery', $event.target.value)"
        type="text"
        placeholder="🔍 Поиск услуг..."
        class="search-input w-full px-4 py-2 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
    >

    <!-- Categories Filter -->
    <div class="flex gap-2 overflow-x-auto pb-2 scrollbar-hide">
      <!-- All Button (Show all services) -->
      <button
          @click="$emit('update:selectedCategory', '')"
          :class="['catalog-btn', selectedCategory === '' ? 'active' : '']"
      >
        🌟 Все
      </button>

      <!-- Category Buttons -->
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
  font-size: 14px;
}

.search-input::placeholder {
  color: rgba(255, 255, 255, 0.5);
}

.search-input:focus {
  background: rgba(255, 255, 255, 0.12);
  border-color: #0077ff;
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
  transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1);
  flex-shrink: 0;
}

.catalog-btn:active {
  transform: scale(0.95);
}

.catalog-btn.active {
  background: #0055FF;
  color: #FFFFFF;
  box-shadow: 0 0 12px rgba(0, 85, 255, 0.4);
}

.catalog-btn:hover {
  background: rgba(0, 85, 255, 0.15);
}

/* Smooth scrolling */
.scrollbar-hide {
  -ms-overflow-style: none;
  scrollbar-width: none;
}

.scrollbar-hide::-webkit-scrollbar {
  display: none;
}
</style>