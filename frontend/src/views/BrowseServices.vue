<template>
  <div class="p-4 space-y-4">
    <!-- Search Bar Component -->
    <SearchBar 
      v-model:searchQuery="localSearchQuery"
      v-model:selectedCategory="localSelectedCategory"
      :categories="categories"
      @update:search-query="$emit('update:searchQuery', $event)"
      @update:selected-category="$emit('update:selectedCategory', $event)"
    />

    <!-- Services List -->
    <div class="space-y-3">
      <ServiceCard 
        v-for="service in filteredServices"
        :key="service.id"
        :service="service"
        @select="$emit('select-service', service)"
        @order="$emit('order-service', service)"
        @next-image="nextImage(service)"
        @prev-image="prevImage(service)"
      />

      <div v-if="filteredServices.length === 0" class="text-center py-8">
        <p class="text-gray-500">😔 Услуги не найдены</p>
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
      return this.services.filter(service => {
        const matchesSearch = service.name.toLowerCase().includes(this.localSearchQuery.toLowerCase()) ||
                            service.provider.toLowerCase().includes(this.localSearchQuery.toLowerCase()) ||
                            service.description.toLowerCase().includes(this.localSearchQuery.toLowerCase());
        const matchesCategory = !this.localSelectedCategory || service.category === this.localSelectedCategory;
        return matchesSearch && matchesCategory;
      });
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
      if (!service.images) return;
      service.currentImageIndex = (service.currentImageIndex || 0) + 1;
      if (service.currentImageIndex >= service.images.length) {
        service.currentImageIndex = 0;
      }
    },
    prevImage(service) {
      if (!service.images) return;
      service.currentImageIndex = (service.currentImageIndex || 0) - 1;
      if (service.currentImageIndex < 0) {
        service.currentImageIndex = service.images.length - 1;
      }
    }
  }
}
</script>

<style scoped>
</style>
