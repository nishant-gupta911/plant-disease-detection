import { useState, useRef } from 'react'
import Hero from './components/Hero'
import ImageUploader from './components/ImageUploader'
import ResultCard from './components/ResultCard'
import ClassesGrid from './components/ClassesGrid'

function App() {
  const [result, setResult] = useState(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)
  const uploaderRef = useRef(null)
  const classesRef = useRef(null)

  const handlePrediction = async (file) => {
    setLoading(true)
    setError(null)
    setResult(null)

    const formData = new FormData()
    formData.append('file', file)

    try {
      const response = await fetch('http://localhost:8001/predict', {
        method: 'POST',
        body: formData
      })

      if (!response.ok) {
        throw new Error(`API error: ${response.statusText}`)
      }

      const data = await response.json()
      setResult(data)
    } catch (err) {
      setError(err.message || 'Failed to get prediction. Make sure the backend is running on http://localhost:8001')
    } finally {
      setLoading(false)
    }
  }

  const handleScroll = (ref) => {
    ref.current?.scrollIntoView({ behavior: 'smooth' })
  }

  return (
    <>
      <nav className="navbar">
        <div className="navbar-brand">
          <span></span>
          PhytoScan
        </div>
        <div style={{ display: 'flex', gap: '2rem' }}>
          <a href="#" onClick={() => handleScroll(uploaderRef)} style={{ color: 'var(--text-secondary)', textDecoration: 'none', fontSize: '14px' }}>
            How It Works
          </a>
          <a href="#" onClick={() => handleScroll(classesRef)} style={{ color: 'var(--text-secondary)', textDecoration: 'none', fontSize: '14px' }}>
            Classes
          </a>
        </div>
      </nav>

      <Hero onCTA={() => handleScroll(uploaderRef)} />

      <div className="container">
        <section className="uploader-section" ref={uploaderRef}>
          <h2>Analyze Your Plant</h2>
          <ImageUploader
            onPrediction={handlePrediction}
            loading={loading}
            error={error}
          />
        </section>

        {loading && (
          <div style={{ textAlign: 'center', margin: '4rem 0' }}>
            <div className="loading-text">
              <div className="spinner"></div>
              <span>Analyzing plant image...</span>
            </div>
          </div>
        )}

        {result && (
          <ResultCard result={result} />
        )}

        <div ref={classesRef}>
          <ClassesGrid />
        </div>
      </div>

      <footer>
        <p>
          Plant Disease Detection System · Powered by EfficientNetB0 + PyTorch · 
          <a href="https://plantvillage.psu.edu/" target="_blank" rel="noopener noreferrer">
            PlantSegV2 Dataset
          </a>
        </p>
      </footer>
    </>
  )
}

export default App
