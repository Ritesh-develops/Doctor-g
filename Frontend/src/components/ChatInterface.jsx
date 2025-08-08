import React, { useState, useEffect, useRef } from 'react'
import { Send, Loader2, Bot } from 'lucide-react' // Add Bot here
import ChatMessage from './ChatMessage'
import ImageUploader from './ImageUploader'
import { apiClient } from '../api/apiClient'
import toast from 'react-hot-toast'

const ChatInterface = ({ conversationId }) => {
  const [messages, setMessages] = useState([])
  const [newMessage, setNewMessage] = useState('')
  const [isLoading, setIsLoading] = useState(false)
  const [isLoadingMessages, setIsLoadingMessages] = useState(true)
  const messagesEndRef = useRef(null)
  const inputRef = useRef(null)

  useEffect(() => {
    if (conversationId) {
      loadMessages()
    }
  }, [conversationId])

  useEffect(() => {
    scrollToBottom()
  }, [messages])

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }

  const loadMessages = async () => {
    setIsLoadingMessages(true)
    try {
      const response = await apiClient.getConversationMessages(conversationId)
      setMessages(response)
    } catch (error) {
      console.error('Error loading messages:', error)
    } finally {
      setIsLoadingMessages(false)
    }
  }

  const sendMessage = async () => {
    if (!newMessage.trim() || isLoading) return

    const messageText = newMessage.trim()
    setNewMessage('')
    setIsLoading(true)

    try {
      // Add user message immediately for better UX
      const userMessage = {
        id: `temp-${Date.now()}`,
        role: 'user',
        content: messageText,
        message_type: 'text',
        timestamp: new Date().toISOString()
      }
      setMessages(prev => [...prev, userMessage])

      // Send to API
      await apiClient.sendMessage(conversationId, messageText)
      
      // Reload messages to get the AI response
      await loadMessages()
    } catch (error) {
      console.error('Error sending message:', error)
      // Remove the temporary message on error
      setMessages(prev => prev.filter(msg => msg.id !== `temp-${Date.now()}`))
    } finally {
      setIsLoading(false)
      inputRef.current?.focus()
    }
  }

  const handleImageUpload = async (file) => {
    setIsLoading(true)
    try {
      await apiClient.analyzeXray(conversationId, file)
      await loadMessages() // Reload to show analysis
    } catch (error) {
      console.error('Error analyzing image:', error)
    } finally {
      setIsLoading(false)
    }
  }

  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault()
      sendMessage()
    }
  }

  if (!conversationId) {
    return (
      <div className="flex items-center justify-center h-full text-gray-500">
        <div className="text-center">
          <Bot className="w-16 h-16 mx-auto mb-4 text-gray-300" />
          <p>Select a conversation to start chatting</p>
        </div>
      </div>
    )
  }

  return (
    <div className="flex flex-col h-full bg-gray-50">
      {/* Messages Area */}
      <div className="flex-1 overflow-y-auto p-4">
        {isLoadingMessages ? (
          <div className="flex justify-center items-center h-full">
            <Loader2 className="w-8 h-8 animate-spin text-blue-500" />
          </div>
        ) : (
          <>
            {messages.map((message, index) => (
              <ChatMessage key={message.id || index} message={message} />
            ))}
            <div ref={messagesEndRef} />
          </>
        )}
      </div>

      {/* Input Area */}
      <div className="bg-white border-t p-4">
        <div className="mb-4">
          <ImageUploader 
            onUpload={handleImageUpload} 
            disabled={isLoading}
            showPreview={false}
          />
        </div>
        
        <div className="flex space-x-3">
          <div className="flex-1 relative">
            <textarea
              ref={inputRef}
              value={newMessage}
              onChange={(e) => setNewMessage(e.target.value)}
              onKeyPress={handleKeyPress}
              placeholder="Ask me about your X-ray results or general medical questions..."
              className="w-full px-4 py-3 border border-gray-300 rounded-lg resize-none focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              rows={3}
              disabled={isLoading}
            />
          </div>
          
          <button
            onClick={sendMessage}
            disabled={isLoading || !newMessage.trim()}
            className="px-6 py-3 bg-blue-500 text-white rounded-lg hover:bg-blue-600 disabled:opacity-50 disabled:cursor-not-allowed flex items-center space-x-2 transition-colors"
          >
            {isLoading ? (
              <Loader2 className="w-5 h-5 animate-spin" />
            ) : (
              <Send className="w-5 h-5" />
            )}
            <span>Send</span>
          </button>
        </div>
      </div>
    </div>
  )
}

export default ChatInterface