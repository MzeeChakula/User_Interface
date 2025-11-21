import { defineStore } from 'pinia'
import { ref } from 'vue'

export const useAuthStore = defineStore('auth', () => {
  const isAuthenticated = ref(false)
  const user = ref(null)
  const token = ref(localStorage.getItem('auth_token') || null)

  const login = async (credentials) => {
    try {
      // TODO: Replace with actual API call
      // const response = await api.post('/auth/login', credentials)

      // Mock login for now
      isAuthenticated.value = true
      user.value = {
        id: '1',
        name: credentials.name || 'User',
        email: credentials.email
      }
      token.value = 'mock_token'
      localStorage.setItem('auth_token', token.value)

      return { success: true }
    } catch (error) {
      console.error('Login error:', error)
      return { success: false, error }
    }
  }

  const logout = () => {
    isAuthenticated.value = false
    user.value = null
    token.value = null
    localStorage.removeItem('auth_token')
  }

  const checkAuth = () => {
    const storedToken = localStorage.getItem('auth_token')
    if (storedToken) {
      token.value = storedToken
      isAuthenticated.value = true
      // TODO: Verify token with backend
    }
  }

  return {
    isAuthenticated,
    user,
    token,
    login,
    logout,
    checkAuth
  }
})
