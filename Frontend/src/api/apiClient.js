import axios from 'axios'
import toast from 'react-hot-toast'

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'

class ApiClient {
  constructor() {
    this.client = axios.create({
      baseURL: `${API_URL}/api/v1`,
      headers: {
        'Content-Type': 'application/json',
      },
    })

    // Request interceptor to add auth token
    this.client.interceptors.request.use(
      (config) => {
        const token = localStorage.getItem('accessToken')
        if (token) {
          config.headers.Authorization = `Bearer ${token}`
        }
        return config
      },
      (error) => {
        return Promise.reject(error)
      }
    )

    // Response interceptor for error handling
    this.client.interceptors.response.use(
      (response) => response,
      (error) => {
        if (error.response?.status === 401) {
          localStorage.removeItem('accessToken')
          localStorage.removeItem('refreshToken')
          window.location.href = '/login'
        }
        return Promise.reject(error)
      }
    )
  }

  // Auth methods
  async login(email, password) {
    try {
      const response = await this.client.post('/auth/login', {
        username: email,
        password: password
      }, {
        headers: {
          'Content-Type': 'application/x-www-form-urlencoded'
        }
      })
      
      const { access_token, token_type } = response.data
      localStorage.setItem('accessToken', access_token)
      toast.success('Login successful!')
      return response.data
    } catch (error) {
      const message = error.response?.data?.detail || 'Login failed'
      toast.error(message)
      throw error
    }
  }

  async register(email, password) {
    try {
      const response = await this.client.post('/auth/register', {
        email,
        password
      })
      toast.success('Registration successful! Please login.')
      return response.data
    } catch (error) {
      const message = error.response?.data?.detail || 'Registration failed'
      toast.error(message)
      throw error
    }
  }

  async getCurrentUser() {
    try {
      const response = await this.client.get('/auth/me')
      return response.data
    } catch (error) {
      throw error
    }
  }

  logout() {
    localStorage.removeItem('accessToken')
    localStorage.removeItem('refreshToken')
    toast.success('Logged out successfully!')
  }

  // Chat methods
  async getConversations() {
    try {
      const response = await this.client.get('/chats/conversations/')
      return response.data
    } catch (error) {
      toast.error('Failed to load conversations')
      throw error
    }
  }

  async createConversation() {
    try {
      const response = await this.client.post('/chats/conversations/')
      toast.success('New conversation created!')
      return response.data
    } catch (error) {
      toast.error('Failed to create conversation')
      throw error
    }
  }

  async getConversationMessages(conversationId) {
    try {
      const response = await this.client.get(`/chats/conversations/${conversationId}/messages`)
      return response.data
    } catch (error) {
      toast.error('Failed to load messages')
      throw error
    }
  }

  async sendMessage(conversationId, message) {
    try {
      const response = await this.client.post(
        `/chats/conversations/${conversationId}/messages`,
        { message }
      )
      return response.data
    } catch (error) {
      toast.error('Failed to send message')
      throw error
    }
  }

  async analyzeXray(conversationId, file) {
    try {
      const formData = new FormData()
      formData.append('file', file)
      
      const response = await this.client.post(
        `/chats/conversations/${conversationId}/analyze`,
        formData,
        {
          headers: {
            'Content-Type': 'multipart/form-data',
          },
        }
      )
      toast.success('X-ray analysis complete!')
      return response.data
    } catch (error) {
      toast.error('Failed to analyze X-ray')
      throw error
    }
  }

  async deleteConversation(conversationId) {
    try {
      await this.client.delete(`/chats/conversations/${conversationId}`)
      toast.success('Conversation deleted')
    } catch (error) {
      toast.error('Failed to delete conversation')
      throw error
    }
  }

  // Scan methods
  async getScans() {
    try {
      const response = await this.client.get('/scans/')
      return response.data
    } catch (error) {
      toast.error('Failed to load scans')
      throw error
    }
  }

  async getScans() {
    try {
        const response = await this.client.get('/scans/')
        return response.data
    } catch (error) {
        console.error('Failed to load scans:', error)
        throw error
    }
}

async getScansCount() {
    try {
        const response = await this.client.get('/scans/count')
        return response.data.count
    } catch (error) {
        console.error('Failed to load scans count:', error)
        throw error
    }
}

async getScansStats() {
    try {
        const response = await this.client.get('/scans/stats')
        return response.data
    } catch (error) {
        console.error('Failed to load scans stats:', error)
        throw error
    }
}
}

export const apiClient = new ApiClient()