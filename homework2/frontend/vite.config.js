import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// In Vite config, use process.env, not import.meta.env
const API_URL = process.env.VITE_API_URL || 'http://localhost:8000'

export default defineConfig({
  plugins: [react()],
  server: {
    port: 3000,
    host: '0.0.0.0',
    proxy: {
      '/api': {
        target: API_URL,
        changeOrigin: true,
      },
      '/socket.io': {
        target: API_URL,
        ws: true,
        changeOrigin: true,
      },
    },
  },
  define: {
    'import.meta.env.VITE_API_URL': JSON.stringify(API_URL),
  },
})

