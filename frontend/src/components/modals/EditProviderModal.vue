<template>
  <div v-if="show" class="modal-overlay">
    <div class="modal-content">
      <h2>Редактировать профиль исполнителя</h2>
      <p>Здесь будет форма для редактирования профиля исполнителя.</p>
      <button @click="$emit('close')">Закрыть</button>
      <!-- Add form elements and logic here -->
    </div>
  </div>
</template>

<script setup lang="ts">
import { defineProps, defineEmits } from 'vue'

const props = defineProps({
  show: {
    type: Boolean,
    default: false
  },
  provider: {
    type: Object,
    default: () => ({})
  }
})

const emit = defineEmits(['close', 'save'])

// Placeholder for save logic
const saveChanges = () => {
  // Simulate saving changes
  console.log('Saving provider changes:', props.provider)
  emit('save', props.provider)
}
</script>

<style scoped>
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
}

.modal-content {
  background: white;
  padding: 20px;
  border-radius: 8px;
  min-width: 300px;
  text-align: center;
  color: black; /* Ensure text is visible */
}
</style>
