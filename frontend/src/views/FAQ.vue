<template>
  <div class="faq-container">
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

    <div class="faq-header">
      <div class="header-content">
        <h1 class="title">Frequently Asked Questions</h1>
        <p class="subtitle">Find answers to common questions about Mzee Chakula</p>
      </div>
    </div>

    <div class="faq-content">
      <div class="search-box">
        <Search :size="20" class="search-icon" />
        <input
          v-model="searchQuery"
          type="text"
          placeholder="Search for answers..."
          class="search-input"
        />
      </div>

      <div class="faq-categories">
        <button
          v-for="category in categories"
          :key="category"
          @click="selectedCategory = category"
          :class="['category-btn', { active: selectedCategory === category }]"
        >
          {{ category }}
        </button>
      </div>

      <div class="faq-list">
        <div
          v-for="(faq, index) in filteredFAQs"
          :key="index"
          class="faq-item"
        >
          <button
            @click="toggleFAQ(index)"
            class="faq-question"
          >
            <span class="question-text">{{ faq.question }}</span>
            <ChevronDown
              :size="20"
              :class="['chevron-icon', { rotated: openFAQ === index }]"
            />
          </button>
          <transition name="accordion">
            <div v-if="openFAQ === index" class="faq-answer">
              <p>{{ faq.answer }}</p>
            </div>
          </transition>
        </div>
      </div>

      <div class="help-section">
        <div class="help-card">
          <HelpCircle :size="48" class="help-icon" />
          <h3>Still have questions?</h3>
          <p>Can't find what you're looking for? Our support team is here to help.</p>
          <button @click="$router.push({ name: 'ContactUs' })" class="contact-btn">
            Contact Us
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useRouter } from 'vue-router'
import { Search, ChevronDown, HelpCircle, ArrowLeft, Home } from 'lucide-vue-next'

const router = useRouter()

const searchQuery = ref('')
const selectedCategory = ref('All')
const openFAQ = ref(null)

const categories = ['All', 'General', 'Nutrition', 'Features', 'Account', 'Privacy']

const faqs = [
  {
    category: 'General',
    question: 'What is Mzee Chakula?',
    answer: 'Mzee Chakula is an AI-powered nutritional assistant designed specifically for elderly care in Uganda. It provides personalized meal plans based on health conditions and locally available foods.'
  },
  {
    category: 'General',
    question: 'Who can use Mzee Chakula?',
    answer: 'Mzee Chakula is designed for caregivers, family members, and healthcare professionals who care for elderly individuals in Uganda. The platform is accessible to anyone interested in improving elderly nutrition.'
  },
  {
    category: 'Nutrition',
    question: 'How are meal plans personalized?',
    answer: 'Our AI analyzes health conditions, dietary restrictions, medication interactions, and food preferences to create customized meal plans using locally available ingredients in Uganda.'
  },
  {
    category: 'Nutrition',
    question: 'Can I specify dietary restrictions?',
    answer: 'Yes! You can specify various dietary restrictions including allergies, religious dietary requirements, medical conditions like diabetes or hypertension, and personal food preferences.'
  },
  {
    category: 'Features',
    question: 'What features does the app offer?',
    answer: 'The app offers AI-powered meal planning, nutritional guidance, recipe suggestions using local foods, health condition tracking, medication interaction alerts, and personalized dietary recommendations.'
  },
  {
    category: 'Features',
    question: 'Can I save my favorite meal plans?',
    answer: 'Yes! You can save your favorite meal plans and recipes for easy access later. Your saved items are stored in your profile and accessible anytime.'
  },
  {
    category: 'Account',
    question: 'How do I create an account?',
    answer: 'You can create an account using your email, phone number, or Google account. Simply click on Sign Up and follow the registration process.'
  },
  {
    category: 'Account',
    question: 'Is my data secure?',
    answer: 'Yes, we take data security seriously. All your personal and health information is encrypted and stored securely. We never share your data with third parties without your explicit consent.'
  },
  {
    category: 'Privacy',
    question: 'What information do you collect?',
    answer: 'We collect information necessary to provide personalized meal plans, including health conditions, dietary preferences, and usage data. All data collection is transparent and with your consent.'
  },
  {
    category: 'Privacy',
    question: 'Can I delete my account?',
    answer: 'Yes, you can delete your account anytime from the Settings page. This will permanently remove all your data from our servers.'
  },
  {
    category: 'Features',
    question: 'Does the app work offline?',
    answer: 'Yes! Mzee Chakula is a Progressive Web App (PWA) that works offline. You can access saved meal plans and previously loaded content even without an internet connection.'
  },
  {
    category: 'Nutrition',
    question: 'Are the recipes based on Ugandan cuisine?',
    answer: 'Absolutely! All our meal plans and recipes are designed around locally available ingredients and traditional Ugandan foods, making them practical and culturally appropriate.'
  }
]

const filteredFAQs = computed(() => {
  let filtered = faqs

  if (selectedCategory.value !== 'All') {
    filtered = filtered.filter(faq => faq.category === selectedCategory.value)
  }

  if (searchQuery.value) {
    const query = searchQuery.value.toLowerCase()
    filtered = filtered.filter(faq =>
      faq.question.toLowerCase().includes(query) ||
      faq.answer.toLowerCase().includes(query)
    )
  }

  return filtered
})

