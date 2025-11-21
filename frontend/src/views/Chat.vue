<template>
  <div class="chat-container">
    <!-- Sidebar for chat history -->
    <aside class="sidebar" :class="{ open: sidebarOpen }">
      <div class="sidebar-header">
        <div class="app-brand">
          <img src="/icons/logotransparent.svg" alt="Logo" class="brand-icon" />
          <h2 class="sidebar-title">Mzee Chakula</h2>
        </div>
        <button @click="toggleSidebar" class="close-btn mobile-only"><X :size="24" /></button>
      </div>

      <button @click="startNewChat" class="new-chat-btn">
        <Plus :size="20" /> New Chat
      </button>

      <!-- Language Selector -->
      <div class="language-selector">
        <Globe :size="18" />
        <select v-model="selectedLanguage" @change="changeLanguage" class="language-select">
          <option value="en">English</option>
          <option value="lg">Luganda</option>
          <option value="sw">Swahili</option>
        </select>
      </div>

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

      <!-- Help & Support Section -->
      <div class="help-section">
        <button @click="toggleHelpDropdown" class="help-header">
          <div class="help-header-content">
            <HelpCircle :size="18" />
            <span>Help & Support</span>
          </div>
          <ChevronDown :size="18" :class="['chevron', { rotated: helpDropdownOpen }]" />
        </button>
        <transition name="dropdown">
          <div v-if="helpDropdownOpen" class="help-links">
            <router-link to="/faq" class="help-link" @click="sidebarOpen = false">
              <MessageSquare :size="16" />
              <span>FAQ</span>
            </router-link>
            <router-link to="/contact-us" class="help-link" @click="sidebarOpen = false">
              <Phone :size="16" />
              <span>Contact Us</span>
            </router-link>
            <router-link to="/send-feedback" class="help-link" @click="sidebarOpen = false">
              <Send :size="16" />
              <span>Send Feedback</span>
            </router-link>
          </div>
        </transition>
      </div>

      <!-- Logout Button -->
      <button @click="handleLogout" class="logout-btn">
        <LogOut :size="20" />
        <span>Logout</span>
      </button>
    </aside>

    <!-- Main chat area -->
    <main class="chat-main">
      <header class="chat-header">
        <button @click="toggleSidebar" class="menu-btn mobile-only"><Menu :size="24" /></button>
        <h1 class="header-title">Graph-Enhanced LLMs for Locally Sourced Elderly Nutrition Planning in Uganda</h1>
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
          <button type="button" @click="openFileUpload" class="input-action-btn" title="Upload Document">
            <Upload :size="20" />
          </button>

          <input
            v-model="messageInput"
            type="text"
            placeholder="Type your message..."
            class="message-input"
            :disabled="chatStore.isLoading"
          />

          <button
            type="button"
            @click="toggleVoiceInput"
            class="input-action-btn voice-btn"
            :class="{ active: isRecording }"
            title="Voice Input"
          >
            <Mic :size="20" v-if="!isRecording" />
            <MicOff :size="20" v-else />
          </button>

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

    <!-- Document Upload Warning Modal -->
    <div v-if="showUploadWarning" class="modal-overlay" @click="showUploadWarning = false">
      <div class="modal-content" @click.stop>
        <div class="modal-header">
          <AlertTriangle :size="48" class="warning-icon" />
          <h3>Document Upload Warning</h3>
        </div>
        <div class="modal-body">
          <p><strong>Important:</strong> Please do not upload documents containing sensitive personal information such as:</p>
          <ul>
            <li>National ID numbers or passports</li>
            <li>Financial information (bank accounts, credit cards)</li>
            <li>Private medical records with identifying details</li>
            <li>Any confidential personal data</li>
          </ul>
          <p>We use RAG (Retrieval-Augmented Generation) to process your documents for better recommendations, but we prioritize your privacy and security.</p>
        </div>
        <div class="modal-actions">
          <button @click="proceedWithUpload" class="btn btn-primary">I Understand, Continue</button>
          <button @click="showUploadWarning = false" class="btn btn-secondary">Cancel</button>
        </div>
      </div>
    </div>

    <!-- Hidden file input -->
    <input
      ref="fileInput"
      type="file"
      @change="handleFileUpload"
      accept=".pdf,.doc,.docx,.txt"
      style="display: none"
    />
  </div>
