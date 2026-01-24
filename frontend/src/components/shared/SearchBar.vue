<template>
  <div class="search-container">
    <!-- Search Input -->
    <div class="search-wrapper">
      <svg class="search-icon" width="16" height="16" viewBox="0 0 16 16" fill="none">
        <circle cx="6.5" cy="6.5" r="4.5" stroke="currentColor" stroke-width="1.2"/>
        <path d="M10.5 10.5L14 14" stroke="currentColor" stroke-width="1.2" stroke-linecap="round"/>
      </svg>
      <input
        :value="searchQuery"
        @input="$emit('update:searchQuery', $event.target.value)"
        type="text"
        placeholder="Поиск услуг..."
        class="search-input"
      />
    </div>

    <!-- Categories Filter -->
    <div class="categories-scroll">
      <!-- All Button (Show all services) -->
      <button
        @click="$emit('update:selectedCategory', '')"
        :class="['category-btn', selectedCategory === '' ? 'active' : '']"
      >
        Все
      </button>

      <!-- Category Buttons -->
      <button
        v-for="cat in categories"
        :key="cat"
        @click="toggleCategory(cat)"
        :class="['category-btn', selectedCategory === cat ? 'active' : '']"
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
      const newCategory = this.selectedCategory === cat ? '' : cat
      this.$emit('update:selectedCategory', newCategory)
    }
  }
}
</script>

<style scoped>
.search-container {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

/* Search Wrapper */
.search-wrapper {
  position: relative;
  display: flex;
  align-items: center;
}

.search-icon {
  position: absolute;
  left: 12px;
  color: var(--color-text-secondary, #999);
  pointer-events: none;
  flex-shrink: 0;
}

.search-input {
  width: 100%;
  padding: 10px 12px 10px 36px;
  background: var(--color-surface, #fff);
  color: var(--color-text, #000);
  border: 1px solid var(--color-border, #e5e5e5);
  border-radius: 8px;
  font-size: 14px;
  transition: all 0.2s ease;
  font-family: inherit;
}

.search-input::placeholder {
  color: var(--color-text-secondary, #999);
}

.search-input:focus {
  outline: none;
  border-color: var(--color-primary, #0055FF);
  background: var(--color-surface, #fff);
  box-shadow: 0 0 0 3px rgba(0, 85, 255, 0.1);
}

.search-input:hover {
  border-color: var(--color-primary, #0055FF);
}

/* Categories Scroll */
.categories-scroll {
  display: flex;
  gap: 8px;
  overflow-x: auto;
  overflow-y: hidden;
  padding-bottom: 4px;
  -webkit-overflow-scrolling: touch;
}

.categories-scroll::-webkit-scrollbar {
  display: none;
}

.categories-scroll {
  -ms-overflow-style: none;
  scrollbar-width: none;
}

/* Category Button */
.category-btn {
  padding: 8px 14px;
  border-radius: 6px;
  font-size: 13px;
  font-weight: 500;
  border: 1px solid var(--color-border, #e5e5e5);
  background: var(--color-surface, #fff);
  color: var(--color-text, #000);
  cursor: pointer;
  white-space: nowrap;
  transition: all 0.2s cubic-bezier(0.16, 1, 0.3, 1);
  flex-shrink: 0;
  font-family: inherit;
}

.category-btn:hover {
  border-color: var(--color-primary, #0055FF);
  background: var(--color-bg-1, #f0f5ff);
  color: var(--color-primary, #0055FF);
}

.category-btn:active {
  transform: scale(0.95);
}

.category-btn.active {
  background: var(--color-primary, #0055FF);
  color: white;
  border-color: var(--color-primary, #0055FF);
  box-shadow: 0 2px 8px rgba(0, 85, 255, 0.3);
}

/* Dark mode support */
@media (prefers-color-scheme: dark) {
  .search-input {
    background: #2a2a2a;
    border-color: #444;
    color: #fff;
  }
  
  .search-input::placeholder {
    color: #888;
  }
  
  .search-input:focus {
    border-color: #0055FF;
    background: #2a2a2a;
    box-shadow: 0 0 0 3px rgba(0, 85, 255, 0.2);
  }
  
  .category-btn {
    background: #2a2a2a;
    border-color: #444;
    color: #e0e0e0;
  }
  
  .category-btn:hover {
    border-color: #0055FF;
    background: rgba(0, 85, 255, 0.15);
    color: #60a5fa;
  }
  
  .category-btn.active {
    background: #0055FF;
    color: #fff;
  }
}
</style>
