import { useEffect, useState } from 'react'
import { useRouter } from 'next/router'
import Nav from '../components/Nav'
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
