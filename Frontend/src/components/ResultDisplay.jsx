import React from 'react'
import { AlertTriangle, CheckCircle, Info, AlertCircle } from 'lucide-react'

const ResultDisplay = ({ result, loading = false }) => {
  if (loading) {
    return (
      <div className="bg-white rounded-lg shadow p-6">
        <div className="animate-pulse">
          <div className="h-4 bg-gray-200 rounded w-1/4 mb-4"></div>
          <div className="space-y-3">
            <div className="h-3 bg-gray-200 rounded"></div>
            <div className="h-3 bg-gray-200 rounded w-5/6"></div>
            <div className="h-3 bg-gray-200 rounded w-4/6"></div>
          </div>
        </div>
      </div>
    )
  }

  if (!result) {
    return null
  }

  const { content, metadata } = result
  const { yolo_results, confidence } = metadata || {}
  
  const getSeverityIcon = (confidence) => {
    if (confidence >= 0.8) return <AlertTriangle className="h-5 w-5 text-red-500" />
    if (confidence >= 0.5) return <AlertCircle className="h-5 w-5 text-yellow-500" />
    if (confidence >= 0.2) return <Info className="h-5 w-5 text-blue-500" />
    return <CheckCircle className="h-5 w-5 text-green-500" />
  }

  const getSeverityColor = (confidence) => {
    if (confidence >= 0.8) return 'border-red-200 bg-red-50'
    if (confidence >= 0.5) return 'border-yellow-200 bg-yellow-50'
    if (confidence >= 0.2) return 'border-blue-200 bg-blue-50'
    return 'border-green-200 bg-green-50'
  }

  return (
    <div className={`rounded-lg border-2 p-6 ${getSeverityColor(confidence)}`}>
      <div className="flex items-start space-x-3">
        {getSeverityIcon(confidence)}
        <div className="flex-1">
          <h3 className="text-lg font-semibold text-gray-900 mb-3">
            Analysis Result
          </h3>
          
          <div className="prose prose-sm max-w-none">
            <p className="text-gray-700 whitespace-pre-line">{content}</p>
          </div>

          {yolo_results && (
            <div className="mt-4 p-4 bg-white/50 rounded-md">
              <h4 className="font-medium text-gray-900 mb-2">Technical Details</h4>
              <div className="grid grid-cols-2 gap-4 text-sm">
                <div>
                  <span className="font-medium">Confidence Score:</span>
                  <div className="mt-1">
                    <div className="bg-gray-200 rounded-full h-2">
                      <div 
                        className="bg-blue-500 h-2 rounded-full transition-all duration-300"
                        style={{ width: `${(confidence * 100)}%` }}
                      ></div>
                    </div>
                    <span className="text-xs text-gray-600 mt-1">
                      {(confidence * 100).toFixed(1)}%
                    </span>
                  </div>
                </div>
                <div>
                  <span className="font-medium">Detections:</span>
                  <span className="ml-2 text-gray-600">
                    {yolo_results.detected_objects?.length || 0} objects found
                  </span>
                </div>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  )
}

export default ResultDisplay