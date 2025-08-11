import React, { useState, useEffect } from 'react'
import { Link, useNavigate } from 'react-router-dom'
import { useAuth } from '../hooks/useAuth'
import { 
  MessageSquare, 
  Upload, 
  History, 
  Activity, 
  TrendingUp, 
  Clock,
  FileText,
  Plus,
  ArrowRight,
  X
} from 'lucide-react'
import { apiClient } from '../api/apiClient'
import toast from 'react-hot-toast'

const loadDashboardData = async () => {
  try {
    const [conversations, scanStats] = await Promise.all([
      apiClient.getConversations(),
      apiClient.getScansStats().catch(() => ({ total_scans: 0, month_scans: 0 }))
    ])
    
    setStats({
      totalConversations: conversations.length,
      totalScans: scanStats.total_scans || 0,
      recentActivity: conversations.slice(0, 5)
    })
  } catch (error) {
    console.error('Error loading dashboard data:', error)
  } finally {
    setLoading(false)
  }
}

const DashboardPage = () => {
  const { user } = useAuth()
  const navigate = useNavigate()
  const [stats, setStats] = useState({
    totalConversations: 0,
    totalScans: 0,
    recentActivity: []
  })
  const [loading, setLoading] = useState(true)
  const [quickUpload, setQuickUpload] = useState(false)
  const [uploading, setUploading] = useState(false)

  useEffect(() => {
    loadDashboardData()
  }, [])

  const loadDashboardData = async () => {
    try {
      const [conversations, scans] = await Promise.all([
        apiClient.getConversations(),
        apiClient.getScans().catch(() => []) // Handle if scans endpoint doesn't exist yet
      ])
      
      setStats({
        totalConversations: conversations.length,
        totalScans: Array.isArray(scans) ? scans.length : 0,
        recentActivity: conversations.slice(0, 5)
      })
    } catch (error) {
      console.error('Error loading dashboard data:', error)
    } finally {
      setLoading(false)
    }
  }

  const startNewConsultation = async () => {
    try {
      const response = await apiClient.createConversation()
      navigate(`/chat/${response.conversation_id}`)
    } catch (error) {
      console.error('Error creating consultation:', error)
      toast.error('Failed to create consultation')
    }
  }

  const handleQuickUploadSelect = (file) => {
    if (!file) return

    // Validate file type
    const allowedTypes = ['image/jpeg', 'image/jpg', 'image/png', 'image/gif', 'image/bmp', 'image/tiff']
    if (!allowedTypes.includes(file.type)) {
      toast.error('Please select a valid image file (JPEG, PNG, GIF, BMP, TIFF)')
      return
    }

    // Validate file size (10MB)
    if (file.size > 10485760) {
      toast.error('File size must be less than 10MB')
      return
    }

    handleQuickUpload(file)
  }

  const handleQuickUpload = async (file) => {
    setUploading(true)
    setQuickUpload(false)

    try {
      // Step 1: Create a new conversation
      toast.loading('Creating consultation...', { id: 'upload-process' })
      const conversationResponse = await apiClient.createConversation()
      const conversationId = conversationResponse.conversation_id

      // Step 2: Upload and analyze the image in that conversation
      toast.loading('Uploading and analyzing X-ray...', { id: 'upload-process' })
      await apiClient.analyzeXray(conversationId, file)

      // Step 3: Navigate to the conversation
      toast.success('X-ray uploaded and analyzed successfully!', { id: 'upload-process' })
      navigate(`/chat/${conversationId}`)

    } catch (error) {
      console.error('Error with quick upload:', error)
      toast.error('Failed to upload and analyze X-ray', { id: 'upload-process' })
    } finally {
      setUploading(false)
    }
  }

  const quickActions = [
    {
      icon: <MessageSquare className="w-6 h-6" />,
      title: 'New Consultation',
      description: 'Start a new medical consultation',
      action: startNewConsultation,
      color: 'bg-blue-500 hover:bg-blue-600'
    },
    {
      icon: <Upload className="w-6 h-6" />,
      title: 'Quick Upload',
      description: 'Upload X-ray for instant analysis',
      action: () => setQuickUpload(true),
      color: 'bg-green-500 hover:bg-green-600'
    },
    {
      icon: <History className="w-6 h-6" />,
      title: 'View History',
      description: 'Browse your consultation history',
      action: () => navigate('/history'),
      color: 'bg-purple-500 hover:bg-purple-600'
    }
  ]

  const formatDate = (dateString) => {
    const date = new Date(dateString)
    return date.toLocaleDateString('en-US', {
      month: 'short',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit'
    })
  }

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="animate-spin rounded-full h-32 w-32 border-b-2 border-blue-500"></div>
      </div>
    )
  }

  return (
    <div className="min-h-screen bg-gray-50 py-8">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        {/* Header */}
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-gray-900">
            Welcome back, {user?.email?.split('@')[0]}!
          </h1>
          <p className="text-gray-600 mt-2">
            Here's your medical consultation overview
          </p>
        </div>

        {/* Stats Cards */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
          <div className="bg-white rounded-lg shadow p-6">
            <div className="flex items-center">
              <div className="p-2 bg-blue-100 rounded-lg">
                <MessageSquare className="w-6 h-6 text-blue-600" />
              </div>
              <div className="ml-4">
                <p className="text-sm font-medium text-gray-600">Total Consultations</p>
                <p className="text-2xl font-bold text-gray-900">{stats.totalConversations}</p>
              </div>
            </div>
          </div>

          <div className="bg-white rounded-lg shadow p-6">
            <div className="flex items-center">
              <div className="p-2 bg-green-100 rounded-lg">
                <Activity className="w-6 h-6 text-green-600" />
              </div>
              <div className="ml-4">
                <p className="text-sm font-medium text-gray-600">X-ray Scans</p>
                <p className="text-2xl font-bold text-gray-900">{stats.totalScans}</p>
              </div>
            </div>
          </div>

          <div className="bg-white rounded-lg shadow p-6">
            <div className="flex items-center">
              <div className="p-2 bg-purple-100 rounded-lg">
                <TrendingUp className="w-6 h-6 text-purple-600" />
              </div>
              <div className="ml-4">
                <p className="text-sm font-medium text-gray-600">This Month</p>
                <p className="text-2xl font-bold text-gray-900">
                  {stats.recentActivity.filter(activity => {
                    const activityDate = new Date(activity.created_at)
                    const currentDate = new Date()
                    return activityDate.getMonth() === currentDate.getMonth()
                  }).length}
                </p>
              </div>
            </div>
          </div>
        </div>

        {/* Quick Actions */}
        <div className="mb-8">
          <h2 className="text-xl font-bold text-gray-900 mb-4">Quick Actions</h2>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            {quickActions.map((action, index) => (
              <button
                key={index}
                onClick={action.action}
                disabled={uploading}
                className={`${action.color} text-white p-6 rounded-lg shadow hover:shadow-md transition-all duration-200 text-left group disabled:opacity-50 disabled:cursor-not-allowed`}
              >
                <div className="flex items-center justify-between mb-4">
                  {uploading && action.title === 'Quick Upload' ? (
                    <div className="w-6 h-6 border-2 border-white border-t-transparent rounded-full animate-spin" />
                  ) : (
                    action.icon
                  )}
                  <ArrowRight className="w-5 h-5 group-hover:translate-x-1 transition-transform" />
                </div>
                <h3 className="text-lg font-semibold mb-2">
                  {uploading && action.title === 'Quick Upload' ? 'Processing...' : action.title}
                </h3>
                <p className="text-white/80 text-sm">
                  {uploading && action.title === 'Quick Upload' ? 'Creating consultation and analyzing X-ray...' : action.description}
                </p>
              </button>
            ))}
          </div>
        </div>

        {/* Recent Activity & Quick Upload Modal */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
          {/* Recent Activity */}
          <div className="bg-white rounded-lg shadow">
            <div className="p-6 border-b border-gray-200">
              <div className="flex items-center justify-between">
                <h2 className="text-lg font-semibold text-gray-900">Recent Activity</h2>
                <Link 
                  to="/history"
                  className="text-blue-600 hover:text-blue-700 text-sm font-medium"
                >
                  View All
                </Link>
              </div>
            </div>
            <div className="p-6">
              {stats.recentActivity.length === 0 ? (
                <div className="text-center py-8">
                  <FileText className="w-12 h-12 text-gray-300 mx-auto mb-4" />
                  <p className="text-gray-500">No consultations yet</p>
                  <p className="text-sm text-gray-400 mt-1">
                    Start your first consultation to see activity here
                  </p>
                </div>
              ) : (
                <div className="space-y-4">
                  {stats.recentActivity.map((activity, index) => (
                    <div 
                      key={activity.id || index}
                      className="flex items-center space-x-3 p-3 hover:bg-gray-50 rounded-lg cursor-pointer"
                      onClick={() => navigate(`/chat/${activity.id}`)}
                    >
                      <div className="p-2 bg-blue-100 rounded-lg">
                        <MessageSquare className="w-4 h-4 text-blue-600" />
                      </div>
                      <div className="flex-1 min-w-0">
                        <p className="text-sm font-medium text-gray-900 truncate">
                          {activity.title}
                        </p>
                        <div className="flex items-center space-x-2 text-xs text-gray-500">
                          <Clock className="w-3 h-3" />
                          <span>{formatDate(activity.updated_at)}</span>
                          <span>•</span>
                          <span>{activity.message_count} messages</span>
                        </div>
                      </div>
                      <ArrowRight className="w-4 h-4 text-gray-400" />
                    </div>
                  ))}
                </div>
              )}
            </div>
          </div>

          {/* Getting Started Guide */}
          <div className="bg-white rounded-lg shadow">
            <div className="p-6 border-b border-gray-200">
              <h2 className="text-lg font-semibold text-gray-900">Getting Started</h2>
            </div>
            <div className="p-6">
              <div className="space-y-4">
                <div className="flex items-start space-x-3">
                  <div className="flex-shrink-0 w-6 h-6 bg-blue-500 text-white rounded-full flex items-center justify-center text-xs font-bold">
                    1
                  </div>
                  <div>
                    <p className="text-sm font-medium text-gray-900">
                      Upload your X-ray image
                    </p>
                    <p className="text-xs text-gray-500 mt-1">
                      Support for JPEG, PNG, and medical imaging formats
                    </p>
                  </div>
                </div>
                
                <div className="flex items-start space-x-3">
                  <div className="flex-shrink-0 w-6 h-6 bg-blue-500 text-white rounded-full flex items-center justify-center text-xs font-bold">
                    2
                  </div>
                  <div>
                    <p className="text-sm font-medium text-gray-900">
                      Get AI analysis
                    </p>
                    <p className="text-xs text-gray-500 mt-1">
                      Our YOLOv11 model detects potential issues in your X-ray
                    </p>
                  </div>
                </div>
                
                <div className="flex items-start space-x-3">
                  <div className="flex-shrink-0 w-6 h-6 bg-blue-500 text-white rounded-full flex items-center justify-center text-xs font-bold">
                    3
                  </div>
                  <div>
                    <p className="text-sm font-medium text-gray-900">
                      Chat for clarification
                    </p>
                    <p className="text-xs text-gray-500 mt-1">
                      Ask follow-up questions to understand your results
                    </p>
                  </div>
                </div>
              </div>
              
              <button
                onClick={startNewConsultation}
                className="w-full mt-6 px-4 py-2 bg-blue-500 text-white rounded-lg hover:bg-blue-600 transition-colors"
              >
                Start Your First Consultation
              </button>
            </div>
          </div>
        </div>

        {/* Quick Upload Modal */}
        {quickUpload && (
          <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
            <div className="bg-white rounded-lg max-w-md w-full p-6">
              <div className="flex items-center justify-between mb-4">
                <h3 className="text-lg font-semibold">Quick X-ray Upload</h3>
                <button
                  onClick={() => setQuickUpload(false)}
                  className="p-2 hover:bg-gray-100 rounded-lg"
                >
                  <X className="w-5 h-5" />
                </button>
              </div>
              
              <div className="border-2 border-dashed border-gray-300 rounded-lg p-8 text-center hover:border-gray-400 transition-colors">
                <Upload className="w-12 h-12 text-gray-400 mx-auto mb-4" />
                <h4 className="text-lg font-medium text-gray-900 mb-2">Upload X-ray Image</h4>
                <p className="text-sm text-gray-600 mb-4">
                  Drag & drop an X-ray image here, or click to select
                </p>
                <input
                  type="file"
                  accept="image/*"
                  onChange={(e) => handleQuickUploadSelect(e.target.files[0])}
                  className="hidden"
                  id="quick-upload-input"
                />
                <label
                  htmlFor="quick-upload-input"
                  className="inline-flex items-center px-4 py-2 bg-blue-500 text-white rounded-lg hover:bg-blue-600 cursor-pointer transition-colors"
                >
                  <Upload className="w-4 h-4 mr-2" />
                  Select File
                </label>
                <p className="text-xs text-gray-500 mt-3">
                  Supported formats: JPEG, PNG, GIF, BMP, TIFF (Max 10MB)
                </p>
              </div>
              
              <p className="text-sm text-gray-600 mt-4">
                This will create a new consultation, upload your X-ray, analyze it, and redirect you to the chat interface with the results ready.
              </p>
            </div>
          </div>
        )}
      </div>
    </div>
  )
}

export default DashboardPage