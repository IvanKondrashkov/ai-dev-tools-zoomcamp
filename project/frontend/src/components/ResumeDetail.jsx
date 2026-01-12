import { useState, useEffect, useRef } from 'react'
import { useParams, useNavigate } from 'react-router-dom'
import { resumeApi, evaluationApi } from '../api/resumes'
import ChatPanel from './ChatPanel'
import EvaluationPanel from './EvaluationPanel'
import './ResumeDetail.css'

const ResumeDetail = () => {
  const { id } = useParams()
  const navigate = useNavigate()
  const [resume, setResume] = useState(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)
  const contentRef = useRef(null)

  useEffect(() => {
    loadResume()
  }, [id])

  const loadResume = async () => {
    try {
      setLoading(true)
      const data = await resumeApi.getById(id)
      setResume(data)
      setError(null)
    } catch (err) {
      setError('Failed to load resume')
      console.error(err)
    } finally {
      setLoading(false)
    }
  }

  if (loading) {
    return <div className="loading">Loading resume...</div>
  }

  if (error || !resume) {
    return (
      <div className="error-container">
        <p>{error || 'Resume not found'}</p>
        <button onClick={() => navigate('/')}>Back to List</button>
      </div>
    )
  }

  return (
    <div className="resume-detail">
      <div className="resume-detail-header">
        <button className="back-button" onClick={() => navigate('/')}>
          ← Back
        </button>
        <h2>{resume.original_filename}</h2>
      </div>

      <div className="resume-detail-content">
        <div className="resume-viewer">
          <div className="resume-viewer-header">
            <span className="file-type-badge">{resume.file_type.toUpperCase()}</span>
            <span className="resume-date">
              Uploaded: {new Date(resume.created_at).toLocaleString()}
            </span>
          </div>
          <div className="resume-content" ref={contentRef}>
            {resume.content ? (
              <pre>{resume.content}</pre>
            ) : (
              <p className="no-content">No content extracted from this file.</p>
            )}
          </div>
        </div>

        <div className="resume-sidebar">
          <EvaluationPanel resumeId={parseInt(id)} />
          <ChatPanel resumeId={parseInt(id)} />
        </div>
      </div>
    </div>
  )
}

export default ResumeDetail

