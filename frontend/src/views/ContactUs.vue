<template>
  <div class="contact-container">
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

    <div class="contact-header">
      <div class="header-content">
        <Phone :size="64" class="header-icon" />
        <h1 class="title">Get in Touch</h1>
        <p class="subtitle">We're here to help and answer any questions you might have</p>
      </div>
    </div>

    <div class="contact-content">
      <div class="contact-grid">
        <!-- Contact Information Cards -->
        <div class="contact-cards">
          <div class="contact-card">
            <div class="card-icon-wrapper primary">
              <Mail :size="32" class="card-icon" />
            </div>
            <h3>Email Us</h3>
            <p class="card-detail">support@mzeechakula.ug</p>
            <p class="card-detail">info@mzeechakula.ug</p>
            <p class="card-description">We'll respond within 24 hours</p>
            <a href="mailto:support@mzeechakula.ug" class="card-action">Send Email</a>
          </div>

          <div class="contact-card">
            <div class="card-icon-wrapper secondary">
              <Phone :size="32" class="card-icon" />
            </div>
            <h3>Call Us</h3>
            <p class="card-detail">+256 700 123 456</p>
            <p class="card-detail">+256 750 987 654</p>
            <p class="card-description">Mon-Fri: 8am - 6pm (EAT)</p>
            <a href="tel:+256700123456" class="card-action">Call Now</a>
          </div>

          <div class="contact-card">
            <div class="card-icon-wrapper accent">
              <MapPin :size="32" class="card-icon" />
            </div>
            <h3>Visit Us</h3>
            <p class="card-detail">Plot 123 Kampala Road</p>
            <p class="card-detail">Kampala, Uganda</p>
            <p class="card-description">Mon-Fri: 9am - 5pm</p>
            <button @click="openMap" class="card-action">Get Directions</button>
          </div>

          <div class="contact-card">
            <div class="card-icon-wrapper info">
              <MessageCircle :size="32" class="card-icon" />
            </div>
            <h3>Live Chat</h3>
            <p class="card-detail">Chat with our support team</p>
            <p class="card-description">Available 24/7 for urgent issues</p>
            <button @click="startChat" class="card-action">Start Chat</button>
          </div>
        </div>

        <!-- Quick Contact Form -->
        <div class="quick-contact-form">
          <h2>Send Us a Message</h2>
          <p class="form-description">Have a quick question? Fill out the form and we'll get back to you shortly.</p>

          <form @submit.prevent="handleQuickContact" class="contact-form">
            <div class="form-row">
              <div class="form-group">
                <label for="name">Name</label>
                <input
                  v-model="contactForm.name"
                  type="text"
                  id="name"
                  placeholder="Your name"
                  required
                />
              </div>

              <div class="form-group">
                <label for="email">Email</label>
                <input
                  v-model="contactForm.email"
                  type="email"
                  id="email"
                  placeholder="your.email@example.com"
                  required
                />
              </div>
            </div>

            <div class="form-group">
              <label for="phone">Phone Number (Optional)</label>
              <input
                v-model="contactForm.phone"
                type="tel"
                id="phone"
                placeholder="+256 700 000 000"
              />
            </div>

            <div class="form-group">
              <label for="subject">Subject</label>
              <input
                v-model="contactForm.subject"
                type="text"
                id="subject"
                placeholder="What is this regarding?"
                required
              />
            </div>

            <div class="form-group">
              <label for="message">Message</label>
              <textarea
                v-model="contactForm.message"
                id="message"
                rows="5"
                placeholder="Your message..."
                required
              ></textarea>
            </div>

            <button type="submit" class="submit-btn" :disabled="loading">
              <Send :size="20" class="btn-icon" v-if="!loading" />
              <span>{{ loading ? 'Sending...' : 'Send Message' }}</span>
            </button>
          </form>

          <div v-if="showSuccess" class="success-alert">
            <CheckCircle2 :size="20" class="alert-icon" />
            <span>Message sent successfully! We'll get back to you soon.</span>
          </div>
        </div>
      </div>

      <!-- Social Media Section -->
      <div class="social-section">
        <h2>Connect With Us</h2>
        <p class="social-description">Follow us on social media for updates and news</p>
        <div class="social-links">
          <a href="#" class="social-link facebook" @click.prevent="alert('Facebook link')">
            <Facebook :size="24" />
            <span>Facebook</span>
          </a>
          <a href="#" class="social-link twitter" @click.prevent="alert('Twitter link')">
            <Twitter :size="24" />
            <span>Twitter</span>
          </a>
          <a href="#" class="social-link instagram" @click.prevent="alert('Instagram link')">
            <Instagram :size="24" />
            <span>Instagram</span>
          </a>
          <a href="#" class="social-link linkedin" @click.prevent="alert('LinkedIn link')">
            <Linkedin :size="24" />
            <span>LinkedIn</span>
          </a>
        </div>
      </div>

      <!-- FAQ Link -->
      <div class="faq-banner">
        <div class="banner-content">
          <HelpCircle :size="48" class="banner-icon" />
          <div class="banner-text">
            <h3>Looking for Quick Answers?</h3>
            <p>Check out our FAQ page for instant solutions to common questions</p>
          </div>
          <button @click="$router.push({ name: 'FAQ' })" class="banner-btn">
            Visit FAQ
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import {
  Phone,
  Mail,
  MapPin,
  MessageCircle,
  Send,
  CheckCircle2,
  HelpCircle,
  Facebook,
  Twitter,
  Instagram,
  Linkedin,
  ArrowLeft,
  Home
} from 'lucide-vue-next'

