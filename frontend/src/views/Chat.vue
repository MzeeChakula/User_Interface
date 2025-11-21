<template>
  <div class="chat-container">
    <!-- Sidebar for chat history -->
    <aside class="sidebar" :class="{ open: sidebarOpen }">
      <div class="sidebar-header">
        <h2 class="sidebar-title">Chat History</h2>
        <button @click="toggleSidebar" class="close-btn mobile-only"><X :size="24" /></button>
      </div>

      <button @click="startNewChat" class="new-chat-btn">
        <Plus :size="20" /> New Chat
      </button>

      <div class="conversations-list">
        <div
          v-for="conv in chatStore.conversations"
          :key="conv.id"
          class="conversation-item"
          :class="{ active: chatStore.currentConversation?.id === conv.id }"
          @click="selectConversation(conv.id)"
        >
          <div class="conv-title">{{ conv.title }}</div>
          <div class="conv-date">{{ formatDate(conv.createdAt) }}</div>
        </div>

        <div v-if="chatStore.conversations.length === 0" class="empty-state">
          <p>No conversations yet</p>
        </div>
      </div>
    </aside>

    <!-- Main chat area -->
    <main class="chat-main">
      <header class="chat-header">
        <button @click="toggleSidebar" class="menu-btn mobile-only"><Menu :size="24" /></button>
        <h1 class="header-title">Mzee Chakula</h1>
        <div class="header-actions">
          <router-link to="/profile" class="icon-btn" title="Profile"><User :size="20" /></router-link>
          <router-link to="/settings" class="icon-btn" title="Settings"><Settings :size="20" /></router-link>
        </div>
      </header>

      <!-- Online/Offline status banner -->
      <div v-if="!isOnline" class="status-banner offline">
        <WifiOff :size="20" class="inline-icon" /> You're offline. Messages will be sent when you're back online.
      </div>

      <!-- Messages area -->
      <div class="messages-container" ref="messagesContainer">
        <div v-if="!chatStore.currentConversation || chatStore.currentConversation.messages.length === 0" class="welcome-section">
          <div class="welcome-icon"><Hand :size="64" /></div>
          <h2 class="welcome-title">Welcome to Mzee Chakula</h2>
          <p class="welcome-text">Ask me anything about nutritional planning for elderly care</p>

          <div class="prompt-suggestions">
            <button
              v-for="prompt in examplePrompts"
              :key="prompt"
              @click="usePrompt(prompt)"
              class="prompt-btn"
            >
              {{ prompt }}
            </button>
          </div>
        </div>

        <div
          v-for="message in chatStore.currentConversation?.messages"
          :key="message.id"
          class="message"
          :class="message.role"
        >
          <div class="message-content">{{ message.content }}</div>
          <div class="message-time">{{ formatTime(message.timestamp) }}</div>
        </div>

        <div v-if="chatStore.isLoading" class="message assistant">
          <div class="message-content typing">
            <span></span><span></span><span></span>
          </div>
        </div>
      </div>

      <!-- Input area -->
      <div class="input-area">
        <form @submit.prevent="sendMessage" class="input-form">
          <input
            v-model="messageInput"
            type="text"
            placeholder="Type your message..."
            class="message-input"
            :disabled="chatStore.isLoading"
          />
          <button
            type="submit"
            class="send-btn"
            :disabled="!messageInput.trim() || chatStore.isLoading"
          >
            <Send :size="20" />
          </button>
        </form>
      </div>
    </main>
  </div>
</template>

<script setup>
import { ref, nextTick, onMounted } from 'vue'
import { useChatStore } from '../stores/chat'
import { useOnlineStatus } from '../composables/useOnlineStatus'
import { X, Plus, Menu, User, Settings, WifiOff, Hand, Send } from 'lucide-vue-next'

const chatStore = useChatStore()
const { isOnline } = useOnlineStatus()

const sidebarOpen = ref(false)
const messageInput = ref('')
const messagesContainer = ref(null)

const examplePrompts = [
  'Create a weekly plan for diabetes',
  'What foods are affordable this week?',
  'Meal plan for someone with hypertension',
  'Low-sodium recipes with local ingredients'
]

onMounted(() => {
  chatStore.loadConversations()
})

const toggleSidebar = () => {
  sidebarOpen.value = !sidebarOpen.value
}

