<template>
  <div class="loader-container">
    <div class="icon-animation">
      <div class="icon-wrapper" :class="{ active: activeIcon === 0 }">
        <span class="icon">🍽️</span>
      </div>
      <div class="icon-wrapper" :class="{ active: activeIcon === 1 }">
        <span class="icon">🏥</span>
      </div>
      <div class="icon-wrapper" :class="{ active: activeIcon === 2 }">
        <span class="icon">👥</span>
      </div>
    </div>
    <p class="loading-text">{{ message }}</p>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'

defineProps({
  message: {
    type: String,
    default: 'Loading...'
  }
})

const activeIcon = ref(0)
let interval = null

onMounted(() => {
  interval = setInterval(() => {
    activeIcon.value = (activeIcon.value + 1) % 3
  }, 600)
})

onUnmounted(() => {
  if (interval) {
    clearInterval(interval)
  }
})
</script>

<style scoped>
.loader-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  min-height: 100vh;
  background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
}

.icon-animation {
  display: flex;
  gap: 1.5rem;
  margin-bottom: 2rem;
}

.icon-wrapper {
  opacity: 0.3;
  transform: scale(0.8);
  transition: all 0.4s ease;
}

.icon-wrapper.active {
  opacity: 1;
  transform: scale(1.2);
}

.icon {
  font-size: 3rem;
  display: block;
}

.loading-text {
  font-size: 1rem;
  color: #6c757d;
  font-weight: 500;
  animation: pulse 1.5s ease-in-out infinite;
}

@keyframes pulse {
  0%, 100% {
    opacity: 0.6;
  }
  50% {
    opacity: 1;
  }
}
</style>