const toggleFAQ = (index) => {
  openFAQ.value = openFAQ.value === index ? null : index
}

const goBack = () => {
  router.back()
}

const goHome = () => {
  router.push({ name: 'Chat' })
}
</script>

<style scoped>
.faq-container {
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

.faq-header {
  background: linear-gradient(135deg, var(--color-primary) 0%, var(--color-primary-dark) 100%);
  padding: 4rem 2rem 3rem;
  text-align: center;
  position: relative;
  overflow: hidden;
}

.faq-header::before {
  content: '';
  position: absolute;
  top: -50%;
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

.title {
  font-size: 2.5rem;
  font-weight: 800;
  color: var(--color-white);
  margin-bottom: 1rem;
  text-shadow: 0 2px 10px rgba(0, 0, 0, 0.2);
}

.subtitle {
  font-size: 1.25rem;
  color: var(--color-secondary);
  font-weight: 500;
}

.faq-content {
  max-width: 900px;
  margin: -2rem auto 0;
  padding: 0 1rem 4rem;
  position: relative;
  z-index: 2;
}

.search-box {
  position: relative;
  margin-bottom: 2rem;
  background: var(--color-white);
  border-radius: 12px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
}

.search-icon {
  position: absolute;
  left: 1.25rem;
  top: 50%;
  transform: translateY(-50%);
  color: var(--color-gray-400);
}

.search-input {
  width: 100%;
  padding: 1.25rem 1.25rem 1.25rem 3.5rem;
  border: 2px solid transparent;
  border-radius: 12px;
  font-size: 1rem;
  transition: all 0.3s ease;
  background: transparent;
}

.search-input:focus {
  outline: none;
  border-color: var(--color-primary);
}

.faq-categories {
  display: flex;
  gap: 0.75rem;
  flex-wrap: wrap;
  margin-bottom: 2rem;
  padding: 1.5rem;
  background: var(--color-white);
  border-radius: 12px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.05);
}

.category-btn {
  padding: 0.625rem 1.25rem;
  border: 2px solid var(--color-gray-300);
  background: var(--color-white);
  color: var(--color-gray-700);
  border-radius: 8px;
  font-size: 0.875rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
}

.category-btn:hover {
  border-color: var(--color-primary);
  color: var(--color-primary);
  transform: translateY(-2px);
}

.category-btn.active {
  background: var(--color-primary);
  border-color: var(--color-primary);
  color: var(--color-white);
}

.faq-list {
  display: flex;
  flex-direction: column;
  gap: 1rem;
  margin-bottom: 3rem;
}

.faq-item {
  background: var(--color-white);
  border-radius: 12px;
  overflow: hidden;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.05);
  transition: all 0.3s ease;
}

.faq-item:hover {
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
}

.faq-question {
  width: 100%;
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1.5rem;
  background: transparent;
  border: none;
  text-align: left;
  cursor: pointer;
  transition: all 0.3s ease;
}

.faq-question:hover {
  background: var(--color-gray-50);
}

.question-text {
  font-size: 1.125rem;
  font-weight: 600;
  color: var(--color-dark);
  flex: 1;
  padding-right: 1rem;
}

.chevron-icon {
  color: var(--color-primary);
  transition: transform 0.3s ease;
  flex-shrink: 0;
}

.chevron-icon.rotated {
  transform: rotate(180deg);
}

.faq-answer {
  padding: 0 1.5rem 1.5rem;
  color: var(--color-gray-700);
  line-height: 1.8;
  font-size: 1rem;
}

.accordion-enter-active,
.accordion-leave-active {
  transition: all 0.3s ease;
  overflow: hidden;
}

.accordion-enter-from,
.accordion-leave-to {
  opacity: 0;
  max-height: 0;
}

.accordion-enter-to,
.accordion-leave-from {
  opacity: 1;
  max-height: 500px;
}

.help-section {
  margin-top: 3rem;
}

.help-card {
  background: linear-gradient(135deg, var(--color-primary) 0%, var(--color-primary-dark) 100%);
  padding: 3rem;
  border-radius: 16px;
  text-align: center;
  color: var(--color-white);
  box-shadow: 0 10px 40px rgba(217, 0, 0, 0.2);
}

.help-icon {
  margin: 0 auto 1.5rem;
  color: var(--color-secondary);
}

.help-card h3 {
  font-size: 1.75rem;
  font-weight: 700;
  margin-bottom: 0.75rem;
}

.help-card p {
  font-size: 1.125rem;
  margin-bottom: 2rem;
  opacity: 0.95;
}

.contact-btn {
  padding: 0.875rem 2rem;
  background: var(--color-white);
  color: var(--color-primary);
  border: none;
  border-radius: 10px;
  font-size: 1rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
}

.contact-btn:hover {
  transform: translateY(-3px);
  box-shadow: 0 8px 25px rgba(0, 0, 0, 0.3);
}

@media (max-width: 768px) {
  .title {
    font-size: 2rem;
  }

  .subtitle {
    font-size: 1rem;
  }

  .faq-content {
    padding: 0 1rem 2rem;
  }

  .faq-categories {
    padding: 1rem;
  }

  .question-text {
    font-size: 1rem;
  }

  .help-card {
    padding: 2rem 1.5rem;
  }

  .help-card h3 {
    font-size: 1.5rem;
  }
}
</style>
