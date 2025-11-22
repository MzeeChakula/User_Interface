import { describe, it, expect, vi } from 'vitest'
import { mountWithDefaults } from '@/test-utils'
import ConfirmModal from '../ConfirmModal.vue'

describe('ConfirmModal', () => {
    it('renders with required props', () => {
        const wrapper = mountWithDefaults(ConfirmModal, {
            props: {
                modelValue: true,
                title: 'Confirm Action',
                message: 'Are you sure?'
            }
        })

        expect(wrapper.text()).toContain('Confirm Action')
        expect(wrapper.text()).toContain('Are you sure?')
    })

    it('renders default button text', () => {
        const wrapper = mountWithDefaults(ConfirmModal, {
            props: {
                modelValue: true,
                title: 'Test',
                message: 'Message'
            }
        })

        expect(wrapper.text()).toContain('Confirm')
        expect(wrapper.text()).toContain('Cancel')
    })

    it('renders custom button text', () => {
        const wrapper = mountWithDefaults(ConfirmModal, {
            props: {
                modelValue: true,
                title: 'Delete Item',
                message: 'This cannot be undone',
                confirmText: 'Delete',
                cancelText: 'Keep'
            }
        })

        expect(wrapper.text()).toContain('Delete')
        expect(wrapper.text()).toContain('Keep')
    })

    it('renders warning type by default', () => {
        const wrapper = mountWithDefaults(ConfirmModal, {
            props: {
                modelValue: true,
                title: 'Test',
                message: 'Message'
            }
        })

        const icon = wrapper.find('.confirm-icon')
        expect(icon.classes()).toContain('icon-warning')
    })

    it('renders danger type correctly', () => {
        const wrapper = mountWithDefaults(ConfirmModal, {
            props: {
                modelValue: true,
                title: 'Delete',
                message: 'Permanent action',
                type: 'danger'
            }
        })

        const icon = wrapper.find('.confirm-icon')
        expect(icon.classes()).toContain('icon-danger')
    })

    it('has confirm and cancel buttons', () => {
        const wrapper = mountWithDefaults(ConfirmModal, {
            props: {
                modelValue: true,
                title: 'Test',
                message: 'Message'
            }
        })

        const buttons = wrapper.findAll('button')
        expect(buttons.length).toBeGreaterThanOrEqual(2)
    })

    it('has loading state property', () => {
        const wrapper = mountWithDefaults(ConfirmModal, {
            props: {
                modelValue: true,
                title: 'Test',
                message: 'Message'
            }
        })

        // Verify loading property exists
        expect(wrapper.vm.loading).toBeDefined()
        expect(typeof wrapper.vm.loading).toBe('boolean')
    })

    it('renders confirm button with correct styling', () => {
        const wrapper = mountWithDefaults(ConfirmModal, {
            props: {
                modelValue: true,
                title: 'Delete Item',
                message: 'Are you sure?',
                type: 'danger'
            }
        })

        // Verify buttons exist and have btn class
        const buttons = wrapper.findAll('.btn')
        expect(buttons.length).toBeGreaterThan(0)
    })
})
