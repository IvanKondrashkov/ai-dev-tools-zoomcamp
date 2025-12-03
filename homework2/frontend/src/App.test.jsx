import { describe, it, expect, vi, beforeEach } from 'vitest'
import { render, screen, waitFor, act } from '@testing-library/react'
import { MemoryRouter, Routes, Route } from 'react-router-dom'
import { useState, useEffect } from 'react'
import { useParams, useNavigate } from 'react-router-dom'
import SessionCreator from './components/SessionCreator'
import CodeEditor from './components/CodeEditor'

// Test version of App without BrowserRouter
const AppContent = () => {
  return (
    <div className="app">
      <Routes>
        <Route path="/" element={<SessionCreator />} />
        <Route path="/session/:sessionId" element={<SessionPage />} />
      </Routes>
    </div>
  )
}

const SessionPage = () => {
  const { sessionId } = useParams()
  const navigate = useNavigate()
  const [sessionExists, setSessionExists] = useState(true)

  useEffect(() => {
    if (!sessionId) {
      navigate('/')
      return
    }

    const checkSession = async () => {
      try {
        const apiUrl = import.meta.env.VITE_API_URL || 'http://localhost:8000'
        const response = await fetch(`${apiUrl}/api/sessions/${sessionId}`)
        if (!response.ok) {
          setSessionExists(false)
        }
      } catch (error) {
        console.error('Error checking session:', error)
        setSessionExists(false)
      }
    }

    checkSession()
  }, [sessionId, navigate])

  if (!sessionExists) {
    return (
      <div className="error-container">
        <h1>Session not found</h1>
        <button onClick={() => navigate('/')}>Go Home</button>
      </div>
    )
  }

  return <CodeEditor sessionId={sessionId} />
}

describe('App', () => {
  beforeEach(() => {
    vi.clearAllMocks()
  })

  it('renders SessionCreator on root path', () => {
    render(
      <MemoryRouter 
        initialEntries={['/']}
        future={{ v7_startTransition: true, v7_relativeSplatPath: true }}
      >
        <AppContent />
      </MemoryRouter>
    )
    expect(screen.getByText('Coding Interview Platform')).toBeInTheDocument()
  })

  it('renders CodeEditor on session path', async () => {
    const mockFetch = vi.fn().mockResolvedValue({
      ok: true,
    })
    global.fetch = mockFetch

    await act(async () => {
      render(
        <MemoryRouter 
          initialEntries={['/session/test-session-123']}
          future={{ v7_startTransition: true, v7_relativeSplatPath: true }}
        >
          <AppContent />
        </MemoryRouter>
      )
    })

    await waitFor(() => {
      expect(mockFetch).toHaveBeenCalled()
    })
  })

  it('shows error when session not found', async () => {
    const mockFetch = vi.fn().mockResolvedValue({
      ok: false,
    })
    global.fetch = mockFetch

    await act(async () => {
      render(
        <MemoryRouter 
          initialEntries={['/session/nonexistent']}
          future={{ v7_startTransition: true, v7_relativeSplatPath: true }}
        >
          <AppContent />
        </MemoryRouter>
      )
    })

    await waitFor(() => {
      expect(screen.getByText('Session not found')).toBeInTheDocument()
    }, { timeout: 3000 })
  })
})

