<template>
  <div class="auth-container">
    <div class="auth-card">
      <div class="header">
        <img src="/icons/logo.svg" alt="Mzee Chakula" class="logo" />
        <h1 class="title">{{ isSignUp ? 'Create Account' : 'Welcome Back' }}</h1>
        <p class="subtitle">{{ isSignUp ? 'Sign up to get started' : 'Sign in to continue' }}</p>
      </div>

      <div class="auth-methods">
        <button class="auth-btn google-btn" @click="handleGoogleAuth">
          <span class="btn-icon">🔐</span>
          {{ isSignUp ? 'Sign up with Google' : 'Sign in with Google' }}
        </button>

        <button class="auth-btn phone-btn" @click="handlePhoneAuth">
          <span class="btn-icon">📱</span>
          {{ isSignUp ? 'Sign up with Phone' : 'Sign in with Phone' }}
        </button>
      </div>

      <div class="divider">
        <span>or</span>
      </div>

      <form @submit.prevent="handleEmailAuth" class="email-form">
        <div class="form-group">
          <label for="name" v-if="isSignUp">Name</label>
          <input
            v-if="isSignUp"
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
        </div>

        <button type="submit" class="submit-btn" :disabled="loading">
          {{ loading ? 'Please wait...' : (isSignUp ? 'Sign Up' : 'Sign In') }}
        </button>
      </form>

      <div class="toggle-mode">
        <p>
          {{ isSignUp ? 'Already have an account?' : "Don't have an account?" }}
          <button @click="toggleMode" class="toggle-btn">
            {{ isSignUp ? 'Sign In' : 'Sign Up' }}
          </button>
        </p>
      </div>

      <div v-if="!isOnline" class="offline-notice">
        <span class="offline-icon">📡</span>
        You're offline. Sign in will be available when you're back online.
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../stores/auth'
import { useOnlineStatus } from '../composables/useOnlineStatus'

const router = useRouter()
const authStore = useAuthStore()
const { isOnline } = useOnlineStatus()

const isSignUp = ref(false)
const loading = ref(false)

const formData = ref({
  name: '',
  email: '',
  password: ''
})

const toggleMode = () => {
  isSignUp.value = !isSignUp.value
  formData.value = { name: '', email: '', password: '' }
}

const handleEmailAuth = async () => {
  loading.value = true

  const result = await authStore.login(formData.value)

  loading.value = false

  if (result.success) {
    router.push({ name: 'Chat' })
  } else {
    alert('Authentication failed. Please try again.')
  }
}

const handleGoogleAuth = () => {
  alert('Google authentication will be implemented with backend integration.')
}

const handlePhoneAuth = () => {
  alert('Phone authentication will be implemented with backend integration.')
}
</script>

<style scoped>
.auth-container {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 2rem 1.5rem;
  background: linear-gradient(135deg, #4361ee 0%, #4cc9f0 100%);
}

.auth-card {
  background: white;
  border-radius: 24px;
  padding: 2.5rem 2rem;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.2);
  width: 100%;
  max-width: 450px;
}

.header {
  text-align: center;
  margin-bottom: 2rem;
}

.logo {
  width: 80px;
  height: 80px;
  margin-bottom: 1rem;
}

.title {
  font-size: 1.75rem;
  font-weight: 700;
  color: #212529;
  margin-bottom: 0.5rem;
}

.subtitle {
  font-size: 1rem;
  color: #6c757d;
}

.auth-methods {
  display: flex;
  flex-direction: column;
  gap: 1rem;
  margin-bottom: 1.5rem;
}

.auth-btn {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.75rem;
  padding: 1rem;
  border-radius: 12px;
  font-size: 1rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  border: 2px solid #dee2e6;
  background: white;
  color: #212529;
}

.auth-btn:hover {
  border-color: #4361ee;
  transform: translateY(-2px);
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.1);
}

.btn-icon {
  font-size: 1.25rem;
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
  background: #dee2e6;
}

.divider::before {
  left: 0;
}

.divider::after {
  right: 0;
}

.divider span {
  background: white;
  padding: 0 1rem;
  color: #6c757d;
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
  color: #495057;
}

.form-group input {
  padding: 0.875rem 1rem;
  border: 2px solid #dee2e6;
  border-radius: 10px;
  font-size: 1rem;
  transition: all 0.3s ease;
}

.form-group input:focus {
  outline: none;
  border-color: #4361ee;
  box-shadow: 0 0 0 3px rgba(67, 97, 238, 0.1);
}

.submit-btn {
  padding: 1rem;
  background: linear-gradient(135deg, #4361ee 0%, #4cc9f0 100%);
  color: white;
  border: none;
  border-radius: 12px;
  font-size: 1rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  margin-top: 0.5rem;
}

.submit-btn:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 5px 20px rgba(67, 97, 238, 0.3);
}

.submit-btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.toggle-mode {
  text-align: center;
  margin-top: 1.5rem;
  font-size: 0.875rem;
  color: #6c757d;
}

.toggle-btn {
  background: none;
  border: none;
  color: #4361ee;
  font-weight: 600;
  cursor: pointer;
  text-decoration: underline;
}

.offline-notice {
  margin-top: 1.5rem;
  padding: 1rem;
  background: #fff3cd;
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
  font-size: 1.25rem;
}
</style>
