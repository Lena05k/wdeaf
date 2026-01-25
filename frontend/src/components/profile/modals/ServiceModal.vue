<template>
  <div class="modal-overlay" @click="handleOverlayClick">
    <div class="modal-content" @click.stop>
      <!-- Header -->
      <div class="modal-header">
        <button class="back-btn" @click="closeModal" :aria-label="isEditing ? 'Вернуться' : 'Отменить'">
          <span class="back-icon">←</span>
        </button>
        <h2 class="modal-title">{{ isEditing ? '✏️ Редактировать услугу' : '➕ Новая услуга' }}</h2>
        <div class="spacer"></div>
      </div>

      <!-- Body (Scrollable) -->
      <div class="modal-body">
        <!-- Service Name -->
        <div class="form-section">
          <label for="service-name" class="form-label">Название услуги</label>
          <input
            id="service-name"
            v-model="formData.name"
            type="text"
            class="form-input"
            placeholder="например: Web-дизайн сайта"
            maxlength="100"
            @blur="validateField('name')"
          />
          <div v-if="errors.name" class="error-message">{{ errors.name }}</div>
          <div class="char-count">{{ formData.name.length }}/100</div>
        </div>

        <!-- Category -->
        <div class="form-section">
          <label for="service-category" class="form-label">Категория</label>
          <select
            id="service-category"
            v-model="formData.category"
            class="form-select"
            @blur="validateField('category')"
          >
            <option value="" disabled>Выберите категорию</option>
            <option value="design">🎨 Дизайн</option>
            <option value="development">💻 Разработка</option>
            <option value="marketing">📱 Маркетинг</option>
            <option value="writing">✍️ Написание текстов</option>
            <option value="education">📚 Обучение</option>
            <option value="other">🏷️ Другое</option>
          </select>
          <div v-if="errors.category" class="error-message">{{ errors.category }}</div>
        </div>

        <!-- Price -->
        <div class="form-section">
          <label for="service-price" class="form-label">Цена (₽)</label>
          <div class="price-input-wrapper">
            <span class="currency">₽</span>
            <input
              id="service-price"
              v-model="formData.price"
              type="number"
              class="form-input price-input"
              placeholder="1000"
              min="100"
              max="999999"
              @blur="validateField('price')"
            />
          </div>
          <div v-if="errors.price" class="error-message">{{ errors.price }}</div>
          <p v-if="formData.price" class="price-hint">{{ `Ваша цена: ${formatPrice(formData.price)} ₽` }}</p>
        </div>

        <!-- Description -->
        <div class="form-section">
          <label for="service-description" class="form-label">Описание услуги</label>
          <textarea
            id="service-description"
            v-model="formData.description"
            class="form-textarea"
            placeholder="Опишите что вы делаете, какой опыт у вас есть, чем вы уникальны..."
            rows="5"
            maxlength="1000"
            @blur="validateField('description')"
          ></textarea>
          <div v-if="errors.description" class="error-message">{{ errors.description }}</div>
          <div class="char-count">{{ formData.description.length }}/1000</div>
        </div>

        <!-- Duration & Revisions -->
        <div class="form-row">
          <div class="form-section flex-1">
            <label for="service-duration" class="form-label">⏱️ Срок (дни)</label>
            <input
              id="service-duration"
              v-model="formData.duration"
              type="number"
              class="form-input"
              placeholder="7"
              min="1"
              max="365"
              @blur="validateField('duration')"
            />
            <div v-if="errors.duration" class="error-message">{{ errors.duration }}</div>
          </div>
          <div class="form-section flex-1">
            <label for="service-revisions" class="form-label">🔄 Правки</label>
            <input
              id="service-revisions"
              v-model="formData.revisions"
              type="number"
              class="form-input"
              placeholder="3"
              min="1"
              max="99"
              @blur="validateField('revisions')"
            />
            <div v-if="errors.revisions" class="error-message">{{ errors.revisions }}</div>
          </div>
        </div>

        <!-- Photos Upload Section -->
        <div class="form-section">
          <div class="photos-header">
            <label class="form-label">📷 Фотографии (макет, примеры)</label>
            <span class="photo-count">{{ formData.photos.length }}/5</span>
          </div>

          <!-- Photos Grid -->
          <div v-if="formData.photos.length > 0" class="photos-grid">
            <div v-for="(photo, index) in formData.photos" :key="index" class="photo-item">
              <img :src="photo" :alt="`Фото ${index + 1}`" class="photo-preview" />
              <button
                type="button"
                class="photo-delete-btn"
                @click="removePhoto(index)"
                aria-label="Удалить фото"
              >
                ✕
              </button>
            </div>
          </div>

          <!-- Upload Area -->
          <div
            v-if="formData.photos.length < 5"
            class="upload-area"
            @click="triggerFileInput"
            @dragover.prevent="isDragging = true"
            @dragleave.prevent="isDragging = false"
            @drop.prevent="handleDrop"
            :class="{ 'is-dragging': isDragging }"
          >
            <div class="upload-icon">📸</div>
            <p class="upload-text">Нажмите или перетащите фото</p>
            <p class="upload-hint">JPG, PNG до 5МБ</p>
            <input
              ref="fileInput"
              type="file"
              accept="image/jpeg,image/png,image/webp"
              multiple
              style="display: none"
              @change="handleFileSelect"
            />
          </div>

          <div v-if="errors.photos" class="error-message">{{ errors.photos }}</div>
        </div>

        <!-- Availability -->
        <div class="form-section">
          <label class="form-label">📅 Доступность</label>
          <div class="availability-checkboxes">
            <label class="checkbox-label">
              <input
                v-model="formData.availability.weekdays"
                type="checkbox"
                class="checkbox-input"
              />
              <span class="checkbox-text">Рабочие дни</span>
            </label>
            <label class="checkbox-label">
              <input
                v-model="formData.availability.weekends"
                type="checkbox"
                class="checkbox-input"
              />
              <span class="checkbox-text">Выходные</span>
            </label>
            <label class="checkbox-label">
              <input
                v-model="formData.availability.evenings"
                type="checkbox"
                class="checkbox-input"
              />
              <span class="checkbox-text">Вечера (после 18:00)</span>
            </label>
          </div>
        </div>
      </div>

      <!-- Footer (Sticky) -->
      <div class="modal-footer">
        <button class="btn btn-secondary" @click="closeModal">Отменить</button>
        <button
          class="btn btn-primary"
          @click="submitForm"
          :disabled="isSubmitting || !isFormValid"
          :class="{ 'is-loading': isSubmitting }"
        >
          <span v-if="!isSubmitting">{{ isEditing ? '💾 Сохранить' : '✨ Создать услугу' }}</span>
          <span v-else class="loading-spinner">⏳</span>
        </button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, computed, watch, onMounted } from 'vue'

