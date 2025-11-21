<template>
  <div class="brand-animation-container">
    <div class="animation-wrapper">
      <!-- Color waves -->
      <div class="color-waves">
        <div ref="wave1" class="wave wave-1"></div>
        <div ref="wave2" class="wave wave-2"></div>
        <div ref="wave3" class="wave wave-3"></div>
      </div>

      <!-- Brand content -->
      <div class="brand-content">
        <h1 ref="brandName" class="brand-name">Mzee Chakula</h1>
        <p ref="brandTagline" class="brand-tagline">Nourishing our Elders, Together</p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import gsap from 'gsap'

const router = useRouter()

// Refs for animated elements
const wave1 = ref(null)
const wave2 = ref(null)
const wave3 = ref(null)
const brandName = ref(null)
const brandTagline = ref(null)

onMounted(() => {
  const timeline = gsap.timeline({
    onComplete: () => {
      // Navigate to welcome screen after animation completes
      setTimeout(() => {
        router.push({ name: 'Welcome' })
      }, 500)
    }
  })

  // Set initial states
  gsap.set([wave1.value, wave2.value, wave3.value], {
    x: '-100%',
    opacity: 0
  })

  gsap.set([brandName.value, brandTagline.value], {
    opacity: 0,
    scale: 0.8,
    y: 20
  })

  // Animate waves sliding in with stagger
  timeline
    .to(wave1.value, {
      x: '0%',
      opacity: 1,
      duration: 0.8,
      ease: 'power3.out'
    })
    .to(wave2.value, {
      x: '0%',
      opacity: 1,
      duration: 0.8,
      ease: 'power3.out'
    }, '-=0.6')
    .to(wave3.value, {
      x: '0%',
      opacity: 1,
      duration: 0.8,
      ease: 'power3.out'
    }, '-=0.6')
    // Animate brand name
    .to(brandName.value, {
      opacity: 1,
      scale: 1,
      y: 0,
      duration: 0.8,
      ease: 'back.out(1.7)'
    }, '-=0.4')
    // Animate tagline
    .to(brandTagline.value, {
      opacity: 1,
      scale: 1,
      y: 0,
      duration: 0.6,
      ease: 'power2.out'
    }, '-=0.4')
    // Hold for a moment
    .to({}, { duration: 0.8 })
    // Fade out
    .to('.brand-animation-container', {
      opacity: 0,
      duration: 0.5,
      ease: 'power2.inOut'
    })
})
</script>

<style scoped>
.brand-animation-container {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100vh;
  background: var(--color-white);
  display: flex;
  align-items: center;
  justify-content: center;
  overflow: hidden;
  z-index: 9999;
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
  left: 0;
  width: 100%;
  height: 100%;
  display: flex;
  flex-direction: column;
}

.wave {
  flex: 1;
  will-change: transform, opacity;
}

.wave-1 {
  background: linear-gradient(90deg, var(--color-primary) 0%, var(--color-primary-dark) 100%);
}

.wave-2 {
  background: linear-gradient(90deg, var(--color-secondary) 0%, var(--color-secondary-dark) 100%);
}

.wave-3 {
  background: linear-gradient(90deg, var(--color-dark) 0%, var(--color-dark-lighter) 100%);
}

.brand-content {
  position: relative;
  z-index: 10;
  text-align: center;
  padding: 2rem;
}

.brand-name {
  font-size: clamp(2.5rem, 8vw, 4rem);
  font-weight: 800;
  color: var(--color-white);
  text-shadow: 0 4px 20px rgba(0, 0, 0, 0.4);
  margin-bottom: 1rem;
  letter-spacing: 0.02em;
  will-change: transform, opacity;
}

.brand-tagline {
  font-size: clamp(1rem, 3vw, 1.5rem);
  color: var(--color-white);
  font-weight: 500;
  text-shadow: 0 2px 10px rgba(0, 0, 0, 0.3);
  will-change: transform, opacity;
}

@media (max-width: 768px) {
  .brand-content {
    padding: 1.5rem;
  }
}

@media (max-width: 480px) {
  .brand-content {
    padding: 1rem;
  }

  .brand-name {
    margin-bottom: 0.75rem;
  }
}
</style>
