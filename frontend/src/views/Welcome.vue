<template>
  <div class="welcome-container">
    <div class="welcome-grid">
      <!-- Left Column - Branding -->
      <div class="brand-column">
        <img src="/icons/logotransparent.svg" alt="Mzee Chakula Logo" class="logo" />
        <h1 class="app-title">Mzee Chakula</h1>
        <p class="app-subtitle">Nourishing our Elders, Together</p>
      </div>

      <!-- Right Column - Tutorial Cards -->
      <div class="tutorial-column">
        <div class="tutorial-content">
          <h2 class="tutorial-header">Get Started</h2>

          <div class="tutorial-cards">
            <div
              v-for="(card, index) in tutorialCards"
              :key="index"
              class="tutorial-card"
              :class="{ active: currentCard === index }"
            >
              <div class="card-icon">
                <component :is="card.icon" :size="80" :stroke-width="1.5" />
              </div>
              <h3 class="card-title">{{ card.title }}</h3>
              <p class="card-description">{{ card.description }}</p>
            </div>
          </div>

          <div class="progress-dots">
            <span
              v-for="(card, index) in tutorialCards"
              :key="index"
              class="dot"
              :class="{ active: currentCard === index }"
              @click="currentCard = index"
            ></span>
          </div>

          <div class="actions">
            <button
              v-if="currentCard < tutorialCards.length - 1"
              @click="nextCard"
              class="btn btn-primary"
            >
              Next
            </button>
            <button
              v-else
              @click="getStarted"
              class="btn btn-primary"
            >
              Get Started
            </button>
            <button @click="skip" class="btn btn-text">Skip Tutorial</button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useAppStore } from '../stores/app'
import { MessageCircle, History, UserCircle, Wifi } from 'lucide-vue-next'
import gsap from 'gsap'

const router = useRouter()
const appStore = useAppStore()

const currentCard = ref(0)

const tutorialCards = [
  {
    icon: MessageCircle,
    title: 'Chat to Get a Plan',
    description: 'Have a natural conversation about nutritional needs, health conditions, and preferences to receive personalized meal plans.'
  },
  {
    icon: History,
    title: 'View Your History',
    description: 'Access all your past conversations and meal plans anytime. Your recommendations are saved for easy reference.'
  },
  {
    icon: UserCircle,
    title: 'Update Your Profile',
    description: 'Customize the elder\'s profile with age, health conditions, dietary preferences, and location for better recommendations.'
  },
  {
    icon: Wifi,
    title: 'Works Offline',
    description: 'Use the app even without internet. Your data is saved locally and synced when you\'re back online.'
  }
]

onMounted(() => {
  gsap.from('.app-title', {
    duration: 1,
    y: -30,
    opacity: 0,
    ease: 'back.out(1.7)'
  })

  gsap.from('.app-subtitle', {
    duration: 0.8,
    y: 20,
    opacity: 0,
    delay: 0.3,
    ease: 'power2.out'
  })
})

const nextCard = () => {
  if (currentCard.value < tutorialCards.length - 1) {
    currentCard.value++
  }
}

const skip = () => {
  appStore.setFirstTimeComplete()
  router.push({ name: 'Auth' })
}

const getStarted = () => {
  appStore.setFirstTimeComplete()
  router.push({ name: 'Auth' })
}
</script>

<style scoped>
.welcome-container {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
  width: 100%;
  overflow: hidden;
}

.welcome-grid {
  display: grid;
  grid-template-columns: 1fr 1.2fr;
  width: 100%;
  height: 100vh;
}

/* Left Column - Branding */
.brand-column {
  background: linear-gradient(135deg, var(--color-primary) 0%, var(--color-primary-dark) 100%);
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 3rem;
  position: relative;
  overflow: hidden;
}

.brand-column::before {
  content: '';
  position: absolute;
  bottom: -50%;
  left: -50%;
  width: 150%;
  height: 150%;
  background: radial-gradient(circle, rgba(252, 220, 4, 0.15) 0%, transparent 60%);
}

.logo {
  width: 200px;
  height: 200px;
  margin: 0 auto 2rem auto;
  display: block;
  filter: drop-shadow(0 10px 40px rgba(0, 0, 0, 0.3));
  z-index: 1;
}

