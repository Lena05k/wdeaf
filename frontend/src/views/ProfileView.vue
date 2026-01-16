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

    <!-- Provider Profile Info (if provider) -->
    <div v-if="userStore.isProvider && userStore.getProviderInfo()" class="mt-6">
      <div class="bg-gradient-to-br from-blue-900/30 to-blue-800/30 border border-blue-800 rounded-lg p-4">
        <div class="flex items-center justify-between mb-3">
          <h3 class="text-lg font-bold">👤 Ваш профиль исполнителя</h3>
          <button
              @click="editProviderProfile"
              class="text-blue-400 hover:text-blue-300 text-lg"
          >
            ✏️
          </button>
        </div>
        <div class="space-y-2 text-sm">
          <p><span class="text-gray-400">О себе:</span> {{ userStore.getProviderInfo()?.description }}</p>
          <div class="flex gap-2 flex-wrap">
            <span 
              v-for="cat in userStore.getProviderInfo()?.categories" 
              :key="cat"
              class="bg-blue-600 text-white px-2 py-1 rounded text-xs"
            >
              {{ getCategoryLabel(cat) }}
            </span>
          </div>
        </div>
      </div>
    </div>

    <!-- Provider Services (if provider) -->
    <div v-if="userStore.isProvider" class="mt-6">
      <div class="flex items-center justify-between mb-3">
        <h3 class="text-lg font-bold">📋 Мои услуги</h3>
        <button
            @click="addNewService"
            class="bg-blue-600 hover:bg-blue-500 text-white px-3 py-1 rounded text-sm transition"
        >
          + Добавить
        </button>
      </div>

      <!-- Service Cards Grid -->
      <div v-if="userStore.providerServices.length > 0" class="grid grid-cols-1 gap-3 mb-3">
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
              {{ getCategoryLabel(service.category) }}
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

      <div v-else class="text-center py-6 text-gray-400">
        <p class="text-2xl mb-2">📭</p>
        <p class="text-sm">У вас еще нет услуг</p>
        <button
            @click="addNewService"
            class="mt-3 bg-blue-600 hover:bg-blue-500 text-white font-semibold py-2 px-4 rounded-lg transition inline-block"
        >
          + Создать первую услугу
        </button>
      </div>
    </div>

    <!-- ======================== MODALS ======================== -->

    <!-- Become Provider Modal (Profile Setup) -->
    <div v-if="showBecomeProviderModal" class="modal-overlay fixed inset-0 bg-black/50 flex items-end z-50">
      <div class="modal-content bg-slate-800 w-full max-w-md rounded-t-2xl border-t border-blue-900 max-h-[90vh] overflow-y-auto">
        <!-- Header -->
        <div class="sticky top-0 bg-slate-800 border-b border-blue-900 p-4 flex justify-between items-center">
          <h2 class="text-xl font-bold">📝 Создать профиль исполнителя</h2>
          <button
              @click="closeBecomeProviderModal"
              class="text-gray-400 hover:text-white text-2xl"
          >
            ✕
          </button>
        </div>

        <!-- Step Indicator -->
        <div class="px-4 pt-4 flex gap-2">
          <div
              v-for="step in 2"
              :key="step"
              :class="[
              'flex-1 h-1 rounded-full transition',
              currentStep >= step ? 'bg-blue-500' : 'bg-slate-700'
            ]"
          />
        </div>

        <!-- Content -->
        <div class="p-4 space-y-4">
          <!-- Step 1: Personal Info & Categories -->
          <div v-if="currentStep === 1">
            <h3 class="text-lg font-semibold text-blue-400 mb-4">Расскажите о себе</h3>

            <div class="space-y-3">
              <div>
                <label class="block text-sm font-semibold mb-2">Ваше имя (может отличаться от Telegram)</label>
                <input
                    v-model="newProviderProfile.name"
                    type="text"
                    placeholder="Например: Иван Петров"
                    class="w-full bg-slate-700 border border-blue-900 rounded-lg px-4 py-2 text-white placeholder-gray-500 focus:outline-none focus:border-blue-500"
                />
              </div>

              <div>
                <label class="block text-sm font-semibold mb-2">О себе и вашем опыте</label>
                <textarea
                    v-model="newProviderProfile.description"
                    placeholder="Расскажите, чем вы занимаетесь, ваш опыт, навыки и почему клиенты должны выбрать вас"
                    rows="4"
                    class="w-full bg-slate-700 border border-blue-900 rounded-lg px-4 py-2 text-white placeholder-gray-500 focus:outline-none focus:border-blue-500 resize-none"
                />
              </div>

              <div>
                <label class="block text-sm font-semibold mb-3">Категории работ</label>
                <p class="text-xs text-gray-400 mb-2">Выберите все подходящие категории</p>
                <div class="space-y-2 bg-slate-700 rounded-lg p-3 border border-blue-900 max-h-48 overflow-y-auto">
                  <label 
                    v-for="cat in availableCategories" 
                    :key="cat.value"
                    class="flex items-center gap-2 cursor-pointer hover:bg-slate-600 p-2 rounded transition"
                  >
                    <input
                        :checked="newProviderProfile.categories.includes(cat.value)"
                        type="checkbox"
                        @change="toggleCategory(cat.value)"
                        class="w-4 h-4"
                    />
                    <span class="text-sm">{{ cat.label }}</span>
                  </label>
                </div>
              </div>
            </div>
          </div>

          <!-- Step 2: Schedule & Verification -->
          <div v-if="currentStep === 2">
            <h3 class="text-lg font-semibold text-blue-400 mb-4">График работы</h3>

            <div class="space-y-4">
              <div>
                <label class="block text-sm font-semibold mb-2">Часовой пояс</label>
                <select
                    v-model="newProviderProfile.timezone"
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
                        v-model="newProviderProfile.availability.weekdays"
                        type="checkbox"
                        class="w-4 h-4"
                    />
                    <span class="text-sm">Будни (Пн-Пт)</span>
                  </label>
                  <label class="flex items-center gap-2 cursor-pointer">
                    <input
                        v-model="newProviderProfile.availability.weekends"
                        type="checkbox"
                        class="w-4 h-4"
                    />
                    <span class="text-sm">Выходные (Сб-Вс)</span>
                  </label>
                  <label class="flex items-center gap-2 cursor-pointer">
                    <input
                        v-model="newProviderProfile.availability.evenings"
                        type="checkbox"
                        class="w-4 h-4"
                    />
                    <span class="text-sm">Вечерние часы (18:00-23:00)</span>
                  </label>
                </div>
              </div>

              <!-- Verification Summary -->
              <div class="bg-blue-900/20 border border-blue-900 rounded-lg p-4 space-y-3">
                <h4 class="font-semibold text-blue-400 mb-3">✓ Проверка информации</h4>
                <div class="space-y-2 text-sm">
                  <p><span class="text-gray-400">Имя:</span> {{ newProviderProfile.name }}</p>
                  <p><span class="text-gray-400">О себе:</span> {{ newProviderProfile.description.substring(0, 50) }}...</p>
                  <p><span class="text-gray-400">Категории:</span> {{ newProviderProfile.categories.length }} выбрано</p>
                  <p><span class="text-gray-400">Часовой пояс:</span> {{ newProviderProfile.timezone }}</p>
                </div>
              </div>
            </div>
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
              v-if="currentStep < 2"
              @click="currentStep++"
              :disabled="!isStep1Valid"
              :class="[
              'flex-1 font-semibold py-2 rounded-lg transition',
              isStep1Valid
                ? 'bg-blue-600 hover:bg-blue-500 text-white'
                : 'bg-gray-700 text-gray-400 cursor-not-allowed'
            ]"
          >
            Далее →
          </button>
          <button
              v-else
              @click="submitProviderProfile"
              :disabled="!isStep2Valid"
              :class="[
              'flex-1 font-semibold py-2 rounded-lg transition',
              isStep2Valid
                ? 'bg-green-600 hover:bg-green-500 text-white'
                : 'bg-gray-700 text-gray-400 cursor-not-allowed'
            ]"
          >
            ✓ Создать профиль
          </button>
        </div>
      </div>
    </div>

    <!-- Create/Edit Service Modal -->
    <div v-if="showServiceModal" class="modal-overlay fixed inset-0 bg-black/50 flex items-end z-50">
      <div class="modal-content bg-slate-800 w-full max-w-md rounded-t-2xl border-t border-blue-900 max-h-[90vh] overflow-y-auto">
        <!-- Header -->
        <div class="sticky top-0 bg-slate-800 border-b border-blue-900 p-4 flex justify-between items-center">
          <h2 class="text-xl font-bold">{{ isEditingService ? '✏️ Редактировать услугу' : '➕ Новая услуга' }}</h2>
          <button
              @click="closeServiceModal"
              class="text-gray-400 hover:text-white text-2xl"
          >
            ✕
          </button>
        </div>

        <!-- Step Indicator -->
        <div class="px-4 pt-4 flex gap-2">
          <div
              v-for="step in 3"
              :key="step"
              :class="[
              'flex-1 h-1 rounded-full transition',
              serviceStep >= step ? 'bg-blue-500' : 'bg-slate-700'
            ]"
          />
        </div>

        <!-- Content -->
        <div class="p-4 space-y-4">
          <!-- Step 1: Basic Info -->
          <div v-if="serviceStep === 1">
            <h3 class="text-lg font-semibold text-blue-400 mb-4">Основная информация</h3>

            <div class="space-y-3">
              <div>
                <label class="block text-sm font-semibold mb-2">Название услуги</label>
                <input
                    v-model="currentService.serviceName"
                    type="text"
                    placeholder="Например: Уроки английского онлайн"
                    class="w-full bg-slate-700 border border-blue-900 rounded-lg px-4 py-2 text-white placeholder-gray-500 focus:outline-none focus:border-blue-500"
                />
              </div>

              <div>
                <label class="block text-sm font-semibold mb-2">Описание услуги</label>
                <textarea
                    v-model="currentService.description"
                    placeholder="Подробное описание того, что вы предлагаете"
                    rows="4"
                    class="w-full bg-slate-700 border border-blue-900 rounded-lg px-4 py-2 text-white placeholder-gray-500 focus:outline-none focus:border-blue-500 resize-none"
                />
              </div>

              <div>
                <label class="block text-sm font-semibold mb-2">Категория</label>
                <select
                    v-model="currentService.category"
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
                    v-model.number="currentService.price"
                    type="number"
                    placeholder="500"
                    class="w-full bg-slate-700 border border-blue-900 rounded-lg px-4 py-2 text-white placeholder-gray-500 focus:outline-none focus:border-blue-500"
                />
              </div>
            </div>
          </div>

          <!-- Step 2: Images -->
          <div v-if="serviceStep === 2">
            <h3 class="text-lg font-semibold text-blue-400 mb-4">Фотографии услуги</h3>
            <p class="text-sm text-gray-400 mb-3">Добавьте до 5 фотографий (макс 5 МБ каждая)</p>

            <!-- Image Preview -->
            <div class="space-y-2">
              <div
                  v-for="(image, index) in currentService.images"
                  :key="index"
                  class="relative bg-slate-700 border border-blue-900 rounded-lg overflow-hidden"
              >
                <img
                    :src="image.preview || image"
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
              <div v-if="currentService.images.length < 5">
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

            <div v-if="currentService.images.length === 0" class="text-center py-6 text-gray-400">
              <p class="text-4xl mb-2">📷</p>
              <p>Добавьте минимум одну фотографию</p>
            </div>
          </div>

          <!-- Step 3: Schedule & Verification -->
          <div v-if="serviceStep === 3">
            <h3 class="text-lg font-semibold text-blue-400 mb-4">График и проверка</h3>

            <div class="space-y-4">
              <div>
                <label class="block text-sm font-semibold mb-3">Доступность для этой услуги</label>
                <div class="space-y-2 bg-slate-700 rounded-lg p-3 border border-blue-900">
                  <label class="flex items-center gap-2 cursor-pointer">
                    <input
                        v-model="currentService.availability.weekdays"
                        type="checkbox"
                        class="w-4 h-4"
                    />
                    <span class="text-sm">Будни (Пн-Пт)</span>
                  </label>
                  <label class="flex items-center gap-2 cursor-pointer">
                    <input
                        v-model="currentService.availability.weekends"
                        type="checkbox"
                        class="w-4 h-4"
                    />
                    <span class="text-sm">Выходные (Сб-Вс)</span>
                  </label>
                  <label class="flex items-center gap-2 cursor-pointer">
                    <input
                        v-model="currentService.availability.evenings"
                        type="checkbox"
                        class="w-4 h-4"
                    />
                    <span class="text-sm">Вечерние часы (18:00-23:00)</span>
                  </label>
                </div>
              </div>

              <!-- Verification Summary -->
              <div class="bg-blue-900/20 border border-blue-900 rounded-lg p-4 space-y-3">
                <h4 class="font-semibold text-blue-400 mb-3">✓ Проверка услуги</h4>
                <div class="space-y-2 text-sm">
                  <p><span class="text-gray-400">Название:</span> {{ currentService.serviceName }}</p>
                  <p><span class="text-gray-400">Категория:</span> {{ getCategoryLabel(currentService.category) }}</p>
                  <p><span class="text-gray-400">Цена:</span> {{ currentService.price }}₽</p>
                  <p><span class="text-gray-400">Фотографий:</span> {{ currentService.images.length }}</p>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Footer Buttons -->
        <div class="sticky bottom-0 bg-slate-800 border-t border-blue-900 p-4 flex gap-2">
          <button
              v-if="serviceStep > 1"
              @click="serviceStep--"
              class="flex-1 bg-slate-700 hover:bg-slate-600 text-white font-semibold py-2 rounded-lg transition"
          >
            ← Назад
          </button>
          <button
              v-if="serviceStep < 3"
              @click="serviceStep++"
              :disabled="!isServiceStepValid"
              :class="[
              'flex-1 font-semibold py-2 rounded-lg transition',
              isServiceStepValid
                ? 'bg-blue-600 hover:bg-blue-500 text-white'
                : 'bg-gray-700 text-gray-400 cursor-not-allowed'
            ]"
          >
            Далее →
          </button>
          <button
              v-else
              @click="submitService"
              :disabled="!isServiceValid"
              :class="[
              'flex-1 font-semibold py-2 rounded-lg transition',
              isServiceValid
                ? 'bg-green-600 hover:bg-green-500 text-white'
                : 'bg-gray-700 text-gray-400 cursor-not-allowed'
            ]"
          >
            {{ isEditingService ? '✓ Сохранить' : '✓ Создать' }}
          </button>
        </div>
      </div>
    </div>

    <!-- View Service Modal -->
    <div v-if="selectedServiceForView" class="modal-overlay fixed inset-0 bg-black/50 flex items-end z-50">
      <div class="modal-content bg-slate-800 w-full max-w-md rounded-t-2xl border-t border-blue-900 max-h-[90vh] overflow-y-auto">
        <!-- Header -->
        <div class="sticky top-0 bg-slate-800 border-b border-blue-900 p-4 flex justify-between items-center">
          <h2 class="text-xl font-bold truncate">{{ selectedServiceForView.serviceName }}</h2>
          <button
              @click="selectedServiceForView = null"
              class="text-gray-400 hover:text-white text-2xl ml-2"
          >
            ✕
          </button>
        </div>

        <!-- Content -->
        <div class="p-4 space-y-4">
          <!-- Image Carousel -->
          <div v-if="selectedServiceForView.images && selectedServiceForView.images.length > 0" class="relative">
            <img
                :src="selectedServiceForView.images[serviceDetailImageIndex].preview || selectedServiceForView.images[serviceDetailImageIndex]"
                :alt="'Service image ' + (serviceDetailImageIndex + 1)"
                class="w-full h-48 object-cover rounded-lg"
            />

            <!-- Navigation Arrows -->
            <div v-if="selectedServiceForView.images.length > 1" class="absolute inset-0 flex items-center justify-between px-2 rounded-lg">
              <button
                  @click="serviceDetailImageIndex = (serviceDetailImageIndex - 1 + selectedServiceForView.images.length) % selectedServiceForView.images.length"
                  class="bg-black/50 text-white p-2 rounded-full hover:bg-black/70"
              >
                ←
              </button>
              <button
                  @click="serviceDetailImageIndex = (serviceDetailImageIndex + 1) % selectedServiceForView.images.length"
                  class="bg-black/50 text-white p-2 rounded-full hover:bg-black/70"
              >
                →
              </button>
            </div>

            <!-- Image Counter -->
            <div class="absolute bottom-2 right-2 bg-black/50 text-white px-2 py-1 rounded text-xs">
              {{ serviceDetailImageIndex + 1 }}/{{ selectedServiceForView.images.length }}
            </div>
          </div>

          <!-- Service Details -->
          <div class="space-y-3">
            <div>
              <p class="text-xs text-gray-400 mb-1">КАТЕГОРИЯ</p>
              <p class="font-semibold">{{ getCategoryLabel(selectedServiceForView.category) }}</p>
            </div>

            <div>
              <p class="text-xs text-gray-400 mb-1">ОПИСАНИЕ</p>
              <p class="text-sm">{{ selectedServiceForView.description }}</p>
            </div>

            <div>
              <p class="text-xs text-gray-400 mb-1">ЦЕНА</p>
              <p class="text-2xl font-bold text-blue-400">{{ selectedServiceForView.price }}₽</p>
            </div>

            <div>
              <p class="text-xs text-gray-400 mb-2">ГРАФИК РАБОТЫ</p>
              <div class="text-sm space-y-1">
                <p v-if="selectedServiceForView.availability?.weekdays" class="text-green-400">✓ Будни (Пн-Пт)</p>
                <p v-if="selectedServiceForView.availability?.weekends" class="text-green-400">✓ Выходные (Сб-Вс)</p>
                <p v-if="selectedServiceForView.availability?.evenings" class="text-green-400">✓ Вечерние часы (18:00-23:00)</p>
              </div>
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
              @click="deleteServiceConfirm(selectedServiceForView.id)"
              class="flex-1 bg-red-600 hover:bg-red-500 text-white font-semibold py-2 rounded-lg transition"
          >
            🗑️ Удалить
          </button>
          <button
              @click="openEditService(selectedServiceForView)"
              class="flex-1 bg-blue-600 hover:bg-blue-500 text-white font-semibold py-2 rounded-lg transition"
          >
            ✏️ Редактировать
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import { useUserStore } from '@/stores/userStore'

