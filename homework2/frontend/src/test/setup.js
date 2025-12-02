import { expect, afterEach, beforeAll, afterAll } from 'vitest'
import { cleanup } from '@testing-library/react'
import * as matchers from '@testing-library/jest-dom/matchers'

expect.extend(matchers)

// Suppress React Router future flag warnings and act() warnings
const originalError = console.error
const originalWarn = console.warn

beforeAll(() => {
  console.error = (...args) => {
    const message = args[0]
    if (
      typeof message === 'string' &&
      (message.includes('React Router Future Flag Warning') ||
       message.includes('v7_startTransition') ||
       message.includes('v7_relativeSplatPath') ||
       message.includes('not wrapped in act(...)') ||
       message.includes('An update to') && message.includes('inside a test'))
    ) {
      return
    }
    originalError.call(console, ...args)
  }

  console.warn = (...args) => {
    const message = args[0]
    if (
      typeof message === 'string' &&
      (message.includes('React Router Future Flag Warning') ||
       message.includes('v7_startTransition') ||
       message.includes('v7_relativeSplatPath') ||
       message.includes('not wrapped in act(...)') ||
       message.includes('An update to') && message.includes('inside a test'))
    ) {
      return
    }
    originalWarn.call(console, ...args)
  }
})

afterAll(() => {
  console.error = originalError
  console.warn = originalWarn
})

afterEach(() => {
  cleanup()
})

