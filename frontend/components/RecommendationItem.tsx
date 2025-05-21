import { useState } from 'react'

interface Recommendation {
  title: string
  type: string
  genre?: string
  reason?: string
  metadata?: Record<string, any>
}

export default function RecommendationItem({ rec }: { rec: Recommendation }) {
  const [seen, setSeen] = useState(false)
  const [loved, setLoved] = useState(false)

  const image = rec.metadata?.poster_url || rec.metadata?.cover_image || null

  return (
    <div
      style={{
        border: '1px solid #ccc',
        padding: '0.5rem',
        marginBottom: '1rem',
        display: 'flex',
        gap: '1rem',
        alignItems: 'flex-start',
      }}
    >
      {image ? (
        <img
          src={image}
          alt={rec.title}
          style={{ width: '100px', height: '150px', objectFit: 'cover' }}
        />
      ) : (
        <div
          style={{
            width: '100px',
            height: '150px',
            background: '#eee',
            display: 'flex',
            justifyContent: 'center',
            alignItems: 'center',
            fontSize: '0.8rem',
          }}
        >
          No Image
        </div>
      )}
      <div style={{ flex: 1 }}>
        <h3 style={{ margin: '0 0 0.25rem 0' }}>
          {rec.title} ({rec.type})
        </h3>
        {rec.genre && (
          <p style={{ margin: '0 0 0.25rem 0', fontStyle: 'italic' }}>{rec.genre}</p>
        )}
        {rec.reason && <p style={{ margin: '0 0 0.5rem 0' }}>{rec.reason}</p>}
        <div>
          <button onClick={() => setSeen(!seen)} style={{ marginRight: '0.5rem' }}>
            {seen ? 'Seen ✔' : 'Seen'}
          </button>
          <button onClick={() => setLoved(!loved)}>
            {loved ? 'Loved ❤️' : 'Loved'}
          </button>
        </div>
      </div>
    </div>
  )
}
