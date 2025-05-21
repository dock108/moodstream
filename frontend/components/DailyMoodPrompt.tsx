import { useEffect, useState } from 'react'
import { useRouter } from 'next/router'

const PRESET_MOODS = ['Happy', 'Tired', 'Curious', 'Stressed', 'Relaxed']

export default function DailyMoodPrompt() {
  const [show, setShow] = useState(false)
  const [customMood, setCustomMood] = useState('')
  const router = useRouter()

  useEffect(() => {
    const today = new Date().toISOString().split('T')[0]
    const last = localStorage.getItem('lastMoodCheckIn')
    if (last !== today) {
      setShow(true)
      const shown = parseInt(localStorage.getItem('analytics_prompt_shown') || '0', 10) + 1
      localStorage.setItem('analytics_prompt_shown', String(shown))
    }
  }, [])

  async function submitMood(mood: string) {
    const today = new Date().toISOString().split('T')[0]
    localStorage.setItem('lastMoodCheckIn', today)
    const selected = parseInt(localStorage.getItem('analytics_mood_selected') || '0', 10) + 1
    localStorage.setItem('analytics_mood_selected', String(selected))
    setShow(false)
    try {
      await fetch('/api/recommendations', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ mood }),
      })
    } catch (err) {
      console.error(err)
    }
    router.push(`/results?mood=${encodeURIComponent(mood)}`)
  }

  function dismiss() {
    const today = new Date().toISOString().split('T')[0]
    localStorage.setItem('lastMoodCheckIn', today)
    const skipped = parseInt(localStorage.getItem('analytics_prompt_skipped') || '0', 10) + 1
    localStorage.setItem('analytics_prompt_skipped', String(skipped))
    setShow(false)
  }

  if (!show) return null

  return (
    <div
      style={{
        position: 'fixed',
        top: 0,
        left: 0,
        right: 0,
        background: '#fff',
        borderBottom: '1px solid #ccc',
        padding: '1rem',
        zIndex: 1000,
      }}
    >
      <p style={{ margin: '0 0 0.5rem 0' }}>Good morning! How are you feeling today?</p>
      <div style={{ display: 'flex', flexWrap: 'wrap', gap: '0.5rem', marginBottom: '0.5rem' }}>
        {PRESET_MOODS.map((m) => (
          <button key={m} onClick={() => submitMood(m)}>{m}</button>
        ))}
      </div>
      <div>
        <input
          type="text"
          placeholder="Your mood"
          value={customMood}
          onChange={(e) => setCustomMood(e.target.value)}
          style={{ padding: '0.25rem', marginRight: '0.5rem' }}
        />
        <button onClick={() => customMood && submitMood(customMood)}>Submit</button>
        <button onClick={dismiss} style={{ marginLeft: '0.5rem' }}>Skip</button>
      </div>
    </div>
  )
}
