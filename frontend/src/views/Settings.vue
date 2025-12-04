<template>
  <div class="settings-container">
    <header class="settings-header">
      <button @click="goBack" class="back-btn">← {{ $t('common.back') }}</button>
      <h1 class="header-title">{{ $t('settings.title') }}</h1>
      <div class="spacer"></div>
    </header>

    <div class="settings-content">
      <div class="settings-grid">
        <!-- Left Column -->
        <div class="settings-column">
          <!-- Language Settings -->
          <section class="settings-section">
        <h2 class="section-title">{{ $t('settings.language') }}</h2>
        <div class="setting-item">
          <div class="setting-info">
            <div class="setting-label">{{ $t('settings.displayLanguage') }}</div>
            <div class="setting-description">{{ $t('settings.chooseLanguage') }}</div>
          </div>
          <select v-model="appStore.language" @change="changeLanguage" class="setting-select">
            <option value="eng">English</option>
            <option value="lug">Luganda</option>
            <option value="nyn">Runyankole</option>
            <option value="ach">Acholi</option>
            <option value="teo">Ateso</option>
            <option value="lgg">Lugbara</option>
          </select>
        </div>
      </section>

      <!-- Notifications Settings -->
      <section class="settings-section">
        <h2 class="section-title">{{ $t('settings.notifications') }}</h2>
        <div class="setting-item">
          <div class="setting-info">
            <div class="setting-label">{{ $t('settings.pushNotifications') }}</div>
            <div class="setting-description">{{ $t('settings.receiveReminders') }}</div>
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
        <button @click="goToFAQ" class="action-btn">
          <HelpCircle class="btn-icon" :size="20" />
          <span>FAQ</span>
          <span class="btn-arrow">→</span>
        </button>
        <button @click="goToContact" class="action-btn">
          <Phone class="btn-icon" :size="20" />
          <span>Contact Us</span>
          <span class="btn-arrow">→</span>
        </button>
        <button @click="goToFeedback" class="action-btn">
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

    <!-- Delete Account Confirmation Modal -->
    <div v-if="showDeleteModal" class="modal-overlay" @click="showDeleteModal = false">
      <div class="modal-content delete-modal" @click.stop>
        <div class="modal-header">
          <Trash2 :size="48" class="modal-icon delete-icon" />
          <h3>Delete Account</h3>
        </div>
        <div class="modal-body">
          <p><strong>Warning:</strong> This action cannot be undone!</p>
          <p>All your data, conversations, and settings will be permanently deleted.</p>
          <div class="confirmation-input">
            <label for="deleteConfirm">Type <strong>DELETE</strong> to confirm:</label>
            <input
              v-model="deleteConfirmText"
              type="text"
              id="deleteConfirm"
              placeholder="DELETE"
              class="confirm-input"
            />
          </div>
        </div>
        <div class="modal-actions">
          <button
            @click="confirmDeleteAccount"
            class="btn btn-danger"
            :disabled="deleteConfirmText !== 'DELETE'"
          >
            Delete My Account
          </button>
          <button @click="closeDeleteModal" class="btn btn-secondary">Cancel</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed, ref } from 'vue'
import { useRouter } from 'vue-router'
import { useI18n } from 'vue-i18n'
import { useAppStore } from '../stores/app'
import { useAuthStore } from '../stores/auth'
import { useChatStore } from '../stores/chat'
import { useOnlineStatus } from '../composables/useOnlineStatus'
import { useModals } from '../composables/useModals'
import { Circle, HelpCircle, MessageCircle, LogOut, Trash2, Eraser, MessageSquare, Phone } from 'lucide-vue-next'

const { t: $t, locale } = useI18n()
const router = useRouter()
const appStore = useAppStore()
const authStore = useAuthStore()
const chatStore = useChatStore()
const { isOnline } = useOnlineStatus()
const { showAlert, showConfirm, showSuccess, showInfo } = useModals()

const showDeleteModal = ref(false)
const deleteConfirmText = ref('')

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

const changeLanguage = async () => {
  // Save language preference to localStorage
  localStorage.setItem('preferred_language', appStore.language)
  
  // Change the i18n locale
  locale.value = appStore.language
  
  const languageNames = {
    'eng': 'English',
    'lug': 'Luganda',
    'nyn': 'Runyankole',
    'ach': 'Acholi',
    'teo': 'Ateso',
    'lgg': 'Lugbara'
  }
  
  const selectedLang = languageNames[appStore.language] || appStore.language
  
  await showSuccess(
    $t('settings.languageUpdated'),
    $t('settings.languageUpdatedMsg') + ` (${selectedLang})`
  )
}

