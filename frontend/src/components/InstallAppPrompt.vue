<template>
  <transition name="slide-up">
    <div v-if="showPrompt" class="install-prompt">
      <div class="prompt-content">
        <div class="prompt-icon">
          <Download :size="24" />
        </div>
        <div class="prompt-text">
          <h3 class="prompt-title">Install Mzee Chakula</h3>
          <p class="prompt-description">Get quick access to nutritional planning for elderly care</p>
        </div>
        <button @click="dismissPrompt" class="close-prompt" title="Close">
          <X :size="20" />
        </button>
      </div>
    </div>
  </transition>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { Download, X } from 'lucide-vue-next'

const showPrompt = ref(false)
const DISMISS_KEY = 'installPromptDismissed'

onMounted(() => {
  // Check if prompt has been dismissed in this session
  const isDismissed = sessionStorage.getItem(DISMISS_KEY)

  if (!isDismissed) {
    // Show prompt after a short delay for better UX
    setTimeout(() => {
      showPrompt.value = true
    }, 2000)
  }
})

const dismissPrompt = () => {
  showPrompt.value = false
  // Store dismissal in sessionStorage so it doesn't show again in this session
  // On next visit/reload, it will show again
  sessionStorage.setItem(DISMISS_KEY, 'true')
}
</script>

<style scoped>
.install-prompt {
  position: fixed;
  bottom: 1rem;
  left: 50%;
  transform: translateX(-50%);
  z-index: 2000;
  width: calc(100% - 2rem);
  max-width: 500px;
}

.prompt-content {
  background: linear-gradient(135deg, var(--color-primary) 0%, var(--color-primary-dark) 100%);
  border-radius: 16px;
  padding: 1rem 1.5rem;
  box-shadow: 0 10px 40px rgba(217, 0, 0, 0.5), 0 5px 20px rgba(217, 0, 0, 0.3);
  display: flex;
  align-items: center;
  gap: 1rem;
  position: relative;
  border: 2px solid rgba(255, 255, 255, 0.2);
}

.prompt-icon {
  width: 48px;
  height: 48px;
  background: rgba(255, 255, 255, 0.2);
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  flex-shrink: 0;
}

.prompt-text {
  flex: 1;
  color: white;
}

.prompt-title {
  font-size: 1rem;
  font-weight: 700;
  margin: 0 0 0.25rem 0;
  color: white;
}

.prompt-description {
  font-size: 0.875rem;
  margin: 0;
  color: rgba(255, 255, 255, 0.9);
  line-height: 1.4;
}

.close-prompt {
  position: absolute;
  top: 0.5rem;
  right: 0.5rem;
  background: rgba(255, 255, 255, 0.2);
  border: none;
  width: 32px;
  height: 32px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  color: white;
  transition: all 0.3s ease;
}

.close-prompt:hover {
  background: rgba(255, 255, 255, 0.3);
  transform: scale(1.1);
}

/* Animations */
.slide-up-enter-active,
.slide-up-leave-active {
  transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
}

.slide-up-enter-from {
  opacity: 0;
  transform: translateX(-50%) translateY(100px);
}

.slide-up-leave-to {
  opacity: 0;
  transform: translateX(-50%) translateY(100px);
}

/* Mobile styles */
@media (max-width: 768px) {
  .install-prompt {
    width: calc(100vw - 2rem);
    max-width: calc(100vw - 2rem);
    bottom: 0.5rem;
    left: 1rem;
    transform: none;
  }

  .prompt-content {
    padding: 0.75rem 2.5rem 0.75rem 0.75rem;
    gap: 0.625rem;
    border-radius: 12px;
  }

  .prompt-icon {
    width: 36px;
    height: 36px;
    border-radius: 8px;
    flex-shrink: 0;
  }

  .prompt-icon svg {
    width: 18px;
    height: 18px;
  }

  .prompt-text {
    flex: 1;
    min-width: 0;
  }

  .prompt-title {
    font-size: 0.8125rem;
    margin: 0 0 0.125rem 0;
    word-wrap: break-word;
  }

  .prompt-description {
    font-size: 0.6875rem;
    line-height: 1.3;
    word-wrap: break-word;
  }

  .close-prompt {
    width: 26px;
    height: 26px;
    top: 0.5rem;
    right: 0.5rem;
    flex-shrink: 0;
  }

  .close-prompt svg {
    width: 14px;
    height: 14px;
  }

  .slide-up-enter-from {
    opacity: 0;
    transform: translateY(100px);
  }

  .slide-up-leave-to {
    opacity: 0;
    transform: translateY(100px);
  }
}
</style>
