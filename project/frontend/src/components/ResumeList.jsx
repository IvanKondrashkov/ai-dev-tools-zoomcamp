import { useState, useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import { resumeApi } from '../api/resumes'
import './ResumeList.css'

const ResumeList = () => {
  const [resumes, setResumes] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)
  const [uploading, setUploading] = useState(false)
  const navigate = useNavigate()

  useEffect(() => {
    loadResumes()
  }, [])

  const loadResumes = async () => {
    try {
      setLoading(true)
      const data = await resumeApi.getAll()
      setResumes(data.resumes || [])
      setError(null)
    } catch (err) {
      setError('Failed to load resumes')
      console.error(err)
    } finally {
      setLoading(false)
    }
  }

  const handleFileUpload = async (event) => {
    const file = event.target.files[0]
    if (!file) return

    // Validate file type
    const fileExtension = file.name.split('.').pop().toLowerCase()
    if (!['pdf', 'txt'].includes(fileExtension)) {
      alert('Only PDF and TXT files are allowed')
      return
    }

    try {
      setUploading(true)
      await resumeApi.create(file)
      await loadResumes()
      event.target.value = '' // Reset input
    } catch (err) {
      alert('Failed to upload resume')
      console.error(err)
    } finally {
      setUploading(false)
    }
  }

  const handleDelete = async (id, event) => {
    event.stopPropagation()
    if (!confirm('Are you sure you want to delete this resume?')) {
      return
    }

    try {
      await resumeApi.delete(id)
      await loadResumes()
    } catch (err) {
      alert('Failed to delete resume')
      console.error(err)
    }
  }

  const handleResumeClick = (id) => {
    navigate(`/resume/${id}`)
  }

  if (loading) {
    return <div className="loading">Loading resumes...</div>
  }

  return (
    <div className="resume-list">
      <div className="resume-list-header">
        <h2>Resumes</h2>
        <label className="upload-button">
          {uploading ? 'Uploading...' : 'Upload Resume'}
          <input
            type="file"
            accept=".pdf,.txt"
            onChange={handleFileUpload}
            disabled={uploading}
            style={{ display: 'none' }}
          />
        </label>
      </div>

      {error && <div className="error">{error}</div>}

      {resumes.length === 0 ? (
        <div className="empty-state">
          <p>No resumes uploaded yet.</p>
          <p>Click "Upload Resume" to get started.</p>
        </div>
      ) : (
        <div className="resume-grid">
          {resumes.map((resume) => (
            <div
              key={resume.id}
              className="resume-card"
              onClick={() => handleResumeClick(resume.id)}
            >
              <div className="resume-card-header">
                <h3>{resume.original_filename}</h3>
                <button
                  className="delete-button"
                  onClick={(e) => handleDelete(resume.id, e)}
                  aria-label="Delete resume"
                >
                  ×
                </button>
              </div>
              <div className="resume-card-body">
                <span className="file-type-badge">{resume.file_type.toUpperCase()}</span>
                <p className="resume-date">
                  Uploaded: {new Date(resume.created_at).toLocaleDateString()}
                </p>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  )
}

export default ResumeList

