// src/env.d.ts
/// <reference types="vite/client" />

declare global {
  interface Window {
    Telegram?: {
      WebApp: {
        ready: () => void
        expand: () => void
        disableVerticalSwipes: () => void
        enableClosingConfirmation: () => void
        setHeaderColor: (color: string) => void
        showAlert: (message: string) => void
        showConfirm: (message: string, callback: (result: boolean) => void) => void
        showPopup: (params: any, callback?: (id?: string) => void) => void
        sendData: (data: string) => void
        close: () => void
        MainButton: {
          show: () => void
          hide: () => void
          setText: (text: string) => void
          setParams: (params: any) => void
          onClick: (callback: () => void) => void
        }
        BackButton: {
          show: () => void
          hide: () => void
          onClick: (callback: () => void) => void
        }
        onEvent: (eventType: string, callback: (...args: any[]) => void) => void
        initData: string
        initDataUnsafe: any
        colorScheme: 'dark' | 'light'
        themeParams: {
          bg_color?: string
          text_color?: string
          hint_color?: string
          link_color?: string
          button_color?: string
          button_text_color?: string
        }
      }
    }
    telegramUser?: any
  }
}

export {}
