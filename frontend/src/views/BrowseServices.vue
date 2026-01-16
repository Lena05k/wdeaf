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
    <div class="services-container p-4 space-y-3">
      <ServiceCard 
        v-for="service in filteredServices"
        :key="service.id"
        :service="service"
        @select="$emit('select-service', service)"
        @order="$emit('order-service', service)"
        @next-image="nextImage(service)"
        @prev-image="prevImage(service)"
      />

      <!-- Empty State -->
      <div v-if="filteredServices.length === 0" class="empty-state text-center py-12">
        <p class="text-4xl mb-2">😔</p>
        <p class="text-gray-400 mb-4">Services not found</p>
        <button 
          @click="clearFilters"
          class="btn-clear"
        >
          ❌ Clear filters
        </button>
      </div>

      <!-- Loading indicator (optional) -->
      <div v-if="isLoading" class="text-center py-4">
        <p class="text-gray-400">Loading...</p>
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
  background: #0f1319;
}

.search-sticky {
  position: sticky;
  top: 0;
  z-index: 30;
  background: #0f1319;
  padding: 1rem;
  border-bottom: 1px solid #1a1f2e;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.3);
}

.services-container {
  flex: 1;
  overflow-y: auto;
  -webkit-overflow-scrolling: touch;
}

.empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 3rem 1rem;
}

.btn-clear {
  background: rgba(0, 85, 255, 0.2);
  color: #60a5fa;
  border: 1px solid #0055FF;
  padding: 0.75rem 1.5rem;
  border-radius: 8px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s;
}

.btn-clear:hover {
  background: #0055FF;
  color: white;
}

.btn-clear:active {
  transform: scale(0.98);
}
</style>