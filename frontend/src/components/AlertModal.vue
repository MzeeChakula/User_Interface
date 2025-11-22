<template>
  <BaseModal v-model="isOpen" :size="size" :close-on-overlay="true">
    <div class="alert-modal">
      <!-- Icon -->
      <div class="alert-icon" :class="iconColorClass">
        <component :is="iconComponent" :size="48" />
      </div>

      <!-- Title -->
      <h3 class="alert-title">{{ title }}</h3>

      <!-- Message -->
      <p class="alert-message" v-html="message"></p>

      <!-- Action -->
      <button
        @click="handleClose"
        class="btn btn-primary btn-full"
      >
        {{ buttonText }}
      </button>
    </div>
  </BaseModal>
</template>

<script setup>
import { computed } from 'vue'
import { CheckCircle, AlertCircle, Info, XCircle } from 'lucide-vue-next'
import BaseModal from './BaseModal.vue'

const props = defineProps({
  modelValue: {
    type: Boolean,
    required: true
  },
  title: {
    type: String,
    default: 'Notification'
  },
  message: {
    type: String,
    required: true
  },
  buttonText: {
    type: String,
    default: 'Got it'
  },
  type: {
    type: String,
    default: 'info', // success, error, info, warning
    validator: (value) => ['success', 'error', 'info', 'warning'].includes(value)
  },
  size: {
    type: String,
    default: 'small'
  }
})

const emit = defineEmits(['update:modelValue', 'close'])

const isOpen = computed({
  get: () => props.modelValue,
  set: (value) => emit('update:modelValue', value)
})

const iconComponent = computed(() => {
  const icons = {
    success: CheckCircle,
    error: XCircle,
    info: Info,
    warning: AlertCircle
  }
  return icons[props.type] || Info
})

const iconColorClass = computed(() => `icon-${props.type}`)

const handleClose = () => {
  isOpen.value = false
  emit('close')
}
</script>

<style scoped>
.alert-modal {
  text-align: center;
}

.alert-icon {
  width: 80px;
  height: 80px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  margin: 0 auto 1.5rem;
}

.icon-success {
  background: #D1FAE5;
  color: #10B981;
}

.icon-error {
  background: #FEE2E2;
  color: #EF4444;
}

.icon-info {
  background: #DBEAFE;
  color: #3B82F6;
}

.icon-warning {
  background: #FEF3C7;
  color: #F59E0B;
}

.alert-title {
  font-size: 1.5rem;
  font-weight: 700;
  color: var(--color-dark);
  margin: 0 0 1rem 0;
}

.alert-message {
  font-size: 1rem;
  color: var(--color-gray-600);
  line-height: 1.6;
  margin: 0 0 2rem 0;
}

.alert-message :deep(strong) {
  color: var(--color-dark);
  font-weight: 600;
}

.btn {
  padding: 0.875rem 1.5rem;
  border-radius: 10px;
  font-weight: 600;
  font-size: 1rem;
  cursor: pointer;
  transition: all 0.3s ease;
  border: none;
}

.btn-full {
  width: 100%;
}

.btn-primary {
  background: linear-gradient(135deg, var(--color-primary) 0%, var(--color-secondary) 100%);
  color: white;
}

.btn-primary:hover {
  transform: translateY(-2px);
  box-shadow: 0 5px 15px rgba(217, 0, 0, 0.3);
}

/* Mobile responsiveness */
@media (max-width: 640px) {
  .alert-icon {
    width: 64px;
    height: 64px;
  }

  .alert-icon :deep(svg) {
    width: 36px;
    height: 36px;
  }

  .alert-title {
    font-size: 1.25rem;
  }

  .alert-message {
    font-size: 0.9375rem;
  }
}
</style>