interface Service {
  id?: string | number
  serviceName: string
  name?: string
  description: string
  category: string
  price: number
  timezone?: string
  availability: {
    weekdays: boolean
    weekends: boolean
    evenings: boolean
  }
  images: any[]
}

const userStore = useUserStore()

// Category mapping
const categoryMap: Record<string, string> = {
  repair: '🏠 Ремонт',
  business: '💼 Бизнес',
  fashion: '👗 Мода',
  education: '📚 Обучение',
  design: '🎨 Дизайн',
  it: '💻 IT'
}

const availableCategories = [
  { value: 'repair', label: '🏠 Ремонт' },
  { value: 'business', label: '💼 Бизнес' },
  { value: 'fashion', label: '👗 Мода' },
  { value: 'education', label: '📚 Обучение' },
  { value: 'design', label: '🎨 Дизайн' },
  { value: 'it', label: '💻 IT' }
]

// Props
interface Props {
  ordersCount?: number
}

withDefaults(defineProps<Props>(), {
  ordersCount: 0
})

// ======================== Provider Profile Modal ========================
const showBecomeProviderModal = ref(false)
const currentStep = ref(1)

const newProviderProfile = ref({
  name: '',
  description: '',
  categories: [] as string[],
  timezone: 'UTC+3',
  availability: {
    weekdays: true,
    weekends: false,
    evenings: true
  }
})

