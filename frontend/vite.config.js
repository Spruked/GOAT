import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [react()],
  server: {
    port: 5173,
    // Enable unsafe-eval for development to avoid CSP issues
    headers: {
      'Content-Security-Policy': "script-src 'self' 'unsafe-eval' 'unsafe-inline' http://localhost:5173 https://cdn.jsdelivr.net"
    },
    proxy: {
      '/api': {
        target: 'http://localhost:5000',
        changeOrigin: true,
      },
      '/glyph': {
        target: 'http://localhost:5000',
        changeOrigin: true,
      },
      '/capture': {
        target: 'http://localhost:5000',
        changeOrigin: true,
      },
      '/upload': {
        target: 'http://localhost:5000',
        changeOrigin: true,
      },
      '/guest': {
        target: 'http://localhost:5000',
        changeOrigin: true,
      },
      '/write': {
        target: 'http://localhost:5000',
        changeOrigin: true,
      },
      '/test': {
        target: 'http://localhost:5000',
        changeOrigin: true,
      }
    }
  },
  build: {
    rollupOptions: {
      output: {
        manualChunks: undefined,
      }
    }
  }
})
