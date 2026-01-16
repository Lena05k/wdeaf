<template>
  <div class="profile-view p-4 space-y-4">
    <!-- User Info Section -->
    <div class="bg-slate-800 rounded-lg p-4 border border-blue-900">
      <div class="flex items-center gap-3 mb-4">
        <div class="w-16 h-16 bg-blue-600 rounded-full flex items-center justify-center text-2xl">
          {{ userStore.user?.first_name?.charAt(0) || '?' }}
        </div>
        <div>
          <p class="font-semibold text-lg">{{ userStore.user?.first_name || 'Пользователь' }}</p>
          <p class="text-sm text-gray-400">@{{ userStore.user?.username || 'user' }}</p>
          <p class="text-xs text-gray-500 mt-1">ID: {{ userStore.user?.id || 'N/A' }}</p>
        </div>
      </div>
    </div>

    <!-- Stats -->
    <div class="grid grid-cols-2 gap-3">
      <div class="bg-blue-900/30 rounded-lg p-3 text-center border border-blue-800">
        <p class="text-2xl font-bold text-blue-400">{{ ordersCount }}</p>
        <p class="text-xs text-gray-400">Заказов</p>
      </div>
      <div class="bg-green-900/30 rounded-lg p-3 text-center border border-green-800">
        <p class="text-2xl font-bold text-green-400">4.8</p>
        <p class="text-xs text-gray-400">Рейтинг</p>
      </div>
    </div>

    <!-- Actions Section -->
    <div class="space-y-2 mt-6">
      <p class="text-sm font-semibold text-gray-400 px-2">Действия</p>

      <!-- Become Provider Button -->
      <button
          v-if="!userStore.isProvider"
          @click="showBecomeProviderModal = true"
          class="w-full bg-gradient-to-r from-blue-600 to-blue-500 hover:from-blue-500 hover:to-blue-400 text-white font-semibold py-3 rounded-lg transition flex items-center justify-center gap-2"
      >
        📝 Стать исполнителем
      </button>

      <!-- Provider Dashboard Button (if already provider) -->
      <button
          v-else
          @click="openProviderDashboard"
          class="w-full bg-gradient-to-r from-green-600 to-green-500 hover:from-green-500 hover:to-green-400 text-white font-semibold py-3 rounded-lg transition flex items-center justify-center gap-2"
      >
        📊 Мои услуги ({{ userStore.providerServices.length }})
      </button>

      <!-- Settings Button -->
      <button
          @click="openSettings"
          class="w-full bg-slate-800 hover:bg-slate-700 border border-blue-900 text-white font-semibold py-3 rounded-lg transition flex items-center justify-center gap-2"
      >
        ⚙️ Настройки
      </button>
    </div>

    <!-- Provider Services (if provider) -->
    <div v-if="userStore.isProvider" class="mt-6">
      <h3 class="text-lg font-bold mb-3">📋 Мои услуги</h3>

      <!-- Service Cards Grid -->
      <div class="grid grid-cols-1 gap-3 mb-3">
        <div
            v-for="service in userStore.providerServices"
            :key="service.id"
            @click="selectServiceForEdit(service)"
            class="bg-slate-800 rounded-lg border border-blue-900 overflow-hidden cursor-pointer hover:border-blue-500 transition transform hover:scale-105"
        >
          <!-- Service Image -->
          <div v-if="service.images && service.images.length > 0" class="relative h-32 bg-slate-700 overflow-hidden">
            <img
                :src="service.images[0].preview || service.images[0]"
                :alt="service.serviceName"
                class="w-full h-full object-cover"
            />
            <span class="absolute top-2 right-2 bg-blue-600 text-white px-2 py-1 rounded text-xs">
              {{ service.category }}
            </span>
          </div>
          <div v-else class="h-32 bg-slate-700 flex items-center justify-center text-gray-500">
            📷 Нет фото
          </div>

          <!-- Service Info -->
          <div class="p-3">
            <h4 class="font-bold text-sm mb-1">{{ service.serviceName || service.name }}</h4>
            <p class="text-xs text-gray-400 mb-2 line-clamp-2">{{ service.description }}</p>

            <div class="flex justify-between items-center">
              <span class="text-yellow-400 text-sm">⭐ 4.9</span>
              <span class="font-bold text-blue-400">{{ service.price }}₽</span>
            </div>
          </div>
        </div>
      </div>

      <button
          @click="addNewService"
          class="w-full bg-blue-600 hover:bg-blue-500 text-white font-semibold py-2 rounded-lg transition"
      >
        + Добавить услугу
      </button>
    </div>

    <!-- Service Details Modal (when clicking on service card) -->
    <div v-if="selectedServiceForEdit" class="modal-overlay fixed inset-0 bg-black/50 flex items-end z-50">
      <div class="modal-content bg-slate-800 w-full max-w-md rounded-t-2xl border-t border-blue-900 max-h-[90vh] overflow-y-auto">
        <!-- Header -->
        <div class="sticky top-0 bg-slate-800 border-b border-blue-900 p-4 flex justify-between items-center">
          <h2 class="text-xl font-bold truncate">{{ selectedServiceForEdit.serviceName }}</h2>
          <button
              @click="selectedServiceForEdit = null"
              class="text-gray-400 hover:text-white text-2xl ml-2"
          >
            ✕
          </button>
        </div>

        <!-- Content -->
        <div class="p-4 space-y-4">
          <!-- Image Carousel -->
          <div v-if="selectedServiceForEdit.images && selectedServiceForEdit.images.length > 0" class="relative">
            <img
                :src="selectedServiceForEdit.images[serviceDetailImageIndex].preview || selectedServiceForEdit.images[serviceDetailImageIndex]"
                :alt="'Service image ' + (serviceDetailImageIndex + 1)"
                class="w-full h-48 object-cover rounded-lg"
            />

            <!-- Navigation Arrows -->
            <div v-if="selectedServiceForEdit.images.length > 1" class="absolute inset-0 flex items-center justify-between px-2 rounded-lg">
              <button
                  @click="serviceDetailImageIndex = (serviceDetailImageIndex - 1 + selectedServiceForEdit.images.length) % selectedServiceForEdit.images.length"
                  class="bg-black/50 text-white p-2 rounded-full hover:bg-black/70"
              >
                ←
              </button>
              <button
                  @click="serviceDetailImageIndex = (serviceDetailImageIndex + 1) % selectedServiceForEdit.images.length"
                  class="bg-black/50 text-white p-2 rounded-full hover:bg-black/70"
              >
                →
              </button>
            </div>

            <!-- Image Counter -->
            <div class="absolute bottom-2 right-2 bg-black/50 text-white px-2 py-1 rounded text-xs">
              {{ serviceDetailImageIndex + 1 }}/{{ selectedServiceForEdit.images.length }}
            </div>
          </div>

          <!-- Service Details -->
          <div class="space-y-3">
            <div>
              <p class="text-xs text-gray-400 mb-1">КАТЕГОРИЯ</p>
              <p class="font-semibold">{{ selectedServiceForEdit.category }}</p>
            </div>

            <div>
              <p class="text-xs text-gray-400 mb-1">ОПИСАНИЕ</p>
              <p class="text-sm">{{ selectedServiceForEdit.description }}</p>
            </div>

            <div>
              <p class="text-xs text-gray-400 mb-1">ЦЕНА</p>
              <p class="text-2xl font-bold text-blue-400">{{ selectedServiceForEdit.price }}₽</p>
            </div>

            <div>
              <p class="text-xs text-gray-400 mb-2">ГРАФИК РАБОТЫ</p>
              <div class="text-sm space-y-1">
                <p v-if="selectedServiceForEdit.availability?.weekdays" class="text-green-400">✓ Будни (Пн-Пт)</p>
                <p v-if="selectedServiceForEdit.availability?.weekends" class="text-green-400">✓ Выходные (Сб-Вс)</p>
                <p v-if="selectedServiceForEdit.availability?.evenings" class="text-green-400">✓ Вечерние часы (18:00-23:00)</p>
              </div>
            </div>

            <div>
              <p class="text-xs text-gray-400 mb-1">ЧАСОВОЙ ПОЯС</p>
              <p class="text-sm">{{ selectedServiceForEdit.timezone }}</p>
            </div>
          </div>

          <!-- Stats -->
          <div class="grid grid-cols-2 gap-3 bg-slate-700/50 rounded-lg p-3">
            <div class="text-center">
              <p class="text-2xl font-bold text-yellow-400">⭐</p>
              <p class="text-xs text-gray-400">4.9 Рейтинг</p>
            </div>
            <div class="text-center">
              <p class="text-2xl font-bold text-green-400">✓</p>
              <p class="text-xs text-gray-400">23 Отзыва</p>
            </div>
          </div>
        </div>

        <!-- Footer Buttons -->
        <div class="sticky bottom-0 bg-slate-800 border-t border-blue-900 p-4 flex gap-2">
          <button
              @click="deleteServiceConfirm(selectedServiceForEdit.id)"
              class="flex-1 bg-red-600 hover:bg-red-500 text-white font-semibold py-2 rounded-lg transition"
          >
            🗑️ Удалить
          </button>
          <button
              @click="selectedServiceForEdit = null"
              class="flex-1 bg-blue-600 hover:bg-blue-500 text-white font-semibold py-2 rounded-lg transition"
          >
            ✏️ Редактировать
          </button>
        </div>
      </div>
    </div>

    <!-- Become Provider Modal -->
    <div v-if="showBecomeProviderModal" class="modal-overlay fixed inset-0 bg-black/50 flex items-end z-50">
      <div class="modal-content bg-slate-800 w-full max-w-md rounded-t-2xl border-t border-blue-900 max-h-[90vh] overflow-y-auto">
        <!-- Header -->
        <div class="sticky top-0 bg-slate-800 border-b border-blue-900 p-4 flex justify-between items-center">
          <h2 class="text-xl font-bold">📝 Стать исполнителем</h2>
          <button
              @click="showBecomeProviderModal = false"
              class="text-gray-400 hover:text-white text-2xl"
          >
            ✕
          </button>
        </div>

        <!-- Step Indicator -->
        <div class="px-4 pt-4 flex gap-2">
          <div
              v-for="step in 4"
              :key="step"
              :class="[
              'flex-1 h-1 rounded-full transition',
              currentStep >= step ? 'bg-blue-500' : 'bg-slate-700'
            ]"
          />
        </div>

        <!-- Content -->
        <div class="p-4 space-y-4">
          <!-- Step 1: Basic Info -->
          <div v-if="currentStep === 1">
            <h3 class="text-lg font-semibold text-blue-400 mb-4">Основная информация</h3>

            <div class="space-y-3">
              <div>
                <label class="block text-sm font-semibold mb-2">Название услуги</label>
                <input
                    v-model="newProvider.serviceName"
                    type="text"
                    placeholder="Например: Уроки английского онлайн"
                    class="w-full bg-slate-700 border border-blue-900 rounded-lg px-4 py-2 text-white placeholder-gray-500 focus:outline-none focus:border-blue-500"
                />
              </div>

              <div>
                <label class="block text-sm font-semibold mb-2">Описание услуги</label>
                <textarea
                    v-model="newProvider.description"
                    placeholder="Подробное описание того, что вы предлагаете"
                    rows="4"
                    class="w-full bg-slate-700 border border-blue-900 rounded-lg px-4 py-2 text-white placeholder-gray-500 focus:outline-none focus:border-blue-500 resize-none"
                />
              </div>

              <div>
                <label class="block text-sm font-semibold mb-2">Категория</label>
                <select
                    v-model="newProvider.category"
                    class="w-full bg-slate-700 border border-blue-900 rounded-lg px-4 py-2 text-white focus:outline-none focus:border-blue-500"
                >
                  <option value="">Выберите категорию</option>
                  <option value="repair">🏠 Ремонт</option>
                  <option value="business">💼 Бизнес</option>
                  <option value="fashion">👗 Мода</option>
                  <option value="education">📚 Обучение</option>
                  <option value="design">🎨 Дизайн</option>
                  <option value="it">💻 IT</option>
                </select>
              </div>

              <div>
                <label class="block text-sm font-semibold mb-2">Цена за услугу (₽)</label>
                <input
                    v-model.number="newProvider.price"
                    type="number"
                    placeholder="500"
                    class="w-full bg-slate-700 border border-blue-900 rounded-lg px-4 py-2 text-white placeholder-gray-500 focus:outline-none focus:border-blue-500"
                />
              </div>
            </div>
          </div>

          <!-- Step 2: Images -->
          <div v-if="currentStep === 2">
            <h3 class="text-lg font-semibold text-blue-400 mb-4">Фотографии услуги</h3>
            <p class="text-sm text-gray-400 mb-3">Добавьте до 5 фотографий (макс 5 МБ каждая)</p>

            <!-- Image Preview -->
            <div class="space-y-2">
              <div
                  v-for="(image, index) in newProvider.images"
                  :key="index"
                  class="relative bg-slate-700 border border-blue-900 rounded-lg overflow-hidden"
              >
                <img
                    :src="image.preview"
                    :alt="'Service image ' + (index + 1)"
                    class="w-full h-32 object-cover"
                />
                <button
                    @click="removeImage(index)"
                    class="absolute top-1 right-1 bg-red-600 text-white rounded-full p-1 hover:bg-red-700"
                >
                  ✕
                </button>
              </div>

              <!-- Add Image Button -->
              <div v-if="newProvider.images.length < 5">
                <label class="flex items-center justify-center gap-2 bg-slate-700 border border-dashed border-blue-900 rounded-lg py-6 cursor-pointer hover:border-blue-500 transition">
                  <span class="text-2xl">📸</span>
                  <span class="text-sm font-semibold">Добавить фото</span>
                  <input
                      type="file"
                      accept="image/*"
                      class="hidden"
                      @change="handleImageUpload"
                  />
                </label>
              </div>
            </div>

            <div v-if="newProvider.images.length === 0" class="text-center py-6 text-gray-400">
              <p class="text-4xl mb-2">📷</p>
              <p>Добавьте минимум одну фотографию</p>
            </div>
          </div>

          <!-- Step 3: Schedule -->
          <div v-if="currentStep === 3">
            <h3 class="text-lg font-semibold text-blue-400 mb-4">График работы</h3>

            <div class="space-y-4">
              <div>
                <label class="block text-sm font-semibold mb-2">Часовой пояс</label>
                <select
                    v-model="newProvider.timezone"
                    class="w-full bg-slate-700 border border-blue-900 rounded-lg px-4 py-2 text-white focus:outline-none focus:border-blue-500"
                >
                  <option value="UTC+3">UTC+3 (Москва)</option>
                  <option value="UTC+4">UTC+4 (Казань)</option>
                  <option value="UTC+5">UTC+5 (Екатеринбург)</option>
                  <option value="UTC+8">UTC+8 (Владивосток)</option>
                </select>
              </div>

              <div>
                <label class="block text-sm font-semibold mb-3">Доступность</label>
                <div class="space-y-2 bg-slate-700 rounded-lg p-3 border border-blue-900">
                  <label class="flex items-center gap-2 cursor-pointer">
                    <input
                        v-model="newProvider.availability.weekdays"
                        type="checkbox"
                        class="w-4 h-4"
                    />
                    <span class="text-sm">Будни (Пн-Пт)</span>
                  </label>
                  <label class="flex items-center gap-2 cursor-pointer">
                    <input
                        v-model="newProvider.availability.weekends"
                        type="checkbox"
                        class="w-4 h-4"
                    />
                    <span class="text-sm">Выходные (Сб-Вс)</span>
                  </label>
                  <label class="flex items-center gap-2 cursor-pointer">
                    <input
                        v-model="newProvider.availability.evenings"
                        type="checkbox"
                        class="w-4 h-4"
                    />
                    <span class="text-sm">Вечерние часы (18:00-23:00)</span>
                  </label>
                </div>
              </div>
            </div>
          </div>

          <!-- Step 4: Verification -->
          <div v-if="currentStep === 4">
            <h3 class="text-lg font-semibold text-blue-400 mb-4">Проверка</h3>

            <div class="bg-blue-900/20 border border-blue-900 rounded-lg p-4 space-y-3">
              <div class="flex items-start gap-2">
                <span class="text-green-400 font-bold">✓</span>
                <div class="text-sm">
                  <p class="font-semibold">{{ newProvider.serviceName }}</p>
                  <p class="text-gray-400">{{ newProvider.category }}</p>
                </div>
              </div>

              <div class="flex items-start gap-2">
                <span class="text-green-400 font-bold">✓</span>
                <div class="text-sm">
                  <p class="font-semibold">{{ newProvider.price }}₽ за услугу</p>
                  <p class="text-gray-400">{{ newProvider.images.length }} фотографий</p>
                </div>
              </div>

              <div class="flex items-start gap-2">
                <span class="text-green-400 font-bold">✓</span>
                <div class="text-sm">
                  <p class="font-semibold">{{ newProvider.timezone }}</p>
                  <p class="text-gray-400">Данные готовы к отправке</p>
                </div>
              </div>
            </div>

            <p class="text-xs text-gray-400 mt-4">
              После отправки ваш профиль исполнителя будет создан и опубликован. Клиенты смогут найти вашу услугу в каталоге.
            </p>
          </div>
        </div>

        <!-- Footer Buttons -->
        <div class="sticky bottom-0 bg-slate-800 border-t border-blue-900 p-4 flex gap-2">
          <button
              v-if="currentStep > 1"
              @click="currentStep--"
              class="flex-1 bg-slate-700 hover:bg-slate-600 text-white font-semibold py-2 rounded-lg transition"
          >
            ← Назад
          </button>
          <button
              v-if="currentStep < 4"
              @click="currentStep++"
              :disabled="!isStepValid"
              :class="[
              'flex-1 font-semibold py-2 rounded-lg transition',
              isStepValid
                ? 'bg-blue-600 hover:bg-blue-500 text-white'
                : 'bg-gray-700 text-gray-400 cursor-not-allowed'
            ]"
          >
            Далее →
          </button>
          <button
              v-else
              @click="submitProvider"
              class="flex-1 bg-green-600 hover:bg-green-500 text-white font-semibold py-2 rounded-lg transition"
          >
            ✓ Создать профиль
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { useUserStore } from '@/stores/userStore'

