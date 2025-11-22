<template>
  <div class="auth-container">
    <div class="auth-grid">
      <!-- Left Column - Branding -->
      <div class="branding-column">
        <div class="branding-content">
          <img src="/icons/logotransparent.svg" alt="Mzee Chakula" class="logo" />
          <h1 class="brand-title">Mzee Chakula</h1>
          <p class="brand-subtitle">Nourishing our Elders, Together</p>
          <p class="brand-description">
            AI-powered nutritional a/ssistant designed for elderly care in Uganda.
            Get personalized meal plans based on health conditions and locally available foods.
          </p>
        </div>
      </div>

      <!-- Right Column - Auth Form -->
      <div class="form-column">
        <div class="auth-card">
          <div class="header">
            <h2 class="title">{{ isSignUp ? 'Create Account' : 'Welcome Back' }}</h2>
            <p class="subtitle">{{ isSignUp ? 'Sign up to get started' : 'Sign in to continue' }}</p>
          </div>

          <div class="auth-methods">
            <button class="auth-btn google-btn" @click="handleGoogleAuth">
              <img src="/icons/google.png" alt="Google" class="google-icon" />
              <span>{{ isSignUp ? 'Google' : 'Google' }}</span>
            </button>

            <button class="auth-btn phone-btn" @click="handlePhoneAuth">
              <Smartphone class="btn-icon" :size="24" />
              <span>{{ isSignUp ? 'Phone' : 'Phone' }}</span>
            </button>
          </div>

          <div class="divider">
            <span>or</span>
          </div>

          <form @submit.prevent="handleEmailAuth" class="email-form">
            <div class="form-group" v-if="isSignUp">
              <label for="name">Name</label>
              <input
                v-model="formData.name"
                type="text"
                id="name"
                placeholder="Enter your name"
                required
              />
            </div>

            <div class="form-group">
              <label for="email">Email</label>
              <input
                v-model="formData.email"
                type="email"
                id="email"
                placeholder="Enter your email"
                required
              />
            </div>

            <div class="form-group">
              <label for="password">Password</label>
              <input
                v-model="formData.password"
                type="password"
                id="password"
                placeholder="Enter your password"
                required
              />
              <div class="forgot-password" v-if="!isSignUp">
                <a href="#" @click.prevent="showResetModal = true">Forgot Password?</a>
              </div>
            </div>

            <button type="submit" class="submit-btn" :disabled="loading">
              {{ loading ? 'Please wait...' : (isSignUp ? 'Sign Up' : 'Sign In') }}
            </button>
          </form>

          <!-- Reset Password Modal -->
          <div v-if="showResetModal" class="modal-overlay">
            <div class="modal-content">
              <h3>Reset Password</h3>
              <p>Enter your email to receive password reset instructions.</p>
              <form @submit.prevent="handleResetPassword">
                <div class="form-group">
                  <label for="reset-email">Email</label>
                  <input
                    v-model="resetEmail"
                    type="email"
                    id="reset-email"
                    placeholder="Enter your email"
                    required
                  />
                </div>
                <div class="modal-actions">
                  <button type="button" @click="showResetModal = false" class="cancel-btn">Cancel</button>
                  <button type="submit" class="submit-btn" :disabled="resetLoading">
                    {{ resetLoading ? 'Sending...' : 'Send Reset Link' }}
                  </button>
                </div>
              </form>
            </div>
          </div>

          <div class="toggle-mode">
            <p>
              {{ isSignUp ? 'Already have an account?' : "Don't have an account?" }}
              <button @click="toggleMode" class="toggle-btn">
                {{ isSignUp ? 'Sign In' : 'Sign Up' }}
              </button>
            </p>
          </div>

          <div v-if="!isOnline" class="offline-notice">
            <WifiOff class="offline-icon" :size="20" />
            You're offline. Sign in will be available when you're back online.
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../stores/auth'
import { useOnlineStatus } from '../composables/useOnlineStatus'
import { useModals } from '../composables/useModals'
import { Smartphone, WifiOff } from 'lucide-vue-next'

const router = useRouter()
const authStore = useAuthStore()
const { isOnline } = useOnlineStatus()
const { showAlert, showSuccess, showError, showInfo } = useModals()

