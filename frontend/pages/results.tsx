import { useEffect, useState } from 'react'
import { useRouter } from 'next/router'
import Nav from '../components/Nav'

import { useUserContent } from '../context/UserContentContext'
import { useAuth } from '../context/AuthContext'
import RecommendationItem from '../components/RecommendationItem'

interface Recommendation {
  title: string
  type: string
  genre?: string
  reason?: string
  metadata?: Record<string, any>
}

export default function Results() {
  const router = useRouter()
  const { mood } = router.query
  const { user } = useAuth()
  const { statuses, markContent } = useUserContent()

  const content = [
    { id: 'movie1', title: 'Back to the Future', type: 'movie' },
    { id: 'game1', title: 'Stardew Valley', type: 'game' },
    { id: 'movie2', title: 'The Breakfast Club', type: 'movie' }
  ]
  const [loading, setLoading] = useState(false)
  const [recs, setRecs] = useState<Recommendation[]>([])

  async function fetchRecs(moodStr: string) {
    setLoading(true)
    try {
      const res = await fetch('/api/recommendations', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ mood: moodStr }),
      })
      const data = await res.json()
      setRecs(data.recommendations || [])
    } catch (err) {
      console.error(err)
    }
    setLoading(false)
  }

  useEffect(() => {
    if (typeof mood === 'string') {
      fetchRecs(mood)
    }
  }, [mood])

  return (
    <div>
      <Nav />
      <h1>Recommendations</h1>
      {mood && <p>Mood: {mood}</p>}
      <ul>
        {content.map((item) => (
          <li key={item.id} style={{ marginBottom: '0.5rem' }}>
            <strong>{item.title}</strong> ({item.type})
            <div>
              <button
                onClick={() => markContent(item.id, item.type, 'seen')}
                style={{
                  fontWeight: statuses[item.id] === 'seen' ? 'bold' : 'normal'
                }}
              >
                Seen
              </button>
              <button
                onClick={() => markContent(item.id, item.type, 'loved')}
                style={{
                  marginLeft: '0.5rem',
                  fontWeight: statuses[item.id] === 'loved' ? 'bold' : 'normal'
                }}
              >
                Loved
              </button>
              {statuses[item.id] && (
                <span style={{ marginLeft: '0.5rem' }}>
                  Current: {statuses[item.id]}
                </span>
              )}
            </div>
          </li>
        ))}
      </ul>
      {!user && <p>Login to save your interactions.</p>}
      {loading && <p>Loading...</p>}
      {recs.map((r, idx) => (
        <RecommendationItem key={idx} rec={r} />
      ))}
      {mood && (
        <button onClick={() => fetchRecs(mood as string)}>Give me another</button>
      )}
    </div>
  )
}
