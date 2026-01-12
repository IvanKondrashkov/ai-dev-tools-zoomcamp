import { describe, it, expect, vi, beforeEach } from 'vitest'
import { render, screen, waitFor } from '@testing-library/react'
import { act } from 'react'
import userEvent from '@testing-library/user-event'
import EvaluationPanel from '../../components/EvaluationPanel'
import { evaluationApi } from '../../api/resumes'

vi.mock('../../api/resumes', () => ({
  resumeApi: {
    getAll: vi.fn(),
    delete: vi.fn(),
    create: vi.fn(),
    getById: vi.fn(),
    update: vi.fn(),
  },
  evaluationApi: {
    getByResumeId: vi.fn(),
    create: vi.fn(),
  },
}))

describe('EvaluationPanel', () => {
  const mockEvaluations = [
    {
      id: 1,
      resume_id: 1,
      rating: 4.5,
      comment: 'Great candidate',
      evaluator_name: 'HR Manager',
      created_at: '2024-01-01T00:00:00Z',
    },
  ]

  beforeEach(() => {
    vi.clearAllMocks()
  })

  it('renders evaluations list', async () => {
    evaluationApi.getByResumeId.mockResolvedValue(mockEvaluations)

    await act(async () => {
      render(<EvaluationPanel resumeId={1} />)
    })

    await waitFor(() => {
      expect(screen.getByText('Evaluations')).toBeInTheDocument()
      expect(screen.getByText('HR Manager')).toBeInTheDocument()
      expect(screen.getByText('Great candidate')).toBeInTheDocument()
    })
  })

  it('shows add evaluation button', async () => {
    evaluationApi.getByResumeId.mockResolvedValue([])

    await act(async () => {
      render(<EvaluationPanel resumeId={1} />)
    })

    await waitFor(() => {
      expect(screen.getByText(/Add Evaluation/i)).toBeInTheDocument()
    })
  })

  it('opens evaluation form when add button clicked', async () => {
    const user = userEvent.setup()
    evaluationApi.getByResumeId.mockResolvedValue([])

    await act(async () => {
      render(<EvaluationPanel resumeId={1} />)
    })

    await waitFor(() => {
      expect(screen.getByText(/Add Evaluation/i)).toBeInTheDocument()
    })

    const addButton = screen.getByText(/Add Evaluation/i)
    await act(async () => {
      await user.click(addButton)
    })

    await waitFor(() => {
      expect(screen.getByLabelText(/Your Name/i)).toBeInTheDocument()
      expect(screen.getByLabelText(/Rating/i)).toBeInTheDocument()
    })
  })
})

