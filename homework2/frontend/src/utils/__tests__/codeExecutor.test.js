import { describe, it, expect, vi, beforeEach, afterEach } from 'vitest'
import {
  executeJavaScript,
  executePython,
  executeGo,
  executeJava,
  executeCode,
} from '../codeExecutor'

describe('codeExecutor', () => {
  beforeEach(() => {
    vi.clearAllMocks()
  })

  afterEach(() => {
    vi.restoreAllMocks()
  })

  describe('executeJavaScript', () => {
    it('executes simple JavaScript code', async () => {
      const result = await executeJavaScript("console.log('Hello');")
      expect(result.error).toBeNull()
      expect(result.output).toContain('Hello')
    })

    it('captures console.log output', async () => {
      const result = await executeJavaScript("console.log('Test', 123);")
      expect(result.error).toBeNull()
      expect(result.output).toContain('Test')
      expect(result.output).toContain('123')
    })

    it('captures console.error output', async () => {
      const result = await executeJavaScript("console.error('Error message');")
      expect(result.error).toBeNull()
      expect(result.output).toContain('ERROR:')
      expect(result.output).toContain('Error message')
    })

    it('handles syntax errors', async () => {
      const result = await executeJavaScript('invalid syntax {')
      expect(result.error).not.toBeNull()
      expect(result.output).toBe('')
    })

    it('returns function return value', async () => {
      const result = await executeJavaScript('return 42;')
      expect(result.error).toBeNull()
      expect(result.output).toContain('42')
    })
  })

  describe('executePython', () => {
    it('handles Pyodide not loaded', async () => {
      // Mock window.pyodide as undefined and prevent script loading
      const originalPyodide = window.pyodide
      const originalPyodideLoading = window.pyodideLoading
      const originalLoadPyodide = window.loadPyodide
      const originalCreateElement = document.createElement
      const originalAppendChild = document.head.appendChild
      
      delete window.pyodide
      delete window.pyodideLoading
      delete window.loadPyodide
      
      // Mock document.createElement and appendChild to prevent script loading
      let scriptErrorTriggered = false
      document.createElement = vi.fn((tagName) => {
        if (tagName === 'script') {
          const script = originalCreateElement.call(document, tagName)
          // Trigger onerror immediately to simulate failed load
          script.onerror = () => {
            scriptErrorTriggered = true
          }
          // Trigger error asynchronously
          Promise.resolve().then(() => {
            if (script.onerror) script.onerror()
          })
          return script
        }
        return originalCreateElement.call(document, tagName)
      })
      
      document.head.appendChild = vi.fn((element) => {
        // Trigger error immediately for script elements
        if (element.tagName === 'SCRIPT' && element.onerror) {
          Promise.resolve().then(() => {
            element.onerror()
          })
        }
        return element
      })

      const result = await executePython('print("Hello")')
      
      // Should return error about Pyodide not being loaded
      expect(result.error).not.toBeNull()
      expect(result.error).toContain('Failed to load Pyodide')
      
      // Restore
      document.createElement = originalCreateElement
      document.head.appendChild = originalAppendChild
      if (originalPyodide !== undefined) window.pyodide = originalPyodide
      if (originalPyodideLoading !== undefined) window.pyodideLoading = originalPyodideLoading
      if (originalLoadPyodide !== undefined) window.loadPyodide = originalLoadPyodide
    }, 2000)
  })

  describe('executeGo', () => {
    it('sends request to backend API', async () => {
      const mockFetch = vi.fn().mockResolvedValue({
        ok: true,
        json: async () => ({ output: 'Go output', error: null }),
      })
      global.fetch = mockFetch

      const result = await executeGo('package main\nfunc main() {}')

      expect(mockFetch).toHaveBeenCalledWith(
        expect.stringContaining('/api/execute'),
        expect.objectContaining({
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: expect.stringContaining('go'),
        })
      )
    })

    it('handles API errors', async () => {
      const mockFetch = vi.fn().mockResolvedValue({
        ok: false,
        json: async () => ({ error: 'API Error' }),
      })
      global.fetch = mockFetch

      const result = await executeGo('code')

      expect(result.error).not.toBeNull()
    })

    it('handles network errors', async () => {
      const mockFetch = vi.fn().mockRejectedValue(new Error('Network error'))
      global.fetch = mockFetch

      const result = await executeGo('code')

      expect(result.error).toContain('Network error')
    })
  })

  describe('executeJava', () => {
    it('sends request to backend API', async () => {
      const mockFetch = vi.fn().mockResolvedValue({
        ok: true,
        json: async () => ({ output: 'Java output', error: null }),
      })
      global.fetch = mockFetch

      const result = await executeJava('System.out.println("Hello");')

      expect(mockFetch).toHaveBeenCalledWith(
        expect.stringContaining('/api/execute'),
        expect.objectContaining({
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: expect.stringContaining('java'),
        })
      )
    })

    it('handles API errors', async () => {
      const mockFetch = vi.fn().mockResolvedValue({
        ok: false,
        json: async () => ({ error: 'API Error' }),
      })
      global.fetch = mockFetch

      const result = await executeJava('code')

      expect(result.error).not.toBeNull()
    })
  })

  describe('executeCode', () => {
    it('calls executeJavaScript for javascript', async () => {
      // Test that executeCode routes to executeJavaScript correctly
      // We can't easily spy on internal function calls, so we test the behavior
      const result = await executeCode('console.log("test");', 'javascript')
      expect(result.error).toBeNull()
      expect(result.output).toContain('test')
    })

    it('calls executeGo for go', async () => {
      const mockFetch = vi.fn().mockResolvedValue({
        ok: true,
        json: async () => ({ output: 'Go executed', error: null }),
      })
      global.fetch = mockFetch

      const result = await executeCode('package main\nfunc main() {}', 'go')
      
      expect(mockFetch).toHaveBeenCalledWith(
        expect.stringContaining('/api/execute'),
        expect.objectContaining({
          method: 'POST',
          body: expect.stringContaining('go'),
        })
      )
      expect(result.error).toBeNull()
    })

    it('calls executeJava for java', async () => {
      const mockFetch = vi.fn().mockResolvedValue({
        ok: true,
        json: async () => ({ output: 'Java executed', error: null }),
      })
      global.fetch = mockFetch

      const result = await executeCode('System.out.println("test");', 'java')
      
      expect(mockFetch).toHaveBeenCalledWith(
        expect.stringContaining('/api/execute'),
        expect.objectContaining({
          method: 'POST',
          body: expect.stringContaining('java'),
        })
      )
      expect(result.error).toBeNull()
    })

    it('returns error for unsupported language', async () => {
      const result = await executeCode('code', 'unsupported')
      expect(result.error).toContain('Unsupported language')
    })
  })
})

