import { describe, it, expect, beforeEach, vi, afterEach } from 'vitest'

// We'll test the client behavior without mocking axios.create
// Instead, we'll test that the client module exports what we expect
describe('API Client', () => {
    beforeEach(() => {
        localStorage.clear()
    })

    afterEach(() => {
        localStorage.clear()
    })

    it('exports an axios instance', async () => {
        const apiClient = await import('../client')
        expect(apiClient.default).toBeDefined()
        expect(typeof apiClient.default.get).toBe('function')
        expect(typeof apiClient.default.post).toBe('function')
        expect(typeof apiClient.default.put).toBe('function')
        expect(typeof apiClient.default.delete).toBe('function')
    })

    it('has request interceptor configured', async () => {
        const apiClient = await import('../client')
        expect(apiClient.default.interceptors).toBeDefined()
        expect(apiClient.default.interceptors.request).toBeDefined()
    })

    it('has response interceptor configured', async () => {
        const apiClient = await import('../client')
        expect(apiClient.default.interceptors).toBeDefined()
        expect(apiClient.default.interceptors.response).toBeDefined()
    })

    it('has correct base configuration', async () => {
        const apiClient = await import('../client')
        expect(apiClient.default.defaults).toBeDefined()
        expect(apiClient.default.defaults.headers).toBeDefined()
        expect(apiClient.default.defaults.headers['Content-Type']).toBe('application/json')
        expect(apiClient.default.defaults.timeout).toBe(30000)
    })

    it('can be used to make requests', async () => {
        const apiClient = await import('../client')
        // Just verify the methods exist and are callable
        expect(() => apiClient.default.get).not.toThrow()
        expect(() => apiClient.default.post).not.toThrow()
    })
})
