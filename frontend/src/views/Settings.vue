<template>
  <div class="settings-container">
    <header class="settings-header">
      <button @click="goBack" class="back-btn">← Back</button>
      <h1 class="header-title">Settings</h1>
      <div class="spacer"></div>
    </header>

    <div class="settings-content">
      <div class="settings-grid">
        <!-- Left Column -->
        <div class="settings-column">
          <!-- Language Settings -->
          <section class="settings-section">
        <h2 class="section-title">Language Preferences</h2>
        <div class="setting-item">
          <div class="setting-info">
            <div class="setting-label">Display Language</div>
            <div class="setting-description">Choose your preferred language</div>
          </div>
          <select v-model="appStore.language" @change="changeLanguage" class="setting-select">
            <option value="en">English</option>
            <option value="lg">Luganda</option>
            <option value="sw">Swahili</option>
          </select>
        </div>
      </section>

      <!-- Notifications Settings -->
      <section class="settings-section">
        <h2 class="section-title">Notifications</h2>
        <div class="setting-item">
          <div class="setting-info">
            <div class="setting-label">Push Notifications</div>
            <div class="setting-description">Receive reminders and tips</div>
          </div>
          <label class="toggle-switch">
            <input
              type="checkbox"
              v-model="appStore.notifications"
              @change="appStore.toggleNotifications"
            />
            <span class="toggle-slider"></span>
          </label>
        </div>
      </section>

      <!-- Connection Status -->
      <section class="settings-section">
        <h2 class="section-title">Connection</h2>
        <div class="setting-item">
          <div class="setting-info">
            <div class="setting-label">Network Status</div>
            <div class="setting-description">
              {{ isOnline ? 'Connected to the internet' : 'Offline mode' }}
            </div>
          </div>
          <div class="status-indicator" :class="{ online: isOnline, offline: !isOnline }">
            <Circle :size="20" :fill="isOnline ? '#10B981' : '#EF4444'" :stroke="isOnline ? '#10B981' : '#EF4444'" />
          </div>
        </div>
      </section>

      <!-- App Information -->
      <section class="settings-section">
        <h2 class="section-title">App Information</h2>
        <div class="info-item">
          <span class="info-label">Version</span>
          <span class="info-value">1.0.0</span>
        </div>
        <div class="info-item">
          <span class="info-label">Storage Used</span>
          <span class="info-value">{{ storageUsed }} KB</span>
        </div>
      </section>
        </div>

        <!-- Right Column -->
        <div class="settings-column">
          <!-- Help & Support -->
          <section class="settings-section">
        <h2 class="section-title">Help & Support</h2>
        <button @click="showFAQ" class="action-btn">
          <HelpCircle class="btn-icon" :size="20" />
          <span>FAQ</span>
          <span class="btn-arrow">→</span>
        </button>
        <button @click="sendFeedback" class="action-btn">
          <MessageCircle class="btn-icon" :size="20" />
          <span>Send Feedback</span>
          <span class="btn-arrow">→</span>
        </button>
      </section>

      <!-- Account Actions -->
      <section class="settings-section">
        <h2 class="section-title">Account</h2>
        <button @click="logout" class="action-btn danger">
          <LogOut class="btn-icon" :size="20" />
          <span>Log Out</span>
        </button>
        <button @click="deleteAccount" class="action-btn danger">
          <Trash2 class="btn-icon" :size="20" />
          <span>Delete Account</span>
        </button>
      </section>

      <!-- Data Management -->
      <section class="settings-section">
        <h2 class="section-title">Data Management</h2>
        <button @click="clearCache" class="action-btn">
          <Eraser class="btn-icon" :size="20" />
          <span>Clear Cache</span>
        </button>
        <button @click="clearConversations" class="action-btn">
          <MessageSquare class="btn-icon" :size="20" />
          <span>Clear All Conversations</span>
        </button>
      </section>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { useRouter } from 'vue-router'
import { useAppStore } from '../stores/app'
import { useAuthStore } from '../stores/auth'
import { useChatStore } from '../stores/chat'
import { useOnlineStatus } from '../composables/useOnlineStatus'
import { Circle, HelpCircle, MessageCircle, LogOut, Trash2, Eraser, MessageSquare } from 'lucide-vue-next'

const router = useRouter()
const appStore = useAppStore()
const authStore = useAuthStore()
const chatStore = useChatStore()
const { isOnline } = useOnlineStatus()

const storageUsed = computed(() => {
  let size = 0
  for (let key in localStorage) {
    if (localStorage.hasOwnProperty(key)) {
      size += localStorage[key].length + key.length
    }
  }
  return (size / 1024).toFixed(2)
})

const goBack = () => {
  router.push({ name: 'Chat' })
}

const changeLanguage = () => {
  alert('Language change will be implemented with i18n integration.')
}

const showFAQ = () => {
  alert('FAQ section will be added in a future update.')
}

const sendFeedback = () => {
  alert('Feedback form will be implemented with backend integration.')
}

const logout = () => {
  if (confirm('Are you sure you want to log out?')) {
    authStore.logout()
    router.push({ name: 'Auth' })
  }
}

const deleteAccount = () => {
  const confirmation = prompt(
    'This action cannot be undone. Type "DELETE" to confirm account deletion:'
  )

  if (confirmation === 'DELETE') {
    authStore.logout()
    localStorage.clear()
    router.push({ name: 'Auth' })
    alert('Your account has been deleted.')
  }
}

