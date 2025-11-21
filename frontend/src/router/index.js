import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '../stores/auth'
import { useAppStore } from '../stores/app'

const routes = [
  {
    path: '/',
    name: 'Home',
    redirect: () => {
      const appStore = useAppStore()
      const authStore = useAuthStore()

      if (appStore.isFirstTime) {
        return { name: 'BrandAnimation' }
      } else if (!authStore.isAuthenticated) {
        return { name: 'Auth' }
      } else {
        return { name: 'Chat' }
      }
    }
  },
  {
    path: '/brand-animation',
    name: 'BrandAnimation',
    component: () => import('../views/BrandAnimation.vue'),
    meta: { requiresGuest: true }
  },
  {
    path: '/welcome',
    name: 'Welcome',
    component: () => import('../views/Welcome.vue'),
    meta: { requiresGuest: true }
  },
  {
    path: '/auth',
    name: 'Auth',
    component: () => import('../views/Auth.vue'),
    meta: { requiresGuest: true }
  },
  {
    path: '/chat',
    name: 'Chat',
    component: () => import('../views/Chat.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/profile',
    name: 'Profile',
    component: () => import('../views/Profile.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/settings',
    name: 'Settings',
    component: () => import('../views/Settings.vue'),
    meta: { requiresAuth: true }
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

router.beforeEach((to, from, next) => {
  const authStore = useAuthStore()
  authStore.checkAuth()

  if (to.meta.requiresAuth && !authStore.isAuthenticated) {
    next({ name: 'Auth' })
  } else if (to.meta.requiresGuest && authStore.isAuthenticated) {
    next({ name: 'Chat' })
  } else {
    next()
  }
})

export default router
