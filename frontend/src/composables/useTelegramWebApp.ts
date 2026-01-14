// src/composables/useTelegramWebApp.ts
import { computed } from 'vue'

export function useTelegramWebApp() {
  const tg = computed(() => window.Telegram?.WebApp)
  
  const getTelegramUser = () => {
    if (!tg.value) return null
    try {
      const initData = new URLSearchParams(tg.value.initData || '')
      const user = initData.get('user')
      return user ? JSON.parse(user) : null
    } catch (e) {
      console.error('Error parsing Telegram user:', e)
      return null
    }
  }
  
  const showAlert = (message: string): void => {
    if (tg.value) {
      tg.value.showAlert(message)
    } else {
      alert(message)
    }
  }
  
  const showConfirm = (message: string, callback: (result: boolean) => void): void => {
    if (tg.value) {
      tg.value.showConfirm(message, callback)
    } else {
      const result = window.confirm(message)
      callback(result)
    }
  }
  
  const showPopup = (params: any, callback?: (id?: string) => void): void => {
    if (tg.value) {
      tg.value.showPopup(params, callback)
    }
  }
  
  const sendData = (data: string): void => {
    if (tg.value) {
      tg.value.sendData(data)
    }
  }
  
  const setBackButtonVisible = (visible: boolean): void => {
    if (tg.value) {
      if (visible) {
        tg.value.BackButton.show()
      } else {
        tg.value.BackButton.hide()
      }
    }
  }
  
  const setMainButtonVisible = (visible: boolean): void => {
    if (tg.value) {
      if (visible) {
        tg.value.MainButton.show()
      } else {
        tg.value.MainButton.hide()
      }
    }
  }
  
  const setMainButtonText = (text: string): void => {
    if (tg.value) {
      tg.value.MainButton.setText(text)
    }
  }
  
  const setMainButtonColor = (color: string): void => {
    if (tg.value) {
      tg.value.MainButton.setParams({ bg_color: color })
    }
  }
  
  const onMainButtonClick = (callback: () => void): void => {
    if (tg.value) {
      tg.value.MainButton.onClick(callback)
    }
  }
  
  const onBackButtonClick = (callback: () => void): void => {
    if (tg.value) {
      tg.value.onEvent('backButtonClicked', callback)
    }
  }
  
  const getTheme = (): 'dark' | 'light' => {
    if (tg.value) {
      return tg.value.colorScheme === 'dark' ? 'dark' : 'light'
    }
    return 'dark'
  }
  
  const getThemeColors = () => {
    if (tg.value && tg.value.themeParams) {
      return {
        bgColor: tg.value.themeParams.bg_color,
        textColor: tg.value.themeParams.text_color,
        hintColor: tg.value.themeParams.hint_color,
        linkColor: tg.value.themeParams.link_color,
        buttonColor: tg.value.themeParams.button_color,
        buttonTextColor: tg.value.themeParams.button_text_color
      }
    }
    return null
  }
  
  const isIframe = (): boolean => {
    try {
      return window.self !== window.top
    } catch (e) {
      return true
    }
  }
  
  const isTelegramWebApp = (): boolean => {
    return !!tg.value
  }
  
  return {
    tg,
    getTelegramUser,
    showAlert,
    showConfirm,
    showPopup,
    sendData,
    setBackButtonVisible,
    setMainButtonVisible,
    setMainButtonText,
    setMainButtonColor,
    onMainButtonClick,
    onBackButtonClick,
    getTheme,
    getThemeColors,
    isIframe,
    isTelegramWebApp
  }
}