const router = useRouter()

const loading = ref(false)
const showSuccess = ref(false)

const contactForm = ref({
  name: '',
  email: '',
  phone: '',
  subject: '',
  message: ''
})

const handleQuickContact = async () => {
  loading.value = true
  showSuccess.value = false

  // Simulate API call
  setTimeout(() => {
    loading.value = false
    showSuccess.value = true

    // Reset form after 3 seconds
    setTimeout(() => {
      contactForm.value = {
        name: '',
        email: '',
        phone: '',
        subject: '',
        message: ''
      }
      showSuccess.value = false
    }, 3000)
  }, 1500)
}

const openMap = () => {
  window.open('https://maps.google.com/?q=Kampala,Uganda', '_blank')
}

const startChat = () => {
  alert('Live chat feature will be implemented with backend integration.')
}

const goBack = () => {
  router.back()
}

const goHome = () => {
  router.push({ name: 'Chat' })
}
</script>

<style scoped>
.contact-container {
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

.contact-header {
  background: linear-gradient(135deg, var(--color-primary) 0%, var(--color-primary-dark) 100%);
  padding: 4rem 2rem 3rem;
  text-align: center;
  position: relative;
  overflow: hidden;
}

.contact-header::before {
  content: '';
  position: absolute;
  bottom: -50%;
  right: -10%;
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

.contact-content {
  max-width: 1400px;
  margin: -2rem auto 0;
  padding: 0 1rem 4rem;
  position: relative;
  z-index: 2;
}

.contact-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 2rem;
  margin-bottom: 3rem;
}

.contact-cards {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 1.5rem;
}

.contact-card {
  background: var(--color-white);
  padding: 2rem;
  border-radius: 12px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.05);
  transition: all 0.3s ease;
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
}

.contact-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 8px 25px rgba(0, 0, 0, 0.1);
}

.card-icon-wrapper {
  width: 80px;
  height: 80px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-bottom: 1.5rem;
}

.card-icon-wrapper.primary {
  background: linear-gradient(135deg, rgba(217, 0, 0, 0.1), rgba(217, 0, 0, 0.2));
}

.card-icon-wrapper.secondary {
  background: linear-gradient(135deg, rgba(252, 220, 4, 0.1), rgba(252, 220, 4, 0.2));
}

.card-icon-wrapper.accent {
  background: linear-gradient(135deg, rgba(16, 185, 129, 0.1), rgba(16, 185, 129, 0.2));
}

.card-icon-wrapper.info {
  background: linear-gradient(135deg, rgba(59, 130, 246, 0.1), rgba(59, 130, 246, 0.2));
}

.card-icon {
  color: var(--color-primary);
}

.card-icon-wrapper.secondary .card-icon {
  color: var(--color-secondary-dark);
}

.card-icon-wrapper.accent .card-icon {
  color: var(--color-success);
}

.card-icon-wrapper.info .card-icon {
  color: var(--color-info);
}

.contact-card h3 {
  font-size: 1.25rem;
  font-weight: 700;
  color: var(--color-dark);
  margin-bottom: 0.75rem;
}

.card-detail {
  font-size: 1rem;
  font-weight: 600;
  color: var(--color-gray-700);
  margin-bottom: 0.25rem;
}

.card-description {
  font-size: 0.875rem;
  color: var(--color-gray-500);
  margin: 0.5rem 0 1.25rem;
}

.card-action {
  padding: 0.625rem 1.5rem;
  background: var(--color-primary);
  color: var(--color-white);
  border: none;
  border-radius: 8px;
  font-size: 0.875rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  text-decoration: none;
  display: inline-block;
}

.card-action:hover {
  background: var(--color-primary-dark);
  transform: translateY(-2px);
}

.quick-contact-form {
  background: var(--color-white);
  padding: 2.5rem;
  border-radius: 12px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
}

