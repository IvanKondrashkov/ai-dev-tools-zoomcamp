import axios from 'axios'

// On Render, use relative paths (Nginx will proxy /api to backend)
// For local development, use VITE_API_URL if set, otherwise default to localhost
const getApiBaseUrl = () => {
  // If VITE_API_URL is explicitly set and not empty, use it (for direct backend access)
  const viteApiUrl = import.meta.env.VITE_API_URL
  if (viteApiUrl && viteApiUrl.trim() !== '') {
    return viteApiUrl
  }
  // Otherwise, use relative path (works with Nginx proxy on Render)
  // This will be '/api' which Nginx will proxy to backend
  return '/api'
}

const API_BASE_URL = getApiBaseUrl()

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
})

// API implementation
export const resumeApi = {
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

// API implementation
export const evaluationApi = {
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

export default api

