// frontend/src/config/api.js
// FAIL-FAST configuration for GOAT

export const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api/v1'
export const WS_URL = import.meta.env.VITE_WS_URL || 'ws://localhost:8000/api/v1/realtime'

// Validate configuration
if (!API_URL) {
  throw new Error('❌ VITE_API_URL is not defined. Create .env.frontend file')
}

if (!API_URL.startsWith('http')) {
  throw new Error(`❌ Invalid VITE_API_URL: ${API_URL}. Must start with http/https`)
}

// Derived endpoints
export const ENDPOINTS = {
  triples: `${API_URL}/triples`,
  query: `${API_URL}/query`,
  video: `${API_URL}/video`,
  health: `${API_URL.replace('/api/v1', '')}/health`,
  analytics: `${API_URL}/analytics`,
  auth: `${API_URL.replace('/api/v1', '')}/auth`
}

console.log('✅ GOAT API Config loaded:', {
  apiUrl: API_URL,
  wsUrl: WS_URL,
  environment: import.meta.env.VITE_ENVIRONMENT || 'development'
})