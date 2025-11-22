# Frontend Tests

Comprehensive test suite for the MzeeChakula Vue 3 frontend application.

## Test Structure

```
src/
├── components/__tests__/
│   ├── AlertModal.test.js
│   ├── AppLoader.test.js
│   └── BaseModal.test.js
├── stores/__tests__/
│   └── auth.test.js
├── api/__tests__/
│   └── client.test.js
└── test-utils/
    ├── setup.js
    └── index.js
```

## Running Tests

### Quick Start

```bash
# Run all tests
npm test

# Run tests in watch mode
npm test -- --watch

# Run tests with UI
npm run test:ui

# Run with coverage
npm run test:coverage
```

### Run Specific Tests

```bash
# Run component tests
npm test -- src/components

# Run store tests
npm test -- src/stores

# Run a specific file
npm test -- AlertModal.test.js
```

## Test Framework

- **Vitest**: Fast unit test framework for Vite projects
- **@vue/test-utils**: Official testing library for Vue 3
- **jsdom**: DOM implementation for Node.js
- **happy-dom**: Alternative fast DOM implementation

## Writing Tests

### Component Tests

```javascript
import { mountWithDefaults } from '@/test-utils'
import MyComponent from '../MyComponent.vue'

describe('MyComponent', () => {
  it('renders correctly', () => {
    const wrapper = mountWithDefaults(MyComponent, {
      props: {
        title: 'Test'
      }
    })
    
    expect(wrapper.text()).toContain('Test')
  })
})
```

### Store Tests

```javascript
import { setActivePinia, createPinia } from 'pinia'
import { useMyStore } from '../myStore'

describe('My Store', () => {
  beforeEach(() => {
    setActivePinia(createPinia())
  })

  it('updates state', () => {
    const store = useMyStore()
    store.updateValue('new value')
    
    expect(store.value).toBe('new value')
  })
})
```

### API Tests

```javascript
import { vi } from 'vitest'
import { myApiFunction } from '../myApi'

vi.mock('axios')

describe('My API', () => {
  it('makes correct request', async () => {
    const result = await myApiFunction()
    expect(result).toBeDefined()
  })
})
```

## Test Utilities

### mountWithDefaults

Mounts a component with Pinia and router mocks:

```javascript
const wrapper = mountWithDefaults(Component, {
  props: { /* ... */ },
  slots: { /* ... */ }
})
```

### Mock Factories

- `createMockRouter()` - Creates a mock Vue Router
- `createTestingPinia()` - Creates a fresh Pinia instance
- `mockApiResponse(data, status)` - Mock successful API response
- `mockApiError(message, status)` - Mock API error

### Sample Data

- `mockUser` - Sample user object
- `mockToken` - Sample JWT token
- `mockChatMessage` - Sample chat message

## Coverage

Coverage reports are generated in `coverage/` directory.

**Coverage Goals:**
- Components: >80%
- Stores: >90%
- API clients: >75%
- Overall: >70%

## Best Practices

1. **Test behavior, not implementation**
2. **Use descriptive test names**
3. **Keep tests focused and simple**
4. **Mock external dependencies**
5. **Clean up after each test**
6. **Test edge cases and error states**

## Troubleshooting

### Tests fail with "Cannot find module"

Make sure path aliases are configured in `vitest.config.js`:

```javascript
resolve: {
  alias: {
    '@': fileURLToPath(new URL('./src', import.meta.url))
  }
}
```

### Component not rendering

Check that you're using `mountWithDefaults` or providing necessary plugins:

```javascript
mount(Component, {
  global: {
    plugins: [createPinia()]
  }
})
```

### Async tests timing out

Use `await` and `flushPromises()`:

```javascript
await wrapper.vm.$nextTick()
await flushPromises()
```

## CI/CD Integration

Add to your CI pipeline:

```yaml
- name: Run frontend tests
  run: |
    cd frontend
    npm install
    npm test
```

## Documentation

- [Vitest Documentation](https://vitest.dev/)
- [Vue Test Utils](https://test-utils.vuejs.org/)
- [Testing Best Practices](https://vuejs.org/guide/scaling-up/testing.html)
