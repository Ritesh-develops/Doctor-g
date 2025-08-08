import React, { useState, useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import { 
  Search, 
  Filter, 
  Calendar, 
  MessageSquare, 
  Activity, 
  ChevronDown,
  Eye,
  Trash2,
  Download,
  Clock,
  FileText
} from 'lucide-react'
import { apiClient } from '../api/apiClient'
import toast from 'react-hot-toast'

const HistoryPage = () => {
  const [conversations, setConversations] = useState([])
  const [filteredConversations, setFilteredConversations] = useState([])
  const [loading, setLoading] = useState(true)
  const [searchTerm, setSearchTerm] = useState('')
  const [filterDate, setFilterDate] = useState('')
  const [sortBy, setSortBy] = useState('newest')
  const [showFilters, setShowFilters] = useState(false)
  const navigate = useNavigate()

  useEffect(() => {
    loadConversations()
  }, [])

  useEffect(() => {
    filterAndSortConversations()
  }, [conversations, searchTerm, filterDate, sortBy])

  const loadConversations = async () => {
    try {
      const response = await apiClient.getConversations()
      setConversations(response)
    } catch (error) {
      console.error('Error loading conversations:', error)
      toast.error('Failed to load conversation history')
    } finally {
      setLoading(false)
    }
  }

  const filterAndSortConversations = () => {
    let filtered = [...conversations]

    // Search filter
    if (searchTerm) {
      filtered = filtered.filter(conv =>
        conv.title.toLowerCase().includes(searchTerm.toLowerCase())
      )
    }

    // Date filter
    if (filterDate) {
      const filterDateTime = new Date(filterDate)
      filtered = filtered.filter(conv => {
        const convDate = new Date(conv.created_at)
        return convDate.toDateString() === filterDateTime.toDateString()
      })
    }

    // Sort
    filtered.sort((a, b) => {
      switch (sortBy) {
        case 'newest':
          return new Date(b.updated_at) - new Date(a.updated_at)
        case 'oldest':
          return new Date(a.updated_at) - new Date(b.updated_at)
        case 'most_messages':
          return b.message_count - a.message_count
        case 'alphabetical':
          return a.title.localeCompare(b.title)
        default:
          return 0
      }
    })

    setFilteredConversations(filtered)
  }

  const handleDeleteConversation = async (conversationId, e) => {
    e.stopPropagation()
    
    if (window.confirm('Are you sure you want to delete this conversation? This action cannot be undone.')) {
      try {
        await apiClient.deleteConversation(conversationId)
        setConversations(conversations.filter(conv => conv.id !== conversationId))
        toast.success('Conversation deleted successfully')
      } catch (error) {
        console.error('Error deleting conversation:', error)
        toast.error('Failed to delete conversation')
      }
    }
  }

  const handleViewConversation = (conversationId) => {
    navigate(`/chat/${conversationId}`)
  }

  const formatDate = (dateString) => {
    const date = new Date(dateString)
    return {
      date: date.toLocaleDateString('en-US', {
        month: 'short',
        day: 'numeric',
        year: 'numeric'
      }),
      time: date.toLocaleTimeString('en-US', {
        hour: '2-digit',
        minute: '2-digit'
      })
    }
  }

  const getRelativeTime = (dateString) => {
    const date = new Date(dateString)
    const now = new Date()
    const diffTime = Math.abs(now - date)
    const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24))

    if (diffDays === 1) return 'Today'
    if (diffDays === 2) return 'Yesterday'
    if (diffDays <= 7) return `${diffDays - 1} days ago`
    if (diffDays <= 30) return `${Math.ceil(diffDays / 7)} weeks ago`
    return `${Math.ceil(diffDays / 30)} months ago`
  }

  const getConversationStats = () => {
    const total = conversations.length
    const thisMonth = conversations.filter(conv => {
      const convDate = new Date(conv.created_at)
      const currentDate = new Date()
      return convDate.getMonth() === currentDate.getMonth() &&
             convDate.getFullYear() === currentDate.getFullYear()
    }).length

    const totalMessages = conversations.reduce((sum, conv) => sum + conv.message_count, 0)

    return { total, thisMonth, totalMessages }
  }

  const clearFilters = () => {
    setSearchTerm('')
    setFilterDate('')
    setSortBy('newest')
  }

  const stats = getConversationStats()

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
          <h1 className="text-3xl font-bold text-gray-900">Consultation History</h1>
          <p className="text-gray-600 mt-2">
            View and manage your medical consultation history
          </p>
        </div>

        {/* Stats */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
          <div className="bg-white rounded-lg shadow p-6">
            <div className="flex items-center">
              <div className="p-2 bg-blue-100 rounded-lg">
                <MessageSquare className="w-6 h-6 text-blue-600" />
              </div>
              <div className="ml-4">
                <p className="text-sm font-medium text-gray-600">Total Consultations</p>
                <p className="text-2xl font-bold text-gray-900">{stats.total}</p>
              </div>
            </div>
          </div>

          <div className="bg-white rounded-lg shadow p-6">
            <div className="flex items-center">
              <div className="p-2 bg-green-100 rounded-lg">
                <Calendar className="w-6 h-6 text-green-600" />
              </div>
              <div className="ml-4">
                <p className="text-sm font-medium text-gray-600">This Month</p>
                <p className="text-2xl font-bold text-gray-900">{stats.thisMonth}</p>
              </div>
            </div>
          </div>

          <div className="bg-white rounded-lg shadow p-6">
            <div className="flex items-center">
              <div className="p-2 bg-purple-100 rounded-lg">
                <Activity className="w-6 h-6 text-purple-600" />
              </div>
              <div className="ml-4">
                <p className="text-sm font-medium text-gray-600">Total Messages</p>
                <p className="text-2xl font-bold text-gray-900">{stats.totalMessages}</p>
              </div>
            </div>
          </div>
        </div>

        {/* Search and Filters */}
        <div className="bg-white rounded-lg shadow p-6 mb-6">
          <div className="flex flex-col lg:flex-row lg:items-center lg:justify-between gap-4">
            <div className="flex flex-col sm:flex-row gap-4 flex-1">
              <div className="relative flex-1 max-w-md">
                <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 w-5 h-5" />
                <input
                  type="text"
                  placeholder="Search conversations..."
                  value={searchTerm}
                  onChange={(e) => setSearchTerm(e.target.value)}
                  className="pl-10 pr-4 py-2 w-full border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                />
              </div>

              <button
                onClick={() => setShowFilters(!showFilters)}
                className="flex items-center space-x-2 px-4 py-2 border border-gray-300 rounded-lg hover:bg-gray-50"
              >
                <Filter className="w-4 h-4" />
                <span>Filters</span>
                <ChevronDown className={`w-4 h-4 transition-transform ${showFilters ? 'rotate-180' : ''}`} />
              </button>
            </div>

            <div className="flex items-center space-x-2">
              <label className="text-sm text-gray-600">Sort by:</label>
              <select
                value={sortBy}
                onChange={(e) => setSortBy(e.target.value)}
                className="border border-gray-300 rounded-lg px-3 py-2 focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              >
                <option value="newest">Newest first</option>
                <option value="oldest">Oldest first</option>
                <option value="most_messages">Most messages</option>
                <option value="alphabetical">A-Z</option>
              </select>
            </div>
          </div>

          {showFilters && (
            <div className="mt-4 pt-4 border-t border-gray-200">
              <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Filter by Date
                  </label>
                  <input
                    type="date"
                    value={filterDate}
                    onChange={(e) => setFilterDate(e.target.value)}
                    className="w-full border border-gray-300 rounded-lg px-3 py-2 focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                  />
                </div>
                
                <div className="flex items-end">
                  <button
                    onClick={clearFilters}
                    className="px-4 py-2 text-gray-600 hover:text-gray-800 hover:bg-gray-100 rounded-lg transition-colors"
                  >
                    Clear Filters
                  </button>
                </div>
              </div>
            </div>
          )}
        </div>

        {/* Conversations List */}
        <div className="bg-white rounded-lg shadow">
          <div className="p-6 border-b border-gray-200">
            <h2 className="text-lg font-semibold text-gray-900">
              Your Consultations ({filteredConversations.length})
            </h2>
          </div>

          {filteredConversations.length === 0 ? (
            <div className="p-12 text-center">
              {searchTerm || filterDate ? (
                <>
                  <Search className="w-12 h-12 text-gray-300 mx-auto mb-4" />
                  <h3 className="text-lg font-medium text-gray-900 mb-2">No results found</h3>
                  <p className="text-gray-500 mb-4">
                    Try adjusting your search terms or filters
                  </p>
                  <button
                    onClick={clearFilters}
                    className="text-blue-600 hover:text-blue-700 font-medium"
                  >
                    Clear all filters
                  </button>
                </>
              ) : (
                <>
                  <FileText className="w-12 h-12 text-gray-300 mx-auto mb-4" />
                  <h3 className="text-lg font-medium text-gray-900 mb-2">No consultations yet</h3>
                  <p className="text-gray-500 mb-4">
                    Start your first medical consultation to see history here
                  </p>
                  <button
                    onClick={() => navigate('/dashboard')}
                    className="px-4 py-2 bg-blue-500 text-white rounded-lg hover:bg-blue-600 transition-colors"
                  >
                    Start New Consultation
                  </button>
                </>
              )}
            </div>
          ) : (
            <div className="divide-y divide-gray-200">
              {filteredConversations.map((conversation) => {
                const dateInfo = formatDate(conversation.updated_at)
                return (
                  <div
                    key={conversation.id}
                    className="p-6 hover:bg-gray-50 cursor-pointer transition-colors"
                    onClick={() => handleViewConversation(conversation.id)}
                  >
                    <div className="flex items-center justify-between">
                      <div className="flex-1 min-w-0">
                        <div className="flex items-center space-x-3 mb-2">
                          <div className="p-2 bg-blue-100 rounded-lg">
                            <MessageSquare className="w-4 h-4 text-blue-600" />
                          </div>
                          <h3 className="text-lg font-medium text-gray-900 truncate">
                            {conversation.title}
                          </h3>
                        </div>

                        <div className="flex items-center space-x-4 text-sm text-gray-500">
                          <div className="flex items-center space-x-1">
                            <Calendar className="w-4 h-4" />
                            <span>{dateInfo.date}</span>
                          </div>
                          
                          <div className="flex items-center space-x-1">
                            <Clock className="w-4 h-4" />
                            <span>{dateInfo.time}</span>
                          </div>

                          <div className="flex items-center space-x-1">
                            <MessageSquare className="w-4 h-4" />
                            <span>{conversation.message_count} messages</span>
                          </div>

                          <span className="px-2 py-1 bg-gray-100 rounded-full text-xs">
                            {getRelativeTime(conversation.updated_at)}
                          </span>
                        </div>
                      </div>

                      <div className="flex items-center space-x-2 ml-4">
                        <button
                          onClick={(e) => {
                            e.stopPropagation()
                            handleViewConversation(conversation.id)
                          }}
                          className="p-2 text-gray-400 hover:text-blue-600 hover:bg-blue-50 rounded-lg transition-colors"
                          title="View conversation"
                        >
                          <Eye className="w-5 h-5" />
                        </button>

                        <button
                          onClick={(e) => handleDeleteConversation(conversation.id, e)}
                          className="p-2 text-gray-400 hover:text-red-600 hover:bg-red-50 rounded-lg transition-colors"
                          title="Delete conversation"
                        >
                          <Trash2 className="w-5 h-5" />
                        </button>
                      </div>
                    </div>
                  </div>
                )
              })}
            </div>
          )}
        </div>

        {/* Pagination would go here if needed */}
        {filteredConversations.length > 0 && (
          <div className="mt-6 flex justify-center">
            <p className="text-sm text-gray-500">
              Showing {filteredConversations.length} of {conversations.length} consultations
            </p>
          </div>
        )}
      </div>
    </div>
  )
}

export default HistoryPage