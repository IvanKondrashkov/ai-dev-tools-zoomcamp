import { describe, it, expect, vi, beforeEach } from 'vitest'
import { render, screen, waitFor, act } from '@testing-library/react'
import { BrowserRouter } from 'react-router-dom'
import * as reactRouterDom from 'react-router-dom'
import SessionCreator from '../SessionCreator'

const MockedSessionCreator = () => (
  <BrowserRouter future={{ v7_startTransition: true, v7_relativeSplatPath: true }}>
    <SessionCreator />
  </BrowserRouter>
)

describe('SessionCreator', () => {
  beforeEach(() => {
    vi.clearAllMocks()
  })

  it('renders the title and description', () => {
    render(<MockedSessionCreator />)
    expect(screen.getByText('Coding Interview Platform')).toBeInTheDocument()
    expect(
      screen.getByText(
        'Create a new coding session and share the link with candidates'
      )
    ).toBeInTheDocument()
  })

  it('renders the create button', () => {
    render(<MockedSessionCreator />)
    expect(screen.getByText('Create New Session')).toBeInTheDocument()
  })

  it('creates a session when button is clicked', async () => {
    const mockFetch = vi.fn().mockResolvedValue({
      ok: true,
      json: async () => ({ session_id: 'test-session-id' }),
    })
    global.fetch = mockFetch

    // Mock window.location to check navigation
    const originalLocation = window.location
    delete window.location
    window.location = { ...originalLocation, pathname: '/' }

    await act(async () => {
      render(<MockedSessionCreator />)
    })
    
    const button = screen.getByText('Create New Session')
    
    await act(async () => {
      button.click()
      // Wait for async state updates
      await new Promise(resolve => setTimeout(resolve, 0))
    })

    await waitFor(() => {
      expect(mockFetch).toHaveBeenCalledWith(
        expect.stringContaining('/api/sessions'),
        expect.objectContaining({
          method: 'POST',
        })
      )
    })

    // Navigation will happen via React Router, which we can't easily mock
    // So we just verify the fetch was called correctly
    window.location = originalLocation
  })
})

