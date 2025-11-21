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

        <!-- Contact Information Cards -->
        <div class="contact-cards">
          <div class="contact-card">
            <div class="card-icon-wrapper primary">
              <Mail :size="28" class="card-icon" />
            </div>
            <h3>Email Us</h3>
            <p class="card-detail">support@mzeechakula.ug</p>
            <p class="card-description">We'll respond within 24 hours</p>
            <button @click="openEmail" class="card-action">Send Email</button>
          </div>

          <div class="contact-card">
            <div class="card-icon-wrapper secondary">
              <Phone :size="28" class="card-icon" />
            </div>
            <h3>Call Us</h3>
            <p class="card-detail">+256 700 123 456</p>
            <p class="card-description">Mon-Fri: 8am - 6pm (EAT)</p>
            <button @click="handleCall" class="card-action">Call Now</button>
          </div>

          <div class="contact-card">
            <div class="card-icon-wrapper accent">
              <MapPin :size="28" class="card-icon" />
            </div>
            <h3>Visit Us</h3>
            <p class="card-detail">Kampala, Uganda</p>
            <p class="card-description">Mon-Fri: 9am - 5pm</p>
            <button @click="openMap" class="card-action">Get Directions</button>
          </div>

          <div class="contact-card">
            <div class="card-icon-wrapper info">
              <MessageCircle :size="28" class="card-icon" />
            </div>
            <h3>Start Chat</h3>
            <p class="card-detail">Chat with our team</p>
            <p class="card-description">Available 24/7</p>
            <button @click="startChat" class="card-action">Open WhatsApp</button>
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

    <!-- Phone Number Copy Modal -->
    <div v-if="showPhoneModal" class="modal-overlay" @click="showPhoneModal = false">
      <div class="modal-content" @click.stop>
        <div class="modal-header">
          <Phone :size="48" class="modal-icon phone-icon" />
          <h3>Call Us</h3>
        </div>
        <div class="modal-body">
          <p class="phone-number">+256 700 123 456</p>
          <button @click="copyPhoneNumber" class="copy-btn">
            <Copy :size="18" v-if="!copied" />
            <CheckCircle2 :size="18" v-else />
            <span>{{ copied ? 'Copied!' : 'Copy Number' }}</span>
          </button>
        </div>
        <div class="modal-actions">
          <button @click="showPhoneModal = false" class="btn btn-secondary">Close</button>
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
  Home,
  Copy
} from 'lucide-vue-next'

const router = useRouter()

const loading = ref(false)
const showSuccess = ref(false)
const showPhoneModal = ref(false)
const copied = ref(false)

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

const openEmail = () => {
  // Open Gmail compose in new tab
  window.open('https://mail.google.com/mail/?view=cm&fs=1&to=support@mzeechakula.ug', '_blank')
}

const handleCall = () => {
  // Check if on mobile device
  const isMobile = /iPhone|iPad|iPod|Android/i.test(navigator.userAgent)

  if (isMobile) {
    // On mobile, directly open phone dialer
    window.location.href = 'tel:+256700123456'
  } else {
    // On desktop/browser, show modal to copy number
    showPhoneModal.value = true
    copied.value = false
  }
}

const copyPhoneNumber = async () => {
  try {
    await navigator.clipboard.writeText('+256700123456')
    copied.value = true
    setTimeout(() => {
      copied.value = false
    }, 2000)
  } catch (err) {
    console.error('Failed to copy:', err)
  }
}

const openMap = () => {
  // Open Google Maps with the location
  window.open('https://www.google.com/maps/search/?api=1&query=Kampala,Uganda', '_blank')
}

const startChat = () => {
  // Open WhatsApp chat
  const phoneNumber = '256700123456' // WhatsApp format without + or spaces
  const message = 'Hello, I need assistance with Mzee Chakula'
  window.open(`https://wa.me/${phoneNumber}?text=${encodeURIComponent(message)}`, '_blank')
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
  padding: 1.5rem;
  border-radius: 12px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.05);
  transition: all 0.3s ease;
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
  height: 100%;
  min-height: 220px;
}

