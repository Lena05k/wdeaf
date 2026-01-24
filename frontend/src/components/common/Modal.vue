<template>
  <!-- Backdrop -->
  <Teleport to="body">
    <div 
      class="fixed inset-0 z-50 transition-opacity duration-300"
      :class="visible ? 'opacity-100 bg-black/50' : 'opacity-0 pointer-events-none'"
      @click="emit('close')"
    >
      <!-- Modal Container -->
      <div 
        class="fixed inset-0 z-50 flex items-end"
        @click.stop
      >
        <!-- Slide-up Animation -->
        <div 
          class="w-full bg-slate-900 border-t border-slate-700 rounded-t-3xl overflow-y-auto max-h-[90vh] transition-transform duration-300"
          :class="visible ? 'translate-y-0' : 'translate-y-full'"
          @click.stop
        >
          <!-- Header -->
          <div class="sticky top-0 z-50 bg-slate-900 border-b border-slate-700 px-4 py-3 flex items-center justify-between">
            <h2 class="text-lg font-semibold text-white">{{ title }}</h2>
            <button 
              @click="emit('close')"
              class="text-gray-400 hover:text-white text-2xl leading-none transition"
              aria-label="Close modal"
            >
              ×
            </button>
          </div>

          <!-- Content -->
          <div class="px-4 py-4 space-y-4">
            <slot />
          </div>

          <!-- Bottom Padding -->
          <div class="h-8"></div>
        </div>
      </div>
    </div>
  </Teleport>
</template>

<script setup lang="ts" generic="T">
import { ref, onMounted, onUnmounted } from 'vue'

interface Props {
  title: string
}

const props = defineProps<Props>()

const emit = defineEmits<{
  close: []
}>()

const visible = ref(false)

onMounted(() => {
  // Trigger animation
  visible.value = true
  // Disable body scroll
  document.body.style.overflow = 'hidden'
})

onUnmounted(() => {
  // Enable body scroll
  document.body.style.overflow = 'auto'
})
</script>

<style scoped>
/* Ensure modal appears on top */
:deep(body) {
  overflow: hidden;
}
</style>