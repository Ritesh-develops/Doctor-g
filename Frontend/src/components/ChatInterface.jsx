import React, { useState, useEffect, useRef } from 'react'
import { Send, Loader2, Bot, Paperclip, X, Upload } from 'lucide-react'
import ChatMessage from './ChatMessage'
import { apiClient } from '../api/apiClient'
import toast from 'react-hot-toast'

const ChatInterface = ({ conversationId }) => {
  const [messages, setMessages] = useState([])
  const [newMessage, setNewMessage] = useState('')
  const [isLoading, setIsLoading] = useState(false)
  const [isLoadingMessages, setIsLoadingMessages] = useState(true)
  const [uploadingFile, setUploadingFile] = useState(null)
  const [isDragging, setIsDragging] = useState(false)
  const messagesEndRef = useRef(null)
  const inputRef = useRef(null)
  const fileInputRef = useRef(null)

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
      setMessages(prev => prev.filter(msg => msg.id !== userMessage.id))
    } finally {
      setIsLoading(false)
      inputRef.current?.focus()
    }
  }

  const handleFileSelect = (file) => {
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

    setUploadingFile(file)
    handleImageUpload(file)
  }

  const handleImageUpload = async (file) => {
    setIsLoading(true)
    try {
      await apiClient.analyzeXray(conversationId, file)
      await loadMessages() // Reload to show analysis
      setUploadingFile(null)
      toast.success('X-ray analysis complete!')
    } catch (error) {
      console.error('Error analyzing image:', error)
      setUploadingFile(null)
      toast.error('Failed to analyze X-ray image')
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

  const handleDragOver = (e) => {
    e.preventDefault()
    setIsDragging(true)
  }

  const handleDragLeave = (e) => {
    e.preventDefault()
    setIsDragging(false)
  }

  const handleDrop = (e) => {
    e.preventDefault()
    setIsDragging(false)
    const files = e.dataTransfer.files
    if (files.length > 0) {
      handleFileSelect(files[0])
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
    <div 
      className={`flex flex-col h-full bg-gray-50 ${isDragging ? 'bg-blue-50' : ''}`}
      onDragOver={handleDragOver}
      onDragLeave={handleDragLeave}
      onDrop={handleDrop}
    >
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

      {/* Drag Overlay */}
      {isDragging && (
        <div className="absolute inset-0 bg-blue-100 bg-opacity-90 flex items-center justify-center z-10 border-2 border-dashed border-blue-400">
          <div className="text-center">
            <Upload className="w-16 h-16 text-blue-500 mx-auto mb-4" />
            <p className="text-xl font-semibold text-blue-700">Drop X-ray image here</p>
            <p className="text-blue-600">JPEG, PNG, GIF, BMP, TIFF formats supported</p>
          </div>
        </div>
      )}

      {/* Uploading File Preview */}
      {uploadingFile && (
        <div className="p-4 bg-blue-50 border-t">
          <div className="flex items-center space-x-3">
            <div className="animate-spin rounded-full h-6 w-6 border-b-2 border-blue-500"></div>
            <span className="text-sm text-blue-700">
              Analyzing {uploadingFile.name}...
            </span>
            <button
              onClick={() => setUploadingFile(null)}
              className="p-1 hover:bg-blue-200 rounded"
            >
              <X className="w-4 h-4 text-blue-600" />
            </button>
          </div>
        </div>
      )}

      {/* Input Area */}
      <div className="bg-white border-t p-4">
        <div className="flex space-x-3">
          {/* File Upload Button */}
          <button
            onClick={() => fileInputRef.current?.click()}
            disabled={isLoading}
            className="p-3 text-gray-500 hover:text-blue-600 hover:bg-blue-50 rounded-lg transition-colors disabled:opacity-50"
            title="Upload X-ray image"
          >
            <Paperclip className="w-5 h-5" />
          </button>

          <input
            ref={fileInputRef}
            type="file"
            accept="image/*"
            onChange={(e) => handleFileSelect(e.target.files[0])}
            className="hidden"
          />
          
          <div className="flex-1 relative">
            <textarea
              ref={inputRef}
              value={newMessage}
              onChange={(e) => setNewMessage(e.target.value)}
              onKeyPress={handleKeyPress}
              placeholder="Ask me about your X-ray results or general medical questions..."
              className="w-full px-4 py-3 border border-gray-300 rounded-lg resize-none focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              rows={1}
              disabled={isLoading}
              style={{ minHeight: '50px', maxHeight: '120px' }}
              onInput={(e) => {
                e.target.style.height = 'auto'
                e.target.style.height = Math.min(e.target.scrollHeight, 120) + 'px'
              }}
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

        <div className="mt-2 text-xs text-gray-500 text-center">
          You can drag & drop X-ray images anywhere or use the paperclip button to upload
        </div>
      </div>
    </div>
  )
}

export default ChatInterface