import { BrowserRouter as Router, Routes, Route, Link, Navigate, useParams } from 'react-router-dom'
import ResumeList from './components/ResumeList'
import ResumeDetail from './components/ResumeDetail'
import './App.css'

// Component to redirect from /chat/resume/:id to /resume/:id
const ChatRedirect = () => {
  const { id } = useParams()
  return <Navigate to={`/resume/${id}`} replace />
}

function App() {
  return (
    <Router>
      <div className="app">
        <header className="app-header">
          <div className="container">
            <Link to="/" className="logo">
              <h1>HR Resume Review Platform</h1>
            </Link>
          </div>
        </header>

        <main className="app-main">
          <div className="container">
            <Routes>
              <Route path="/" element={<ResumeList />} />
              <Route path="/resume/:id" element={<ResumeDetail />} />
              {/* Redirect old chat route to resume detail page */}
              <Route path="/chat/resume/:id" element={<ChatRedirect />} />
            </Routes>
          </div>
        </main>
      </div>
    </Router>
  )
}

export default App

