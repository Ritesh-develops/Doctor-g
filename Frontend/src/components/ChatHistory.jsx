import React, { useState, useEffect } from 'react'
import { Plus, MessageSquare, Trash2, MoreVertical } from 'lucide-react'
import ConversationItem from './ConversationItem'
import { apiClient } from '../api/apiClient'
import toast from 'react-hot-toast'

const ChatHistory = ({ onSelectConversation, selectedConversationId, onConversationCreated }) => {
  const [conversations, setConversations] = useState([])
  const [loading, setLoading] = useState(true)
  const [creatingConversation, setCreatingConversation] = useState(false)

  useEffect(() => {
    loadConversations()
  }, [])

  const loadConversations = async () => {
    try {
      const response = await apiClient.getConversations()
      setConversations(response)
    } catch (error) {
      console.error('Error loading conversations:', error)
    } finally {
      setLoading(false)
    }
  }

  const createNewConversation = async () => {
    if (creatingConversation) return

    setCreatingConversation(true)
    try {
      const response = await apiClient.createConversation()
      const newConversation = {
        id: response.conversation_id,
        title: response.title,
        created_at: response.created_at,
        updated_at: response.created_at,
        message_count: 1
      }
      
      setConversations([newConversation, ...conversations])
      onSelectConversation(newConversation.id)
      
      if (onConversationCreated) {
        onConversationCreated(newConversation.id)
      }
    } catch (error) {
      console.error('Error creating conversation:', error)
    } finally {
      setCreatingConversation(false)
    }
  }

  const deleteConversation = async (conversationId) => {
    if (window.confirm('Are you sure you want to delete this conversation?')) {
      try {
        await apiClient.deleteConversation(conversationId)
        setConversations(conversations.filter(conv => conv.id !== conversationId))
        
        if (selectedConversationId === conversationId) {
          onSelectConversation(null)
        }
      } catch (error) {
        console.error('Error deleting conversation:', error)
      }
    }
  }

  return (
    <div className="w-80 bg-white border-r h-full flex flex-col">
      {/* Header */}
      <div className="p-4 border-b bg-gray-50">
        <button
          onClick={createNewConversation}
          disabled={creatingConversation}
          className="w-full flex items-center justify-center space-x-2 px-4 py-3 bg-blue-500 text-white rounded-lg hover:bg-blue-600 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
        >
          {creatingConversation ? (
            <div className="w-5 h-5 border-2 border-white border-t-transparent rounded-full animate-spin"></div>
          ) : (
            <Plus className="w-5 h-5" />
          )}
          <span>{creatingConversation ? 'Creating...' : 'New Consultation'}</span>
        </button>
      </div>

      {/* Conversations List */}
      <div className="flex-1 overflow-y-auto">
        {loading ? (
          <div className="p-4">
            <div className="space-y-3">
              {[...Array(5)].map((_, i) => (
                <div key={i} className="animate-pulse">
                  <div className="h-4 bg-gray-200 rounded w-3/4 mb-2"></div>
                  <div className="h-3 bg-gray-200 rounded w-1/2"></div>
                </div>
              ))}
            </div>
          </div>
        ) : conversations.length === 0 ? (
          <div className="p-6 text-center text-gray-500">
            <MessageSquare className="w-12 h-12 mx-auto mb-3 text-gray-300" />
            <p className="text-sm">No conversations yet</p>
            <p className="text-xs mt-1">Start a new consultation to begin</p>
          </div>
        ) : (
          <div className="divide-y divide-gray-200">
            {conversations.map((conversation) => (
              <ConversationItem
                key={conversation.id}
                conversation={conversation}
                isSelected={selectedConversationId === conversation.id}
                onClick={() => onSelectConversation(conversation.id)}
                onDelete={() => deleteConversation(conversation.id)}
              />
            ))}
          </div>
        )}
      </div>
    </div>
  )
}

export default ChatHistory