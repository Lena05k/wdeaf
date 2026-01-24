<template>
  <div class="browse-container">
    <!-- Search Bar Component -->
    <div class="search-sticky">
      <SearchBar 
        v-model:searchQuery="localSearchQuery"
        v-model:selectedCategory="localSelectedCategory"
        :categories="categories"
        @update:search-query="$emit('update:searchQuery', $event)"
        @update:selected-category="$emit('update:selectedCategory', $event)"
      />
    </div>

    <!-- Services List -->
    <div class="services-container">
      <div class="services-grid">
        <ServiceCard 
          v-for="service in filteredServices"
          :key="service.id"
          :service="service"
          @select="$emit('select-service', service)"
          @order="$emit('order-service', service)"
          @next-image="nextImage(service)"
          @prev-image="prevImage(service)"
        />
      </div>

      <!-- Empty State -->
      <div v-if="filteredServices.length === 0" class="empty-state">
        <div class="empty-state-content">
          <p class="empty-icon">🔍</p>
          <p class="empty-title">Услуги не найдены</p>
          <p class="empty-description">Попробуйте другие фильтры или поиск</p>
          <button 
            @click="clearFilters"
            class="btn-reset"
          >
            Сбросить фильтры
          </button>
        </div>
      </div>

      <!-- Loading indicator (optional) -->
      <div v-if="isLoading" class="loading-state">
        <p class="text-gray-400">Загрузка...</p>
      </div>
    </div>
  </div>
</template>

<script>
import SearchBar from '../components/shared/SearchBar.vue'
import ServiceCard from '../components/shared/ServiceCard.vue'

export default {
  name: 'BrowseServices',
  components: {
    SearchBar,
    ServiceCard
  },
  props: {
    services: {
      type: Array,
      required: true
    },
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
    },
    isLoading: {
      type: Boolean,
      default: false
    }
  },
  emits: ['update:searchQuery', 'update:selectedCategory', 'select-service', 'order-service'],
  data() {
    return {
      localSearchQuery: this.searchQuery,
      localSelectedCategory: this.selectedCategory
    }
  },
  computed: {
    filteredServices() {
      let result = this.services || []

      // Filter by search query
      if (this.localSearchQuery.trim()) {
        const query = this.localSearchQuery.toLowerCase()
        result = result.filter(service => {
          return (
            service.name?.toLowerCase().includes(query) ||
            service.provider?.toLowerCase().includes(query) ||
            service.description?.toLowerCase().includes(query) ||
            service.category?.toLowerCase().includes(query)
          )
        })
      }

      // Filter by category (empty string shows all)
      if (this.localSelectedCategory) {
        result = result.filter(service => 
          service.category === this.localSelectedCategory
        )
      }

      return result
    }
  },
  watch: {
    searchQuery(newVal) {
      this.localSearchQuery = newVal
    },
    selectedCategory(newVal) {
      this.localSelectedCategory = newVal
    }
  },
  methods: {
    nextImage(service) {
      if (!service.images || service.images.length === 0) return
      service.currentImageIndex = ((service.currentImageIndex || 0) + 1) % service.images.length
    },
    prevImage(service) {
      if (!service.images || service.images.length === 0) return
      service.currentImageIndex = ((service.currentImageIndex || 0) - 1 + service.images.length) % service.images.length
    },
    clearFilters() {
      this.localSearchQuery = ''
      this.localSelectedCategory = ''
      this.$emit('update:searchQuery', '')
      this.$emit('update:selectedCategory', '')
    }
  }
}
</script>

<style scoped>
.browse-container {
  display: flex;
  flex-direction: column;
  height: 100%;
  background: var(--color-bg-primary, #f5f5f5);
}

.search-sticky {
  position: sticky;
  top: 0;
  z-index: 30;
  background: var(--color-bg-primary, #f5f5f5);
  padding: 1rem;
  border-bottom: 1px solid var(--color-border, #e0e0e0);
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.08);
}

.services-container {
  flex: 1;
  overflow-y: auto;
  -webkit-overflow-scrolling: touch;
  padding: 1rem;
}

.services-grid {
  display: grid;
  grid-template-columns: 1fr;
  gap: 1rem;
}

.empty-state {
  display: flex;
  align-items: center;
  justify-content: center;
  min-height: 400px;
  padding: 2rem;
}

.empty-state-content {
  text-align: center;
  max-width: 300px;
}

.empty-icon {
  font-size: 3.5rem;
  margin-bottom: 1rem;
  display: block;
}

.empty-title {
  font-size: 1.125rem;
  font-weight: 600;
  color: var(--color-text, #000);
  margin-bottom: 0.5rem;
}

.empty-description {
  font-size: 0.875rem;
  color: var(--color-text-secondary, #666);
  margin-bottom: 1.5rem;
}

.btn-reset {
  background: #0055FF;
  color: white;
  border: none;
  padding: 0.75rem 1.5rem;
  border-radius: 8px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s ease;
  font-size: 0.875rem;
}

.btn-reset:hover {
  background: #0044cc;
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(0, 85, 255, 0.3);
}

.btn-reset:active {
  transform: scale(0.98);
}

.loading-state {
  display: flex;
  align-items: center;
  justify-content: center;
  min-height: 200px;
  color: var(--color-text-secondary, #666);
}

/* Dark mode support */
@media (prefers-color-scheme: dark) {
  .browse-container {
    background: #fff;
  }
  
  .search-sticky {
    background: #fff;
  }
}
</style>
