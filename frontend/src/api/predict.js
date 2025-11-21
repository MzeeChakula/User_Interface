import apiClient from './client'

export const predictAPI = {
  /**
   * Predict caloric needs for an individual
   * @param {Object} data - { age, weight, height, gender, activity_level }
   * @returns {Promise}
   */
  async predictCalories(data) {
    const response = await apiClient.post('/predict/', data)
    return response.data
  },

  /**
   * Get food recommendations based on profile
   * @param {Object} params - Query parameters { dietary_preference?, allergens?, max_results? }
   * @returns {Promise}
   */
  async getFoodRecommendations(params = {}) {
    const response = await apiClient.get('/predict/recommend', { params })
    return response.data
  },

  /**
   * Get example input format for predictions
   * @returns {Promise}
   */
  async getExampleInput() {
    const response = await apiClient.get('/predict/example')
    return response.data
  }
}
