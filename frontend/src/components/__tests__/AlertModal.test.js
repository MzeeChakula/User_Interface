import { describe, it, expect } from 'vitest'
import { mountWithDefaults } from '@/test-utils'
import AlertModal from '../AlertModal.vue'

describe('AlertModal', () => {
    it('renders with default props', () => {
        const wrapper = mountWithDefaults(AlertModal, {
            props: {
                modelValue: true,
                message: 'Test message'
            }
        })

        expect(wrapper.text()).toContain('Test message')
        expect(wrapper.text()).toContain('Notification') // default title
        expect(wrapper.text()).toContain('Got it') // default button text
    })

    it('renders with custom title and button text', () => {
        const wrapper = mountWithDefaults(AlertModal, {
            props: {
                modelValue: true,
                title: 'Custom Title',
                message: 'Custom message',
                buttonText: 'Close'
            }
        })

        expect(wrapper.text()).toContain('Custom Title')
        expect(wrapper.text()).toContain('Close')
    })

    it('renders success type with correct icon', () => {
        const wrapper = mountWithDefaults(AlertModal, {
            props: {
                modelValue: true,
                message: 'Success message',
                type: 'success'
            }
        })

        const iconDiv = wrapper.find('.alert-icon')
        expect(iconDiv.classes()).toContain('icon-success')
    })

    it('renders error type with correct icon', () => {
        const wrapper = mountWithDefaults(AlertModal, {
            props: {
                modelValue: true,
                message: 'Error message',
                type: 'error'
            }
        })

        const iconDiv = wrapper.find('.alert-icon')
        expect(iconDiv.classes()).toContain('icon-error')
    })

    it('renders warning type with correct icon', () => {
        const wrapper = mountWithDefaults(AlertModal, {
            props: {
                modelValue: true,
                message: 'Warning message',
                type: 'warning'
            }
        })

        const iconDiv = wrapper.find('.alert-icon')
        expect(iconDiv.classes()).toContain('icon-warning')
    })

    it('renders info type with correct icon', () => {
        const wrapper = mountWithDefaults(AlertModal, {
            props: {
                modelValue: true,
                message: 'Info message',
                type: 'info'
            }
        })

        const iconDiv = wrapper.find('.alert-icon')
        expect(iconDiv.classes()).toContain('icon-info')
    })

    it('renders HTML in message', () => {
        const wrapper = mountWithDefaults(AlertModal, {
            props: {
                modelValue: true,
                message: 'Message with <strong>bold text</strong>'
            }
        })

        const message = wrapper.find('.alert-message')
        expect(message.html()).toContain('<strong>bold text</strong>')
    })

    it('passes size prop to BaseModal', () => {
        const wrapper = mountWithDefaults(AlertModal, {
            props: {
                modelValue: true,
                message: 'Test message',
                size: 'large'
            }
        })

        // BaseModal should receive the size prop
        expect(wrapper.findComponent({ name: 'BaseModal' }).props('size')).toBe('large')
    })
})
