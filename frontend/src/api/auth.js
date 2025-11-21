import apiClient from './client'

export const authAPI = {
  /**
   * Register a new user
   * @param {Object} userData - { email, password, name }
   * @returns {Promise}
   */
  async register(userData) {
    const response = await apiClient.post('/auth/register', userData)
    return response.data
  },

  /**
   * Login user and get JWT token
   * @param {Object} credentials - { username (email), password }
   * @returns {Promise}
   */
  async login(credentials) {
    // Backend expects form data for OAuth2
    const formData = new URLSearchParams()
    formData.append('username', credentials.email)
    formData.append('password', credentials.password)

    const response = await apiClient.post('/auth/token', formData, {
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded'
      }
    })
    return response.data
  },

  /**
   * Get current user information
   * @returns {Promise}
   */
  async getCurrentUser() {
    const response = await apiClient.get('/auth/me')
    return response.data
  },

  /**
   * Request password reset
   * @param {Object} data - { email }
   * @returns {Promise}
   */
  async resetPassword(data) {
    const response = await apiClient.post('/auth/reset-password', data)
    return response.data
  }
}
