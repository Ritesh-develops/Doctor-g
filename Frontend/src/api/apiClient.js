import axios from 'axios'
import toast from 'react-hot-toast'

// Fix URL construction - remove trailing slash
const API_URL = (import.meta.env.VITE_API_URL || 'https://your-render-backend-url.onrender.com').replace(/\/$/, '')

class ApiClient {
  constructor() {
    this.client = axios.create({
      baseURL: `${API_URL}/api/v1`, // This will create proper URLs
      headers: {
        'Content-Type': 'application/json',
      },
      timeout: 30000,
    })

    // Request interceptor to add auth token
    this.client.interceptors.request.use(
      (config) => {
        const token = localStorage.getItem('accessToken')
        if (token) {
          config.headers.Authorization = `Bearer ${token}`
        }
        
        // Debug log - remove double slashes if any
        console.log(`🚀 ${config.method?.toUpperCase()} ${config.url}`)
        
        return config
      },
      (error) => {
        console.error('Request error:', error)
        return Promise.reject(error)
      }
    )

    // Response interceptor for error handling
    this.client.interceptors.response.use(
      (response) => {
        console.log(`✅ ${response.config.method?.toUpperCase()} ${response.config.url} - ${response.status}`)
        return response
      },
      (error) => {
        console.error('❌ Response error:', error)
        
        if (error.response?.status === 401) {
          localStorage.removeItem('accessToken')
          localStorage.removeItem('refreshToken')
          window.location.href = '/login'
        }
        
        // Detailed error logging
        if (error.response) {
          console.error('Error details:', {
            status: error.response.status,
            data: error.response.data,
            url: error.config?.url,
            fullUrl: error.config?.baseURL + error.config?.url
          })
        } else if (error.request) {
          console.error('Network error - no response:', error.request)
          toast.error('Cannot connect to server. Please check your internet connection.')
        } else {
          console.error('Request configuration error:', error.message)
        }
        
        return Promise.reject(error)
      }
    )
  }

  // Auth methods
  async login(email, password) {
    try {
      console.log('🔐 Attempting login...', { 
        email, 
        baseURL: this.client.defaults.baseURL 
      })
      
      const formData = new FormData()
      formData.append('username', email)
      formData.append('password', password)
      
      const response = await this.client.post('/auth/login', formData, {
        headers: {
          'Content-Type': 'application/x-www-form-urlencoded'
        }
      })
      
      const { access_token, token_type } = response.data
      localStorage.setItem('accessToken', access_token)
      toast.success('Login successful!')
      return response.data
    } catch (error) {
      console.error('Login failed:', error)
      const message = error.response?.data?.detail || 'Login failed'
      toast.error(message)
      throw error
    }
  }

  async register(email, password, full_name = '') {
    try {
      console.log('📝 Attempting registration...', { 
        email, 
        baseURL: this.client.defaults.baseURL 
      })
      
      const response = await this.client.post('/auth/register', {
        email,
        password,
        full_name
      })
      
      toast.success('Registration successful! Please login.')
      return response.data
    } catch (error) {
      console.error('Registration failed:', error)
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
          timeout: 60000,
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