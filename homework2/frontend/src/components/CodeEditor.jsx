import { useState, useEffect, useRef } from 'react'
import { io } from 'socket.io-client'
import Editor from '@monaco-editor/react'
import { executeCode } from '../utils/codeExecutor'
import './CodeEditor.css'

const CodeEditor = ({ sessionId }) => {
  const [code, setCode] = useState(() => {
    // Set initial code based on language
    return '// Write your code here\n'
  })
  const [language, setLanguage] = useState('javascript')
  const [output, setOutput] = useState('')
  const [isExecuting, setIsExecuting] = useState(false)
  const socketRef = useRef(null)
  const editorRef = useRef(null)

  useEffect(() => {
    const apiUrl = import.meta.env.VITE_API_URL || 'http://localhost:8000'
    const socket = io(apiUrl, {
      path: '/socket.io/',
    })

    socket.on('connect', () => {
      socket.emit('join_session', { session_id: sessionId })
    })

    socket.on('code_update', (data) => {
      if (data.session_id === sessionId) {
        setCode(data.code)
        setLanguage(data.language || 'javascript')
      }
    })

    socket.on('language_update', (data) => {
      if (data.session_id === sessionId) {
        const newLanguage = data.language
        setLanguage(newLanguage)
        
        // Update code template based on new language
        const templates = {
          javascript: '// Write your code here\n',
          python: '# Write your code here\n',
          go: 'package main\n\nimport "fmt"\n\nfunc main() {\n\t// Write your code here\n}\n',
          java: 'public class Main {\n    public static void main(String[] args) {\n        // Write your code here\n    }\n}\n',
        }
        
        // Update code to new language template
        setCode(templates[newLanguage] || '// Write your code here\n')
        
        // Clear output when language changes
        setOutput('')
      }
    })

    socketRef.current = socket

    return () => {
      socket.disconnect()
    }
  }, [sessionId])

  const handleEditorChange = (value) => {
    if (value !== code) {
      setCode(value || '')
      if (socketRef.current) {
        socketRef.current.emit('code_change', {
          session_id: sessionId,
          code: value || '',
        })
      }
    }
  }

  const handleLanguageChange = (e) => {
    const newLanguage = e.target.value
    setLanguage(newLanguage)
    
    // Update code template based on new language
    const templates = {
      javascript: '// Write your code here\n',
      python: '# Write your code here\n',
      go: 'package main\n\nimport "fmt"\n\nfunc main() {\n\t// Write your code here\n}\n',
      java: 'public class Main {\n    public static void main(String[] args) {\n        // Write your code here\n    }\n}\n',
    }
    
    // Always update code to new language template
    setCode(templates[newLanguage] || '// Write your code here\n')
    
    // Clear output when language changes
    setOutput('')
    
    if (socketRef.current) {
      socketRef.current.emit('language_change', {
        session_id: sessionId,
        language: newLanguage,
      })
      
      // Also emit code change to sync with other clients
      socketRef.current.emit('code_change', {
        session_id: sessionId,
        code: templates[newLanguage] || '// Write your code here\n',
      })
    }
  }

  const handleExecute = async () => {
    setIsExecuting(true)
    setOutput('Executing...\n')

    try {
      // Execute code in browser
      const result = await executeCode(code, language)
      
      if (result.error) {
        setOutput(`Error: ${result.error}`)
      } else {
        setOutput(result.output || 'Code executed successfully (no output)')
      }
    } catch (error) {
      setOutput(`Error: ${error.message}`)
    } finally {
      setIsExecuting(false)
    }
  }

  const handleCopyLink = () => {
    const url = `${window.location.origin}/session/${sessionId}`
    navigator.clipboard.writeText(url)
    alert('Link copied to clipboard!')
  }

  return (
    <div className="code-editor-container">
      <div className="editor-header">
        <div className="header-left">
          <h2>Session: {sessionId}</h2>
          <button onClick={handleCopyLink} className="copy-button">
            Copy Link
          </button>
        </div>
        <div className="header-right">
          <select
            value={language}
            onChange={handleLanguageChange}
            className="language-select"
          >
            <option value="javascript">JavaScript</option>
            <option value="python">Python</option>
            <option value="go">Go</option>
            <option value="java">Java</option>
          </select>
          <button
            onClick={handleExecute}
            disabled={isExecuting}
            className="execute-button"
          >
            {isExecuting ? 'Running...' : 'Run Code'}
          </button>
        </div>
      </div>
      <div className="editor-content">
        <div className="editor-panel">
          <Editor
            height="100%"
            language={language}
            value={code}
            onChange={handleEditorChange}
            theme="vs-dark"
            options={{
              minimap: { enabled: true },
              fontSize: 14,
              wordWrap: 'on',
              automaticLayout: true,
            }}
            onMount={(editor) => {
              editorRef.current = editor
            }}
          />
        </div>
        <div className="output-panel">
          <div className="output-header">Output</div>
          <pre className="output-content">{output || 'Output will appear here...'}</pre>
        </div>
      </div>
    </div>
  )
}

export default CodeEditor

