<template>
  <Teleport to="body">
    <TransitionGroup name="toast" tag="div" class="toast-container" :class="positionClass">
      <div
        v-for="toast in toasts"
        :key="toast.id"
        class="toast"
        :class="[`toast-${toast.type}`, { 'toast-dismissible': toast.dismissible }]"
        @click="toast.dismissible && removeToast(toast.id)"
      >
        <div class="toast-icon">
          <component :is="getIcon(toast.type)" :size="20" />
        </div>
        <div class="toast-content">
          <div class="toast-title">{{ toast.title }}</div>
          <div v-if="toast.message" class="toast-message">{{ toast.message }}</div>
        </div>
        <button
          v-if="toast.dismissible"
          @click.stop="removeToast(toast.id)"
          class="toast-close"
          aria-label="Close"
        >
          <X :size="16" />
        </button>
      </div>
    </TransitionGroup>
  </Teleport>
</template>

<script setup>
import { ref } from 'vue'
import { CheckCircle, AlertCircle, Info, XCircle, X } from 'lucide-vue-next'

const props = defineProps({
  position: {
    type: String,
    default: 'top-right', // top-right, top-left, bottom-right, bottom-left, top-center, bottom-center
    validator: (value) => [
      'top-right',
      'top-left',
      'bottom-right',
      'bottom-left',
      'top-center',
      'bottom-center'
    ].includes(value)
  }
})

const toasts = ref([])
let toastId = 0

const positionClass = `toast-position-${props.position}`

const getIcon = (type) => {
  const icons = {
    success: CheckCircle,
    error: XCircle,
    info: Info,
    warning: AlertCircle
  }
  return icons[type] || Info
}

const addToast = ({ title, message = '', type = 'info', duration = 3000, dismissible = true }) => {
  const id = ++toastId
  const toast = { id, title, message, type, dismissible }

  toasts.value.push(toast)

  if (duration > 0) {
    setTimeout(() => {
      removeToast(id)
    }, duration)
  }

  return id
}

const removeToast = (id) => {
  const index = toasts.value.findIndex(t => t.id === id)
  if (index > -1) {
    toasts.value.splice(index, 1)
  }
}

const clearAll = () => {
  toasts.value = []
}

// Expose methods
defineExpose({
  addToast,
  removeToast,
  clearAll
})
</script>

<style scoped>
.toast-container {
  position: fixed;
  z-index: 10000;
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
  pointer-events: none;
}

.toast-position-top-right {
  top: 1rem;
  right: 1rem;
}

.toast-position-top-left {
  top: 1rem;
  left: 1rem;
}

.toast-position-bottom-right {
  bottom: 1rem;
  right: 1rem;
}

.toast-position-bottom-left {
  bottom: 1rem;
  left: 1rem;
}

.toast-position-top-center {
  top: 1rem;
  left: 50%;
  transform: translateX(-50%);
}

.toast-position-bottom-center {
  bottom: 1rem;
  left: 50%;
  transform: translateX(-50%);
}

.toast {
  display: flex;
  align-items: flex-start;
  gap: 0.75rem;
  background: white;
  border-radius: 12px;
  padding: 1rem 1.25rem;
  box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04);
  min-width: 300px;
  max-width: 400px;
  pointer-events: auto;
  border-left: 4px solid;
  transition: all 0.3s ease;
}

.toast:hover {
  transform: translateY(-2px);
  box-shadow: 0 15px 30px -5px rgba(0, 0, 0, 0.15), 0 10px 10px -5px rgba(0, 0, 0, 0.04);
}

.toast-dismissible {
  cursor: pointer;
}

.toast-success {
  border-left-color: #10B981;
}

.toast-error {
  border-left-color: #EF4444;
}

.toast-info {
  border-left-color: #3B82F6;
}

.toast-warning {
  border-left-color: #F59E0B;
}

.toast-icon {
  flex-shrink: 0;
  width: 32px;
  height: 32px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
}

.toast-success .toast-icon {
  background: #D1FAE5;
  color: #10B981;
}

.toast-error .toast-icon {
  background: #FEE2E2;
  color: #EF4444;
}

.toast-info .toast-icon {
  background: #DBEAFE;
  color: #3B82F6;
}

.toast-warning .toast-icon {
  background: #FEF3C7;
  color: #F59E0B;
}

.toast-content {
  flex: 1;
  min-width: 0;
}

.toast-title {
  font-weight: 600;
  font-size: 0.9375rem;
  color: var(--color-dark);
  line-height: 1.4;
}

.toast-message {
  font-size: 0.875rem;
  color: var(--color-gray-600);
  margin-top: 0.25rem;
  line-height: 1.4;
}

.toast-close {
  flex-shrink: 0;
  width: 24px;
  height: 24px;
  border-radius: 50%;
  background: var(--color-gray-100);
  border: none;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  color: var(--color-gray-600);
  transition: all 0.2s ease;
  padding: 0;
}

.toast-close:hover {
  background: var(--color-gray-200);
  color: var(--color-dark);
}

/* Toast animations */
.toast-enter-active,
.toast-leave-active {
  transition: all 0.3s ease;
}

.toast-position-top-right .toast-enter-from,
.toast-position-top-left .toast-enter-from,
.toast-position-top-center .toast-enter-from {
  opacity: 0;
  transform: translateY(-20px);
}

.toast-position-bottom-right .toast-enter-from,
.toast-position-bottom-left .toast-enter-from,
.toast-position-bottom-center .toast-enter-from {
  opacity: 0;
  transform: translateY(20px);
}

.toast-leave-to {
  opacity: 0;
  transform: translateX(100px);
}

.toast-move {
  transition: transform 0.3s ease;
}

/* Mobile responsiveness */
@media (max-width: 640px) {
  .toast-container {
    left: 1rem !important;
    right: 1rem !important;
    transform: none !important;
  }

  .toast {
    min-width: auto;
    max-width: none;
  }
}
</style>
