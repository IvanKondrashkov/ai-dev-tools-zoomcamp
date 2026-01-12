import { describe, it, expect, vi, beforeEach } from 'vitest'
import { render, screen, waitFor } from '@testing-library/react'
import { BrowserRouter } from 'react-router-dom'
import { act } from 'react'
import ResumeList from '../../components/ResumeList'
import { resumeApi } from '../../api/resumes'

// Mock the API
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

describe('ResumeList', () => {
  const mockResumes = {
    resumes: [
      {
        id: 1,
        filename: 'resume1.pdf',
        original_filename: 'John_Doe_Resume.pdf',
        file_type: 'pdf',
        created_at: '2024-01-01T00:00:00Z',
      },
      {
        id: 2,
        filename: 'resume2.txt',
        original_filename: 'Jane_Smith_Resume.txt',
        file_type: 'txt',
        created_at: '2024-01-02T00:00:00Z',
      },
    ],
    total: 2,
  }

  beforeEach(() => {
    vi.clearAllMocks()
  })

  it('renders resume list with data', async () => {
    resumeApi.getAll.mockResolvedValue(mockResumes)

    await act(async () => {
      render(
        <BrowserRouter future={{ v7_startTransition: true, v7_relativeSplatPath: true }}>
          <ResumeList />
        </BrowserRouter>
      )
    })

    await waitFor(() => {
      expect(screen.getByText('Resumes')).toBeInTheDocument()
      expect(screen.getByText('John_Doe_Resume.pdf')).toBeInTheDocument()
      expect(screen.getByText('Jane_Smith_Resume.txt')).toBeInTheDocument()
    })
  })

  it('renders empty state when no resumes', async () => {
    resumeApi.getAll.mockResolvedValue({ resumes: [], total: 0 })

    await act(async () => {
      render(
        <BrowserRouter future={{ v7_startTransition: true, v7_relativeSplatPath: true }}>
          <ResumeList />
        </BrowserRouter>
      )
    })

    await waitFor(() => {
      expect(screen.getByText(/No resumes uploaded yet/i)).toBeInTheDocument()
    })
  })

  it('shows upload button', async () => {
    resumeApi.getAll.mockResolvedValue({ resumes: [], total: 0 })

    await act(async () => {
      render(
        <BrowserRouter future={{ v7_startTransition: true, v7_relativeSplatPath: true }}>
          <ResumeList />
        </BrowserRouter>
      )
    })

    await waitFor(() => {
      // Find upload button by class name (more specific)
      const uploadButton = document.querySelector('.upload-button')
      expect(uploadButton).toBeInTheDocument()
      expect(uploadButton).toHaveTextContent(/Upload Resume/i)
    })
  })
})

