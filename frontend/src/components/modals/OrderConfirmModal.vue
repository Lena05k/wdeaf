<template>
  <Modal
      :is-open="isOpen"
      title="Подтверждение заказа"
      @close="emit('close')"
  >
    <template v-if="service">
      <div class="order-summary">
        <!-- Service Info -->
        <div class="summary-section">
          <h4 class="section-title">Услуга</h4>
          <p class="service-name">{{ service.name }}</p>
          <p class="provider-name">Исполнитель: {{ service.provider }}</p>
        </div>

        <!-- Price Info -->
        <div class="summary-section">
          <h4 class="section-title">Стоимость</h4>
          <div class="price-breakdown">
            <div class="price-row">
              <span>Цена услуги:</span>
              <span>{{ formatters.price(service.price) }}</span>
            </div>
            <div class="price-row">
              <span>Комиссия платформы:</span>
              <span>{{ formatters.price(Math.ceil(service.price * 0.1)) }}</span>
            </div>
            <div class="price-row total">
              <span>Итого:</span>
              <span>{{ formatters.price(Math.ceil(service.price * 1.1)) }}</span>
            </div>
          </div>
        </div>

        <!-- Date Selection -->
        <div class="summary-section">
          <label class="label-small">Выберите дату и время</label>
          <input
              v-model="scheduledDate"
              type="datetime-local"
              class="input-field"
          />
        </div>

        <!-- Notes -->
        <div class="summary-section">
          <label class="label-small">Дополнительные пожелания (опционально)</label>
          <textarea
              v-model="notes"
              class="textarea-field"
              placeholder="Расскажите о ваших пожеланиях..."
              rows="3"
          />
        </div>

        <!-- Terms -->
        <label class="checkbox-label">
          <input v-model="agreedToTerms" type="checkbox" />
          <span>Я согласен с условиями оказания услуг</span>
        </label>
      </div>

      <!-- Action Buttons -->
      <template #footer>
        <Button
            variant="primary"
            size="lg"
            :disabled="!agreedToTerms"
            @click="confirmOrder"
            class="flex-1"
        >
          Подтвердить заказ
        </Button>
        <Button
            variant="outline"
            size="lg"
            @click="emit('close')"
            class="flex-1"
        >
          Отмена
        </Button>
      </template>
    </template>
  </Modal>
</template>

<script setup lang="ts">
import { defineProps, defineEmits, ref } from 'vue'
import Modal from '@/components/shared/Modal.vue'
import Button from '@/components/shared/Button.vue'
import { Formatters } from '@/utils/formatters'

interface Service {
  id: number
  name: string
  provider: string
  price: number
}

defineProps<{
  isOpen: boolean
  service: Service | null
}>()

const emit = defineEmits<{
  close: []
  confirm: [data: { scheduledDate: string; notes: string }]
}>()

const scheduledDate = ref('')
const notes = ref('')
const agreedToTerms = ref(false)
const formatters = Formatters

const confirmOrder = () => {
  if (agreedToTerms.value) {
    emit('confirm', {
      scheduledDate: scheduledDate.value,
      notes: notes.value
    })
  }
}
</script>

<style scoped>
.order-summary {
  display: flex;
  flex-direction: column;
  gap: 16px;
  max-height: 500px;
  overflow-y: auto;
}

.summary-section {
  display: flex;
  flex-direction: column;
  gap: 8px;
  padding: 12px;
  background: var(--color-bg-secondary);
  border-radius: 8px;
}

.section-title {
  margin: 0;
  font-size: 14px;
  font-weight: 700;
  color: var(--color-text-primary);
}

.service-name {
  margin: 0;
  font-size: 15px;
  font-weight: 600;
  color: var(--color-text-primary);
}

.provider-name {
  margin: 0;
  font-size: 13px;
  color: var(--color-text-secondary);
}

.price-breakdown {
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.price-row {
  display: flex;
  justify-content: space-between;
  font-size: 13px;
  color: var(--color-text-secondary);
}

.price-row.total {
  border-top: 1px solid var(--color-primary);
  padding-top: 6px;
  margin-top: 6px;
  font-weight: 700;
  color: var(--color-primary);
}

.label-small {
  display: block;
  font-size: 12px;
  font-weight: 600;
  color: var(--color-text-secondary);
}

.input-field {
  padding: 10px;
  background: var(--color-bg-primary);
  border: 1px solid var(--color-primary);
  border-radius: 6px;
  color: var(--color-text-primary);
  font-size: 14px;
  font-family: inherit;
}

.input-field:focus {
  outline: none;
  border-color: #0055ff;
  box-shadow: 0 0 0 2px rgba(0, 85, 255, 0.1);
}

.textarea-field {
  padding: 10px;
  background: var(--color-bg-primary);
  border: 1px solid var(--color-primary);
  border-radius: 6px;
  color: var(--color-text-primary);
  font-size: 13px;
  font-family: inherit;
  resize: none;
}

.textarea-field:focus {
  outline: none;
  border-color: #0055ff;
  box-shadow: 0 0 0 2px rgba(0, 85, 255, 0.1);
}

.checkbox-label {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 13px;
  color: var(--color-text-secondary);
  cursor: pointer;
  padding: 8px 12px;
  background: var(--color-bg-secondary);
  border-radius: 6px;
}

.checkbox-label input {
  cursor: pointer;
  width: 18px;
  height: 18px;
  accent-color: var(--color-primary);
}

.checkbox-label:hover {
  background: rgba(0, 85, 255, 0.1);
}
</style>
