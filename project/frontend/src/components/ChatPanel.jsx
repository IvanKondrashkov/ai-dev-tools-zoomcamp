import { useState, useEffect, useRef } from 'react'
import { mockChatApi } from '../api/mock.js'
import './ChatPanel.css'

const USE_MOCK = import.meta.env.VITE_USE_MOCK === 'true' || import.meta.env.VITE_API_URL === undefined

const ChatPanel = ({ resumeId }) => {
  const [messages, setMessages] = useState([])
  const [newMessage, setNewMessage] = useState('')
  const [username, setUsername] = useState('')
  const [ws, setWs] = useState(null)
  const [connected, setConnected] = useState(false)
  const messagesEndRef = useRef(null)
  const usernameSetRef = useRef(false)

  useEffect(() => {
    // Get or set username from localStorage
    const savedUsername = localStorage.getItem('chat_username')
    if (savedUsername) {
      setUsername(savedUsername)
      usernameSetRef.current = true
    }

    // Load existing messages
    loadMessages()

    // In mock mode, simulate connection
    if (USE_MOCK) {
      setConnected(true)
    }

    // Cleanup on unmount
    return () => {
      if (ws) {
        ws.close()
      }
    }
  }, [resumeId])

  // Connect to WebSocket when username is set and not using mock
  useEffect(() => {
    if (USE_MOCK || !usernameSetRef.current || !resumeId || !username.trim()) return

    // Build WebSocket URL
    const wsProtocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:'
    let wsHost
    if (import.meta.env.VITE_WS_URL) {
      wsHost = import.meta.env.VITE_WS_URL
    } else if (window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1') {
      // Local development
      wsHost = window.location.host.replace(':5173', ':8000').replace(':3000', ':8000')
    } else {
      // Docker/production - use same host with ws protocol
      wsHost = window.location.host
    }
    const wsUrl = `${wsProtocol}//${wsHost}/api/chat/ws/${resumeId}`
    
    console.log('Connecting to WebSocket:', wsUrl)
    const websocket = new WebSocket(wsUrl)

    websocket.onopen = () => {
      console.log('WebSocket connected')
      setConnected(true)
      setWs(websocket)
    }

    websocket.onmessage = (event) => {
      const data = JSON.parse(event.data)
      if (data.error) {
        console.error('WebSocket error:', data.error)
        return
      }
      setMessages((prev) => [...prev, data])
    }

    websocket.onerror = (error) => {
      console.error('WebSocket error:', error)
      setConnected(false)
    }

    websocket.onclose = (event) => {
      console.log('WebSocket closed:', event.code, event.reason)
      setConnected(false)
      setWs(null)
    }

    return () => {
      if (websocket.readyState === WebSocket.OPEN || websocket.readyState === WebSocket.CONNECTING) {
        websocket.close()
      }
    }
  }, [resumeId, username])

  useEffect(() => {
    scrollToBottom()
  }, [messages])

  const loadMessages = async () => {
    try {
      if (USE_MOCK) {
        const data = await mockChatApi.getMessages(resumeId)
        setMessages(data || [])
      } else {
        const apiBaseUrl = import.meta.env.VITE_API_URL || 'http://localhost:8000/api'
        const response = await fetch(`${apiBaseUrl}/chat/resume/${resumeId}`)
        const data = await response.json()
        setMessages(data || [])
      }
    } catch (err) {
      console.error('Failed to load messages:', err)
    }
  }

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }

  const handleUsernameSubmit = (e) => {
    e.preventDefault()
    if (username.trim()) {
      localStorage.setItem('chat_username', username.trim())
      usernameSetRef.current = true
      // Force re-render to trigger WebSocket connection
      setUsername(username.trim())
    }
  }

  const handleSendMessage = async (e) => {
    e.preventDefault()
    if (!newMessage.trim()) return
    if (!username.trim()) {
      alert('Please set your username first')
      return
    }

    if (USE_MOCK) {
      // Use mock API
      const message = await mockChatApi.sendMessage(resumeId, username.trim(), newMessage.trim())
      setMessages((prev) => [...prev, message])
      setNewMessage('')
    } else {
      // Use real WebSocket
      if (!ws || !connected) return
      ws.send(
        JSON.stringify({
          username: username.trim(),
          message: newMessage.trim(),
        })
      )
      setNewMessage('')
    }
  }

  if (!usernameSetRef.current) {
    return (
      <div className="chat-panel">
        <div className="panel-header">
          <h3>Chat</h3>
        </div>
        <form className="username-form" onSubmit={handleUsernameSubmit}>
          <input
            type="text"
            value={username}
            onChange={(e) => setUsername(e.target.value)}
            placeholder="Enter your name to join chat"
            required
          />
          <button type="submit">Join</button>
        </form>
      </div>
    )
  }

  return (
    <div className="chat-panel">
      <div className="panel-header">
        <h3>Chat</h3>
        {!USE_MOCK && (
          <span className={`connection-status ${connected ? 'connected' : 'disconnected'}`}>
            {connected ? '●' : '○'}
          </span>
        )}
      </div>

      <div className="chat-messages">
        {messages.length === 0 ? (
          <p className="empty-text">No messages yet. Start the conversation!</p>
        ) : (
          messages.map((message) => (
            <div
              key={message.id}
              className={`chat-message ${
                message.username === username.trim() ? 'own-message' : ''
              }`}
            >
              <div className="message-header">
                <span className="message-username">{message.username}</span>
                <span className="message-time">
                  {new Date(message.created_at).toLocaleTimeString()}
                </span>
              </div>
              <p className="message-text">{message.message}</p>
            </div>
          ))
        )}
        <div ref={messagesEndRef} />
      </div>

      <form className="chat-input-form" onSubmit={handleSendMessage}>
        <input
          type="text"
          value={newMessage}
          onChange={(e) => setNewMessage(e.target.value)}
          placeholder="Type a message..."
          disabled={!USE_MOCK && !connected}
        />
        <button type="submit" disabled={(!USE_MOCK && !connected) || !newMessage.trim()}>
          Send
        </button>
      </form>
    </div>
  )
}

export default ChatPanel