const isStep1Valid = computed(() => {
  return (
    newProviderProfile.value.name.trim().length > 0 &&
    newProviderProfile.value.description.trim().length > 10 &&
    newProviderProfile.value.categories.length > 0
  )
})

const isStep2Valid = computed(() => {
  return Object.values(newProviderProfile.value.availability).some(v => v)
})

const toggleCategory = (category: string) => {
  const index = newProviderProfile.value.categories.indexOf(category)
  if (index === -1) {
    newProviderProfile.value.categories.push(category)
  } else {
    newProviderProfile.value.categories.splice(index, 1)
  }
}

const submitProviderProfile = () => {
  userStore.setProviderInfo({
    serviceName: newProviderProfile.value.name,
    description: newProviderProfile.value.description,
    category: newProviderProfile.value.categories[0],
    categories: newProviderProfile.value.categories,
    price: 0,
    timezone: newProviderProfile.value.timezone,
    availability: newProviderProfile.value.availability,
    maxConcurrentOrders: 5
  })

  closeBecomeProviderModal()
}

const closeBecomeProviderModal = () => {
  showBecomeProviderModal.value = false
  currentStep.value = 1
  newProviderProfile.value = {
    name: '',
    description: '',
    categories: [],
    timezone: 'UTC+3',
    availability: {
      weekdays: true,
      weekends: false,
      evenings: true
    }
  }
}

