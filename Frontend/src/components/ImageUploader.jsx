import React, { useCallback, useState } from 'react'
import { useDropzone } from 'react-dropzone'
import { Upload, Image, X } from 'lucide-react'

const ImageUploader = ({ onUpload, disabled = false, showPreview = true }) => {
  const [preview, setPreview] = useState(null)
  const [uploading, setUploading] = useState(false)

  const onDrop = useCallback(async (acceptedFiles) => {
    const file = acceptedFiles[0]
    if (!file) return

    // Create preview
    if (showPreview) {
      const reader = new FileReader()
      reader.onload = () => setPreview(reader.result)
      reader.readAsDataURL(file)
    }

    // Upload file
    if (onUpload) {
      setUploading(true)
      try {
        await onUpload(file)
      } catch (error) {
        console.error('Upload error:', error)
      } finally {
        setUploading(false)
      }
    }
  }, [onUpload, showPreview])

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: {
      'image/*': ['.jpeg', '.jpg', '.png', '.gif', '.bmp', '.tiff']
    },
    multiple: false,
    disabled: disabled || uploading
  })

  const clearPreview = () => {
    setPreview(null)
  }

  return (
    <div className="w-full">
      {preview && showPreview ? (
        <div className="relative mb-4">
          <img
            src={preview}
            alt="X-ray preview"
            className="w-full h-64 object-contain bg-gray-100 rounded-lg"
          />
          <button
            onClick={clearPreview}
            className="absolute top-2 right-2 p-1 bg-red-500 text-white rounded-full hover:bg-red-600"
          >
            <X className="h-4 w-4" />
          </button>
        </div>
      ) : (
        <div
          {...getRootProps()}
          className={`border-2 border-dashed rounded-lg p-8 text-center cursor-pointer transition-colors ${
            isDragActive
              ? 'border-blue-400 bg-blue-50'
              : 'border-gray-300 hover:border-gray-400'
          } ${
            disabled || uploading
              ? 'opacity-50 cursor-not-allowed'
              : ''
          }`}
        >
          <input {...getInputProps()} />
          
          <div className="flex flex-col items-center space-y-4">
            {uploading ? (
              <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-500"></div>
            ) : (
              <div className="p-3 bg-gray-100 rounded-full">
                {isDragActive ? (
                  <Upload className="h-8 w-8 text-blue-500" />
                ) : (
                  <Image className="h-8 w-8 text-gray-400" />
                )}
              </div>
            )}
            
            <div>
              <p className="text-lg font-medium text-gray-900">
                {uploading ? 'Analyzing X-ray...' : 'Upload X-ray Image'}
              </p>
              <p className="text-sm text-gray-500 mt-1">
                {uploading 
                  ? 'Please wait while we analyze your image'
                  : isDragActive
                  ? 'Drop the image here'
                  : 'Drag & drop an X-ray image here, or click to select'
                }
              </p>
            </div>
            
            <p className="text-xs text-gray-400">
              Supported formats: JPEG, PNG, GIF, BMP, TIFF
            </p>
          </div>
        </div>
      )}
    </div>
  )
}

export default ImageUploader