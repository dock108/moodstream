import { useRouter } from 'next/router'
import Nav from '../components/Nav'
import { useUserContent } from '../context/UserContentContext'
import { useAuth } from '../context/AuthContext'

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
    </div>
  )
}
