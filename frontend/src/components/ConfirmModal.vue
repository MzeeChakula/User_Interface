<template>
  <BaseModal v-model="isOpen" :size="size" :close-on-overlay="closeOnOverlay">
    <div class="confirm-modal">
      <!-- Icon -->
      <div class="confirm-icon" :class="iconColorClass">
        <component :is="iconComponent" :size="48" />
      </div>

      <!-- Title -->
      <h3 class="confirm-title">{{ title }}</h3>

      <!-- Message -->
      <p class="confirm-message">{{ message }}</p>

      <!-- Actions -->
      <div class="confirm-actions">
        <button
          @click="handleCancel"
          class="btn btn-secondary"
          :disabled="loading"
        >
          {{ cancelText }}
        </button>
        <button
          @click="handleConfirm"
          class="btn"
          :class="confirmButtonClass"
          :disabled="loading"
        >
          <span v-if="loading" class="btn-loader"></span>
          <span v-else>{{ confirmText }}</span>
        </button>
      </div>
    </div>
  </BaseModal>
</template>

<script setup>
import { ref, computed } from 'vue'
import { AlertTriangle, AlertCircle, Info, CheckCircle, Trash2, LogOut } from 'lucide-vue-next'
import BaseModal from './BaseModal.vue'

const props = defineProps({
  modelValue: {
    type: Boolean,
    required: true
  },
  title: {
    type: String,
    required: true
  },
  message: {
    type: String,
    required: true
  },
  confirmText: {
    type: String,
    default: 'Confirm'
  },
  cancelText: {
    type: String,
    default: 'Cancel'
  },
  type: {
    type: String,
    default: 'warning', // warning, danger, info, success
    validator: (value) => ['warning', 'danger', 'info', 'success'].includes(value)
  },
  size: {
    type: String,
    default: 'small'
  },
  closeOnOverlay: {
    type: Boolean,
    default: false
  },
  onConfirm: {
    type: Function,
    default: null
  }
})

const emit = defineEmits(['update:modelValue', 'confirm', 'cancel'])

const isOpen = computed({
  get: () => props.modelValue,
  set: (value) => emit('update:modelValue', value)
})

const loading = ref(false)

const iconComponent = computed(() => {
  const icons = {
    warning: AlertTriangle,
    danger: Trash2,
    info: Info,
    success: CheckCircle
  }
  return icons[props.type] || AlertCircle
})

const iconColorClass = computed(() => `icon-${props.type}`)

const confirmButtonClass = computed(() => {
  const classes = {
    warning: 'btn-warning',
    danger: 'btn-danger',
    info: 'btn-primary',
    success: 'btn-success'
  }
  return classes[props.type] || 'btn-primary'
})

const handleConfirm = async () => {
  if (props.onConfirm) {
    loading.value = true
    try {
      await props.onConfirm()
      isOpen.value = false
      emit('confirm')
    } catch (error) {
      console.error('Confirmation error:', error)
    } finally {
      loading.value = false
    }
  } else {
    isOpen.value = false
    emit('confirm')
  }
}

const handleCancel = () => {
  isOpen.value = false
  emit('cancel')
}
</script>

<style scoped>
.confirm-modal {
  text-align: center;
}

.confirm-icon {
  width: 80px;
  height: 80px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  margin: 0 auto 1.5rem;
}

.icon-warning {
  background: #FEF3C7;
  color: #F59E0B;
}

.icon-danger {
  background: #FEE2E2;
  color: #EF4444;
}

.icon-info {
  background: #DBEAFE;
  color: #3B82F6;
}

.icon-success {
  background: #D1FAE5;
  color: #10B981;
}

.confirm-title {
  font-size: 1.5rem;
  font-weight: 700;
  color: var(--color-dark);
  margin: 0 0 1rem 0;
}

.confirm-message {
  font-size: 1rem;
  color: var(--color-gray-600);
  line-height: 1.6;
  margin: 0 0 2rem 0;
}

.confirm-actions {
  display: flex;
  gap: 1rem;
}

.btn {
  flex: 1;
  padding: 0.875rem 1.5rem;
  border-radius: 10px;
  font-weight: 600;
  font-size: 1rem;
  cursor: pointer;
  transition: all 0.3s ease;
  border: none;
  position: relative;
}

.btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.btn-primary {
  background: linear-gradient(135deg, var(--color-primary) 0%, var(--color-secondary) 100%);
  color: white;
}

.btn-primary:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 5px 15px rgba(217, 0, 0, 0.3);
}

.btn-warning {
  background: linear-gradient(135deg, #F59E0B 0%, #D97706 100%);
  color: white;
}

.btn-warning:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 5px 15px rgba(245, 158, 11, 0.3);
}

.btn-danger {
  background: linear-gradient(135deg, #EF4444 0%, #DC2626 100%);
  color: white;
}

.btn-danger:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 5px 15px rgba(239, 68, 68, 0.3);
}

.btn-success {
  background: linear-gradient(135deg, #10B981 0%, #059669 100%);
  color: white;
}

.btn-success:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 5px 15px rgba(16, 185, 129, 0.3);
}

.btn-secondary {
  background: var(--color-gray-200);
  color: var(--color-gray-700);
}

.btn-secondary:hover:not(:disabled) {
  background: var(--color-gray-300);
}

.btn-loader {
  display: inline-block;
  width: 16px;
  height: 16px;
  border: 2px solid rgba(255, 255, 255, 0.3);
  border-top-color: white;
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

/* Mobile responsiveness */
@media (max-width: 640px) {
  .confirm-icon {
    width: 64px;
    height: 64px;
  }

  .confirm-icon :deep(svg) {
    width: 36px;
    height: 36px;
  }

  .confirm-title {
    font-size: 1.25rem;
  }

  .confirm-message {
    font-size: 0.9375rem;
  }

  .confirm-actions {
    flex-direction: column-reverse;
  }

  .btn {
    width: 100%;
  }
}
</style>
