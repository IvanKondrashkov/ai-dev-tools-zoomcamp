import { describe, it, expect, vi, beforeEach, afterEach } from 'vitest'
import { render, screen, waitFor, act } from '@testing-library/react'
import { BrowserRouter } from 'react-router-dom'
import CodeEditor from '../CodeEditor'
import * as codeExecutor from '../../utils/codeExecutor'

// Mock Monaco Editor
vi.mock('@monaco-editor/react', () => ({
  default: ({ value, onChange, language }) => (
    <textarea
      data-testid="monaco-editor"
      value={value}
      onChange={(e) => onChange?.(e.target.value)}
      data-language={language}
    />
  ),
}))

// Mock socket.io-client
const mockSocket = {
  on: vi.fn(),
  emit: vi.fn(),
  disconnect: vi.fn(),
  enter_room: vi.fn(),
}

vi.mock('socket.io-client', () => ({
  io: vi.fn(() => mockSocket),
}))

const MockedCodeEditor = ({ sessionId }) => (
  <BrowserRouter future={{ v7_startTransition: true, v7_relativeSplatPath: true }}>
    <CodeEditor sessionId={sessionId} />
  </BrowserRouter>
)

describe('CodeEditor', () => {
  beforeEach(() => {
    vi.clearAllMocks()
  })

  afterEach(() => {
    vi.restoreAllMocks()
  })

  it('renders the code editor', async () => {
    await act(async () => {
      render(<MockedCodeEditor sessionId="test-session-123" />)
    })
    expect(screen.getByTestId('monaco-editor')).toBeInTheDocument()
  })

  it('displays session ID', async () => {
    await act(async () => {
      render(<MockedCodeEditor sessionId="test-session-123" />)
    })
    expect(screen.getByText(/Session: test-session-123/i)).toBeInTheDocument()
  })

  it('renders language selector', async () => {
    await act(async () => {
      render(<MockedCodeEditor sessionId="test-session-123" />)
    })
    const languageSelect = screen.getByRole('combobox')
    expect(languageSelect).toBeInTheDocument()
  })

  it('renders run code button', async () => {
    await act(async () => {
      render(<MockedCodeEditor sessionId="test-session-123" />)
    })
    expect(screen.getByText('Run Code')).toBeInTheDocument()
  })

  it('renders copy link button', async () => {
    await act(async () => {
      render(<MockedCodeEditor sessionId="test-session-123" />)
    })
    expect(screen.getByText('Copy Link')).toBeInTheDocument()
  })

  it('executes code when run button is clicked', async () => {
    const mockExecuteCode = vi.spyOn(codeExecutor, 'executeCode')
    mockExecuteCode.mockResolvedValue({ output: 'Hello, World!', error: null })

    await act(async () => {
      render(<MockedCodeEditor sessionId="test-session-123" />)
    })
    
    const runButton = screen.getByText('Run Code')
    
    await act(async () => {
      runButton.click()
      // Wait for async state updates
      await new Promise(resolve => setTimeout(resolve, 0))
    })

    await waitFor(() => {
      expect(mockExecuteCode).toHaveBeenCalled()
    })
  })

  it('displays error when code execution fails', async () => {
    const mockExecuteCode = vi.spyOn(codeExecutor, 'executeCode')
    mockExecuteCode.mockResolvedValue({ output: '', error: 'Syntax error' })

    await act(async () => {
      render(<MockedCodeEditor sessionId="test-session-123" />)
    })
    
    const runButton = screen.getByText('Run Code')
    
    await act(async () => {
      runButton.click()
      // Wait for async state updates
      await new Promise(resolve => setTimeout(resolve, 0))
    })

    await waitFor(() => {
      expect(screen.getByText(/Error: Syntax error/i)).toBeInTheDocument()
    })
  })

  it('copies link to clipboard when copy button is clicked', () => {
    const mockWriteText = vi.fn()
    global.navigator.clipboard = {
      writeText: mockWriteText,
    }
    global.alert = vi.fn()

    render(<MockedCodeEditor sessionId="test-session-123" />)
    
    const copyButton = screen.getByText('Copy Link')
    copyButton.click()

    expect(mockWriteText).toHaveBeenCalled()
  })
})