// ======================== Service Modal ========================
const showServiceModal = ref(false)
const serviceStep = ref(1)
const isEditingService = ref(false)

const defaultService: Service = {
  serviceName: '',
  description: '',
  category: '',
  price: 0,
  availability: {
    weekdays: true,
    weekends: false,
    evenings: true
  },
  images: []
}

const currentService = ref<Service>({ ...defaultService })

const isServiceStepValid = computed(() => {
  switch (serviceStep.value) {
    case 1:
      return (
        currentService.value.serviceName.trim().length > 0 &&
        currentService.value.description.trim().length > 10 &&
        currentService.value.category.length > 0 &&
        currentService.value.price > 0
      )
    case 2:
      return currentService.value.images.length > 0
    case 3:
      return Object.values(currentService.value.availability).some(v => v)
    default:
      return false
  }
})

const isServiceValid = computed(() => isServiceStepValid.value)

const handleImageUpload = (event: Event) => {
  const target = event.target as HTMLInputElement
  const files = target.files
  if (files) {
    Array.from(files).forEach(file => {
      if (file.size > 5 * 1024 * 1024) {
        alert('Файл слишком большой (макс 5 МБ)')
        return
      }

      const reader = new FileReader()
      reader.onload = (e) => {
        if (currentService.value.images.length < 5 && e.target?.result) {
          currentService.value.images.push({
            file,
            preview: e.target.result
          })
        }
      }
      reader.readAsDataURL(file)
    })
  }
  target.value = ''
}