.contact-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 8px 25px rgba(0, 0, 0, 0.1);
}

.card-icon-wrapper {
  width: 64px;
  height: 64px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-bottom: 1rem;
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
  font-size: 1.125rem;
  font-weight: 700;
  color: var(--color-dark);
  margin-bottom: 0.5rem;
}

.card-detail {
  font-size: 0.9375rem;
  font-weight: 600;
  color: var(--color-gray-700);
  margin-bottom: 0.25rem;
}

.card-description {
  font-size: 0.8125rem;
  color: var(--color-gray-500);
  margin: 0.5rem 0 1rem;
  flex: 1;
}

.card-action {
  padding: 0.625rem 1.25rem;
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
  margin-top: auto;
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

  .header-title {
    font-size: 1rem;
  }

  .contact-content {
    padding: 0 1rem 2rem;
  }

  .contact-grid {
    grid-template-columns: 1fr;
  }

  .contact-cards {
    grid-template-columns: repeat(2, 1fr);
    gap: 0.75rem;
  }

  .contact-card {
    padding: 1rem;
    min-height: 200px;
  }

  .card-icon-wrapper {
    width: 52px;
    height: 52px;
    margin-bottom: 0.75rem;
  }

  .card-icon-wrapper svg {
    width: 24px;
    height: 24px;
  }

  .contact-card h3 {
    font-size: 0.9375rem;
    margin-bottom: 0.375rem;
  }

  .card-detail {
    font-size: 0.8125rem;
  }

  .card-description {
    font-size: 0.6875rem;
    margin: 0.375rem 0 0.75rem;
  }

  .card-action {
    padding: 0.5rem 0.875rem;
    font-size: 0.75rem;
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

  .modal-content {
    padding: 1.5rem;
  }

  .modal-header h3 {
    font-size: 1.25rem;
  }

  .phone-number {
    font-size: 1.25rem;
  }

  .copy-btn {
    padding: 0.75rem 1.25rem;
    font-size: 0.9375rem;
  }
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
  z-index: 1000;
  padding: 1rem;
}

.modal-content {
  background: var(--color-white);
  border-radius: 16px;
  padding: 2rem;
  max-width: 400px;
  width: 100%;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
  animation: slideIn 0.3s ease;
}

.modal-header {
  text-align: center;
  margin-bottom: 1.5rem;
}

.modal-icon {
  margin-bottom: 1rem;
}

.phone-icon {
  color: var(--color-secondary-dark);
}

.modal-header h3 {
  font-size: 1.5rem;
  font-weight: 700;
  color: var(--color-dark);
  margin: 0;
}

.modal-body {
  text-align: center;
  margin-bottom: 1.5rem;
}

.phone-number {
  font-size: 1.5rem;
  font-weight: 700;
  color: var(--color-primary);
  margin: 0 0 1.5rem 0;
  letter-spacing: 1px;
}

.copy-btn {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
  padding: 0.875rem 1.5rem;
  background: var(--color-gray-100);
  border: 2px solid var(--color-gray-300);
  border-radius: 10px;
  font-size: 1rem;
  font-weight: 600;
  color: var(--color-dark);
  cursor: pointer;
  transition: all 0.3s ease;
  margin: 0 auto;
}

.copy-btn:hover {
  background: var(--color-gray-200);
  border-color: var(--color-primary);
  color: var(--color-primary);
}

.modal-actions {
  display: flex;
  gap: 1rem;
}

.btn {
  flex: 1;
  padding: 0.875rem;
  border-radius: 10px;
  font-size: 1rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  border: none;
}

.btn-secondary {
  background: var(--color-gray-200);
  color: var(--color-gray-700);
}

.btn-secondary:hover {
  background: var(--color-gray-300);
}

@keyframes slideIn {
  from {
    opacity: 0;
    transform: translateY(-20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}
</style>
