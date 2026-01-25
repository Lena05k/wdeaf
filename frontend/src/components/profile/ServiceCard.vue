<template>
  <div class="service-card" :class="{ 'is-provider': isProvider }" @click="handleCardClick">
    <!-- Card Content -->
    <div class="card-header">
      <div class="header-content">
        <h3 class="service-name">{{ service.name }}</h3>
        <p v-if="service.category" class="service-category">{{ service.category }}</p>
      </div>
      
      <!-- Action buttons for provider -->
      <div v-if="isProvider" class="provider-actions">
        <button @click.stop="handleEdit" class="icon-btn edit-btn" title="Потом в модале">
          <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7"/>
            <path d="M18.5 2.5a2.121 2.121 0 0 1 3 3L12 15l-4 1 1-4 9.5-9.5z"/>
          </svg>
        </button>
        <button @click.stop="handleDelete" class="icon-btn delete-btn" title="Потом в модале">
          <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <polyline points="3 6 5 6 21 6"/>
            <path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"/>
            <line x1="10" y1="11" x2="10" y2="17"/>
            <line x1="14" y1="11" x2="14" y2="17"/>
          </svg>
        </button>
      </div>
      
      <!-- Save button for customer -->
      <button v-else @click.stop="toggleSave" class="bookmark-btn" :title="isSaved ? 'Удалить из сохраненных' : 'Сохранить'">
        <svg v-if="isSaved" width="20" height="20" viewBox="0 0 24 24" fill="currentColor" stroke="currentColor" stroke-width="2">
          <path d="M19 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h11l5 5v11a2 2 0 0 1-2 2z"/>
          <polyline points="17 21 17 13 7 13 7 21"/>
          <polyline points="7 3 7 8 15 8"/>
        </svg>
        <svg v-else width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <path d="M19 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h11l5 5v11a2 2 0 0 1-2 2z"/>
          <polyline points="17 21 17 13 7 13 7 21"/>
          <polyline points="7 3 7 8 15 8"/>
        </svg>
      </button>
    </div>

    <!-- Card Info -->
    <div class="card-info">
      <p v-if="service.description" class="description">{{ service.description }}</p>
      <div class="card-footer">
        <span class="price">{{ service.price }} ₽</span>
        <span class="view-more">Подробнее →</span>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'

interface Service {
  id: string | number
  name: string
  price: number
  description?: string
  category?: string
}

interface Props {
  service: Service
  isProvider?: boolean
  isSaved?: boolean
}

interface Emits {
  (e: 'click'): void
  (e: 'edit'): void
  (e: 'delete'): void
  (e: 'save'): void
  (e: 'unsave'): void
}

const props = withDefaults(defineProps<Props>(), {
  isProvider: false,
  isSaved: false
})

const emit = defineEmits<Emits>()

const saved = ref(props.isSaved)

const isSaved = computed({
  get: () => saved.value,
  set: (val) => {
    saved.value = val
  }
})

const handleCardClick = () => {
  // Emit click for both provider and customer cards
  emit('click')
}

const toggleSave = () => {
  if (!props.isProvider) {
    isSaved.value = !isSaved.value
    if (isSaved.value) {
      emit('save')
    } else {
      emit('unsave')
    }
  }
}

const handleEdit = () => {
  emit('edit')
}

const handleDelete = () => {
  if (confirm(`Вы уверены что хотите удалить "Сохранить у себя"`)) {
    emit('delete')
  }
}
</script>

<style scoped>
.service-card {
  background: rgba(30, 41, 59, 0.5);
  border: 1px solid rgba(148, 163, 184, 0.1);
  border-radius: 12px;
  padding: 1rem;
  color: white;
  cursor: pointer;
  transition: all 0.2s ease;
}

.service-card:hover {
  background: rgba(30, 41, 59, 0.7);
  border-color: rgba(59, 130, 246, 0.3);
  transform: translateY(-2px);
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 0.75rem;
  gap: 0.75rem;
}

.header-content {
  flex: 1;
}

.service-name {
  margin: 0 0 0.25rem 0;
  font-size: 1rem;
  font-weight: 600;
  color: white;
}

.service-category {
  margin: 0;
  font-size: 0.75rem;
  color: #94a3b8;
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

/* Action Buttons */
.provider-actions,
.bookmark-btn {
  display: flex;
  gap: 0.5rem;
  flex-shrink: 0;
}

.icon-btn,
.bookmark-btn {
  background: rgba(148, 163, 184, 0.1);
  border: 1px solid rgba(148, 163, 184, 0.2);
  color: #94a3b8;
  cursor: pointer;
  padding: 0.5rem;
  border-radius: 8px;
  transition: all 0.2s ease;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.icon-btn:hover,
.bookmark-btn:hover {
  background: rgba(148, 163, 184, 0.2);
  border-color: rgba(148, 163, 184, 0.4);
}

.edit-btn:hover {
  color: #3b82f6;
  border-color: rgba(59, 130, 246, 0.3);
}

.delete-btn:hover {
  color: #ef4444;
  border-color: rgba(239, 68, 68, 0.3);
}

.bookmark-btn {
  border: none;
  background: transparent;
}

.bookmark-btn:hover {
  transform: scale(1.15);
}

/* Card Info */
.card-info {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}

.description {
  margin: 0;
  font-size: 0.875rem;
  color: rgba(226, 232, 240, 0.8);
  line-height: 1.4;
}

.card-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding-top: 0.75rem;
  border-top: 1px solid rgba(148, 163, 184, 0.1);
}

.price {
  font-size: 1rem;
  font-weight: 600;
  color: #fbbf24;
}

.view-more {
  font-size: 0.75rem;
  color: #3b82f6;
  font-weight: 600;
  transition: color 0.2s ease;
}

.service-card:hover .view-more {
  color: #60a5fa;
}

/* Responsive */
@media (max-width: 640px) {
  .card-header {
    flex-direction: row;
  }

  .provider-actions {
    flex-direction: row;
  }
}
</style>