.app-title {
  font-size: 3.5rem;
  font-weight: 800;
  color: var(--color-white);
  margin-bottom: 1rem;
  text-shadow: 0 4px 20px rgba(0, 0, 0, 0.3);
  z-index: 1;
  text-align: center;
}

.app-subtitle {
  font-size: 1.5rem;
  color: var(--color-secondary);
  font-weight: 600;
  text-shadow: 0 2px 10px rgba(0, 0, 0, 0.2);
  z-index: 1;
  text-align: center;
}

/* Right Column - Tutorial */
.tutorial-column {
  background: var(--color-white);
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 3rem 2rem;
}

.tutorial-content {
  width: 100%;
  max-width: 600px;
}

.tutorial-header {
  font-size: 2rem;
  font-weight: 700;
  color: var(--color-dark);
  margin-bottom: 2rem;
  text-align: center;
}

.tutorial-cards {
  position: relative;
  height: 380px;
  margin-bottom: 2rem;
}

.tutorial-card {
  position: absolute;
  width: 100%;
  background: var(--color-white);
  border-radius: 20px;
  padding: 2rem;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
  text-align: center;
  opacity: 0;
  transform: translateX(50px);
  pointer-events: none;
  transition: all 0.4s ease;
  border: 2px solid var(--color-gray-200);
}

.tutorial-card.active {
  opacity: 1;
  transform: translateX(0);
  pointer-events: auto;
  border-color: var(--color-primary);
}

.card-icon {
  margin-bottom: 1.5rem;
  color: var(--color-primary);
  display: flex;
  align-items: center;
  justify-content: center;
}

.card-title {
  font-size: 1.5rem;
  font-weight: 600;
  color: var(--color-dark);
  margin-bottom: 1rem;
}

.card-description {
  font-size: 1rem;
  color: var(--color-gray-600);
  line-height: 1.6;
}

.progress-dots {
  display: flex;
  gap: 0.75rem;
  margin-bottom: 2rem;
  justify-content: center;
}

.dot {
  width: 12px;
  height: 12px;
  border-radius: 50%;
  background: var(--color-gray-300);
  cursor: pointer;
  transition: all 0.3s ease;
}

.dot.active {
  background: var(--color-primary);
  transform: scale(1.3);
}

.actions {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.btn {
  padding: 1rem 2rem;
  border-radius: 12px;
  font-size: 1rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  border: none;
}

.btn-primary {
  background: var(--color-primary);
  color: var(--color-white);
}

.btn-primary:hover {
  background: var(--color-primary-dark);
  transform: translateY(-2px);
  box-shadow: 0 5px 20px rgba(217, 0, 0, 0.3);
}

.btn-text {
  background: transparent;
  color: var(--color-gray-600);
}

.btn-text:hover {
  color: var(--color-primary);
}

/* Responsive */
@media (max-width: 1024px) {
  .welcome-grid {
    grid-template-columns: 1fr;
  }

  .brand-column {
    height: 40vh;
    padding: 2rem;
  }

  .logo {
    width: 120px;
    height: 120px;
  }

  .app-title {
    font-size: 2.5rem;
  }

  .app-subtitle {
    font-size: 1.25rem;
  }

  .tutorial-column {
    height: 60vh;
  }
}

@media (max-width: 768px) {
  .brand-column {
    padding: 1.5rem;
  }

  .logo {
    width: 100px;
    height: 100px;
    margin-bottom: 1rem;
  }

  .app-title {
    font-size: 2rem;
  }

  .app-subtitle {
    font-size: 1rem;
  }

  .tutorial-column {
    padding: 2rem 1.5rem;
    display: flex;
    align-items: center;
    justify-content: center;
  }

  .tutorial-content {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
  }

  .tutorial-header {
    font-size: 1.5rem;
    margin-bottom: 1.5rem;
  }

  .tutorial-cards {
    height: 350px;
    width: 100%;
  }

  .card-icon svg {
    width: 64px;
    height: 64px;
  }
}

@media (max-width: 480px) {
  .tutorial-card {
    padding: 1.5rem 1rem;
  }

  .card-title {
    font-size: 1.25rem;
  }

  .card-description {
    font-size: 0.875rem;
  }

  .card-icon svg {
    width: 56px;
    height: 56px;
  }

  .tutorial-cards {
    height: 320px;
  }
}
</style>
