import { useState, useEffect } from 'react'
import { evaluationApi } from '../api/resumes'
import './EvaluationPanel.css'

const EvaluationPanel = ({ resumeId }) => {
  const [evaluations, setEvaluations] = useState([])
  const [loading, setLoading] = useState(true)
  const [showForm, setShowForm] = useState(false)
  const [rating, setRating] = useState(3)
  const [comment, setComment] = useState('')
  const [evaluatorName, setEvaluatorName] = useState('')
  const [submitting, setSubmitting] = useState(false)

  useEffect(() => {
    loadEvaluations()
  }, [resumeId])

  const loadEvaluations = async () => {
    try {
      setLoading(true)
      const data = await evaluationApi.getByResumeId(resumeId)
      setEvaluations(data || [])
    } catch (err) {
      console.error('Failed to load evaluations:', err)
    } finally {
      setLoading(false)
    }
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    if (!evaluatorName.trim()) {
      alert('Please enter your name')
      return
    }

    try {
      setSubmitting(true)
      await evaluationApi.create({
        resume_id: resumeId,
        rating: parseFloat(rating),
        comment: comment.trim() || null,
        evaluator_name: evaluatorName.trim(),
      })
      setRating(3)
      setComment('')
      setEvaluatorName('')
      setShowForm(false)
      await loadEvaluations()
    } catch (err) {
      alert('Failed to submit evaluation')
      console.error(err)
    } finally {
      setSubmitting(false)
    }
  }

  const averageRating = evaluations.length > 0
    ? (evaluations.reduce((sum, e) => sum + e.rating, 0) / evaluations.length).toFixed(1)
    : 0

  return (
    <div className="evaluation-panel">
      <div className="panel-header">
        <h3>Evaluations</h3>
        {evaluations.length > 0 && (
          <span className="average-rating">Avg: {averageRating} ⭐</span>
        )}
      </div>

      {!showForm ? (
        <button
          className="add-evaluation-button"
          onClick={() => setShowForm(true)}
        >
          + Add Evaluation
        </button>
      ) : (
        <form className="evaluation-form" onSubmit={handleSubmit}>
          <div className="form-group">
            <label htmlFor="evaluator-name">Your Name</label>
            <input
              id="evaluator-name"
              type="text"
              value={evaluatorName}
              onChange={(e) => setEvaluatorName(e.target.value)}
              placeholder="Enter your name"
              required
            />
          </div>

          <div className="form-group">
            <label htmlFor="rating">Rating</label>
            <div className="rating-input">
              <input
                id="rating"
                type="range"
                min="1"
                max="5"
                step="0.5"
                value={rating}
                onChange={(e) => setRating(e.target.value)}
              />
              <span className="rating-value">{rating} ⭐</span>
            </div>
          </div>

          <div className="form-group">
            <label htmlFor="comment">Comment (optional)</label>
            <textarea
              id="comment"
              value={comment}
              onChange={(e) => setComment(e.target.value)}
              placeholder="Add your comment..."
              rows="4"
            />
          </div>

          <div className="form-actions">
            <button
              type="button"
              onClick={() => {
                setShowForm(false)
                setRating(3)
                setComment('')
                setEvaluatorName('')
              }}
            >
              Cancel
            </button>
            <button type="submit" disabled={submitting}>
              {submitting ? 'Submitting...' : 'Submit'}
            </button>
          </div>
        </form>
      )}

      <div className="evaluations-list">
        {loading ? (
          <p className="loading-text">Loading evaluations...</p>
        ) : evaluations.length === 0 ? (
          <p className="empty-text">No evaluations yet.</p>
        ) : (
          evaluations.map((evaluation) => (
            <div key={evaluation.id} className="evaluation-item">
              <div className="evaluation-header">
                <span className="evaluator-name">{evaluation.evaluator_name}</span>
                <span className="evaluation-rating">{evaluation.rating} ⭐</span>
              </div>
              {evaluation.comment && (
                <p className="evaluation-comment">{evaluation.comment}</p>
              )}
              <span className="evaluation-date">
                {new Date(evaluation.created_at).toLocaleString()}
              </span>
            </div>
          ))
        )}
      </div>
    </div>
  )
}

export default EvaluationPanel

