import { defineStore } from 'pinia'
import { ref } from 'vue'
import { authAPI } from '../api'

export const useAuthStore = defineStore('auth', () => {
  const isAuthenticated = ref(false)
  const user = ref(null)
  const token = ref(localStorage.getItem('auth_token') || null)
  const loading = ref(false)
  const error = ref(null)

  const register = async (userData) => {
    loading.value = true
    error.value = null
    try {
      await authAPI.register(userData)

      // After registration, log the user in
      return await login({ email: userData.email, password: userData.password })
    } catch (err) {
      console.error('Registration error:', err)
      error.value = err.response?.data?.detail || 'Registration failed'
      return { success: false, error: error.value }
    } finally {
      loading.value = false
    }
  }

  const login = async (credentials) => {
    loading.value = true
    error.value = null
    try {
      const response = await authAPI.login(credentials)

      token.value = response.access_token
      localStorage.setItem('auth_token', token.value)
      isAuthenticated.value = true

      // Fetch user data
      await fetchUser()

      return { success: true }
    } catch (err) {
      console.error('Login error:', err)
      error.value = err.response?.data?.detail || 'Login failed'
      return { success: false, error: error.value }
    } finally {
      loading.value = false
    }
  }

  const resetPassword = async (email) => {
    loading.value = true
    error.value = null
    try {
      await authAPI.resetPassword({ email })
      return { success: true }
    } catch (err) {
      console.error('Reset password error:', err)
      error.value = err.response?.data?.detail || 'Failed to send reset email'
      return { success: false, error: error.value }
    } finally {
      loading.value = false
    }
  }

  const fetchUser = async () => {
    try {
      const userData = await authAPI.getCurrentUser()
      user.value = userData
    } catch (err) {
      console.error('Fetch user error:', err)
      // If fetching user fails, clear auth
      logout()
    }
  }

  const logout = () => {
    isAuthenticated.value = false
    user.value = null
    token.value = null
    localStorage.removeItem('auth_token')
  }

  const checkAuth = async () => {
    const storedToken = localStorage.getItem('auth_token')
    if (storedToken) {
      token.value = storedToken
      isAuthenticated.value = true
      // Verify token with backend by fetching user
      try {
        await fetchUser()
      } catch (err) {
        // Token is invalid, clear auth
        logout()
      }
    }
  }

  return {
    isAuthenticated,
    user,
    token,
    loading,
    error,
    register,
    login,
    logout,
    checkAuth,
    checkAuth,
    fetchUser,
    resetPassword
  }
})
