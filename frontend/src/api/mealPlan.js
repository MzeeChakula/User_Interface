import apiClient from './client'

export const mealPlanAPI = {
  /**
   * Generate a meal plan
   * @param {Object} planData - { name, age, health_conditions, preferred_foods }
   * @returns {Promise}
   */
  async generateMealPlan(planData) {
    const response = await apiClient.post('/meal-plan/generate', planData)
    return response.data
  },

  /**
   * Download meal plan as PDF
   * @param {Object} planData - { name, age, health_conditions, preferred_foods }
   * @returns {Promise<Blob>}
   */
  async downloadPDF(planData) {
    const response = await apiClient.post('/meal-plan/generate/pdf', planData, {
      responseType: 'blob'
    })

    // Create a download link
    const blob = new Blob([response.data], { type: 'application/pdf' })
    const url = window.URL.createObjectURL(blob)
    const link = document.createElement('a')
    link.href = url
    link.download = `meal_plan_${planData.name.replace(/\s/g, '_')}_${new Date().toISOString().split('T')[0]}.pdf`
    document.body.appendChild(link)
    link.click()
    document.body.removeChild(link)
    window.URL.revokeObjectURL(url)

    return blob
  }
}
