import { useEffect, useState } from 'react'

function ClassesGrid() {
  const [classes, setClasses] = useState([])
  const [searchTerm, setSearchTerm] = useState('')
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)
  const [selectedFilter, setSelectedFilter] = useState('All')

  const plantFilters = ['All', 'Tomato', 'Potato', 'Corn', 'Apple', 'Other']

  useEffect(() => {
    const fetchClasses = async () => {
      try {
        const response = await fetch('http://localhost:8001/classes')
        if (!response.ok) {
          throw new Error('Failed to fetch classes')
        }
        const data = await response.json()
        setClasses(data.classes || [])
      } catch (err) {
        setError(err.message)
      } finally {
        setLoading(false)
      }
    }

    fetchClasses()
  }, [])

  const filteredClasses = classes.filter(className => {
    const matchesSearch = className.toLowerCase().includes(searchTerm.toLowerCase())
    if (selectedFilter === 'All') return matchesSearch
    if (selectedFilter === 'Other') {
      const plantName = className.split('_')[0]
      return !['Tomato', 'Potato', 'Corn', 'Apple', 'Grape', 'Rice', 'Wheat'].includes(plantName) && matchesSearch
    }
    return className.startsWith(selectedFilter) && matchesSearch
  })

  return (
    <section className="classes-section">
      <div className="classes-header">
        <h2>Supported Diseases</h2>
        <p>38 plant-disease combinations from the PlantVillage dataset</p>
      </div>

      <div style={{ display: 'flex', gap: '0.75rem', justifyContent: 'center', marginBottom: '2rem', flexWrap: 'wrap' }}>
        {plantFilters.map((filter) => (
          <button
            key={filter}
            onClick={() => setSelectedFilter(filter)}
            style={{
              padding: '8px 16px',
              borderRadius: '20px',
              border: selectedFilter === filter ? '1px solid var(--accent-glow)' : '1px solid var(--border)',
              background: selectedFilter === filter ? 'rgba(74, 222, 128, 0.15)' : 'transparent',
              color: selectedFilter === filter ? 'var(--accent-glow)' : 'var(--text-secondary)',
              cursor: 'pointer',
              fontSize: '13px',
              fontWeight: 600,
              fontFamily: 'Plus Jakarta Sans, sans-serif',
              transition: 'all 0.2s ease'
            }}
          >
            {filter}
          </button>
        ))}
      </div>

      <div className="search-box">
        <input
          type="text"
          placeholder="Search diseases..."
          value={searchTerm}
          onChange={(e) => setSearchTerm(e.target.value)}
        />
      </div>

      {loading ? (
        <div style={{ textAlign: 'center', padding: '3rem' }}>
          <div className="spinner" style={{ margin: '0 auto 1rem' }}></div>
          <p>Loading supported classes...</p>
        </div>
      ) : error ? (
        <div className="empty-state">
          <p>Could not load classes. Make sure the backend is running.</p>
        </div>
      ) : filteredClasses.length > 0 ? (
        <div className="classes-grid">
          {filteredClasses.map((className, idx) => (
            <div key={idx} className="class-item">
              <p>{className.replace(/_/g, ' ')}</p>
            </div>
          ))}
        </div>
      ) : (
        <div className="empty-state">
          <p>No results found for "{searchTerm}"</p>
        </div>
      )}
    </section>
  )
}

export default ClassesGrid
