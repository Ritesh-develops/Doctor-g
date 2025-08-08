import React from 'react'
import { User, Bot, Clock, Image as ImageIcon } from 'lucide-react'
import ResultDisplay from './ResultDisplay'

const ChatMessage = ({ message }) => {
  const { role, content, message_type, metadata, timestamp } = message
  const isUser = role === 'user'
  const isAnalysis = message_type === 'analysis'

  const formatTime = (timestamp) => {
    return new Date(timestamp).toLocaleTimeString([], { 
      hour: '2-digit', 
      minute: '2-digit' 
    })
  }

  return (
    <div className={`flex ${isUser ? 'justify-end' : 'justify-start'} mb-4`}>
      <div className={`flex max-w-[80%] ${isUser ? 'flex-row-reverse' : 'flex-row'}`}>
        {/* Avatar */}
        <div className={`flex-shrink-0 ${isUser ? 'ml-3' : 'mr-3'}`}>
          <div className={`w-8 h-8 rounded-full flex items-center justify-center ${
            isUser 
              ? 'bg-blue-500' 
              : 'bg-green-500'
          }`}>
            {isUser ? (
              <User className="w-5 h-5 text-white" />
            ) : (
              <Bot className="w-5 h-5 text-white" />
            )}
          </div>
        </div>

        {/* Message Content */}
        <div className={`flex-1 ${isUser ? 'text-right' : 'text-left'}`}>
          <div className={`inline-block p-3 rounded-lg ${
            isUser 
              ? 'bg-blue-500 text-white' 
              : 'bg-white border shadow-sm'
          }`}>
            {message_type === 'image' && (
              <div className="flex items-center space-x-2 mb-2">
                <ImageIcon className="w-4 h-4" />
                <span className="text-sm">X-ray image uploaded</span>
              </div>
            )}
            
            {isAnalysis ? (
              <div className="text-left">
                <div className="mb-3">
                  <div className="flex items-center space-x-2 mb-2">
                    <Bot className="w-4 h-4 text-green-600" />
                    <span className="font-medium text-green-600">AI Analysis Complete</span>
                  </div>
                  <p className="text-gray-800 whitespace-pre-line">{content}</p>
                </div>
                
                {metadata && (
                  <div className="mt-3 p-3 bg-gray-50 rounded border">
                    <h4 className="font-medium text-gray-800 mb-2">Detection Details</h4>
                    
                    {metadata.confidence && (
                      <div className="mb-2">
                        <div className="flex justify-between text-sm">
                          <span>Confidence Level:</span>
                          <span>{(metadata.confidence * 100).toFixed(1)}%</span>
                        </div>
                        <div className="w-full bg-gray-200 rounded-full h-2 mt-1">
                          <div 
                            className="bg-blue-500 h-2 rounded-full transition-all duration-300"
                            style={{ width: `${(metadata.confidence * 100)}%` }}
                          ></div>
                        </div>
                      </div>
                    )}
                    
                    {metadata.detected_objects && metadata.detected_objects.length > 0 && (
                      <div className="text-sm">
                        <span className="font-medium">Objects Detected: </span>
                        <span>{metadata.detected_objects.length}</span>
                      </div>
                    )}
                  </div>
                )}
              </div>
            ) : (
              <p className="whitespace-pre-line">{content}</p>
            )}
          </div>
          
          {/* Timestamp */}
          <div className={`flex items-center mt-1 text-xs text-gray-500 ${
            isUser ? 'justify-end' : 'justify-start'
          }`}>
            <Clock className="w-3 h-3 mr-1" />
            <span>{formatTime(timestamp)}</span>
          </div>
        </div>
      </div>
    </div>
  )
}

export default ChatMessage