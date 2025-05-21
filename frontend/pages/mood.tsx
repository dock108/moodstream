import { useState } from 'react'
import { useRouter } from 'next/router'
import Nav from '../components/Nav'

const PRESET_MOODS = [
  { label: 'Happy', emoji: '😄' },
  { label: 'Stressed', emoji: '😫' },
  { label: 'Nostalgic', emoji: '📻' },
  { label: 'Adventurous', emoji: '🧗' },
  { label: 'Romantic', emoji: '💕' },
  { label: 'Bored', emoji: '😐' },
]

export default function Mood() {
  const [customMood, setCustomMood] = useState('')
  const [loading, setLoading] = useState(false)
  const router = useRouter()

  async function submitMood(mood: string) {
    setLoading(true)
    try {
      await fetch('/api/recommendations', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ mood }),
      })
    } catch (err) {
      console.error(err)
    }
    setLoading(false)
    router.push(`/results?mood=${encodeURIComponent(mood)}`)
  }

  if (loading) {
    return (
      <div>
        <Nav />
        <p>Loading…</p>
      </div>
    )
  }

  return (
    <div>
      <Nav />
      <h1>Select Your Mood</h1>
      <div style={{ display: 'flex', flexWrap: 'wrap', gap: '0.5rem' }}>
        {PRESET_MOODS.map((m) => (
          <button
            key={m.label}
            onClick={() => submitMood(m.label)}
            title={m.label}
            style={{ padding: '0.5rem 1rem', fontSize: '1rem' }}
          >
            <span style={{ marginRight: '0.25rem' }}>{m.emoji}</span>
            {m.label}
          </button>
        ))}
      </div>
      <div style={{ marginTop: '1rem' }}>
        <input
          type="text"
          placeholder="Describe your mood…"
          value={customMood}
          onChange={(e) => setCustomMood(e.target.value)}
          style={{ padding: '0.5rem', width: '60%' }}
        />
        <button
          onClick={() => customMood && submitMood(customMood)}
          style={{ marginLeft: '0.5rem', padding: '0.5rem 1rem' }}
        >
          Let’s Go
        </button>
      </div>
    </div>
  )
}