const startNewChat = () => {
  chatStore.createConversation()
  sidebarOpen.value = false
}

const selectConversation = (id) => {
  chatStore.setCurrentConversation(id)
  sidebarOpen.value = false
}

const usePrompt = (prompt) => {
  messageInput.value = prompt
  sendMessage()
}

const sendMessage = async () => {
  if (!messageInput.value.trim()) return

  const userMessage = {
    role: 'user',
    content: messageInput.value
  }

  chatStore.addMessage(userMessage)
  messageInput.value = ''

  await nextTick()
  scrollToBottom()

  // Simulate AI response
  chatStore.isLoading = true

  setTimeout(() => {
    const aiResponse = {
      role: 'assistant',
      content: 'This is a placeholder response. The AI backend will be integrated to provide actual nutritional advice based on your query.'
    }

    chatStore.addMessage(aiResponse)
    chatStore.isLoading = false

    nextTick(() => scrollToBottom())
  }, 1500)
}

const scrollToBottom = () => {
  if (messagesContainer.value) {
    messagesContainer.value.scrollTop = messagesContainer.value.scrollHeight
  }
}

const formatDate = (dateString) => {
  const date = new Date(dateString)
  const today = new Date()
  const yesterday = new Date(today)
  yesterday.setDate(yesterday.getDate() - 1)

  if (date.toDateString() === today.toDateString()) {
    return 'Today'
  } else if (date.toDateString() === yesterday.toDateString()) {
    return 'Yesterday'
  } else {
    return date.toLocaleDateString()
  }
}

const formatTime = (dateString) => {
  return new Date(dateString).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
}
</script>

<style scoped>
.chat-container {
  display: flex;
  height: 100vh;
  background: var(--color-gray-50);
}

/* Sidebar */
.sidebar {
  width: 280px;
  background: white;
  border-right: 1px solid var(--color-gray-200);
  display: flex;
  flex-direction: column;
  transition: transform 0.3s ease;
}

.sidebar-header {
  padding: 1.5rem;
  border-bottom: 1px solid var(--color-gray-200);
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.sidebar-title {
  font-size: 1.25rem;
  font-weight: 700;
  color: #212529;
  margin: 0;
}

.close-btn {
  background: none;
  border: none;
  font-size: 1.5rem;
  cursor: pointer;
  color: #6c757d;
  display: none;
}

.new-chat-btn {
  margin: 1rem;
  padding: 0.875rem;
  background: linear-gradient(135deg, var(--color-primary) 0%, var(--color-secondary) 100%);
  color: white;
  border: none;
  border-radius: 10px;
  font-weight: 600;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
  transition: all 0.3s ease;
}

.new-chat-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 5px 15px rgba(67, 97, 238, 0.3);
}

.conversations-list {
  flex: 1;
  overflow-y: auto;
  padding: 0.5rem;
}

.conversation-item {
  padding: 1rem;
  margin-bottom: 0.5rem;
  border-radius: 10px;
  cursor: pointer;
  transition: all 0.2s ease;
}

.conversation-item:hover {
  background: var(--color-gray-50);
}

.conversation-item.active {
  background: var(--color-gray-100);
  border-left: 3px solid var(--color-primary);
}