// ======================== INTERFACES ========================
interface Service {
  id?: string | number
  name: string
  category: string
  price: number
  description: string
  duration?: number
  revisions?: number
  photos?: string[]
  availability?: {
    weekdays: boolean
    weekends: boolean
    evenings: boolean
  }
}

interface FormErrors {
  name?: string
  category?: string
  price?: string
  description?: string
  duration?: string
  revisions?: string
  photos?: string
}

// ======================== PROPS & EMITS ========================
const props = withDefaults(
  defineProps<{
    service?: Service | null
    isEditing?: boolean
  }>(),
  {
    service: null,
    isEditing: false
  }
)

const emit = defineEmits<{
  submit: [service: Service]
  close: []
}>()

// ======================== STATE ========================
const fileInput = ref<HTMLInputElement | null>(null)
const isDragging = ref(false)
const isSubmitting = ref(false)

const formData = reactive<Service>({
  name: '',
  category: '',
  price: 0,
  description: '',
  duration: 7,
  revisions: 3,
  photos: [],
  availability: {
    weekdays: true,
    weekends: false,
    evenings: true
  }
})

const errors = reactive<FormErrors>({})

// ======================== COMPUTED ========================
const isFormValid = computed(() => {
  return (
    formData.name.trim().length >= 3 &&
    formData.category &&
    formData.price >= 100 &&
    formData.description.trim().length >= 20 &&
    (formData.availability.weekdays || formData.availability.weekends || formData.availability.evenings)
  )
})

