import { describe, it, expect } from 'vitest'
import { mount } from '@vue/test-utils'
import { createPinia } from 'pinia'
import AppLoader from '../AppLoader.vue'

describe('AppLoader', () => {
    const createWrapper = (props = {}) => {
        return mount(AppLoader, {
            props,
            global: {
                plugins: [createPinia()]
            }
        })
    }

    it('renders loader container', () => {
        const wrapper = createWrapper()

        expect(wrapper.find('.loader-container').exists()).toBe(true)
    })

    it('displays custom message when provided', () => {
        const wrapper = createWrapper({
            message: 'Loading data...'
        })

        expect(wrapper.text()).toContain('Loading data...')
    })

    it('displays default message when not provided', () => {
        const wrapper = createWrapper()

        expect(wrapper.text()).toContain('Loading...')
    })

    it('renders icon animation', () => {
        const wrapper = createWrapper()

        expect(wrapper.find('.icon-animation').exists()).toBe(true)
        expect(wrapper.findAll('.icon-wrapper')).toHaveLength(3)
    })

    it('has loading text element', () => {
        const wrapper = createWrapper()

        expect(wrapper.find('.loading-text').exists()).toBe(true)
    })
})
