function ResultCard({ result }) {
  // Handle error responses
  if (result.error) {
    return (
      <section className="result-section">
        <div className="card" style={{ borderColor: '#f87171', borderTop: '3px solid #f87171' }}>
          <div className="result-header">
            <div className="result-icon" style={{ fontSize: '40px' }}>❌</div>
            <div className="result-info">
              <h3 style={{ color: '#f87171' }}>{result.error}</h3>
              <div className="status-badge" style={{ background: 'rgba(248, 113, 113, 0.1)', color: '#f87171', borderColor: '#f87171' }}>
                ⚠ Validation Failed
              </div>
            </div>
          </div>
          <div style={{ padding: '1.5rem', backgroundColor: 'rgba(248, 113, 113, 0.05)', borderRadius: '8px', marginTop: '1rem' }}>
            <p style={{ color: 'var(--text-primary)', lineHeight: '1.6' }}>
              {result.message}
            </p>
            {result.top_5 && result.top_5.length > 0 && (
              <div style={{ marginTop: '1rem' }}>
                <p style={{ fontSize: '12px', color: 'var(--text-muted)', marginBottom: '0.5rem' }}>
                  Model predictions (for reference):
                </p>
                <div className="top3-predictions">
                  {result.top_5.map((pred, idx) => (
                    <div key={idx} className="prediction-bar">
                      <div className="prediction-class">
                        {pred[0].replace(/_/g, ' ')}
                      </div>
                      <div className="prediction-bar-bg">
                        <div
                          className="prediction-bar-fill"
                          style={{ width: `${pred[1] * 100}%` }}
                        >
                          {pred[1] > 0.1 && `${(pred[1] * 100).toFixed(1)}%`}
                        </div>
                      </div>
                      <div className="prediction-confidence">
                        {(pred[1] * 100).toFixed(1)}%
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            )}
          </div>
        </div>
      </section>
    )
  }

  // Disease descriptions
  const diseaseDescriptions = {
    'Tomato_Late_blight': 'Late blight caused by *Phytophthora infestans*. Water-soaked spots on leaves and stems. Control with fungicides and improve air circulation.',
    'Tomato_Early_blight': 'Early blight caused by *Alternaria solani*. Circular brown spots with concentric rings. Remove affected leaves and apply copper fungicide.',
    'Tomato_Septoria_leaf_spot': 'Fungal disease with small circular lesions. Caused by *Septoria lycopersici*. Practice crop rotation and improve ventilation.',
    'Tomato_Spider_mites_Two-spotted_spider_mite': 'Arachnid pest causing stippling and webbing. Manage with insecticidal soap or neem oil.',
    'Tomato_Bacterial_spot': 'Bacterial disease with dark, greasy-looking lesions. Caused by *Xanthomonas*. Use bacterial copper fungicide.',
    'Tomato_Target_Spot': 'Fungal disease with target-shaped lesions. Use fungicides and remove infected leaves regularly.',
    'Tomato_Yellow_Leaf_Curl_Virus': 'Viral disease spread by whiteflies. Plants show yellowing and curling. Control whiteflies to prevent spread.',
    'Tomato_Mosaic_virus': 'Virus causing mottled, mosaic-like leaf patterns. Remove infected plants and control aphids.',
    'Pepper_Bell_healthy': 'Your plant is healthy! Continue regular watering, fertilizing, and monitor for pests.',
    'Potato_Early_blight': 'Early blight on potato. Brown lesions with concentric rings. Use resistant varieties and fungicides.',
    'Potato_Late_blight': 'Late blight causing water-soaked areas. Critical disease - act immediately with fungicides.',
    'Potato_Healthy': 'Your potato plant is in excellent condition!',
    'Apple_Cedar_apple_rust': 'Fungal disease requiring alternate host control. Yellow-orange lesions on leaves. Prune infected branches.',
    'Apple_Black_rot': 'Fungal rot disease with black decay. Use fungicides in spring. Remove infected fruit and branches.',
    'Grape_Esca_(Black_Measles)': 'Fungal disease affecting grape vines. Prune infected wood and dispose properly.',
    'Corn_(maize)_Cercospora_leaf_spot_Gray_leaf_spot': 'Fungal disease with rectangular gray lesions. Use resistant varieties and fungicides.',
    'Rice_Hispa': 'Pest causing skeletonized leaves. Control with insecticides and manage field conditions.',
    'Rice_Leaf_scald': 'Fungal disease affecting rice paddy. Manage with fungicides and improve water management.',
    'Wheat_Septoria': 'Fungal disease affecting wheat. Brown lesions on leaves. Use resistant varieties and fungicides.'
  }

  const isHealthy = result.predicted_class.toLowerCase().includes('healthy')
  const displayClass = result.predicted_class.replace(/_/g, ' ')
  const description = diseaseDescriptions[result.predicted_class] || 'Monitor your plant regularly and maintain good growing conditions.'

  // Calculate circumference for SVG progress ring
  const radius = 45
  const circumference = 2 * Math.PI * radius
  const strokeDashoffset = circumference - (result.confidence) * circumference

  return (
    <section className="result-section">
      <div className="card">
        <div className="result-header">
          <div className="result-icon">
            {isHealthy ? '✅' : '🦠'}
          </div>
          <div className="result-info">
            <h3>{displayClass}</h3>
            <div className={`status-badge ${isHealthy ? 'healthy' : 'diseased'}`}>
              {isHealthy ? '✓ Healthy' : '⚠ Disease Detected'}
            </div>
          </div>
        </div>

        <div className="progress-ring-container">
          <svg width="120" height="120" className="progress-ring">
            <circle
              cx="60"
              cy="60"
              r={radius}
              fill="none"
              stroke="rgba(74, 222, 128, 0.1)"
              strokeWidth="8"
            />
            <circle
              cx="60"
              cy="60"
              r={radius}
              fill="none"
              stroke={isHealthy ? 'var(--accent-primary)' : 'var(--warning)'}
              strokeWidth="8"
              className="progress-ring-circle"
              strokeDasharray={circumference}
              strokeDashoffset={strokeDashoffset}
              strokeLinecap="round"
            />
            <text
              x="60"
              y="70"
              textAnchor="middle"
              fill="var(--text-primary)"
              fontSize="24"
              fontWeight="700"
              fontFamily="JetBrains Mono, monospace"
            >
              {Math.round(result.confidence * 100)}%
            </text>
          </svg>
          <div style={{ textAlign: 'center' }}>
            <p style={{ color: 'var(--text-muted)', fontSize: '13px', marginBottom: '0.5rem' }}>
              Confidence Score
            </p>
            <p className="confidence-value">
              {(result.confidence * 100).toFixed(2)}%
            </p>
          </div>
        </div>

        <div className="top3-predictions">
          <h4>Top 5 Predictions</h4>
          {result.top_5.map((pred, idx) => (
            <div key={idx} className="prediction-bar">
              <div className="prediction-class">
                {pred[0].replace(/_/g, ' ')}
              </div>
              <div className="prediction-bar-bg">
                <div
                  className="prediction-bar-fill"
                  style={{ width: `${pred[1] * 100}%` }}
                >
                  {pred[1] > 0.1 && `${(pred[1] * 100).toFixed(1)}%`}
                </div>
              </div>
              <div className="prediction-confidence">
                {(pred[1] * 100).toFixed(1)}%
              </div>
            </div>
          ))}
        </div>

        <div className="disease-info">
          <h5>ℹ Information</h5>
          <p>{description}</p>
        </div>
      </div>
    </section>
  )
}

export default ResultCard
