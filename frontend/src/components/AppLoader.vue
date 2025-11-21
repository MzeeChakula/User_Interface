<template>
  <div class="loader-container">
    <div class="icon-animation">
      <div class="icon-wrapper" :class="{ active: activeIcon === 0 }">
        <Utensils :size="48" :stroke-width="2" />
      </div>
      <div class="icon-wrapper" :class="{ active: activeIcon === 1 }">
        <Heart :size="48" :stroke-width="2" />
      </div>
      <div class="icon-wrapper" :class="{ active: activeIcon === 2 }">
        <Users :size="48" :stroke-width="2" />
      </div>
    </div>
    <p class="loading-text">{{ message }}</p>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import { Utensils, Heart, Users } from 'lucide-vue-next'

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
  background: var(--color-white);
  width: 100%;
}

.icon-animation {
  display: flex;
  gap: 2rem;
  margin-bottom: 2rem;
}

.icon-wrapper {
  opacity: 0.3;
  transform: scale(0.8);
  transition: all 0.4s ease;
  color: var(--color-gray-400);
}

.icon-wrapper.active {
  opacity: 1;
  transform: scale(1.2);
  color: var(--color-primary);
}

.loading-text {
  font-size: 1rem;
  color: var(--color-gray-600);
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

@media (max-width: 480px) {
  .icon-animation {
    gap: 1.5rem;
  }
}
</style>
