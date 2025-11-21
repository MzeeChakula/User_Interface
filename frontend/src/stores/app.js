import { defineStore } from 'pinia'
import { ref } from 'vue'

export const useAppStore = defineStore('app', () => {
  const isFirstTime = ref(localStorage.getItem('hasSeenIntro') !== 'true')
  const language = ref(localStorage.getItem('language') || 'en')
  const notifications = ref(localStorage.getItem('notifications') === 'true')
  const isOnline = ref(navigator.onLine)
  const showLoader = ref(false)

  const setFirstTimeComplete = () => {
    isFirstTime.value = false
    localStorage.setItem('hasSeenIntro', 'true')
  }

  const setLanguage = (lang) => {
    language.value = lang
    localStorage.setItem('language', lang)
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
