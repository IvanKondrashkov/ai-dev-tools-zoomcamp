import { describe, it, expect, vi, beforeEach } from 'vitest'
import axios from 'axios'
import { resumeApi, evaluationApi } from '../../api/resumes'

// Mock axios
vi.mock('axios')
const mockedAxios = axios

describe('Resume API', () => {
  beforeEach(() => {
    vi.clearAllMocks()
  })

  describe('resumeApi', () => {
    it('getAll fetches all resumes', async () => {
      const mockData = { resumes: [], total: 0 }
      mockedAxios.create.mockReturnValue({
        get: vi.fn().mockResolvedValue({ data: mockData }),
      })

      const api = mockedAxios.create()
      const result = await api.get('/resumes/')

      expect(result.data).toEqual(mockData)
    })

    it('getById fetches a specific resume', async () => {
      const mockResume = { id: 1, filename: 'test.pdf' }
      mockedAxios.create.mockReturnValue({
        get: vi.fn().mockResolvedValue({ data: mockResume }),
      })

      const api = mockedAxios.create()
      const result = await api.get('/resumes/1')

      expect(result.data).toEqual(mockResume)
    })

    it('create uploads a new resume', async () => {
      const mockFile = new File(['content'], 'test.pdf', { type: 'application/pdf' })
      const mockResponse = { id: 1, filename: 'test.pdf' }
      
      mockedAxios.create.mockReturnValue({
        post: vi.fn().mockResolvedValue({ data: mockResponse }),
      })

      const api = mockedAxios.create()
      const formData = new FormData()
      formData.append('file', mockFile)
      const result = await api.post('/resumes/', formData, {
        headers: { 'Content-Type': 'multipart/form-data' },
      })

      expect(result.data).toEqual(mockResponse)
    })

    it('delete removes a resume', async () => {
      mockedAxios.create.mockReturnValue({
        delete: vi.fn().mockResolvedValue({}),
      })

      const api = mockedAxios.create()
      await api.delete('/resumes/1')

      expect(api.delete).toHaveBeenCalledWith('/resumes/1')
    })
  })

  describe('evaluationApi', () => {
    it('getByResumeId fetches evaluations for a resume', async () => {
      const mockEvaluations = [{ id: 1, rating: 4.5 }]
      mockedAxios.create.mockReturnValue({
        get: vi.fn().mockResolvedValue({ data: mockEvaluations }),
      })

      const api = mockedAxios.create()
      const result = await api.get('/evaluations/resume/1')

      expect(result.data).toEqual(mockEvaluations)
    })

    it('create creates a new evaluation', async () => {
      const mockEvaluation = { id: 1, rating: 4.5 }
      mockedAxios.create.mockReturnValue({
        post: vi.fn().mockResolvedValue({ data: mockEvaluation }),
      })

      const api = mockedAxios.create()
      const evaluationData = { resume_id: 1, rating: 4.5, evaluator_name: 'Test' }
      const result = await api.post('/evaluations/', evaluationData)

      expect(result.data).toEqual(mockEvaluation)
    })
  })
})

