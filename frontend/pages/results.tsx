import { useRouter } from 'next/router'
import Nav from '../components/Nav'

export default function Results() {
  const router = useRouter()
  const { mood } = router.query

  return (
    <div>
      <Nav />
      <h1>Recommendations</h1>
      {mood && <p>Mood: {mood}</p>}
      <p>Placeholder for recommendations.</p>
    </div>
  )
}