const removeImage = (index: number) => {
  currentService.value.images.splice(index, 1)
}

const addNewService = () => {
  isEditingService.value = false
  currentService.value = { ...defaultService }
  serviceStep.value = 1
  showServiceModal.value = true
}

const openEditService = (service: Service) => {
  isEditingService.value = true
  currentService.value = JSON.parse(JSON.stringify(service))
  serviceStep.value = 1
  showServiceModal.value = true
  selectedServiceForView.value = null
}

const submitService = () => {
  if (isEditingService.value && currentService.value.id) {
    userStore.updateService(currentService.value.id, currentService.value)
  } else {
    userStore.addService(currentService.value)
  }

  closeServiceModal()
}

const closeServiceModal = () => {
  showServiceModal.value = false
  serviceStep.value = 1
  currentService.value = { ...defaultService }
  isEditingService.value = false
}

// ======================== View Service Modal ========================
const selectedServiceForView = ref<Service | null>(null)
const serviceDetailImageIndex = ref(0)

const selectServiceForEdit = (service: Service) => {
  selectedServiceForView.value = service
  serviceDetailImageIndex.value = 0
}

const deleteServiceConfirm = (serviceId: string | number | undefined) => {
  if (serviceId && confirm('Вы уверены? Услуга будет удалена.')) {
    userStore.deleteService(serviceId)
    selectedServiceForView.value = null
  }
}

// ======================== Utils ========================
const getCategoryLabel = (value: string) => {
  return categoryMap[value] || value
}

const editProviderProfile = () => {
  showBecomeProviderModal.value = true
  const providerInfo = userStore.getProviderInfo()
  if (providerInfo) {
    newProviderProfile.value = {
      name: providerInfo.serviceName,
      description: providerInfo.description,
      categories: providerInfo.categories || [providerInfo.category],
      timezone: providerInfo.timezone,
      availability: providerInfo.availability
    }
  }
}

const openProviderDashboard = () => {
  console.log('📊 Opening provider dashboard')
}

const openSettings = () => {
  console.log('⚙️ Opening settings')
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