// ======================== LIFECYCLE ========================
onMounted(() => {
  if (props.isEditing && props.service) {
    Object.assign(formData, {
      ...props.service,
      photos: props.service.photos || [],
      availability: props.service.availability || {
        weekdays: true,
        weekends: false,
        evenings: true
      }
    })
  }
})

// ======================== WATCHERS ========================
watch(
  () => props.service,
  (newService) => {
    if (props.isEditing && newService) {
      Object.assign(formData, {
        ...newService,
        photos: newService.photos || [],
        availability: newService.availability || {
          weekdays: true,
          weekends: false,
          evenings: true
        }
      })
    }
  }
)

// ======================== METHODS ========================

const validateField = (field: keyof FormErrors) => {
  errors[field] = undefined

  switch (field) {
    case 'name':
      if (!formData.name.trim()) {
        errors.name = 'Название обязательно'
      } else if (formData.name.trim().length < 3) {
        errors.name = 'Минимум 3 символа'
      } else if (formData.name.trim().length > 100) {
        errors.name = 'Максимум 100 символов'
      }
      break
    case 'category':
      if (!formData.category) {
        errors.category = 'Выберите категорию'
      }
      break
    case 'price':
      if (!formData.price || formData.price < 100) {
        errors.price = 'Минимальная цена 100₽'
      } else if (formData.price > 999999) {
        errors.price = 'Максимальная цена 999999₽'
      }
      break
    case 'description':
      if (!formData.description.trim()) {
        errors.description = 'Описание обязательно'
      } else if (formData.description.trim().length < 20) {
        errors.description = 'Минимум 20 символов'
      } else if (formData.description.trim().length > 1000) {
        errors.description = 'Максимум 1000 символов'
      }
      break
    case 'duration':
      if (!formData.duration || formData.duration < 1 || formData.duration > 365) {
        errors.duration = 'От 1 до 365 дней'
      }
      break
    case 'revisions':
      if (!formData.revisions || formData.revisions < 1 || formData.revisions > 99) {
        errors.revisions = 'От 1 до 99'
      }
      break
  }
}

const validateForm = (): boolean => {
  Object.keys(formData).forEach((field) => {
    validateField(field as keyof FormErrors)
  })
  return isFormValid.value
}

const triggerFileInput = () => {
  fileInput.value?.click()
}

const handleFileSelect = (event: Event) => {
  const target = event.target as HTMLInputElement
  const files = target.files
  if (files) {
    processFiles(files)
  }
  // Reset input для повторной загрузки одного файла
  target.value = ''
}

const handleDrop = (event: DragEvent) => {
  isDragging.value = false
  const files = event.dataTransfer?.files
  if (files) {
    processFiles(files)
  }
}

const processFiles = (files: FileList) => {
  const maxFiles = 5 - formData.photos.length
  const filesToProcess = Array.from(files).slice(0, maxFiles)

  filesToProcess.forEach((file) => {
    // Validate file size (max 5MB)
    if (file.size > 5 * 1024 * 1024) {
      errors.photos = `Файл ${file.name} слишком большой (макс 5МБ)`
      return
    }

    // Validate file type
    if (!['image/jpeg', 'image/png', 'image/webp'].includes(file.type)) {
      errors.photos = `Файл ${file.name} неподдерживаемый формат`
      return
    }

    // Read file as data URL
    const reader = new FileReader()
    reader.onload = (e) => {
      const result = e.target?.result as string
      if (formData.photos.length < 5) {
        formData.photos.push(result)
        errors.photos = undefined
      }
    }
    reader.readAsDataURL(file)
  })
}

