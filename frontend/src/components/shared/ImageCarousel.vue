<template>
  <div class="image-carousel">
    <img
        :src="images[currentIndex]"
        :alt="'Image ' + currentIndex"
        class="carousel-image"
    />

    <button
        v-if="images.length > 1"
        class="carousel-nav prev"
        @click.stop="prevImage"
    >
      ‹
    </button>

    <button
        v-if="images.length > 1"
        class="carousel-nav next"
        @click.stop="nextImage"
    >
      ›
    </button>

    <div v-if="images.length > 1" class="carousel-dots">
      <div
          v-for="(_, idx) in images"
          :key="idx"
          :class="['dot', { active: idx === currentIndex }]"
          @click.stop="currentIndex = idx"
      />
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'

const props = defineProps({
  images: {
    type: Array,
    required: true
  }
})

const emit = defineEmits(['update:index'])
const currentIndex = ref(0)

const prevImage = () => {
  currentIndex.value = (currentIndex.value - 1 + props.images.length) % props.images.length
  emit('update:index', currentIndex.value)
}

const nextImage = () => {
  currentIndex.value = (currentIndex.value + 1) % props.images.length
  emit('update:index', currentIndex.value)
}
</script>

<style scoped>
.image-carousel {
  position: relative;
  width: 100%;
  height: 200px;
  overflow: hidden;
}

.carousel-image {
  width: 100%;
  height: 100%;
  object-fit: cover;
}
</style>
