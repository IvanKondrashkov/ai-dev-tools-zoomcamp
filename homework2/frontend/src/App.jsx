import { useState, useEffect } from 'react'
import { BrowserRouter, Routes, Route, useParams, useNavigate } from 'react-router-dom'
import CodeEditor from './components/CodeEditor'
import SessionCreator from './components/SessionCreator'
import './App.css'

const App = () => {
  return (
    <BrowserRouter future={{ v7_startTransition: true, v7_relativeSplatPath: true }}>
      <div className="app">
        <Routes>
          <Route path="/" element={<SessionCreator />} />
          <Route path="/session/:sessionId" element={<SessionPage />} />
        </Routes>
      </div>
    </BrowserRouter>
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

export default App

