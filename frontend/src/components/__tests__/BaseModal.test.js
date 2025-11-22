import { describe, it, expect, vi } from 'vitest'
import { mount } from '@vue/test-utils'
import { createPinia } from 'pinia'
import BaseModal from '../BaseModal.vue'

describe('BaseModal', () => {
    const createWrapper = (props = {}, slots = {}) => {
        return mount(BaseModal, {
            props: {
                modelValue: false,
                ...props
            },
            slots,
            global: {
                plugins: [createPinia()],
                stubs: {
                    teleport: true
                }
            }
        })
    }

    it('renders when modelValue is true', () => {
        const wrapper = createWrapper({ modelValue: true })

        expect(wrapper.find('.modal-overlay').exists()).toBe(true)
    })

    it('does not render when modelValue is false', () => {
        const wrapper = createWrapper({ modelValue: false })

        expect(wrapper.find('.modal-overlay').exists()).toBe(false)
    })

    it('renders slot content', () => {
        const wrapper = createWrapper(
            { modelValue: true },
            { default: '<div class="test-content">Test Content</div>' }
        )

        expect(wrapper.html()).toContain('Test Content')
    })

    it('emits update:modelValue when overlay is clicked and closeOnOverlay is true', async () => {
        const wrapper = createWrapper({
            modelValue: true,
            closeOnOverlay: true
        })

        const overlay = wrapper.find('.modal-overlay')
        await overlay.trigger('click')

        expect(wrapper.emitted('update:modelValue')).toBeTruthy()
        expect(wrapper.emitted('update:modelValue')[0]).toEqual([false])
    })

    it('does not close when overlay is clicked and closeOnOverlay is false', async () => {
        const wrapper = createWrapper({
            modelValue: true,
            closeOnOverlay: false
        })

        const overlay = wrapper.find('.modal-overlay')
        await overlay.trigger('click')

        expect(wrapper.emitted('update:modelValue')).toBeFalsy()
    })

    it('applies correct size class', () => {
        const wrapper = createWrapper({
            modelValue: true,
            size: 'large'
        })

        const modalContainer = wrapper.find('.modal-container')
        expect(modalContainer.classes()).toContain('modal-large')
    })

    it('applies medium size by default', () => {
        const wrapper = createWrapper({ modelValue: true })

        const modalContainer = wrapper.find('.modal-container')
        expect(modalContainer.classes()).toContain('modal-medium')
    })

    it('stops propagation when modal container is clicked', async () => {
        const wrapper = createWrapper({
            modelValue: true,
            closeOnOverlay: true
        })

        const modalContainer = wrapper.find('.modal-container')
        await modalContainer.trigger('click')

        // Should not emit update:modelValue when clicking container (event stopped)
        expect(wrapper.emitted('update:modelValue')).toBeFalsy()
    })

    it('renders close button when showClose is true', () => {
        const wrapper = createWrapper({
            modelValue: true,
            showClose: true
        })

        expect(wrapper.find('.modal-close').exists()).toBe(true)
    })

    it('does not render close button when showClose is false', () => {
        const wrapper = createWrapper({
            modelValue: true,
            showClose: false
        })

        expect(wrapper.find('.modal-close').exists()).toBe(false)
    })
})