.conv-title {
  font-weight: 600;
  color: #212529;
  margin-bottom: 0.25rem;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.conv-date {
  font-size: 0.75rem;
  color: #6c757d;
}

.empty-state {
  text-align: center;
  padding: 2rem 1rem;
  color: #6c757d;
}

/* Main chat area */
.chat-main {
  flex: 1;
  display: flex;
  flex-direction: column;
  overflow: hidden;
}

.chat-header {
  background: white;
  border-bottom: 1px solid var(--color-gray-200);
  padding: 1rem 1.5rem;
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.menu-btn {
  background: none;
  border: none;
  font-size: 1.5rem;
  cursor: pointer;
  color: #212529;
  margin-right: 1rem;
  display: none;
}

.header-title {
  font-size: 1.25rem;
  font-weight: 700;
  color: var(--color-primary);
  margin: 0;
  flex: 1;
}

.header-actions {
  display: flex;
  gap: 0.75rem;
}

.icon-btn {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  background: var(--color-gray-50);
  text-decoration: none;
  font-size: 1.25rem;
  transition: all 0.2s ease;
}

.icon-btn:hover {
  background: #e9ecef;
  transform: scale(1.1);
}

.status-banner {
  padding: 0.75rem 1.5rem;
  text-align: center;
  font-size: 0.875rem;
  font-weight: 500;
}

.status-banner.offline {
  background: #fff3cd;
  color: #856404;
}

.inline-icon {
  display: inline-block;
  vertical-align: middle;
  margin-right: 0.5rem;
}

.messages-container {
  flex: 1;
  overflow-y: auto;
  padding: 2rem 1.5rem;
}

.welcome-section {
  text-align: center;
  max-width: 600px;
  margin: 4rem auto;
}

.welcome-icon {
  font-size: 4rem;
  margin-bottom: 1rem;
}

.welcome-title {
  font-size: 2rem;
  font-weight: 700;
  color: #212529;
  margin-bottom: 0.5rem;
}

.welcome-text {
  font-size: 1.125rem;
  color: #6c757d;
  margin-bottom: 2rem;
}

.prompt-suggestions {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 1rem;
}

.prompt-btn {
  padding: 1rem;
  background: white;
  border: 2px solid var(--color-gray-200);
  border-radius: 12px;
  font-size: 0.875rem;
  cursor: pointer;
  transition: all 0.3s ease;
  text-align: left;
}

.prompt-btn:hover {
  border-color: var(--color-primary);
  transform: translateY(-2px);
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.1);
}

.message {
  display: flex;
  flex-direction: column;
  margin-bottom: 1.5rem;
  max-width: 80%;
}

.message.user {
  align-self: flex-end;
  align-items: flex-end;
}

.message.assistant {
  align-self: flex-start;
  align-items: flex-start;
}

.message-content {
  padding: 1rem 1.25rem;
  border-radius: 18px;
  line-height: 1.5;
}

.message.user .message-content {
  background: linear-gradient(135deg, var(--color-primary) 0%, var(--color-secondary) 100%);
  color: white;
}

.message.assistant .message-content {
  background: white;
  color: #212529;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
}

.message-time {
  font-size: 0.75rem;
  color: #6c757d;
  margin-top: 0.25rem;
  padding: 0 0.5rem;
}

.typing {
  display: flex;
  gap: 0.5rem;
  padding: 1rem 1.5rem !important;
}

.typing span {
  width: 8px;
  height: 8px;
  background: #6c757d;
  border-radius: 50%;
  animation: typing 1.4s infinite;
}

.typing span:nth-child(2) {
  animation-delay: 0.2s;
}

.typing span:nth-child(3) {
  animation-delay: 0.4s;
}

@keyframes typing {
  0%, 60%, 100% {
    transform: translateY(0);
  }
  30% {
    transform: translateY(-10px);
  }
}

.input-area {
  background: white;
  border-top: 1px solid var(--color-gray-200);
  padding: 1.5rem;
}

.input-form {
  display: flex;
  gap: 1rem;
  max-width: 1000px;
  margin: 0 auto;
}

.message-input {
  flex: 1;
  padding: 1rem 1.25rem;
  border: 2px solid var(--color-gray-200);
  border-radius: 24px;
  font-size: 1rem;
  transition: all 0.3s ease;
}

.message-input:focus {
  outline: none;
  border-color: var(--color-primary);
  box-shadow: 0 0 0 3px rgba(67, 97, 238, 0.1);
}

.send-btn {
  width: 50px;
  height: 50px;
  border-radius: 50%;
  background: linear-gradient(135deg, var(--color-primary) 0%, var(--color-secondary) 100%);
  border: none;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.3s ease;
}

.send-btn:hover:not(:disabled) {
  transform: scale(1.1);
  box-shadow: 0 5px 15px rgba(67, 97, 238, 0.3);
}

.send-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.send-icon {
  font-size: 1.25rem;
}

/* Mobile styles */
@media (max-width: 768px) {
  .sidebar {
    position: fixed;
    left: 0;
    top: 0;
    height: 100vh;
    z-index: 1000;
    transform: translateX(-100%);
  }

  .sidebar.open {
    transform: translateX(0);
  }

  .mobile-only {
    display: block !important;
  }

  .menu-btn {
    display: block !important;
  }

  .message {
    max-width: 90%;
  }

  .welcome-section {
    margin: 2rem auto;
  }

  .prompt-suggestions {
    grid-template-columns: 1fr;
  }
}
</style>
