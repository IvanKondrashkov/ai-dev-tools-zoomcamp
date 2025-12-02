import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import './SessionCreator.css'

const SessionCreator = () => {
  const [loading, setLoading] = useState(false)
  const navigate = useNavigate()

  const handleCreateSession = async () => {
    setLoading(true)
    try {
      const apiUrl = import.meta.env.VITE_API_URL || 'http://localhost:8000'
      const response = await fetch(`${apiUrl}/api/sessions`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
      })

      if (!response.ok) {
        throw new Error('Failed to create session')
      }

      const data = await response.json()
      navigate(`/session/${data.session_id}`)
    } catch (error) {
      console.error('Error creating session:', error)
      alert('Failed to create session. Please try again.')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="session-creator">
      <div className="session-creator-content">
        <h1>Coding Interview Platform</h1>
        <p>Create a new coding session and share the link with candidates</p>
        <button
          onClick={handleCreateSession}
          disabled={loading}
          className="create-button"
        >
          {loading ? 'Creating...' : 'Create New Session'}
        </button>
      </div>
    </div>
  )
}

export default SessionCreator

