import { useRef, useState } from 'react'

function ImageUploader({ onPrediction, loading, error }) {
  const [preview, setPreview] = useState(null)
  const [fileName, setFileName] = useState(null)
  const [fileSize, setFileSize] = useState(null)
  const [dragover, setDragover] = useState(false)
  const fileInputRef = useRef(null)

  const formatFileSize = (bytes) => {
    if (bytes === 0) return '0 Bytes'
    const k = 1024
    const sizes = ['Bytes', 'KB', 'MB']
    const i = Math.floor(Math.log(bytes) / Math.log(k))
    return Math.round((bytes / Math.pow(k, i)) * 100) / 100 + ' ' + sizes[i]
  }

  const handleFileSelect = (file) => {
    if (!file.type.startsWith('image/')) {
      alert('Please select a valid image file')
      return
    }

    setFileName(file.name)
    setFileSize(formatFileSize(file.size))
    const reader = new FileReader()
    reader.onload = (e) => {
      setPreview(e.target.result)
    }
    reader.readAsDataURL(file)
  }

  const handleInputChange = (e) => {
    const file = e.target.files[0]
    if (file) handleFileSelect(file)
  }

  const handleDragOver = (e) => {
    e.preventDefault()
    setDragover(true)
  }

  const handleDragLeave = () => {
    setDragover(false)
  }

  const handleDrop = (e) => {
    e.preventDefault()
    setDragover(false)
    const file = e.dataTransfer.files[0]
    if (file) handleFileSelect(file)
  }

  const handleAnalyze = () => {
    if (fileInputRef.current?.files[0]) {
      onPrediction(fileInputRef.current.files[0])
    }
  }

  const handleClick = () => {
    fileInputRef.current?.click()
  }

  return (
    <div className="card">
      <div
        className={`dropzone ${dragover ? 'dragover' : ''}`}
        onDragOver={handleDragOver}
        onDragLeave={handleDragLeave}
        onDrop={handleDrop}
        onClick={handleClick}
      >
        <div className="dropzone-content">
          <div className="dropzone-icon">🍃</div>
          <p>Drop your leaf image here</p>
          <p className="dropzone-hint">or click to browse</p>
          <div className="dropzone-hint" style={{ marginTop: '0.75rem', fontSize: '12px' }}>
            JPG, PNG, WEBP — up to 10MB
          </div>
        </div>
        <input
          ref={fileInputRef}
          type="file"
          accept="image/*"
          onChange={handleInputChange}
        />
      </div>

      {preview && (
        <div className="preview-container">
          <img src={preview} alt="Preview" className="preview-image" />
          <div className="preview-filename">
            📄 {fileName} · {fileSize}
          </div>
          <button
            className="btn-primary analyze-button"
            onClick={handleAnalyze}
            disabled={loading}
          >
            {loading ? '◌ Analyzing...' : '→ Analyze Plant'}
          </button>
        </div>
      )}

      {error && (
        <div style={{
          marginTop: '1.5rem',
          padding: '1rem',
          background: 'rgba(248, 113, 113, 0.1)',
          border: '1px solid rgba(248, 113, 113, 0.3)',
          borderRadius: '8px',
          color: '#fca5a5',
          fontSize: '13px'
        }}>
          <strong>⚠ Error:</strong> {error}
        </div>
      )}
    </div>
  )
}

export default ImageUploader
