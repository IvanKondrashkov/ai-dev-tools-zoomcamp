// Mock API for frontend development
// This allows frontend to work without backend

const MOCK_DELAY = 500 // Simulate network delay

const mockResumes = [
  {
    id: 1,
    filename: 'resume1.pdf',
    original_filename: 'John_Doe_Resume.pdf',
    file_type: 'pdf',
    file_path: '/uploads/resume1.pdf',
    content: 'John Doe\nSoftware Engineer\n5 years of experience in React and Python...',
    created_at: new Date().toISOString(),
    updated_at: null,
  },
  {
    id: 2,
    filename: 'resume2.txt',
    original_filename: 'Jane_Smith_Resume.txt',
    file_type: 'txt',
    file_path: '/uploads/resume2.txt',
    content: 'Jane Smith\nData Scientist\nExpert in machine learning and data analysis...',
    created_at: new Date().toISOString(),
    updated_at: null,
  },
]

const mockEvaluations = {
  1: [
    {
      id: 1,
      resume_id: 1,
      rating: 4.5,
      comment: 'Strong technical skills, good experience',
      evaluator_name: 'HR Manager',
      created_at: new Date().toISOString(),
    },
  ],
  2: [
    {
      id: 2,
      resume_id: 2,
      rating: 5.0,
      comment: 'Excellent candidate, highly recommended',
      evaluator_name: 'Tech Lead',
      created_at: new Date().toISOString(),
    },
  ],
}

const mockChatMessages = {
  1: [
    {
      id: 1,
      resume_id: 1,
      username: 'HR Manager',
      message: 'This candidate looks promising',
      created_at: new Date().toISOString(),
    },
  ],
  2: [
    {
      id: 2,
      resume_id: 2,
      username: 'Tech Lead',
      message: 'Great technical background',
      created_at: new Date().toISOString(),
    },
  ],
}

const delay = (ms) => new Promise((resolve) => setTimeout(resolve, ms))

export const mockResumeApi = {
  getAll: async () => {
    await delay(MOCK_DELAY)
    return {
      resumes: mockResumes,
      total: mockResumes.length,
    }
  },

  getById: async (id) => {
    await delay(MOCK_DELAY)
    const resume = mockResumes.find((r) => r.id === parseInt(id))
    if (!resume) {
      throw new Error('Resume not found')
    }
    return resume
  },

  create: async (file) => {
    await delay(MOCK_DELAY * 2)
    const newResume = {
      id: mockResumes.length + 1,
      filename: file.name,
      original_filename: file.name,
      file_type: file.name.split('.').pop().toLowerCase(),
      file_path: `/uploads/${file.name}`,
      content: `Mock content from ${file.name}`,
      created_at: new Date().toISOString(),
      updated_at: null,
    }
    mockResumes.push(newResume)
    return newResume
  },

  update: async (id, file) => {
    await delay(MOCK_DELAY * 2)
    const resume = mockResumes.find((r) => r.id === parseInt(id))
    if (!resume) {
      throw new Error('Resume not found')
    }
    resume.filename = file.name
    resume.original_filename = file.name
    resume.file_type = file.name.split('.').pop().toLowerCase()
    resume.content = `Updated mock content from ${file.name}`
    resume.updated_at = new Date().toISOString()
    return resume
  },

  delete: async (id) => {
    await delay(MOCK_DELAY)
    const index = mockResumes.findIndex((r) => r.id === parseInt(id))
    if (index === -1) {
      throw new Error('Resume not found')
    }
    mockResumes.splice(index, 1)
    delete mockEvaluations[id]
    delete mockChatMessages[id]
  },
}

export const mockEvaluationApi = {
  getByResumeId: async (resumeId) => {
    await delay(MOCK_DELAY)
    return mockEvaluations[resumeId] || []
  },

  create: async (evaluation) => {
    await delay(MOCK_DELAY)
    const newEvaluation = {
      id: Date.now(),
      ...evaluation,
      created_at: new Date().toISOString(),
    }
    if (!mockEvaluations[evaluation.resume_id]) {
      mockEvaluations[evaluation.resume_id] = []
    }
    mockEvaluations[evaluation.resume_id].push(newEvaluation)
    return newEvaluation
  },
}

export const mockChatApi = {
  getMessages: async (resumeId) => {
    await delay(MOCK_DELAY)
    return mockChatMessages[resumeId] || []
  },

  sendMessage: async (resumeId, username, message) => {
    await delay(MOCK_DELAY)
    const newMessage = {
      id: Date.now(),
      resume_id: resumeId,
      username,
      message,
      created_at: new Date().toISOString(),
    }
    if (!mockChatMessages[resumeId]) {
      mockChatMessages[resumeId] = []
    }
    mockChatMessages[resumeId].push(newMessage)
    return newMessage
  },
}

