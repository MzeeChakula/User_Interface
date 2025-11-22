import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import tailwindcss from '@tailwindcss/vite'
import { VitePWA } from 'vite-plugin-pwa'

// https://vite.dev/config/
export default defineConfig({
  plugins: [
    vue(),
    tailwindcss(),
    VitePWA({
      registerType: 'autoUpdate',
      includeAssets: ['icons/favicon.ico', 'icons/logo.svg'],
      manifest: {
        name: 'Mzee Chakula',
        short_name: 'MzeeChakula',
        description: 'AI-powered nutritional assistant for elderly care in Uganda',
        theme_color: '#D90000',
        background_color: '#1E1E1E',
        display: 'standalone',
        start_url: '/',
        scope: '/',
        icons: [
          {
            src: '/icons/pwa-64x64.png',
            sizes: '64x64',
            type: 'image/png'
          },
          {
            src: '/icons/pwa-192x192.png',
            sizes: '192x192',
            type: 'image/png'
          },
          {
            src: '/icons/pwa-512x512.png',
            sizes: '512x512',
            type: 'image/png',
            purpose: 'any'
          },
          {
            src: '/icons/maskable-icon-512x512.png',
            sizes: '512x512',
            type: 'image/png',
            purpose: 'maskable'
          }
        ]
      },
      workbox: {
        globPatterns: ['**/*.{js,css,html}'],
        globDirectory: 'dist',
        runtimeCaching: [
          {
            urlPattern: /^https:\/\/api\..*/i,
            handler: 'NetworkFirst',
            options: {
              cacheName: 'api-cache',
              expiration: {
                maxEntries: 50,
                maxAgeSeconds: 60 * 60 * 24
              },
              cacheableResponse: {
                statuses: [0, 200]
              }
            }
          }
        ]
      },
      devOptions: {
        enabled: true
      }
    })
  ],
  server: {
    proxy: {
      '^/auth/.*': {
        target: 'http://localhost:8000',
        changeOrigin: true
      },
      '^/predict/.*': {
        target: 'http://localhost:8000',
        changeOrigin: true
      },
      '^/health/.*': {
        target: 'http://localhost:8000',
        changeOrigin: true
      },
      '^/chat/message': {
        target: 'http://localhost:8000',
        changeOrigin: true
      },
      '^/ai/.*': {
        target: 'http://localhost:8000',
        changeOrigin: true
      },
      '^/meal-plan/.*': {
        target: 'http://localhost:8000',
        changeOrigin: true
      },
      '^/foods/.*': {
        target: 'http://localhost:8000',
        changeOrigin: true
      },
      '/docs': {
        target: 'http://localhost:8000',
        changeOrigin: true
      },
      '/redoc': {
        target: 'http://localhost:8000',
        changeOrigin: true
      },
      '/openapi.json': {
        target: 'http://localhost:8000',
        changeOrigin: true
      }
    }
  }
})
