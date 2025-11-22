import { mount } from '@vue/test-utils'
import { createPinia } from 'pinia'
import { vi } from 'vitest'

/**
 * Create a mock router for testing
 */
export function createMockRouter(routes = []) {
    return {
        push: vi.fn(),
        replace: vi.fn(),
        go: vi.fn(),
        back: vi.fn(),
        forward: vi.fn(),
        currentRoute: {
            value: {
                path: '/',
                name: 'home',
                params: {},
                query: {},
                meta: {}
            }
        },
        options: {
            routes
        }
    }
}

/**
 * Create a fresh Pinia instance for testing
 */
export function createTestingPinia(options = {}) {
    return createPinia()
}

/**
 * Mount a component with common test setup
 */
export function mountWithDefaults(component, options = {}) {
    const pinia = createTestingPinia()
    const router = createMockRouter()

    return mount(component, {
        global: {
            plugins: [pinia],
            mocks: {
                $router: router,
                $route: router.currentRoute.value
            },
            stubs: {
                teleport: true,
                ...options.stubs
            }
        },
        ...options
    })
}

/**
 * Wait for next tick and all promises
 */
export async function flushPromises() {
    return new Promise(resolve => setTimeout(resolve, 0))
}

/**
 * Mock API response
 */
export function mockApiResponse(data, status = 200) {
    return Promise.resolve({
        data,
        status,
        statusText: 'OK',
        headers: {},
        config: {}
    })
}

/**
 * Mock API error
 */
export function mockApiError(message = 'API Error', status = 500) {
    const error = new Error(message)
    error.response = {
        data: { detail: message },
        status,
        statusText: 'Error'
    }
    return Promise.reject(error)
}

/**
 * Sample user data for tests
 */
export const mockUser = {
    id: 1,
    email: 'test@example.com',
    full_name: 'Test User',
    is_active: true
}

/**
 * Sample auth token
 */
export const mockToken = 'mock-jwt-token-12345'

/**
 * Sample chat message
 */
export const mockChatMessage = {
    role: 'user',
    content: 'Test message',
    timestamp: new Date().toISOString()
}
