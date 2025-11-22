import { describe, it, expect, beforeEach, vi } from 'vitest'
import { mount } from '@vue/test-utils'
import { createPinia } from 'pinia'
import ToastNotification from '../ToastNotification.vue'

describe('ToastNotification', () => {
    let wrapper

    beforeEach(() => {
        wrapper = mount(ToastNotification, {
            global: {
                plugins: [createPinia()],
                stubs: {
                    teleport: true
                }
            }
        })
    })

    it('renders without toasts initially', () => {
        expect(wrapper.findAll('.toast')).toHaveLength(0)
    })

    it('adds a toast', async () => {
        wrapper.vm.addToast({
            title: 'Test Toast',
            message: 'Test message',
            type: 'info'
        })

        await wrapper.vm.$nextTick()

        expect(wrapper.findAll('.toast')).toHaveLength(1)
        expect(wrapper.text()).toContain('Test Toast')
        expect(wrapper.text()).toContain('Test message')
    })

    it('adds multiple toasts', async () => {
        wrapper.vm.addToast({ title: 'Toast 1', type: 'success' })
        wrapper.vm.addToast({ title: 'Toast 2', type: 'error' })

        await wrapper.vm.$nextTick()

        expect(wrapper.findAll('.toast')).toHaveLength(2)
    })

    it('applies correct type class', async () => {
        wrapper.vm.addToast({ title: 'Success', type: 'success' })

        await wrapper.vm.$nextTick()

        const toast = wrapper.find('.toast')
        expect(toast.classes()).toContain('toast-success')
    })

    it('removes toast manually', async () => {
        const id = wrapper.vm.addToast({ title: 'Test', type: 'info' })

        await wrapper.vm.$nextTick()
        expect(wrapper.findAll('.toast')).toHaveLength(1)

        wrapper.vm.removeToast(id)
        await wrapper.vm.$nextTick()

        expect(wrapper.findAll('.toast')).toHaveLength(0)
    })

    it('auto-dismisses toast after duration', async () => {
        vi.useFakeTimers()

        wrapper.vm.addToast({
            title: 'Auto dismiss',
            type: 'info',
            duration: 1000
        })

        await wrapper.vm.$nextTick()
        expect(wrapper.findAll('.toast')).toHaveLength(1)

        vi.advanceTimersByTime(1100)
        await wrapper.vm.$nextTick()

        expect(wrapper.findAll('.toast')).toHaveLength(0)

        vi.useRealTimers()
    })

    it('does not auto-dismiss when duration is 0', async () => {
        vi.useFakeTimers()

        wrapper.vm.addToast({
            title: 'Persistent',
            type: 'info',
            duration: 0
        })

        await wrapper.vm.$nextTick()
        vi.advanceTimersByTime(5000)
        await wrapper.vm.$nextTick()

        expect(wrapper.findAll('.toast')).toHaveLength(1)

        vi.useRealTimers()
    })

    it('clears all toasts', async () => {
        wrapper.vm.addToast({ title: 'Toast 1', type: 'info' })
        wrapper.vm.addToast({ title: 'Toast 2', type: 'success' })
        wrapper.vm.addToast({ title: 'Toast 3', type: 'error' })

        await wrapper.vm.$nextTick()
        expect(wrapper.findAll('.toast')).toHaveLength(3)

        wrapper.vm.clearAll()
        await wrapper.vm.$nextTick()

        expect(wrapper.findAll('.toast')).toHaveLength(0)
    })

    it('renders close button when dismissible', async () => {
        wrapper.vm.addToast({
            title: 'Dismissible',
            type: 'info',
            dismissible: true
        })

        await wrapper.vm.$nextTick()

        expect(wrapper.find('.toast-close').exists()).toBe(true)
    })

    it('removes toast when close button clicked', async () => {
        wrapper.vm.addToast({
            title: 'Test',
            type: 'info',
            dismissible: true
        })

        await wrapper.vm.$nextTick()

        const closeButton = wrapper.find('.toast-close')
        await closeButton.trigger('click')
        await wrapper.vm.$nextTick()

        expect(wrapper.findAll('.toast')).toHaveLength(0)
    })

    it('applies correct position class', () => {
        const wrapperWithPosition = mount(ToastNotification, {
            props: {
                position: 'bottom-left'
            },
            global: {
                plugins: [createPinia()],
                stubs: {
                    teleport: true
                }
            }
        })

        const container = wrapperWithPosition.find('.toast-container')
        expect(container.classes()).toContain('toast-position-bottom-left')
    })

    it('returns toast ID when adding', () => {
        const id = wrapper.vm.addToast({ title: 'Test', type: 'info' })

        expect(typeof id).toBe('number')
        expect(id).toBeGreaterThan(0)
    })
})
