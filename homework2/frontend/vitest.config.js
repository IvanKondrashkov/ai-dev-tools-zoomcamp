import { defineConfig } from 'vitest/config'
import react from '@vitejs/plugin-react'

export default defineConfig({
  plugins: [react()],
  test: {
    environment: 'jsdom',
    globals: true,
    setupFiles: './src/test/setup.js',
    // Suppress console warnings in test output
    onConsoleLog: (log, type) => {
      if (type === 'warn' || type === 'error') {
        if (
          typeof log === 'string' &&
          (log.includes('React Router Future Flag Warning') ||
           log.includes('v7_startTransition') ||
           log.includes('v7_relativeSplatPath') ||
           log.includes('not wrapped in act(...)') ||
           (log.includes('An update to') && log.includes('inside a test')))
        ) {
          return false // Suppress this log
        }
      }
      return true
    },
  },
})

