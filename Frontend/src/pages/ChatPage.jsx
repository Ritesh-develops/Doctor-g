import React, { useState, useEffect } from 'react'
import { useParams, useNavigate } from 'react-router-dom'
import ChatHistory from '../components/ChatHistory'
import ChatInterface from '../components/ChatInterface'

const ChatPage = () => {
  const { conversationId } = useParams()
  const [selectedConversationId, setSelectedConversationId] = useState(conversationId || null)
  const navigate = useNavigate()

  useEffect(() => {
    if (conversationId && conversationId !== selectedConversationId) {
      setSelectedConversationId(conversationId)
    }
  }, [conversationId])

  const handleSelectConversation = (id) => {
    setSelectedConversationId(id)
    if (id) {
      navigate(`/chat/${id}`)
    } else {
      navigate('/chat')
    }
  }

  const handleConversationCreated = (id) => {
    navigate(`/chat/${id}`)
  }

  return (
    <div className="h-screen flex bg-gray-50">
      <ChatHistory 
        onSelectConversation={handleSelectConversation}
        selectedConversationId={selectedConversationId}
        onConversationCreated={handleConversationCreated}
      />
      <div className="flex-1">
        <ChatInterface conversationId={selectedConversationId} />
      </div>
    </div>
  )
}

export default ChatPage