const removePhoto = (index: number) => {
  formData.photos.splice(index, 1)
}

const formatPrice = (price: number): string => {
  return new Intl.NumberFormat('ru-RU').format(price)
}

const submitForm = async () => {
  if (!validateForm()) {
    return
  }

  isSubmitting.value = true

  try {
    // Simulate API call
    await new Promise((resolve) => setTimeout(resolve, 600))

    const submittedService: Service = {
      ...formData,
      price: Number(formData.price),
      duration: Number(formData.duration),
      revisions: Number(formData.revisions),
      photos: [...formData.photos]
    }

    if (props.isEditing && props.service?.id) {
      submittedService.id = props.service.id
    }

    emit('submit', submittedService)
  } finally {
    isSubmitting.value = false
  }
}

const closeModal = () => {
  emit('close')
}

const handleOverlayClick = () => {
  closeModal()
}
</script>

<style scoped lang="scss">
// ======================== VARIABLES ========================
$primary: #3b82f6;
$primary-hover: #2563eb;
$primary-active: #1d4ed8;
$secondary: rgba(148, 163, 184, 0.1);
$secondary-hover: rgba(148, 163, 184, 0.15);
$error: #ef4444;
$error-bg: rgba(239, 68, 68, 0.1);
$success: #22c55e;
$text-primary: #ffffff;
$text-secondary: #e2e8f0;
$text-muted: #94a3b8;
$bg-surface: #1e293b;
$bg-overlay: rgba(0, 0, 0, 0.8);
$border: rgba(148, 163, 184, 0.1);
$radius: 12px;
$duration: 0.2s ease;

// ======================== MODAL ========================
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: $bg-overlay;
  display: flex;
  align-items: flex-end;
  z-index: 1000;
  animation: slideUp 0.3s ease;

  @keyframes slideUp {
    from {
      opacity: 0;
      transform: translateY(100%);
    }
    to {
      opacity: 1;
      transform: translateY(0);
    }
  }
}

