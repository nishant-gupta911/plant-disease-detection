function Hero({ onCTA }) {
  return (
    <section className="hero">
      <div className="hero-content">
        <h1>
          Detect Plant Disease<br />
          <span className="headline-accent">With AI Precision</span>
        </h1>
        <p>
          Upload a leaf photo. Get instant diagnosis powered by EfficientNetB3 trained on 54,000+ images.
        </p>
        <div className="stat-pills">
          <div className="stat-pill">38 Disease Classes</div>
          <div className="stat-pill">97% Accuracy</div>
        </div>
        <button className="btn-primary cta-button" onClick={onCTA}>
          Start Analysis
        </button>
        <div style={{ marginTop: '3rem', fontSize: '24px', animation: 'float-leaf 3s ease-in-out infinite' }}>
          ↓
        </div>
      </div>
    </section>
  )
}

export default Hero
