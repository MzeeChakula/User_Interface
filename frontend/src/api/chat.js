import apiClient from './client'

export const chatAPI = {
  /**
   * Send a message to the AI assistant
   * @param {Object} messageData - { message, language?, profile? }
   * @returns {Promise}
   */
  async sendMessage(messageData) {
    const response = await apiClient.post('/chat/message', messageData)
    return response.data
  }
}
