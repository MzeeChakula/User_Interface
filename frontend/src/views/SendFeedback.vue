<template>
  <div class="feedback-container">
    <div class="top-nav">
      <button @click="goBack" class="back-btn">
        <ArrowLeft :size="20" />
        <span>Back</span>
      </button>
      <button @click="goHome" class="home-btn">
        <Home :size="20" />
        <span>Home</span>
      </button>
    </div>

    <div class="feedback-header">
      <div class="header-content">
        <MessageSquare :size="64" class="header-icon" />
        <h1 class="title">Send Us Your Feedback</h1>
        <p class="subtitle">We'd love to hear your thoughts, suggestions, or concerns</p>
      </div>
    </div>

    <div class="feedback-content">
      <div class="form-card">
        <form @submit.prevent="handleSubmit" class="feedback-form">
          <div class="form-group">
            <label for="name">Your Name</label>
            <input
              v-model="formData.name"
              type="text"
              id="name"
              placeholder="Enter your name"
              required
            />
          </div>

          <div class="form-group">
            <label for="email">Email Address</label>
            <input
              v-model="formData.email"
              type="email"
              id="email"
              placeholder="your.email@example.com"
              required
            />
          </div>

          <div class="form-group">
            <label for="category">Feedback Category</label>
            <select v-model="formData.category" id="category" required>
              <option value="">Select a category</option>
              <option value="bug">Bug Report</option>
              <option value="feature">Feature Request</option>
              <option value="improvement">Improvement Suggestion</option>
              <option value="general">General Feedback</option>
              <option value="other">Other</option>
            </select>
          </div>

          <div class="form-group">
            <label for="rating">Rate Your Experience</label>
            <div class="rating-container">
              <button
                v-for="star in 5"
                :key="star"
                type="button"
                @click="formData.rating = star"
                class="star-btn"
              >
                <Star
                  :size="32"
                  :class="['star-icon', { filled: star <= formData.rating }]"
                  :fill="star <= formData.rating ? 'currentColor' : 'none'"
                />
              </button>
            </div>
            <span class="rating-text">{{ getRatingText() }}</span>
          </div>

          <div class="form-group">
            <label for="subject">Subject</label>
            <input
              v-model="formData.subject"
              type="text"
              id="subject"
              placeholder="Brief description of your feedback"
              required
            />
          </div>

          <div class="form-group">
            <label for="message">Your Message</label>
            <textarea
              v-model="formData.message"
              id="message"
              rows="6"
              placeholder="Please provide detailed feedback..."
              required
            ></textarea>
            <span class="character-count">{{ formData.message.length }} / 1000</span>
          </div>

          <div class="form-actions">
            <button type="submit" class="submit-btn" :disabled="loading">
              <Send :size="20" class="btn-icon" v-if="!loading" />
              <span>{{ loading ? 'Sending...' : 'Send Feedback' }}</span>
            </button>
            <button type="button" @click="resetForm" class="reset-btn">
              Reset Form
            </button>
          </div>
        </form>

        <div v-if="showSuccess" class="success-message">
          <CheckCircle2 :size="48" class="success-icon" />
          <h3>Thank You!</h3>
          <p>Your feedback has been successfully submitted. We'll review it and get back to you soon.</p>
        </div>
      </div>

      <div class="info-cards">
        <div class="info-card">
          <Lightbulb :size="32" class="card-icon" />
          <h3>Suggest a Feature</h3>
          <p>Have an idea to make Mzee Chakula better? We're always looking to improve!</p>
        </div>

        <div class="info-card">
          <Bug :size="32" class="card-icon" />
          <h3>Report a Bug</h3>
          <p>Found something not working right? Let us know so we can fix it quickly.</p>
        </div>

        <div class="info-card">
          <Heart :size="32" class="card-icon" />
          <h3>Share Your Experience</h3>
          <p>Love using Mzee Chakula? We'd love to hear about your positive experience!</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { MessageSquare, Send, Star, CheckCircle2, Lightbulb, Bug, Heart, ArrowLeft, Home } from 'lucide-vue-next'

const router = useRouter()

const loading = ref(false)
const showSuccess = ref(false)

const formData = ref({
  name: '',
  email: '',
  category: '',
  rating: 0,
  subject: '',
  message: ''
})

const getRatingText = () => {
  const texts = ['', 'Poor', 'Fair', 'Good', 'Very Good', 'Excellent']
  return texts[formData.value.rating] || 'Select a rating'
}

const handleSubmit = async () => {
  loading.value = true
  showSuccess.value = false

  // Simulate API call
  setTimeout(() => {
    loading.value = false
    showSuccess.value = true

    // Hide success message and reset form after 5 seconds
    setTimeout(() => {
      showSuccess.value = false
      resetForm()
    }, 5000)
  }, 1500)
}

const resetForm = () => {
  formData.value = {
    name: '',
    email: '',
    category: '',
    rating: 0,
    subject: '',
    message: ''
  }
}

const goBack = () => {
  router.back()
}

const goHome = () => {
  router.push({ name: 'Chat' })
}
</script>

<style scoped>
.feedback-container {
  min-height: 100vh;
  background: var(--color-gray-50);
}

.top-nav {
  background: var(--color-white);
  padding: 1rem 2rem;
  display: flex;
  gap: 1rem;
  align-items: center;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.05);
}

