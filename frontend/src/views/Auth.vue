<template>
  <div class="auth-container">
    <div class="auth-card">
      <div class="header">
        <img src="/icons/logotransparent.svg" alt="Mzee Chakula" class="logo" />
        <h1 class="title">{{ isSignUp ? 'Create Account' : 'Welcome Back' }}</h1>
        <p class="subtitle">{{ isSignUp ? 'Sign up to get started' : 'Sign in to continue' }}</p>
      </div>

      <div class="auth-methods">
        <button class="auth-btn google-btn" @click="handleGoogleAuth">
          <Lock class="btn-icon" :size="20" />
          {{ isSignUp ? 'Sign up with Google' : 'Sign in with Google' }}
        </button>

        <button class="auth-btn phone-btn" @click="handlePhoneAuth">
          <Smartphone class="btn-icon" :size="20" />
          {{ isSignUp ? 'Sign up with Phone' : 'Sign in with Phone' }}
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
        <WifiOff class="offline-icon" :size="20" />
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
import { Lock, Smartphone, WifiOff } from 'lucide-vue-next'

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
  background: linear-gradient(135deg, var(--color-primary) 0%, var(--color-primary-dark) 100%);
  width: 100%;
}

.auth-card {
  background: var(--color-white);
  border-radius: 24px;
  padding: 2.5rem 2rem;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
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
  color: var(--color-dark);
  margin-bottom: 0.5rem;
}

.subtitle {
  font-size: 1rem;
  color: var(--color-gray-600);
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
  background: var(--color-warning);
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
  font-size: 1.25rem;
}

@media (max-width: 768px) {
  .auth-container {
    padding: 1.5rem 1rem;
  }

  .auth-card {
    padding: 2rem 1.5rem;
  }

  .logo {
    width: 70px;
    height: 70px;
  }

  .title {
    font-size: 1.5rem;
  }
}

@media (max-width: 480px) {
  .auth-card {
    padding: 1.5rem 1rem;
  }

  .header {
    margin-bottom: 1.5rem;
  }
}
</style>
