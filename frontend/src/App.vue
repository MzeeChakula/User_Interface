<script setup>
import { onMounted } from 'vue'
import { useRegisterSW } from 'virtual:pwa-register/vue'
import AppLoader from './components/AppLoader.vue'
import { useAppStore } from './stores/app'
import { useOnlineStatus } from './composables/useOnlineStatus'

const appStore = useAppStore()
const { isOnline } = useOnlineStatus()

const { updateServiceWorker } = useRegisterSW({
  onRegistered(r) {
    console.log('Service Worker registered:', r)
  },
  onRegisterError(error) {
    console.error('Service Worker registration error:', error)
  }
})

onMounted(() => {
  appStore.setOnlineStatus(isOnline.value)
})
</script>

<template>
  <div id="app">
    <AppLoader v-if="appStore.showLoader" />
    <router-view v-else />
  </div>
</template>

<style>
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

body {
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', 'Oxygen',
    'Ubuntu', 'Cantarell', 'Fira Sans', 'Droid Sans', 'Helvetica Neue',
    sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
}

#app {
  width: 100%;
  min-height: 100vh;
}
</style>