</template>

<script setup>
import { ref, nextTick, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useChatStore } from '../stores/chat'
import { useAuthStore } from '../stores/auth'
import { useAppStore } from '../stores/app'
import { useOnlineStatus } from '../composables/useOnlineStatus'
import {
  X, Plus, Menu, User, Settings, WifiOff, Hand, Send,
  LogOut, Globe, Upload, Mic, MicOff, AlertTriangle,
  HelpCircle, MessageSquare, Phone, ChevronDown
} from 'lucide-vue-next'

const router = useRouter()
const chatStore = useChatStore()
const authStore = useAuthStore()
const appStore = useAppStore()
const { isOnline } = useOnlineStatus()

const sidebarOpen = ref(false)
const messageInput = ref('')
const messagesContainer = ref(null)
const selectedLanguage = ref(appStore.language)
const isRecording = ref(false)
const showUploadWarning = ref(false)
const fileInput = ref(null)
const helpDropdownOpen = ref(false)

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

const toggleHelpDropdown = () => {
  helpDropdownOpen.value = !helpDropdownOpen.value
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

const changeLanguage = () => {
  appStore.setLanguage(selectedLanguage.value)
  // TODO: Implement actual language change with i18n
  alert(`Language changed to: ${selectedLanguage.value}. Full translation coming soon!`)
}

const handleLogout = () => {
  if (confirm('Are you sure you want to logout?')) {
    authStore.logout()
    router.push({ name: 'Auth' })
  }
}

const toggleVoiceInput = () => {
  if (!isRecording.value) {
    // Start recording
    isRecording.value = true
    // TODO: Implement actual voice recording
    alert('Voice input will be implemented with speech recognition API')
    setTimeout(() => {
      isRecording.value = false
    }, 3000)
  } else {
    // Stop recording
    isRecording.value = false
  }
}

const openFileUpload = () => {
  showUploadWarning.value = true
}

const proceedWithUpload = () => {
  showUploadWarning.value = false
  fileInput.value?.click()
}

const handleFileUpload = (event) => {
  const file = event.target.files[0]
  if (file) {
    // TODO: Implement actual file upload and RAG processing
    alert(`File "${file.name}" will be processed with RAG for better recommendations.`)
    // Reset file input
    event.target.value = ''
  }
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
  padding: 1rem 1.5rem;
  border-bottom: 1px solid var(--color-gray-200);
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.app-brand {
  display: flex;
  align-items: center;
  gap: 0.75rem;
}

.brand-icon {
  width: 32px;
  height: 32px;
}

.sidebar-title {
  font-size: 1.125rem;
  font-weight: 700;
  color: var(--color-primary);
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
  box-shadow: 0 5px 15px rgba(217, 0, 0, 0.3);
}

.language-selector {
  margin: 0 1rem 1rem 1rem;
  padding: 0.75rem;
  background: var(--color-gray-50);
  border-radius: 10px;
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.language-selector svg {
  color: var(--color-primary);
}

.language-select {
  flex: 1;
  border: none;
  background: transparent;
  font-size: 0.875rem;
  font-weight: 600;
  color: var(--color-dark);
  cursor: pointer;
}

.language-select:focus {
  outline: none;
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

.help-section {
  margin: 0 1rem 1rem 1rem;
  background: var(--color-gray-50);
  border-radius: 12px;
  border: 2px solid var(--color-gray-200);
  overflow: hidden;
}

.help-header {
  width: 100%;
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 1rem;
  background: transparent;
  border: none;
  cursor: pointer;
  transition: all 0.3s ease;
}

.help-header:hover {
  background: var(--color-white);
}

.help-header-content {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 0.875rem;
  font-weight: 700;
  color: var(--color-dark);
}

.help-header-content svg {
  color: var(--color-primary);
}

.chevron {
  color: var(--color-gray-500);
  transition: transform 0.3s ease;
}

.chevron.rotated {
  transform: rotate(180deg);
}

.help-links {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
  padding: 0 1rem 1rem 1rem;
}

.help-link {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  padding: 0.75rem;
  background: var(--color-white);
  border-radius: 8px;
  text-decoration: none;
  color: var(--color-gray-700);
  font-size: 0.875rem;
  font-weight: 600;
  transition: all 0.3s ease;
  border: 1px solid transparent;
}

.help-link:hover {
  background: var(--color-white);
  border-color: var(--color-primary);
  color: var(--color-primary);
  transform: translateX(5px);
}

.help-link svg {
  flex-shrink: 0;
  color: var(--color-primary);
}

.logout-btn {
  margin: 1rem;
  padding: 0.875rem;
  background: white;
  border: 2px solid var(--color-gray-200);
  border-radius: 10px;
  font-weight: 600;
  color: var(--color-gray-700);
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
  transition: all 0.3s ease;
}

.logout-btn:hover {
  border-color: var(--color-primary);
  color: var(--color-primary);
  transform: translateY(-2px);
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
  color: var(--color-dark);
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
  transition: all 0.2s ease;
  color: var(--color-dark);
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
  margin-bottom: 1rem;
  color: var(--color-primary);
  display: flex;
  justify-content: center;
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
  gap: 0.75rem;
  max-width: 1000px;
  margin: 0 auto;
  align-items: center;
}

.input-action-btn {
  width: 44px;
  height: 44px;
  border-radius: 50%;
  background: var(--color-gray-100);
  border: none;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.3s ease;
  color: var(--color-gray-600);
}

.input-action-btn:hover {
  background: var(--color-gray-200);
  color: var(--color-primary);
  transform: scale(1.1);
}

.input-action-btn.voice-btn.active {
  background: var(--color-primary);
  color: white;
  animation: pulse 1.5s infinite;
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
  box-shadow: 0 0 0 3px rgba(217, 0, 0, 0.1);
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
  color: white;
}

.send-btn:hover:not(:disabled) {
  transform: scale(1.1);
  box-shadow: 0 5px 15px rgba(217, 0, 0, 0.3);
}

.send-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

/* Modal */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
}

.modal-content {
  background: white;
  border-radius: 16px;
  padding: 2rem;
  max-width: 500px;
  margin: 1rem;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
}

.modal-header {
  text-align: center;
  margin-bottom: 1.5rem;
}

.warning-icon {
  color: #F59E0B;
  margin-bottom: 1rem;
}

.modal-header h3 {
  font-size: 1.5rem;
  font-weight: 700;
  color: var(--color-dark);
}

.modal-body {
  margin-bottom: 2rem;
}

.modal-body p {
  margin-bottom: 1rem;
  line-height: 1.6;
}

.modal-body ul {
  margin-left: 1.5rem;
  margin-bottom: 1rem;
}

.modal-body li {
  margin-bottom: 0.5rem;
  color: var(--color-gray-700);
}

.modal-actions {
  display: flex;
  gap: 1rem;
}

.btn {
  flex: 1;
  padding: 1rem;
  border-radius: 10px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  border: none;
}

.btn-primary {
  background: var(--color-primary);
  color: white;
}

.btn-primary:hover {
  background: var(--color-primary-dark);
  transform: translateY(-2px);
}

.btn-secondary {
  background: var(--color-gray-200);
  color: var(--color-gray-700);
}

.btn-secondary:hover {
  background: var(--color-gray-300);
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

  .input-form {
    gap: 0.5rem;
  }

  .input-action-btn {
    width: 40px;
    height: 40px;
  }
}

/* Dropdown Animation */
.dropdown-enter-active,
.dropdown-leave-active {
  transition: all 0.3s ease;
  overflow: hidden;
}

.dropdown-enter-from,
.dropdown-leave-to {
  opacity: 0;
  max-height: 0;
  padding: 0 1rem;
}

.dropdown-enter-to,
.dropdown-leave-from {
  opacity: 1;
  max-height: 300px;
  padding: 0 1rem 1rem 1rem;
}
</style>