export default {
  name: 'ProfileView',
  props: {
    userData: Object,
    ordersCount: Number
  },
  setup() {
    const userStore = useUserStore()
    return { userStore }
  },
  data() {
    return {
      showBecomeProviderModal: false,
      currentStep: 1,
      selectedServiceForEdit: null,
      serviceDetailImageIndex: 0,
      newProvider: {
        serviceName: '',
        description: '',
        category: '',
        price: 0,
        timezone: 'UTC+3',
        availability: {
          weekdays: true,
          weekends: false,
          evenings: true
        },
        images: []
      }
    }
  },
  computed: {
    isStepValid() {
      switch (this.currentStep) {
        case 1:
          return (
              this.newProvider.serviceName.trim().length > 0 &&
              this.newProvider.description.trim().length > 10 &&
              this.newProvider.category.length > 0 &&
              this.newProvider.price > 0
          )
        case 2:
          return this.newProvider.images.length > 0
        case 3:
          return Object.values(this.newProvider.availability).some(v => v)
        case 4:
          return true
        default:
          return false
      }
    }
  },
  methods: {
    handleImageUpload(event) {
      const files = event.target.files
      if (files) {
        Array.from(files).forEach(file => {
          if (file.size > 5 * 1024 * 1024) {
            alert('Файл слишком большой (макс 5 МБ)')
            return
          }

          const reader = new FileReader()
          reader.onload = (e) => {
            if (this.newProvider.images.length < 5) {
              this.newProvider.images.push({
                file,
                preview: e.target.result
              })
            }
          }
          reader.readAsDataURL(file)
        })
      }
      event.target.value = ''
    },
    removeImage(index) {
      this.newProvider.images.splice(index, 1)
    },
    submitProvider() {
      console.log('📝 Creating provider:', this.newProvider)

      this.userStore.addService({
        serviceName: this.newProvider.serviceName,
        name: this.newProvider.serviceName,
        description: this.newProvider.description,
        category: this.newProvider.category,
        price: this.newProvider.price,
        images: this.newProvider.images,
        availability: this.newProvider.availability,
        timezone: this.newProvider.timezone
      })

      this.showBecomeProviderModal = false
      this.currentStep = 1
      this.newProvider = {
        serviceName: '',
        description: '',
        category: '',
        price: 0,
        timezone: 'UTC+3',
        availability: {
          weekdays: true,
          weekends: false,
          evenings: true
        },
        images: []
      }

      this.$emit('show-toast', '✅ Профиль исполнителя создан!')
    },
    selectServiceForEdit(service) {
      this.selectedServiceForEdit = service
      this.serviceDetailImageIndex = 0
    },
    deleteServiceConfirm(serviceId) {
      if (confirm('Вы уверены? Услуга будет удалена.')) {
        this.userStore.deleteService(serviceId)
        this.selectedServiceForEdit = null
        this.$emit('show-toast', '🗑️ Услуга удалена')
      }
    },
    openProviderDashboard() {
      console.log('📊 Opening provider dashboard')
      this.$emit('show-toast', '👤 Профиль исполнителя открыт')
    },
    openSettings() {
      this.$emit('open-settings')
    },
    addNewService() {
      this.showBecomeProviderModal = true
      this.currentStep = 1
    }
  }
}
</script>

<style scoped>
.profile-view {
  max-width: 400px;
  margin: 0 auto;
}

.modal-overlay {
  animation: fadeIn 0.3s ease-out;
}

.modal-content {
  animation: slideUp 0.3s ease-out;
}

@keyframes fadeIn {
  from {
    opacity: 0;
  }
  to {
    opacity: 1;
  }
}

@keyframes slideUp {
  from {
    transform: translateY(100%);
  }
  to {
    transform: translateY(0);
  }
}
</style>
