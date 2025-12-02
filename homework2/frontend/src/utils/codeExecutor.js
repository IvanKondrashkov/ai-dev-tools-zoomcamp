// Code execution utilities for different languages

export const executeJavaScript = async (code) => {
  try {
    // Capture console.log output
    let output = ''
    const originalLog = console.log
    const originalError = console.error
    const originalWarn = console.warn
    
    console.log = (...args) => {
      output += args.map(arg => 
        typeof arg === 'object' ? JSON.stringify(arg, null, 2) : String(arg)
      ).join(' ') + '\n'
    }
    
    console.error = (...args) => {
      output += 'ERROR: ' + args.map(arg => 
        typeof arg === 'object' ? JSON.stringify(arg, null, 2) : String(arg)
      ).join(' ') + '\n'
    }
    
    console.warn = (...args) => {
      output += 'WARN: ' + args.map(arg => 
        typeof arg === 'object' ? JSON.stringify(arg, null, 2) : String(arg)
      ).join(' ') + '\n'
    }
    
    // Execute code in a safe context
    // Wrap in try-catch to handle errors
    let result
    try {
      result = new Function(code)()
    } catch (execError) {
      // Restore original console methods before returning error
      console.log = originalLog
      console.error = originalError
      console.warn = originalWarn
      return { output: '', error: execError.message }
    }
    
    // Restore original console methods
    console.log = originalLog
    console.error = originalError
    console.warn = originalWarn
    
    // If function returns a value, add it to output
    if (result !== undefined) {
      output += String(result) + '\n'
    }
    
    return { output: output || 'Code executed successfully (no output)', error: null }
  } catch (error) {
    return { output: '', error: error.message }
  }
}

export const executePython = async (code) => {
  try {
    // Load Pyodide if not already loaded
    if (!window.pyodide) {
      // Check if script is already being loaded
      if (window.pyodideLoading) {
        await window.pyodideLoading
      } else {
        window.pyodideLoading = new Promise((resolve, reject) => {
          // Load Pyodide via script tag
          if (document.querySelector('script[src*="pyodide"]')) {
            // Script already exists, wait for it to load
            const checkInterval = setInterval(() => {
              if (window.loadPyodide) {
                clearInterval(checkInterval)
                window.loadPyodide({
                  indexURL: 'https://cdn.jsdelivr.net/pyodide/v0.24.1/full/',
                }).then((pyodide) => {
                  window.pyodide = pyodide
                  delete window.pyodideLoading
                  resolve()
                }).catch(reject)
              }
            }, 100)
            setTimeout(() => {
              clearInterval(checkInterval)
              reject(new Error('Pyodide loading timeout'))
            }, 30000)
          } else {
            const script = document.createElement('script')
            script.src = 'https://cdn.jsdelivr.net/pyodide/v0.24.1/full/pyodide.js'
            script.onload = () => {
              window.loadPyodide({
                indexURL: 'https://cdn.jsdelivr.net/pyodide/v0.24.1/full/',
              }).then((pyodide) => {
                window.pyodide = pyodide
                delete window.pyodideLoading
                resolve()
              }).catch(reject)
            }
            script.onerror = () => {
              delete window.pyodideLoading
              reject(new Error('Failed to load Pyodide script'))
            }
            document.head.appendChild(script)
          }
        })
        await window.pyodideLoading
      }
    }
    
    // Capture stdout
    window.pyodide.runPython(`
import sys
from io import StringIO
_stdout = StringIO()
sys.stdout = _stdout
`)
    
    try {
      window.pyodide.runPython(code)
      const stdout = window.pyodide.runPython('_stdout.getvalue()')
      return { output: stdout || 'Code executed successfully (no output)', error: null }
    } catch (error) {
      return { output: '', error: error.message }
    }
  } catch (error) {
    return { 
      output: '', 
      error: `Failed to load Pyodide: ${error.message}. Please refresh the page.` 
    }
  }
}

export const executeGo = async (code) => {
  try {
    // Execute Go code on the server
    const apiUrl = import.meta.env.VITE_API_URL || 'http://localhost:8000'
    const response = await fetch(`${apiUrl}/api/execute`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        code,
        language: 'go',
      }),
    })
    
    if (!response.ok) {
      const errorData = await response.json().catch(() => ({ error: 'Failed to execute Go code' }))
      return { output: '', error: errorData.error || `HTTP ${response.status}` }
    }
    
    const data = await response.json()
    
    if (data.error) {
      return { output: '', error: data.error }
    }
    
    return { output: data.output || 'Code executed successfully (no output)', error: null }
  } catch (error) {
    return { 
      output: '', 
      error: `Go execution error: ${error.message}. Make sure the backend server is running.` 
    }
  }
}

export const executeJava = async (code) => {
  try {
    // Execute Java code on the server
    const apiUrl = import.meta.env.VITE_API_URL || 'http://localhost:8000'
    const response = await fetch(`${apiUrl}/api/execute`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        code,
        language: 'java',
      }),
    })
    
    if (!response.ok) {
      const errorData = await response.json().catch(() => ({ error: 'Failed to execute Java code' }))
      return { output: '', error: errorData.error || `HTTP ${response.status}` }
    }
    
    const data = await response.json()
    
    if (data.error) {
      return { output: '', error: data.error }
    }
    
    return { output: data.output || 'Code executed successfully (no output)', error: null }
  } catch (error) {
    return { 
      output: '', 
      error: `Java execution error: ${error.message}. Make sure the backend server is running.` 
    }
  }
}

export const executeCode = async (code, language) => {
  switch (language) {
    case 'javascript':
      return await executeJavaScript(code)
    case 'python':
      return await executePython(code)
    case 'go':
      return await executeGo(code)
    case 'java':
      return await executeJava(code)
    default:
      return { output: '', error: `Unsupported language: ${language}` }
  }
}