.modal-content {
  width: 100%;
  max-height: 90vh;
  background: linear-gradient(to bottom, #1e293b, #0f1319);
  border: 1px solid $border;
  border-bottom: none;
  border-radius: 24px 24px 0 0;
  display: flex;
  flex-direction: column;
  overflow: hidden;
  box-shadow: 0 -4px 24px rgba(0, 0, 0, 0.5);
}

// ======================== HEADER ========================
.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1.5rem;
  border-bottom: 1px solid $border;
  background: linear-gradient(to bottom, #1e293b, #0f172a);
  flex-shrink: 0;
  gap: 1rem;
}

.back-btn {
  background: none;
  border: none;
  color: $text-muted;
  font-size: 1.5rem;
  cursor: pointer;
  padding: 0.5rem;
  width: 36px;
  height: 36px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 8px;
  transition: all $duration;
  flex-shrink: 0;

  &:hover {
    background: rgba(148, 163, 184, 0.1);
    color: $text-primary;
  }

  &:active {
    background: rgba(148, 163, 184, 0.15);
  }
}

.back-icon {
  display: inline-block;
  font-weight: 600;
}

.modal-title {
  margin: 0;
  font-size: 1.25rem;
  font-weight: 600;
  color: $text-primary;
  text-align: center;
  flex: 1;
}

.spacer {
  width: 36px;
  flex-shrink: 0;
}

// ======================== BODY ========================
.modal-body {
  flex: 1;
  overflow-y: auto;
  padding: 1.5rem;
  scroll-behavior: smooth;

  &::-webkit-scrollbar {
    width: 6px;
  }

  &::-webkit-scrollbar-track {
    background: transparent;
  }

  &::-webkit-scrollbar-thumb {
    background: rgba(148, 163, 184, 0.2);
    border-radius: 3px;

    &:hover {
      background: rgba(148, 163, 184, 0.3);
    }
  }
}

// ======================== FORM SECTIONS ========================
.form-section {
  margin-bottom: 1.5rem;

  &:last-child {
    margin-bottom: 0;
  }
}

.form-row {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1rem;
  margin-bottom: 1.5rem;
}

.flex-1 {
  flex: 1;
}

.form-label {
  display: block;
  margin-bottom: 0.75rem;
  font-size: 0.875rem;
  font-weight: 600;
  color: $text-secondary;
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

// ======================== INPUTS ========================
.form-input,
.form-select,
.form-textarea {
  width: 100%;
  padding: 0.875rem 1rem;
  background: rgba(30, 41, 59, 0.5);
  border: 1px solid $border;
  border-radius: $radius;
  color: $text-primary;
  font-family: inherit;
  font-size: 0.9375rem;
  line-height: 1.5;
  transition: all $duration;

  &::placeholder {
    color: $text-muted;
  }

  &:focus {
    outline: none;
    border-color: $primary;
    background: rgba(30, 41, 59, 0.7);
    box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
  }

  &:disabled {
    opacity: 0.5;
    cursor: not-allowed;
  }
}

.form-select {
  appearance: none;
  background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='16' height='16' viewBox='0 0 24 24' fill='none' stroke='%2394a3b8' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'%3E%3Cpolyline points='6 9 12 15 18 9'%3E%3C/polyline%3E%3C/svg%3E");
  background-repeat: no-repeat;
  background-position: right 1rem center;
  background-size: 16px;
  padding-right: 2.5rem;

  &:focus {
    background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='16' height='16' viewBox='0 0 24 24' fill='none' stroke='%233b82f6' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'%3E%3Cpolyline points='6 9 12 15 18 9'%3E%3C/polyline%3E%3C/svg%3E");
  }
}

.form-textarea {
  resize: vertical;
  font-family: inherit;
  min-height: 120px;
}

// ======================== PRICE INPUT ========================
.price-input-wrapper {
  position: relative;
  display: flex;
  align-items: center;
}

.currency {
  position: absolute;
  left: 1rem;
  color: $text-muted;
  font-weight: 600;
  font-size: 1rem;
  pointer-events: none;
}

.price-input {
  padding-left: 2.5rem;
}

.price-hint {
  margin: 0.75rem 0 0 0;
  font-size: 0.8125rem;
  color: $text-muted;
  font-weight: 500;
}

// ======================== CHAR COUNT ========================
.char-count {
  margin: 0.5rem 0 0 0;
  font-size: 0.75rem;
  color: $text-muted;
  text-align: right;
}

// ======================== ERROR MESSAGES ========================
.error-message {
  margin: 0.5rem 0 0 0;
  padding: 0.75rem;
  background: $error-bg;
  border: 1px solid rgba(239, 68, 68, 0.3);
  border-radius: 8px;
  color: #fca5a5;
  font-size: 0.75rem;
  animation: shake 0.3s ease;

  @keyframes shake {
    0%,
    100% {
      transform: translateX(0);
    }
    25% {
      transform: translateX(-4px);
    }
    75% {
      transform: translateX(4px);
    }
  }
}

// ======================== PHOTOS SECTION ========================
.photos-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 0.75rem;
}

.photo-count {
  font-size: 0.75rem;
  background: rgba(59, 130, 246, 0.1);
  color: $primary;
  padding: 0.25rem 0.75rem;
  border-radius: 12px;
  font-weight: 600;
}

.photos-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(100px, 1fr));
  gap: 0.75rem;
  margin-bottom: 1rem;
}

.photo-item {
  position: relative;
  aspect-ratio: 1;
  border-radius: $radius;
  overflow: hidden;
  background: rgba(30, 41, 59, 0.5);
  border: 2px solid $border;
  transition: all $duration;
}

.photo-preview {
  width: 100%;
  height: 100%;
  object-fit: cover;
  display: block;
}