const goToFAQ = () => {
  router.push({ name: 'FAQ' })
}

const goToContact = () => {
  router.push({ name: 'ContactUs' })
}

const goToFeedback = () => {
  router.push({ name: 'SendFeedback' })
}

const logout = async () => {
  const confirmed = await showConfirm({
    title: 'Confirm Logout',
    message: 'Are you sure you want to log out of your account?',
    type: 'warning',
    confirmText: 'Logout',
    cancelText: 'Stay Logged In'
  })

  if (confirmed) {
    authStore.logout()
    router.push({ name: 'Auth' })
    showSuccess('Logged Out', 'You have been successfully logged out')
  }
}

const deleteAccount = () => {
  showDeleteModal.value = true
}

const confirmDeleteAccount = async () => {
  authStore.logout()
  localStorage.clear()
  router.push({ name: 'Auth' })
  await showAlert({
    title: 'Account Deleted',
    message: 'Your account has been permanently deleted.',
    type: 'success'
  })
}

const closeDeleteModal = () => {
  showDeleteModal.value = false
  deleteConfirmText.value = ''
}

const clearCache = async () => {
  const confirmed = await showConfirm({
    title: 'Clear Cache',
    message: 'Are you sure you want to clear the cache? Your login session will be preserved.',
    type: 'warning',
    confirmText: 'Clear Cache',
    cancelText: 'Cancel'
  })

  if (confirmed) {
    const authToken = localStorage.getItem('auth_token')
    const hasSeenIntro = localStorage.getItem('hasSeenIntro')

    localStorage.clear()

    if (authToken) localStorage.setItem('auth_token', authToken)
    if (hasSeenIntro) localStorage.setItem('hasSeenIntro', hasSeenIntro)

    showSuccess('Cache Cleared', 'Application cache has been cleared successfully')
  }
}

const clearConversations = async () => {
  const confirmed = await showConfirm({
    title: 'Delete All Conversations',
    message: 'Are you sure you want to delete all conversations? This action cannot be undone.',
    type: 'danger',
    confirmText: 'Delete All',
    cancelText: 'Cancel'
  })

  if (confirmed) {
    chatStore.conversations = []
    chatStore.currentConversation = null
    chatStore.saveConversations()
    showSuccess('Conversations Deleted', 'All conversations have been permanently deleted')
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

/* Modal Styles */
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
  z-index: 2000;
}

.modal-content {
  background: white;
  border-radius: 16px;
  padding: 2rem;
  max-width: 500px;
  width: 90%;
  margin: 1rem;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
}

.modal-header {
  text-align: center;
  margin-bottom: 1.5rem;
}

.modal-icon {
  margin-bottom: 1rem;
}

.delete-icon {
  color: #dc3545;
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
  color: var(--color-gray-700);
}

.confirmation-input {
  margin-top: 1.5rem;
}

.confirmation-input label {
  display: block;
  margin-bottom: 0.5rem;
  font-weight: 600;
  color: var(--color-dark);
}

.confirm-input {
  width: 100%;
  padding: 0.75rem 1rem;
  border: 2px solid var(--color-gray-300);
  border-radius: 8px;
  font-size: 1rem;
  transition: all 0.3s ease;
}

.confirm-input:focus {
  outline: none;
  border-color: #dc3545;
  box-shadow: 0 0 0 3px rgba(220, 53, 69, 0.1);
}

.modal-actions {
  display: flex;
  gap: 1rem;
  flex-direction: column;
}

.btn {
  padding: 1rem;
  border-radius: 10px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  border: none;
  font-size: 1rem;
}

.btn-danger {
  background: #dc3545;
  color: white;
}

.btn-danger:hover:not(:disabled) {
  background: #c82333;
  transform: translateY(-2px);
  box-shadow: 0 5px 15px rgba(220, 53, 69, 0.3);
}

.btn-danger:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.btn-secondary {
  background: var(--color-gray-200);
  color: var(--color-gray-700);
}

.btn-secondary:hover {
  background: var(--color-gray-300);
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

  .header-title {
    font-size: 1rem;
  }

  .setting-item {
    flex-direction: column;
    align-items: flex-start;
    gap: 1rem;
  }

  .setting-select {
    width: 100%;
  }
}
</style>
