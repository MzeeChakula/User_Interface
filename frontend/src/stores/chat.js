import { defineStore } from 'pinia'
import { ref } from 'vue'
import { chatAPI } from '../api'
import { useProfileStore } from './profile'
import { useAppStore } from './app'

export const useChatStore = defineStore('chat', () => {
  const conversations = ref([])
  const currentConversation = ref(null)
  const isLoading = ref(false)
  const error = ref(null)

  const loadConversations = () => {
    const saved = localStorage.getItem('conversations')
    if (saved) {
      conversations.value = JSON.parse(saved)
    }
  }

  const saveConversations = () => {
    localStorage.setItem('conversations', JSON.stringify(conversations.value))
  }

  const createConversation = (title = 'New Chat') => {
    const conversation = {
      id: Date.now().toString(),
      title,
      messages: [],
      createdAt: new Date().toISOString()
    }
    conversations.value.unshift(conversation)
    currentConversation.value = conversation
    saveConversations()
    return conversation
  }

  const addMessage = (message) => {
    if (!currentConversation.value) {
      createConversation()
    }

    currentConversation.value.messages.push({
      id: Date.now().toString(),
      ...message,
      timestamp: new Date().toISOString()
    })

    // Update conversation title from first user message
    if (currentConversation.value.messages.length === 1 && message.role === 'user') {
      currentConversation.value.title = message.content.slice(0, 50) + '...'
    }

    saveConversations()
  }

  const sendMessage = async (messageContent) => {
    if (!currentConversation.value) {
      createConversation()
    }

    // Add user message to conversation
    const userMessage = {
      role: 'user',
      content: messageContent
    }
    addMessage(userMessage)

    isLoading.value = true
    error.value = null

    try {
      const profileStore = useProfileStore()
      const appStore = useAppStore()

      // Send message to backend with profile and language context
      const response = await chatAPI.sendMessage({
        message: messageContent,
        language: appStore.language || 'en',
        profile: profileStore.elderProfile || undefined
      })

      // Add AI response to conversation
      const aiMessage = {
        role: 'assistant',
        content: response.response || response.message || 'Sorry, I could not process that request.'
      }
      addMessage(aiMessage)

      return response
    } catch (err) {
      console.error('Chat error:', err)
      error.value = err.response?.data?.detail || 'Failed to send message'

      // Add error message
      const errorMessage = {
        role: 'assistant',
        content: `Sorry, I encountered an error: ${error.value}. Please try again.`
      }
      addMessage(errorMessage)

      throw err
    } finally {
      isLoading.value = false
    }
  }

  const setCurrentConversation = (conversationId) => {
    currentConversation.value = conversations.value.find(c => c.id === conversationId)
  }

  const deleteConversation = (conversationId) => {
    conversations.value = conversations.value.filter(c => c.id !== conversationId)
    if (currentConversation.value?.id === conversationId) {
      currentConversation.value = null
    }
    saveConversations()
  }

  return {
    conversations,
    currentConversation,
    isLoading,
    error,
    loadConversations,
    createConversation,
    addMessage,
    sendMessage,
    setCurrentConversation,
    deleteConversation
  }
})