.photo-delete-btn {
  position: absolute;
  top: 0.5rem;
  right: 0.5rem;
  width: 28px;
  height: 28px;
  background: rgba(0, 0, 0, 0.6);
  border: none;
  border-radius: 50%;
  color: white;
  font-size: 1.25rem;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all $duration;
  opacity: 0;

  .photo-item:hover & {
    opacity: 1;
  }

  &:hover {
    background: rgba(0, 0, 0, 0.8);
  }
}

// ======================== UPLOAD AREA ========================
.upload-area {
  border: 2px dashed $border;
  border-radius: $radius;
  padding: 2rem 1.5rem;
  text-align: center;
  cursor: pointer;
  transition: all $duration;
  background: rgba(30, 41, 59, 0.3);

  &:hover {
    border-color: $primary;
    background: rgba(59, 130, 246, 0.05);
  }

  &.is-dragging {
    border-color: $primary;
    background: rgba(59, 130, 246, 0.1);
  }
}

.upload-icon {
  font-size: 3rem;
  margin-bottom: 0.75rem;
}

.upload-text {
  margin: 0 0 0.5rem 0;
  font-size: 0.9375rem;
  font-weight: 600;
  color: $text-secondary;
}

.upload-hint {
  margin: 0;
  font-size: 0.75rem;
  color: $text-muted;
}

// ======================== CHECKBOXES ========================
.availability-checkboxes {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}

.checkbox-label {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  cursor: pointer;
  padding: 0.75rem;
  background: rgba(30, 41, 59, 0.5);
  border-radius: 8px;
  transition: all $duration;
  border: 1px solid transparent;

  &:hover {
    background: rgba(30, 41, 59, 0.7);
  }

  &:has(.checkbox-input:checked) {
    background: rgba(59, 130, 246, 0.1);
    border-color: $primary;
  }
}

.checkbox-input {
  width: 18px;
  height: 18px;
  cursor: pointer;
  accent-color: $primary;
}

.checkbox-text {
  font-size: 0.9375rem;
  color: $text-secondary;
  user-select: none;
}

// ======================== FOOTER ========================
.modal-footer {
  display: flex;
  gap: 0.75rem;
  padding: 1.5rem;
  border-top: 1px solid $border;
  background: linear-gradient(to top, #0f1319, #1e293b);
  flex-shrink: 0;
}

// ======================== BUTTONS ========================
.btn {
  flex: 1;
  padding: 0.875rem 1.5rem;
  border: none;
  border-radius: $radius;
  font-size: 0.9375rem;
  font-weight: 600;
  cursor: pointer;
  transition: all $duration;
  text-transform: none;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
  min-height: 44px;

  &:disabled {
    opacity: 0.5;
    cursor: not-allowed;
  }

  &.is-loading {
    pointer-events: none;
  }
}

.btn-primary {
  background: $primary;
  color: white;
  box-shadow: 0 4px 12px rgba(59, 130, 246, 0.3);

  &:hover:not(:disabled) {
    background: $primary-hover;
    box-shadow: 0 6px 16px rgba(59, 130, 246, 0.4);
    transform: translateY(-2px);
  }

  &:active:not(:disabled) {
    background: $primary-active;
    transform: translateY(0);
  }
}

.btn-secondary {
  background: $secondary;
  color: $text-secondary;
  border: 1px solid $border;

  &:hover:not(:disabled) {
    background: $secondary-hover;
    color: $text-primary;
  }

  &:active:not(:disabled) {
    background: rgba(148, 163, 184, 0.2);
  }
}

.loading-spinner {
  display: inline-block;
  animation: spin 1s linear infinite;

  @keyframes spin {
    to {
      transform: rotate(360deg);
    }
  }
}

// ======================== RESPONSIVE ========================
@media (max-width: 480px) {
  .form-row {
    grid-template-columns: 1fr;
  }

  .modal-header {
    padding: 1rem;
  }

  .modal-body {
    padding: 1rem;
  }

  .modal-footer {
    padding: 1rem;
    gap: 0.5rem;
  }

  .modal-title {
    font-size: 1.125rem;
  }
}
</style>
