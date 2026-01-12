import { useState } from 'react'
import { BrowserRouter as Router, Routes, Route, Link } from 'react-router-dom'
import ResumeList from './components/ResumeList'
import ResumeDetail from './components/ResumeDetail'
import './App.css'

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
            </Routes>
          </div>
        </main>
      </div>
    </Router>
  )
}

export default App

