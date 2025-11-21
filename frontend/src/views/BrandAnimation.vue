<template>
  <div class="brand-animation-container">
    <div class="animation-wrapper">
      <div class="color-waves">
        <div class="wave wave-1"></div>
        <div class="wave wave-2"></div>
        <div class="wave wave-3"></div>
      </div>
      <div class="brand-content" :class="{ show: showBrand }">
        <h1 class="brand-name">Mzee Chakula</h1>
        <p class="brand-tagline">Nourishing our Elders, Together</p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()
const showBrand = ref(false)

onMounted(() => {
  setTimeout(() => {
    showBrand.value = true
  }, 800)

  setTimeout(() => {
    router.push({ name: 'Welcome' })
  }, 3500)
})
</script>

<style scoped>
.brand-animation-container {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100vh;
  background: #ffffff;
  display: flex;
  align-items: center;
  justify-content: center;
  overflow: hidden;
}

.animation-wrapper {
  position: relative;
  width: 100%;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
}

.color-waves {
  position: absolute;
  top: 0;
  left: -100%;
  width: 100%;
  height: 100%;
  display: flex;
  flex-direction: column;
  animation: slideIn 1.2s ease-out forwards;
}

@keyframes slideIn {
  to {
    left: 0;
  }
}

.wave {
  flex: 1;
  opacity: 0;
  animation: fadeIn 0.6s ease-out forwards;
}

.wave-1 {
  background: linear-gradient(90deg, #ffd60a 0%, #ffc300 100%);
  animation-delay: 0.2s;
}

.wave-2 {
  background: linear-gradient(90deg, #4cc9f0 0%, #4361ee 100%);
  animation-delay: 0.4s;
}

.wave-3 {
  background: linear-gradient(90deg, #52b788 0%, #2d6a4f 100%);
  animation-delay: 0.6s;
}

@keyframes fadeIn {
  to {
    opacity: 1;
  }
}

.brand-content {
  position: relative;
  z-index: 10;
  text-align: center;
  opacity: 0;
  transform: scale(0.8);
  transition: all 0.8s cubic-bezier(0.34, 1.56, 0.64, 1);
}

.brand-content.show {
  opacity: 1;
  transform: scale(1);
}

.brand-name {
  font-size: 3.5rem;
  font-weight: 700;
  color: #ffffff;
  text-shadow: 0 4px 20px rgba(0, 0, 0, 0.3);
  margin-bottom: 1rem;
  letter-spacing: 0.05em;
}

.brand-tagline {
  font-size: 1.25rem;
  color: #ffffff;
  font-weight: 400;
  text-shadow: 0 2px 10px rgba(0, 0, 0, 0.2);
  opacity: 0.95;
}

@media (max-width: 768px) {
  .brand-name {
    font-size: 2.5rem;
  }

  .brand-tagline {
    font-size: 1rem;
  }
}
</style>
