import { defineStore } from 'pinia'
import { ref } from 'vue'

export const useChatStore = defineStore('chat', () => {
  const conversations = ref([])
  const currentConversation = ref(null)
  const isLoading = ref(false)

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
    loadConversations,
    createConversation,
    addMessage,
    setCurrentConversation,
    deleteConversation
  }
})
