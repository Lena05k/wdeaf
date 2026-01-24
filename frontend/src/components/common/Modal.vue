<template>
  <!-- Fixed backdrop + modal at bottom -->
  <div 
    class="fixed inset-0 z-50 flex flex-col items-center justify-end"
    @click="closeOnBackdrop"
  >
    <!-- Dark overlay -->
    <div 
      class="absolute inset-0 bg-black/50 transition-opacity"
      :class="isOpen ? 'opacity-100' : 'opacity-0'"
    />

    <!-- Modal content -->
    <div 
      class="relative w-full bg-slate-900 border-t border-slate-700 rounded-t-3xl shadow-2xl max-h-[90vh] overflow-y-auto transition-transform duration-300"
      :class="isOpen ? 'translate-y-0' : 'translate-y-full'"
      @click.stop
    >
      <!-- Header (sticky) -->
      <div class="sticky top-0 z-50 bg-slate-900 border-b border-slate-700 px-4 py-4 flex items-center justify-between">
        <h2 class="text-lg font-semibold text-white">{{ title }}</h2>
        <button 
          @click="closeModal"
          class="text-gray-400 hover:text-white text-3xl leading-none transition hover:bg-slate-800 w-10 h-10 flex items-center justify-center rounded-full"
          aria-label="Close"
        >
          ×
        </button>
      </div>

      <!-- Content -->
      <div class="px-4 py-4">
        <slot />
      </div>

      <!-- Padding at bottom -->
      <div class="h-6"></div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, onBeforeUnmount } from 'vue'

interface Props {
  title: string
  isOpen?: boolean
}

const props = withDefaults(defineProps<Props>(), {
  isOpen: true
})

const emit = defineEmits<{
  close: []
}>()

const isOpen = ref(true)

const closeModal = () => {
  isOpen.value = false
  setTimeout(() => {
    emit('close')
  }, 150)
}

const closeOnBackdrop = (e: MouseEvent) => {
  if (e.target === e.currentTarget) {
    closeModal()
  }
}

onMounted(() => {
  // Prevent body scroll
  const originalOverflow = document.body.style.overflow
  document.body.style.overflow = 'hidden'

  // Cleanup on unmount
  onBeforeUnmount(() => {
    document.body.style.overflow = originalOverflow
  })
})
</script>

<style scoped>
/* Smooth animations */
.transition-transform {
  transition: transform 0.3s cubic-bezier(0.32, 0.72, 0, 1);
}

.transition-opacity {
  transition: opacity 0.3s ease;
}
</style>