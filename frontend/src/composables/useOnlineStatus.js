import { ref, onMounted, onUnmounted } from 'vue'

export function useOnlineStatus() {
  const isOnline = ref(navigator.onLine)
  const wasOffline = ref(false)

  const updateOnlineStatus = () => {
    const currentStatus = navigator.onLine

    if (!isOnline.value && currentStatus) {
      wasOffline.value = true
    }

    isOnline.value = currentStatus
  }

  const checkServerConnection = async (apiUrl = '/api/health') => {
    try {
      const response = await fetch(apiUrl, {
        method: 'HEAD',
        cache: 'no-cache',
        signal: AbortSignal.timeout(5000)
      })
      return response.ok
    } catch (error) {
      console.warn('Server connection check failed:', error)
      return false
    }
  }

  onMounted(() => {
    window.addEventListener('online', updateOnlineStatus)
    window.addEventListener('offline', updateOnlineStatus)
  })

  onUnmounted(() => {
    window.removeEventListener('online', updateOnlineStatus)
    window.removeEventListener('offline', updateOnlineStatus)
  })

  return {
    isOnline,
    wasOffline,
    checkServerConnection
  }
}
