import { defineStore } from 'pinia'
import { ref, watch } from 'vue'

export const useAppStore = defineStore('app', () => {
  const isFirstTime = ref(localStorage.getItem('hasSeenIntro') !== 'true')
  const language = ref(localStorage.getItem('preferred_language') || 'eng')
  const notifications = ref(localStorage.getItem('notifications') === 'true')
  const isOnline = ref(navigator.onLine)
  const showLoader = ref(false)

  // Auto-save language when it changes
  watch(language, (newLang) => {
    localStorage.setItem('preferred_language', newLang)
  })

  const setFirstTimeComplete = () => {
    isFirstTime.value = false
    localStorage.setItem('hasSeenIntro', 'true')
  }

  const setLanguage = (lang) => {
    language.value = lang
    localStorage.setItem('preferred_language', lang)
  }

  const toggleNotifications = () => {
    notifications.value = !notifications.value
    localStorage.setItem('notifications', notifications.value.toString())
  }

  const setOnlineStatus = (status) => {
    isOnline.value = status
  }

  const setLoader = (status) => {
    showLoader.value = status
  }

  return {
    isFirstTime,
    language,
    notifications,
    isOnline,
    showLoader,
    setFirstTimeComplete,
    setLanguage,
    toggleNotifications,
    setOnlineStatus,
    setLoader
  }
})
