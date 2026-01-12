import axios from 'axios'
import * as mockApi from './mock.js'

// Use mock API if VITE_USE_MOCK is true or if API is not available
const USE_MOCK = import.meta.env.VITE_USE_MOCK === 'true' || import.meta.env.VITE_API_URL === undefined

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api'

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
})

// Real API implementation
const realResumeApi = {
  // Get all resumes
  getAll: async () => {
    const response = await api.get('/resumes/')
    return response.data
  },

  // Get a specific resume
  getById: async (id) => {
    const response = await api.get(`/resumes/${id}`)
    return response.data
  },

  // Upload a new resume
  create: async (file) => {
    const formData = new FormData()
    formData.append('file', file)
    const response = await api.post('/resumes/', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    })
    return response.data
  },

  // Update a resume
  update: async (id, file) => {
    const formData = new FormData()
    formData.append('file', file)
    const response = await api.put(`/resumes/${id}`, formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    })
    return response.data
  },

  // Delete a resume
  delete: async (id) => {
    await api.delete(`/resumes/${id}`)
  },
}

// Real API implementation
const realEvaluationApi = {
  // Get all evaluations for a resume
  getByResumeId: async (resumeId) => {
    const response = await api.get(`/evaluations/resume/${resumeId}`)
    return response.data
  },

  // Create a new evaluation
  create: async (evaluation) => {
    const response = await api.post('/evaluations/', evaluation)
    return response.data
  },
}

// Export either mock or real API based on configuration
export const resumeApi = USE_MOCK ? mockApi.mockResumeApi : realResumeApi
export const evaluationApi = USE_MOCK ? mockApi.mockEvaluationApi : realEvaluationApi

export default api