.quick-contact-form h2 {
  font-size: 1.75rem;
  font-weight: 700;
  color: var(--color-dark);
  margin-bottom: 0.5rem;
}

.form-description {
  font-size: 1rem;
  color: var(--color-gray-600);
  margin-bottom: 2rem;
}

.contact-form {
  display: flex;
  flex-direction: column;
  gap: 1.25rem;
}

.form-row {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1rem;
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

.form-group input,
.form-group textarea {
  padding: 0.875rem 1rem;
  border: 2px solid var(--color-gray-300);
  border-radius: 10px;
  font-size: 1rem;
  font-family: inherit;
  transition: all 0.3s ease;
}

.form-group input:focus,
.form-group textarea:focus {
  outline: none;
  border-color: var(--color-primary);
  box-shadow: 0 0 0 3px rgba(217, 0, 0, 0.1);
}

.form-group textarea {
  resize: vertical;
}

.submit-btn {
  padding: 1rem 2rem;
  background: var(--color-primary);
  color: var(--color-white);
  border: none;
  border-radius: 10px;
  font-size: 1rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
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

.success-alert {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  padding: 1rem;
  background: #D1FAE5;
  border: 2px solid var(--color-success);
  border-radius: 10px;
  color: #065F46;
  font-weight: 600;
  margin-top: 1rem;
  animation: slideDown 0.3s ease;
}

.alert-icon {
  color: var(--color-success);
  flex-shrink: 0;
}

.social-section {
  background: var(--color-white);
  padding: 3rem;
  border-radius: 12px;
  text-align: center;
  margin-bottom: 2rem;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.05);
}

.social-section h2 {
  font-size: 1.75rem;
  font-weight: 700;
  color: var(--color-dark);
  margin-bottom: 0.5rem;
}

.social-description {
  font-size: 1rem;
  color: var(--color-gray-600);
  margin-bottom: 2rem;
}

.social-links {
  display: flex;
  justify-content: center;
  gap: 1.5rem;
  flex-wrap: wrap;
}

.social-link {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 0.5rem;
  padding: 1.5rem;
  background: var(--color-gray-50);
  border-radius: 12px;
  text-decoration: none;
  color: var(--color-gray-700);
  transition: all 0.3s ease;
  min-width: 120px;
}

.social-link:hover {
  transform: translateY(-5px);
  box-shadow: 0 5px 20px rgba(0, 0, 0, 0.1);
}

.social-link.facebook:hover {
  background: #1877F2;
  color: white;
}

.social-link.twitter:hover {
  background: #1DA1F2;
  color: white;
}

.social-link.instagram:hover {
  background: linear-gradient(45deg, #F58529, #DD2A7B, #8134AF);
  color: white;
}

.social-link.linkedin:hover {
  background: #0A66C2;
  color: white;
}

.faq-banner {
  background: linear-gradient(135deg, var(--color-primary) 0%, var(--color-primary-dark) 100%);
  border-radius: 16px;
  padding: 3rem;
  box-shadow: 0 10px 40px rgba(217, 0, 0, 0.2);
}

.banner-content {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 2rem;
  color: var(--color-white);
}

.banner-icon {
  color: var(--color-secondary);
  flex-shrink: 0;
}

.banner-text {
  flex: 1;
}

.banner-text h3 {
  font-size: 1.5rem;
  font-weight: 700;
  margin-bottom: 0.5rem;
}

.banner-text p {
  font-size: 1rem;
  opacity: 0.95;
}

.banner-btn {
  padding: 0.875rem 2rem;
  background: var(--color-white);
  color: var(--color-primary);
  border: none;
  border-radius: 10px;
  font-size: 1rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  flex-shrink: 0;
}

.banner-btn:hover {
  transform: translateY(-3px);
  box-shadow: 0 8px 25px rgba(0, 0, 0, 0.3);
}

@media (max-width: 1200px) {
  .contact-grid {
    grid-template-columns: 1fr;
  }
}

@media (max-width: 768px) {
  .title {
    font-size: 2rem;
  }

  .subtitle {
    font-size: 1rem;
  }

  .contact-content {
    padding: 0 1rem 2rem;
  }

  .contact-cards {
    grid-template-columns: 1fr;
  }

  .quick-contact-form {
    padding: 2rem 1.5rem;
  }

  .form-row {
    grid-template-columns: 1fr;
  }

  .social-section {
    padding: 2rem 1.5rem;
  }

  .faq-banner {
    padding: 2rem 1.5rem;
  }

  .banner-content {
    flex-direction: column;
    text-align: center;
  }

  .banner-btn {
    width: 100%;
  }
}
</style>
