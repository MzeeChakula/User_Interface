import { ref, h, render } from 'vue'
import AlertModal from '../components/AlertModal.vue'
import ConfirmModal from '../components/ConfirmModal.vue'
import ToastNotification from '../components/ToastNotification.vue'

// Toast container singleton
let toastContainer = null

const getToastContainer = () => {
  if (!toastContainer) {
    const container = document.createElement('div')
    document.body.appendChild(container)

    const vnode = h(ToastNotification, { position: 'top-right' })
    render(vnode, container)
    toastContainer = vnode.component.exposed
  }
  return toastContainer
}

export function useModals() {
  /**
   * Show an alert modal
   * @param {Object} options - Alert options
   * @param {string} options.title - Alert title
   * @param {string} options.message - Alert message (supports HTML)
   * @param {string} options.type - Alert type: 'success', 'error', 'info', 'warning'
   * @param {string} options.buttonText - Button text
   * @returns {Promise<void>}
   */
  const showAlert = (options) => {
    return new Promise((resolve) => {
      const {
        title = 'Notification',
        message,
        type = 'info',
        buttonText = 'Got it'
      } = options

      const container = document.createElement('div')
      document.body.appendChild(container)

      const isOpen = ref(true)

      const handleClose = () => {
        isOpen.value = false
        setTimeout(() => {
          render(null, container)
          document.body.removeChild(container)
          resolve()
        }, 300)
      }

      const vnode = h(AlertModal, {
        modelValue: isOpen.value,
        'onUpdate:modelValue': (value) => {
          isOpen.value = value
        },
        title,
        message,
        type,
        buttonText,
        onClose: handleClose
      })

      render(vnode, container)
    })
  }

  /**
   * Show a confirmation modal
   * @param {Object} options - Confirmation options
   * @param {string} options.title - Modal title
   * @param {string} options.message - Modal message
   * @param {string} options.type - Modal type: 'warning', 'danger', 'info', 'success'
   * @param {string} options.confirmText - Confirm button text
   * @param {string} options.cancelText - Cancel button text
   * @param {Function} options.onConfirm - Async function to call on confirm
   * @returns {Promise<boolean>} - true if confirmed, false if cancelled
   */
  const showConfirm = (options) => {
    return new Promise((resolve) => {
      const {
        title = 'Confirm Action',
        message,
        type = 'warning',
        confirmText = 'Confirm',
        cancelText = 'Cancel',
        onConfirm = null
      } = options

      const container = document.createElement('div')
      document.body.appendChild(container)

      const isOpen = ref(true)

      const cleanup = () => {
        setTimeout(() => {
          render(null, container)
          document.body.removeChild(container)
        }, 300)
      }

      const handleConfirm = async () => {
        isOpen.value = false
        cleanup()
        resolve(true)
      }

      const handleCancel = () => {
        isOpen.value = false
        cleanup()
        resolve(false)
      }

      const vnode = h(ConfirmModal, {
        modelValue: isOpen.value,
        'onUpdate:modelValue': (value) => {
          isOpen.value = value
        },
        title,
        message,
        type,
        confirmText,
        cancelText,
        onConfirm,
        onConfirm: handleConfirm,
        onCancel: handleCancel
      })

      render(vnode, container)
    })
  }

  /**
   * Show a toast notification
   * @param {Object} options - Toast options
   * @param {string} options.title - Toast title
   * @param {string} options.message - Toast message (optional)
   * @param {string} options.type - Toast type: 'success', 'error', 'info', 'warning'
   * @param {number} options.duration - Duration in ms (0 for persistent)
   * @param {boolean} options.dismissible - Whether toast can be dismissed
   * @returns {number} - Toast ID
   */
  const showToast = (options) => {
    const {
      title,
      message = '',
      type = 'info',
      duration = 3000,
      dismissible = true
    } = options

    const toast = getToastContainer()
    return toast.addToast({ title, message, type, duration, dismissible })
  }

  /**
   * Show a success toast
   * @param {string} title - Toast title
   * @param {string} message - Toast message (optional)
   */
  const showSuccess = (title, message = '') => {
    return showToast({ title, message, type: 'success' })
  }

  /**
   * Show an error toast
   * @param {string} title - Toast title
   * @param {string} message - Toast message (optional)
   */
  const showError = (title, message = '') => {
    return showToast({ title, message, type: 'error' })
  }

  /**
   * Show an info toast
   * @param {string} title - Toast title
   * @param {string} message - Toast message (optional)
   */
  const showInfo = (title, message = '') => {
    return showToast({ title, message, type: 'info' })
  }

  /**
   * Show a warning toast
   * @param {string} title - Toast title
   * @param {string} message - Toast message (optional)
   */
  const showWarning = (title, message = '') => {
    return showToast({ title, message, type: 'warning' })
  }

  return {
    showAlert,
    showConfirm,
    showToast,
    showSuccess,
    showError,
    showInfo,
    showWarning
  }
}
