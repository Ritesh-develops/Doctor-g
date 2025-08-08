import React, { useState } from 'react'
import { MessageSquare, Calendar, Trash2, MoreVertical } from 'lucide-react'

const ConversationItem = ({ conversation, isSelected, onClick, onDelete }) => {
  const [showMenu, setShowMenu] = useState(false)

  const formatDate = (dateString) => {
    const date = new Date(dateString)
    const now = new Date()
    const diffTime = Math.abs(now - date)
    const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24))

    if (diffDays === 1) return 'Today'
    if (diffDays === 2) return 'Yesterday'
    if (diffDays <= 7) return `${diffDays - 1} days ago`
    
    return date.toLocaleDateString()
  }

  const handleMenuClick = (e) => {
    e.stopPropagation()
    setShowMenu(!showMenu)
  }

  const handleDeleteClick = (e) => {
    e.stopPropagation()
    setShowMenu(false)
    onDelete()
  }

  return (
    <div
      onClick={onClick}
      className={`relative p-4 cursor-pointer hover:bg-gray-50 transition-colors ${
        isSelected ? 'bg-blue-50 border-r-2 border-blue-500' : ''
      }`}
    >
      <div className="flex items-start justify-between">
        <div className="flex-1 min-w-0">
          <div className="flex items-center space-x-2 mb-2">
            <MessageSquare className="w-4 h-4 text-gray-400 flex-shrink-0" />
            <h3 className="text-sm font-medium text-gray-900 truncate">
              {conversation.title}
            </h3>
          </div>
          
          <div className="flex items-center space-x-4 text-xs text-gray-500">
            <div className="flex items-center space-x-1">
              <Calendar className="w-3 h-3" />
              <span>{formatDate(conversation.updated_at)}</span>
            </div>
            
            <span>{conversation.message_count} messages</span>
          </div>
        </div>

        <div className="relative">
          <button
            onClick={handleMenuClick}
            className="p-1 rounded hover:bg-gray-200 transition-colors"
          >
            <MoreVertical className="w-4 h-4 text-gray-400" />
          </button>

          {showMenu && (
            <>
              <div 
                className="fixed inset-0 z-10" 
                onClick={() => setShowMenu(false)}
              ></div>
              <div className="absolute right-0 mt-1 w-32 bg-white rounded-md shadow-lg border z-20">
                <button
                  onClick={handleDeleteClick}
                  className="flex items-center space-x-2 w-full px-3 py-2 text-sm text-red-600 hover:bg-red-50 transition-colors"
                >
                  <Trash2 className="w-4 h-4" />
                  <span>Delete</span>
                </button>
              </div>
            </>
          )}
        </div>
      </div>
    </div>
  )
}

export default ConversationItem