const isSignUp = ref(false)
const loading = ref(false)

const formData = ref({
  name: '',
  email: '',
  password: ''
})

const showResetModal = ref(false)
const resetEmail = ref('')
const resetLoading = ref(false)

const handleResetPassword = async () => {
  resetLoading.value = true
  const result = await authStore.resetPassword(resetEmail.value)
  resetLoading.value = false

  if (result.success) {
    await showAlert({
      title: 'Reset Email Sent',
      message: 'If an account exists with this email, you will receive password reset instructions.',
      type: 'success'
    })
    showResetModal.value = false
    resetEmail.value = ''
  } else {
    showError('Reset Failed', result.error || 'Failed to send reset email. Please try again.')
  }
}

const toggleMode = () => {
  isSignUp.value = !isSignUp.value
  formData.value = { name: '', email: '', password: '' }
}

const handleEmailAuth = async () => {
  console.log('handleEmailAuth called', { isSignUp: isSignUp.value, formData: formData.value })
  loading.value = true

  let result
  if (isSignUp.value) {
    console.log('Calling authStore.register')
    result = await authStore.register(formData.value)
  } else {
    console.log('Calling authStore.login')
    result = await authStore.login(formData.value)
  }
  console.log('Auth result:', result)

  loading.value = false

  if (result.success) {
    if (isSignUp.value) {
      // Registration successful
      await showSuccess('Account Created', 'Your account has been created successfully! Please sign in.')
      isSignUp.value = false
      // Keep email filled, clear password
      formData.value.password = ''
    } else {
      // Login successful
      router.push({ name: 'Chat' })
    }
  } else {
    showError('Authentication Failed', result.error || 'Authentication failed. Please try again.')
  }
}

const handleGoogleAuth = async () => {
  await showInfo(
    'Coming Soon',
    'Google authentication will be available soon with backend integration.'
  )
}

const handlePhoneAuth = async () => {
  await showInfo(
    'Coming Soon',
    'Phone authentication will be available soon with backend integration.'
  )
}
</script>

<style scoped>
.auth-container {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: var(--color-white);
  width: 100%;
  overflow: hidden;
}

.auth-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  width: 100%;
  height: 100vh;
}

/* Left Column - Branding */
.branding-column {
  background: linear-gradient(135deg, var(--color-primary) 0%, var(--color-primary-dark) 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 3rem;
  position: relative;
  overflow: hidden;
}

.branding-column::before {
  content: '';
  position: absolute;
  top: -50%;
  right: -50%;
  width: 100%;
  height: 100%;
  background: radial-gradient(circle, rgba(252, 220, 4, 0.1) 0%, transparent 70%);
}

.branding-content {
  text-align: center;
  z-index: 1;
  max-width: 500px;
}

.logo {
  width: 180px;
  height: 180px;
  margin: 0 auto 2rem auto;
  display: block;
  filter: drop-shadow(0 10px 30px rgba(0, 0, 0, 0.3));
}

.brand-title {
  font-size: 3rem;
  font-weight: 800;
  color: var(--color-white);
  margin-bottom: 1rem;
  text-shadow: 0 4px 20px rgba(0, 0, 0, 0.3);
}

.brand-subtitle {
  font-size: 1.5rem;
  color: var(--color-secondary);
  margin-bottom: 2rem;
  font-weight: 600;
}

.brand-description {
  font-size: 1.125rem;
  color: rgba(255, 255, 255, 0.9);
  line-height: 1.8;
  text-shadow: 0 2px 10px rgba(0, 0, 0, 0.2);
}

/* Right Column - Form */
.form-column {
  background: var(--color-white);
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 2rem;
  overflow-y: auto;
}

.auth-card {
  width: 100%;
  max-width: 450px;
}

.header {
  text-align: center;
  margin-bottom: 2rem;
}

.title {
  font-size: 1.75rem;
  font-weight: 700;
  color: var(--color-dark);
  margin-bottom: 0.5rem;
}

.subtitle {
  font-size: 1rem;
  color: var(--color-gray-600);
}

.auth-methods {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1rem;
  margin-bottom: 1.5rem;
}

.auth-btn {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
  padding: 1rem 0.5rem;
  border-radius: 12px;
  font-size: 0.875rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  border: 2px solid var(--color-gray-300);
  background: var(--color-white);
  color: var(--color-dark);
}

.auth-btn:hover {
  border-color: var(--color-primary);
  transform: translateY(-2px);
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.1);
}