const clearCache = () => {
  if (confirm('Are you sure you want to clear the cache?')) {
    const authToken = localStorage.getItem('auth_token')
    const hasSeenIntro = localStorage.getItem('hasSeenIntro')

    localStorage.clear()

    if (authToken) localStorage.setItem('auth_token', authToken)
    if (hasSeenIntro) localStorage.setItem('hasSeenIntro', hasSeenIntro)

    alert('Cache cleared successfully!')
  }
}

const clearConversations = () => {
  if (confirm('Are you sure you want to delete all conversations? This cannot be undone.')) {
    chatStore.conversations = []
    chatStore.currentConversation = null
    chatStore.saveConversations()
    alert('All conversations have been deleted.')
  }
}
</script>

<style scoped>
.settings-container {
  min-height: 100vh;
  background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
}

.settings-header {
  background: white;
  border-bottom: 1px solid var(--color-gray-200);
  padding: 1rem 1.5rem;
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.back-btn {
  background: none;
  border: none;
  font-size: 1rem;
  font-weight: 600;
  color: var(--color-primary);
  cursor: pointer;
  transition: all 0.2s ease;
}

.back-btn:hover {
  color: #2d46b9;
}

.header-title {
  font-size: 1.25rem;
  font-weight: 700;
  color: #212529;
  margin: 0;
}

.spacer {
  width: 60px;
}

.settings-content {
  padding: 1.5rem;
  max-width: 1400px;
  margin: 0 auto;
}

.settings-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 2rem;
}

.settings-column {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.settings-section {
  background: white;
  border-radius: 20px;
  padding: 1.5rem;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.08);
  border: 1px solid rgba(217, 0, 0, 0.08);
  transition: all 0.3s ease;
}

.settings-section:hover {
  box-shadow: 0 15px 40px rgba(0, 0, 0, 0.12);
  transform: translateY(-2px);
}

.section-title {
  font-size: 1.125rem;
  font-weight: 700;
  background: linear-gradient(135deg, var(--color-primary) 0%, var(--color-secondary) 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  margin: 0 0 1rem 0;
  padding-bottom: 0.75rem;
  border-bottom: 2px solid var(--color-gray-100);
}

.setting-item {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 1rem 0;
}

.setting-info {
  flex: 1;
}

.setting-label {
  font-size: 1rem;
  font-weight: 600;
  color: #212529;
  margin-bottom: 0.25rem;
}

.setting-description {
  font-size: 0.875rem;
  color: #6c757d;
}

.setting-select {
  padding: 0.5rem 1rem;
  border: 2px solid var(--color-gray-200);
  border-radius: 8px;
  font-size: 0.875rem;
  background: white;
  cursor: pointer;
  transition: all 0.2s ease;
}

.setting-select:focus {
  outline: none;
  border-color: var(--color-primary);
}

.toggle-switch {
  position: relative;
  width: 52px;
  height: 28px;
  display: inline-block;
}

.toggle-switch input {
  opacity: 0;
  width: 0;
  height: 0;
}

.toggle-slider {
  position: absolute;
  cursor: pointer;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: linear-gradient(135deg, #ccc 0%, #aaa 100%);
  transition: 0.3s;
  border-radius: 28px;
}

.toggle-slider:before {
  position: absolute;
  content: "";
  height: 20px;
  width: 20px;
  left: 4px;
  bottom: 4px;
  background-color: white;
  transition: 0.3s;
  border-radius: 50%;
}

input:checked + .toggle-slider {
  background: linear-gradient(135deg, var(--color-primary) 0%, var(--color-secondary) 100%);
}

input:checked + .toggle-slider:before {
  transform: translateX(24px);
}

.status-indicator {
  font-size: 1.5rem;
}

.info-item {
  display: flex;
  justify-content: space-between;
  padding: 0.875rem 0;
  border-bottom: 1px solid var(--color-gray-50);
}

.info-item:last-child {
  border-bottom: none;
}

.info-label {
  font-size: 0.875rem;
  color: #6c757d;
}

.info-value {
  font-size: 0.875rem;
  font-weight: 600;
  color: #212529;
}

.action-btn {
  width: 100%;
  display: flex;
  align-items: center;
  gap: 1rem;
  padding: 1rem 1.25rem;
  border: 2px solid var(--color-gray-200);
  border-radius: 12px;
  background: linear-gradient(135deg, #ffffff 0%, #f8f9fa 100%);
  cursor: pointer;
  transition: all 0.3s ease;
  font-size: 1rem;
  margin-bottom: 0.75rem;
  font-weight: 500;
}

.action-btn:last-child {
  margin-bottom: 0;
}

.action-btn:hover {
  border-color: var(--color-primary);
  background: linear-gradient(135deg, #ffffff 0%, #fff5f5 100%);
  transform: translateX(8px);
  box-shadow: 0 5px 15px rgba(217, 0, 0, 0.1);
}

.action-btn.danger {
  border-color: #dc3545;
  color: #dc3545;
}

.action-btn.danger:hover {
  background: #fff5f5;
  border-color: #dc3545;
}

.btn-icon {
  font-size: 1.25rem;
}

.btn-arrow {
  margin-left: auto;
  color: #6c757d;
}

@media (max-width: 1024px) {
  .settings-grid {
    grid-template-columns: 1fr;
  }
}

@media (max-width: 768px) {
  .settings-content {
    padding: 1rem;
  }

  .settings-section {
    padding: 1rem;
  }

  .settings-grid {
    gap: 1.5rem;
  }
}
</style>