.back-btn,
.home-btn {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.625rem 1.25rem;
  border: 2px solid var(--color-gray-300);
  background: var(--color-white);
  color: var(--color-dark);
  border-radius: 8px;
  font-size: 0.938rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
}

.back-btn:hover,
.home-btn:hover {
  border-color: var(--color-primary);
  color: var(--color-primary);
  transform: translateY(-2px);
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.1);
}

.feedback-header {
  background: linear-gradient(135deg, var(--color-primary) 0%, var(--color-primary-dark) 100%);
  padding: 4rem 2rem 3rem;
  text-align: center;
  position: relative;
  overflow: hidden;
}

.feedback-header::before {
  content: '';
  position: absolute;
  top: -50%;
  left: -10%;
  width: 60%;
  height: 200%;
  background: radial-gradient(circle, rgba(252, 220, 4, 0.1) 0%, transparent 70%);
}

.header-content {
  max-width: 800px;
  margin: 0 auto;
  position: relative;
  z-index: 1;
}

.header-icon {
  color: var(--color-secondary);
  margin: 0 auto 1rem;
}

.title {
  font-size: 2.5rem;
  font-weight: 800;
  color: var(--color-white);
  margin-bottom: 1rem;
  text-shadow: 0 2px 10px rgba(0, 0, 0, 0.2);
}

.subtitle {
  font-size: 1.25rem;
  color: rgba(255, 255, 255, 0.95);
  font-weight: 500;
}

.feedback-content {
  max-width: 1200px;
  margin: -2rem auto 0;
  padding: 0 1rem 4rem;
  position: relative;
  z-index: 2;
}

.form-card {
  background: var(--color-white);
  border-radius: 16px;
  padding: 3rem;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
  margin-bottom: 3rem;
  position: relative;
}

.feedback-form {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
  position: relative;
}

.form-group label {
  font-size: 0.875rem;
  font-weight: 600;
  color: var(--color-gray-700);
}

.form-group input,
.form-group select,
.form-group textarea {
  padding: 0.875rem 1rem;
  border: 2px solid var(--color-gray-300);
  border-radius: 10px;
  font-size: 1rem;
  font-family: inherit;
  transition: all 0.3s ease;
  background: var(--color-white);
}

.form-group input:focus,
.form-group select:focus,
.form-group textarea:focus {
  outline: none;
  border-color: var(--color-primary);
  box-shadow: 0 0 0 3px rgba(217, 0, 0, 0.1);
}

.form-group textarea {
  resize: vertical;
  min-height: 150px;
}

.character-count {
  font-size: 0.75rem;
  color: var(--color-gray-500);
  text-align: right;
}

.rating-container {
  display: flex;
  gap: 0.5rem;
  margin-bottom: 0.5rem;
}

.star-btn {
  background: none;
  border: none;
  padding: 0;
  cursor: pointer;
  transition: transform 0.2s ease;
}

.star-btn:hover {
  transform: scale(1.2);
}

.star-icon {
  color: var(--color-gray-300);
  transition: all 0.2s ease;
}

.star-icon.filled {
  color: var(--color-secondary);
}

.rating-text {
  font-size: 0.875rem;
  color: var(--color-gray-600);
  font-weight: 600;
}

.form-actions {
  display: flex;
  gap: 1rem;
  margin-top: 1rem;
}

.submit-btn,
.reset-btn {
  padding: 1rem 2rem;
  border-radius: 10px;
  font-size: 1rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
}

.submit-btn {
  background: var(--color-primary);
  color: var(--color-white);
  border: none;
  flex: 1;
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

.reset-btn {
  background: var(--color-white);
  color: var(--color-gray-700);
  border: 2px solid var(--color-gray-300);
}

.reset-btn:hover {
  border-color: var(--color-gray-400);
  background: var(--color-gray-50);
}

.success-message {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: var(--color-white);
  border-radius: 16px;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  text-align: center;
  padding: 3rem;
  animation: fadeIn 0.5s ease;
}

.success-icon {
  color: var(--color-success);
  margin-bottom: 1.5rem;
}

.success-message h3 {
  font-size: 1.75rem;
  font-weight: 700;
  color: var(--color-dark);
  margin-bottom: 0.75rem;
}

.success-message p {
  font-size: 1.125rem;
  color: var(--color-gray-600);
  max-width: 500px;
}

.info-cards {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 1.5rem;
}

.info-card {
  background: var(--color-white);
  padding: 2rem;
  border-radius: 12px;
  text-align: center;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.05);
  transition: all 0.3s ease;
}

.info-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 8px 25px rgba(0, 0, 0, 0.1);
}

.card-icon {
  color: var(--color-primary);
  margin: 0 auto 1rem;
}

.info-card h3 {
  font-size: 1.25rem;
  font-weight: 700;
  color: var(--color-dark);
  margin-bottom: 0.75rem;
}

.info-card p {
  font-size: 0.938rem;
  color: var(--color-gray-600);
  line-height: 1.6;
}

@keyframes fadeIn {
  from {
    opacity: 0;
  }
  to {
    opacity: 1;
  }
}

@media (max-width: 768px) {
  .title {
    font-size: 2rem;
  }

  .subtitle {
    font-size: 1rem;
  }

  .form-card {
    padding: 2rem 1.5rem;
  }

  .feedback-content {
    padding: 0 1rem 2rem;
  }

  .form-actions {
    flex-direction: column;
  }

  .info-cards {
    grid-template-columns: 1fr;
  }
}
</style>
