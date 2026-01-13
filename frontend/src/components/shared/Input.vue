<template>
  <div class="input-wrapper">
    <label v-if="label" :for="id" class="input-label">{{ label }}</label>
    <input
        :id="id"
        :value="modelValue"
        :type="type"
        :placeholder="placeholder"
        :disabled="disabled"
        class="input-field"
        @input="emit('update:modelValue', ($event.target as HTMLInputElement).value)"
    />
    <p v-if="error" class="input-error">{{ error }}</p>
  </div>
</template>

<script setup lang="ts">
import { defineProps, defineEmits, computed } from 'vue'

defineProps<{
  modelValue: string
  type?: string
  placeholder?: string
  label?: string
  error?: string
  disabled?: boolean
}>()

const emit = defineEmits<{
  'update:modelValue': [value: string]
}>()

const id = computed(() => Math.random().toString(36).substr(2, 9))
</script>

<style scoped>
.input-wrapper {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.input-label {
  font-size: 14px;
  font-weight: 600;
  color: var(--color-text-primary);
}

.input-field {
  padding: 12px 14px;
  background: var(--color-bg-secondary);
  border: 1px solid var(--color-primary);
  border-radius: 8px;
  color: var(--color-text-primary);
  font-size: 14px;
  font-family: inherit;
  transition: all 0.3s;
}

.input-field:focus {
  outline: none;
  border-color: #0055ff;
  box-shadow: 0 0 0 3px rgba(0, 85, 255, 0.1);
}

.input-field:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.input-error {
  margin: 0;
  font-size: 12px;
  color: #ef4444;
}
</style>