.btn-icon {
  color: var(--color-primary);
}

.google-icon {
  width: 24px;
  height: 24px;
  object-fit: contain;
}

.divider {
  text-align: center;
  margin: 1.5rem 0;
  position: relative;
}

.divider::before,
.divider::after {
  content: '';
  position: absolute;
  top: 50%;
  width: 40%;
  height: 1px;
  background: var(--color-gray-300);
}

.divider::before {
  left: 0;
}

.divider::after {
  right: 0;
}

.divider span {
  background: var(--color-white);
  padding: 0 1rem;
  color: var(--color-gray-500);
  font-size: 0.875rem;
}

.email-form {
  display: flex;
  flex-direction: column;
  gap: 1.25rem;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.form-group label {
  font-size: 0.875rem;
  font-weight: 600;
  color: var(--color-gray-700);
}

.form-group input {
  padding: 0.875rem 1rem;
  border: 2px solid var(--color-gray-300);
  border-radius: 10px;
  font-size: 1rem;
  transition: all 0.3s ease;
}

.form-group input:focus {
  outline: none;
  border-color: var(--color-primary);
  box-shadow: 0 0 0 3px rgba(217, 0, 0, 0.1);
}

.submit-btn {
  padding: 1rem;
  background: var(--color-primary);
  color: var(--color-white);
  border: none;
  border-radius: 12px;
  font-size: 1rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  margin-top: 0.5rem;
}

.submit-btn:hover:not(:disabled) {
  background: var(--color-primary-dark);
  transform: translateY(-2px);
  box-shadow: 0 5px 20px rgba(217, 0, 0, 0.3);
}

.submit-btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.toggle-mode {
  text-align: center;
  margin-top: 1.5rem;
  font-size: 0.875rem;
  color: var(--color-gray-600);
}

.toggle-btn {
  background: none;
  border: none;
  color: var(--color-primary);
  font-weight: 600;
  cursor: pointer;
  text-decoration: underline;
}

.offline-notice {
  margin-top: 1.5rem;
  padding: 1rem;
  background: #FFF3CD;
  border-radius: 10px;
  text-align: center;
  font-size: 0.875rem;
  color: #856404;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
}

.offline-icon {
  flex-shrink: 0;
}

/* Responsive */
@media (max-width: 1024px) {
  .auth-grid {
    grid-template-columns: 1fr;
  }

  .branding-column {
    display: none;
  }

  .form-column {
    padding: 2rem 1.5rem;
  }
}

@media (max-width: 480px) {
  .form-column {
    padding: 1.5rem 1rem;
  }

  .auth-card {
    max-width: 100%;
  }

  .title {
    font-size: 1.5rem;
  }

  .auth-methods {
    grid-template-columns: 1fr;
  }

  .auth-btn {
    flex-direction: row;
    font-size: 1rem;
    padding: 1rem;
  }
}

.forgot-password {
  text-align: right;
  margin-top: 0.25rem;
}

.forgot-password a {
  color: var(--color-primary);
  font-size: 0.875rem;
  text-decoration: none;
}

.forgot-password a:hover {
  text-decoration: underline;
}

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
  background: var(--color-white);
  padding: 2rem;
  border-radius: 12px;
  width: 90%;
  max-width: 400px;
  box-shadow: 0 10px 25px rgba(0, 0, 0, 0.2);
}

.modal-content h3 {
  margin-bottom: 1rem;
  color: var(--color-dark);
}

.modal-content p {
  margin-bottom: 1.5rem;
  color: var(--color-gray-600);
  font-size: 0.9rem;
}

.modal-actions {
  display: flex;
  gap: 1rem;
  margin-top: 1.5rem;
}

.cancel-btn {
  padding: 1rem;
  background: var(--color-gray-200);
  color: var(--color-dark);
  border: none;
  border-radius: 12px;
  font-size: 1rem;
  font-weight: 600;
  cursor: pointer;
  flex: 1;
}

.cancel-btn:hover {
  background: var(--color-gray-300);
}
</style>
