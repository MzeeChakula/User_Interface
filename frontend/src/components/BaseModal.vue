<template>
  <Teleport to="body">
    <Transition name="modal">
      <div v-if="modelValue" class="modal-overlay" @click="handleOverlayClick">
        <div class="modal-container" :class="sizeClass" @click.stop>
          <!-- Close button -->
          <button v-if="showClose" @click="close" class="modal-close" aria-label="Close">
            <X :size="20" />
          </button>

          <!-- Modal content -->
          <div class="modal-content">
            <slot></slot>
          </div>
        </div>
      </div>
    </Transition>
  </Teleport>
</template>

<script setup>
import { computed } from 'vue'
import { X } from 'lucide-vue-next'

const props = defineProps({
  modelValue: {
    type: Boolean,
    required: true
  },
  size: {
    type: String,
    default: 'medium', // small, medium, large
    validator: (value) => ['small', 'medium', 'large'].includes(value)
  },
  closeOnOverlay: {
    type: Boolean,
    default: true
  },
  showClose: {
    type: Boolean,
    default: true
  }
})

const emit = defineEmits(['update:modelValue', 'close'])

const sizeClass = computed(() => `modal-${props.size}`)

const close = () => {
  emit('update:modelValue', false)
  emit('close')
}

const handleOverlayClick = () => {
  if (props.closeOnOverlay) {
    close()
  }
}
</script>

<style scoped>
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.6);
  backdrop-filter: blur(4px);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 9999;
  padding: 1rem;
}

.modal-container {
  background: white;
  border-radius: 16px;
  box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.25);
  position: relative;
  max-height: 90vh;
  overflow-y: auto;
  width: 100%;
}

.modal-small {
  max-width: 400px;
}

.modal-medium {
  max-width: 500px;
}

.modal-large {
  max-width: 700px;
}

.modal-close {
  position: absolute;
  top: 1rem;
  right: 1rem;
  width: 36px;
  height: 36px;
  border-radius: 50%;
  background: var(--color-gray-100);
  border: none;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  color: var(--color-gray-600);
  transition: all 0.2s ease;
  z-index: 10;
}

.modal-close:hover {
  background: var(--color-gray-200);
  color: var(--color-dark);
  transform: scale(1.1);
}

.modal-content {
  padding: 2rem;
}

/* Modal animations */
.modal-enter-active,
.modal-leave-active {
  transition: all 0.3s ease;
}

.modal-enter-from,
.modal-leave-to {
  opacity: 0;
}

.modal-enter-from .modal-container,
.modal-leave-to .modal-container {
  transform: scale(0.9) translateY(-20px);
}

.modal-enter-active .modal-container,
.modal-leave-active .modal-container {
  transition: all 0.3s ease;
}

/* Mobile responsiveness */
@media (max-width: 640px) {
  .modal-container {
    max-height: 95vh;
    border-radius: 12px;
  }

  .modal-content {
    padding: 1.5rem;
  }

  .modal-small,
  .modal-medium,
  .modal-large {
    max-width: 100%;
  }
}
</style>
