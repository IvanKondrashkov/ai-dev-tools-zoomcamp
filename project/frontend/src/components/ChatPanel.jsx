import { useState, useEffect, useRef } from 'react'
import './ChatPanel.css'

const ChatPanel = ({ resumeId }) => {
  const [messages, setMessages] = useState([])
  const [newMessage, setNewMessage] = useState('')
  const [username, setUsername] = useState('')
  const [ws, setWs] = useState(null)
  const [connected, setConnected] = useState(false)
  const [isJoined, setIsJoined] = useState(false)
  const messagesEndRef = useRef(null)

  // Load messages when component mounts or resumeId changes
  useEffect(() => {
    console.log('ChatPanel mounted/updated for resume:', resumeId)
    loadMessages()
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [resumeId])

  // Initialize state when component mounts or resumeId changes
  useEffect(() => {
    console.log('Initializing ChatPanel for resume:', resumeId)
    
    // Reset WebSocket connection when resumeId changes
    if (ws) {
      ws.close()
      setWs(null)
    }
    setConnected(false)
    setIsJoined(false)
    
    // Always start with Join form - don't auto-join based on sessionStorage
    // This ensures each tab/window requires explicit join action
    // sessionStorage may be shared when duplicating tabs
    setUsername('')
    
    // Cleanup on unmount
    return () => {
      if (ws) {
        ws.close()
      }
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [resumeId])

  // Connect to WebSocket when username is set
  useEffect(() => {
    if (!isJoined || !resumeId || !username.trim()) return

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
  }, [resumeId, username, isJoined])

  useEffect(() => {
    scrollToBottom()
  }, [messages])

  const loadMessages = async () => {
    try {
      console.log('Loading messages for resume:', resumeId)
      // Use relative path (works with Nginx proxy on Render)
      // Or use VITE_API_URL if set (for direct backend access)
      const apiBaseUrl = import.meta.env.VITE_API_URL && import.meta.env.VITE_API_URL.trim() !== ''
        ? import.meta.env.VITE_API_URL
        : '/api'
      const url = `${apiBaseUrl}/chat/resume/${resumeId}`
      console.log('Fetching messages from:', url)
      const response = await fetch(url)
      if (!response.ok) {
        console.error('Failed to load messages:', response.status, response.statusText)
        setMessages([])
        return
      }
      const data = await response.json()
      setMessages(data || [])
      console.log('Loaded messages from API:', data?.length || 0, 'messages')
    } catch (err) {
      console.error('Failed to load messages:', err)
      setMessages([])
    }
  }

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }

  const handleUsernameSubmit = (e) => {
    e.preventDefault()
    if (username.trim()) {
      const trimmedUsername = username.trim()
      // Save username to sessionStorage (for persistence within this tab)
      // But don't rely on it for auto-join - always require explicit join action
      sessionStorage.setItem('chat_username', trimmedUsername)
      sessionStorage.setItem(`chat_joined_${resumeId}`, 'true')
      setUsername(trimmedUsername)
      setIsJoined(true) // This will trigger re-render and WebSocket connection
      console.log('User joined chat:', trimmedUsername)
    }
  }

  const handleSendMessage = async (e) => {
    e.preventDefault()
    if (!newMessage.trim()) return
    if (!username.trim()) {
      alert('Please set your username first')
      return
    }

    if (!ws || !connected) return
    ws.send(
      JSON.stringify({
        username: username.trim(),
        message: newMessage.trim(),
      })
    )
    setNewMessage('')
  }

  // Show Join form if user hasn't joined yet
  if (!isJoined) {
    return (
      <div className="chat-panel">
        <div className="panel-header">
          <h3>Chat</h3>
        </div>
        <div className="chat-messages">
          {messages.length === 0 ? (
            <p className="empty-text">No messages yet. Join to start chatting!</p>
          ) : (
            messages.map((message) => (
              <div key={message.id} className="chat-message">
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
        <form className="username-form" onSubmit={handleUsernameSubmit}>
          <input
            type="text"
            value={username}
            onChange={(e) => setUsername(e.target.value)}
            placeholder="Enter your name to join chat"
            required
            autoFocus
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
        <span className={`connection-status ${connected ? 'connected' : 'disconnected'}`}>
          {connected ? '●' : '○'}
        </span>
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
          disabled={!connected}
        />
        <button type="submit" disabled={!connected || !newMessage.trim()}>
          Send
        </button>
      </form>
    </div>
  )
}

export default ChatPanel

