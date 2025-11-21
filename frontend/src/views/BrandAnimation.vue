<template>
  <div class="brand-animation-container">
    <div class="animation-wrapper">
      <!-- Animated Wave SVGs -->
      <svg class="wave-svg wave-svg-1" ref="wave1" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1440 320" preserveAspectRatio="none">
        <path fill="url(#gradient1)" d="M0,160L48,170.7C96,181,192,203,288,197.3C384,192,480,160,576,149.3C672,139,768,149,864,170.7C960,192,1056,224,1152,224C1248,224,1344,192,1392,176L1440,160L1440,320L1392,320C1344,320,1248,320,1152,320C1056,320,960,320,864,320C768,320,672,320,576,320C480,320,384,320,288,320C192,320,96,320,48,320L0,320Z"></path>
        <defs>
          <linearGradient id="gradient1" x1="0%" y1="0%" x2="100%" y2="0%">
            <stop offset="0%" style="stop-color:#D90000;stop-opacity:1" />
            <stop offset="100%" style="stop-color:#B00000;stop-opacity:1" />
          </linearGradient>
        </defs>
      </svg>

      <svg class="wave-svg wave-svg-2" ref="wave2" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1440 320" preserveAspectRatio="none">
        <path fill="url(#gradient2)" d="M0,96L48,112C96,128,192,160,288,165.3C384,171,480,149,576,133.3C672,117,768,107,864,122.7C960,139,1056,181,1152,186.7C1248,192,1344,160,1392,144L1440,128L1440,320L1392,320C1344,320,1248,320,1152,320C1056,320,960,320,864,320C768,320,672,320,576,320C480,320,384,320,288,320C192,320,96,320,48,320L0,320Z"></path>
        <defs>
          <linearGradient id="gradient2" x1="0%" y1="0%" x2="100%" y2="0%">
            <stop offset="0%" style="stop-color:#FCDC04;stop-opacity:1" />
            <stop offset="100%" style="stop-color:#E6C804;stop-opacity:1" />
          </linearGradient>
        </defs>
      </svg>

      <svg class="wave-svg wave-svg-3" ref="wave3" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1440 320" preserveAspectRatio="none">
        <path fill="url(#gradient3)" d="M0,224L48,213.3C96,203,192,181,288,181.3C384,181,480,203,576,208C672,213,768,203,864,192C960,181,1056,171,1152,165.3C1248,160,1344,160,1392,160L1440,160L1440,320L1392,320C1344,320,1248,320,1152,320C1056,320,960,320,864,320C768,320,672,320,576,320C480,320,384,320,288,320C192,320,96,320,48,320L0,320Z"></path>
        <defs>
          <linearGradient id="gradient3" x1="0%" y1="0%" x2="100%" y2="0%">
            <stop offset="0%" style="stop-color:#1E1E1E;stop-opacity:1" />
            <stop offset="100%" style="stop-color:#2A2A2A;stop-opacity:1" />
          </linearGradient>
        </defs>
      </svg>

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
    y: '100%',
    opacity: 0
  })

  gsap.set([brandName.value, brandTagline.value], {
    opacity: 0,
    scale: 0.8,
    y: 20
  })

  // Animate waves flowing up with stagger
  timeline
    .to(wave1.value, {
      y: '0%',
      opacity: 1,
      duration: 1,
      ease: 'power2.out'
    })
    .to(wave2.value, {
      y: '0%',
      opacity: 0.9,
      duration: 1.2,
      ease: 'power2.out'
    }, '-=0.7')
    .to(wave3.value, {
      y: '0%',
      opacity: 0.8,
      duration: 1.4,
      ease: 'power2.out'
    }, '-=0.9')
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

.wave-svg {
  position: absolute;
  bottom: 0;
  left: 0;
  width: 100%;
  height: 100%;
  will-change: transform, opacity;
}

.wave-svg-1 {
  z-index: 3;
  animation: wave-float-1 6s ease-in-out infinite;
}

.wave-svg-2 {
  z-index: 2;
  animation: wave-float-2 7s ease-in-out infinite;
  animation-delay: 0.5s;
}

.wave-svg-3 {
  z-index: 1;
  animation: wave-float-3 8s ease-in-out infinite;
  animation-delay: 1s;
}

@keyframes wave-float-1 {
  0%, 100% {
    transform: translateY(0px) translateX(0px);
  }
  50% {
    transform: translateY(-15px) translateX(10px);
  }
}

@keyframes wave-float-2 {
  0%, 100% {
    transform: translateY(0px) translateX(0px);
  }
  50% {
    transform: translateY(-20px) translateX(-10px);
  }
}

@keyframes wave-float-3 {
  0%, 100% {
    transform: translateY(0px) translateX(0px);
  }
  50% {
    transform: translateY(-10px) translateX(15px);
  }
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
