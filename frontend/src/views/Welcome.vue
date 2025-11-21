<template>
  <div class="welcome-container">
    <div class="logo-section">
      <img src="/icons/logotransparent.svg" alt="Mzee Chakula Logo" class="logo" />
      <h1 class="app-title">Mzee Chakula</h1>
    </div>

    <div class="tutorial-section">
      <div class="cards-wrapper">
        <div
          v-for="(card, index) in tutorialCards"
          :key="index"
          class="tutorial-card"
          :class="{ active: currentCard === index }"
        >
          <div class="card-icon">
            <component :is="card.icon" :size="64" :stroke-width="1.5" />
          </div>
          <h2 class="card-title">{{ card.title }}</h2>
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
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAppStore } from '../stores/app'
import { MessageCircle, History, UserCircle, Wifi } from 'lucide-vue-next'

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
  flex-direction: column;
  align-items: center;
  justify-content: space-between;
  padding: 2rem 1.5rem;
  background: var(--color-white);
  width: 100%;
}

.logo-section {
  text-align: center;
  margin-top: 2rem;
}

.logo {
  width: 120px;
  height: 120px;
  margin-bottom: 1rem;
}

.app-title {
  font-size: 2rem;
  font-weight: 700;
  color: var(--color-primary);
  margin: 0;
}

.tutorial-section {
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  width: 100%;
  max-width: 500px;
}

.cards-wrapper {
  position: relative;
  width: 100%;
  height: 320px;
  margin-bottom: 2rem;
}

.tutorial-card {
  position: absolute;
  width: 100%;
  background: var(--color-white);
  border-radius: 20px;
  padding: 2.5rem 2rem;
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
  transform: scale(1.2);
}

.actions {
  width: 100%;
  max-width: 400px;
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

@media (max-width: 768px) {
  .welcome-container {
    padding: 1.5rem 1rem;
  }

  .logo {
    width: 100px;
    height: 100px;
  }

  .app-title {
    font-size: 1.75rem;
  }

  .tutorial-card {
    padding: 2rem 1.5rem;
  }

  .cards-wrapper {
    height: 340px;
  }
}

@media (max-width: 480px) {
  .logo-section {
    margin-top: 1rem;
  }

  .tutorial-card {
    padding: 1.5rem 1rem;
  }

  .card-title {
    font-size: 1.25rem;
  }

  .card-description {
    font-size: 0.875rem;
  }
}
</style>
