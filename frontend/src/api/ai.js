import apiClient from './client'

export const aiAPI = {
  /**
   * Translate text to specified language
   * @param {Object} data - { text, target_language, source_language? }
   * @returns {Promise}
   */
  async translate(data) {
    const response = await apiClient.post('/ai/translate', data)
    return response.data
  },

  /**
   * Detect language of text
   * @param {string} text - Text to detect language
   * @returns {Promise}
   */
  async detectLanguage(text) {
    const response = await apiClient.post('/ai/detect-language', { text })
    return response.data
  },

  /**
   * Get list of supported languages
   * @returns {Promise}
   */
  async getSupportedLanguages() {
    const response = await apiClient.get('/ai/languages')
    return response.data
  },

  /**
   * Perform RAG query with search
   * @param {Object} data - { query, search_web? }
   * @returns {Promise}
   */
  async ragQuery(data) {
    const response = await apiClient.post('/ai/rag', data)
    return response.data
  },

  /**
   * Upload document for RAG processing
   * @param {File} file - Document file to upload
   * @param {Function} onUploadProgress - Progress callback
   * @returns {Promise}
   */
  async uploadDocument(file, onUploadProgress) {
    const formData = new FormData()
    formData.append('file', file)

    const response = await apiClient.post('/ai/rag/upload', formData, {
      headers: {
        'Content-Type': 'multipart/form-data'
      },
      onUploadProgress: (progressEvent) => {
        if (onUploadProgress) {
          const percentCompleted = Math.round((progressEvent.loaded * 100) / progressEvent.total)
          onUploadProgress(percentCompleted)
        }
      }
    })
    return response.data
  }
}
