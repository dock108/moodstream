import { useRouter } from 'next/router'
import { useEffect } from 'react'
import Nav from '../components/Nav'
import { useAuth } from '../context/AuthContext'

export default function Quiz() {
  const { user, loading } = useAuth()
  const router = useRouter()

  useEffect(() => {
    if (!loading && !user) {
      router.replace('/login')
    }
  }, [loading, user, router])

  if (!user) {
    return (
      <div>
        <Nav />
        <p>Loading...</p>
      </div>
    )
  }

  return (
    <div>
      <Nav />
      <h1>Quiz Page</h1>
      <p>Placeholder for user quizzes.</p>
    </div>
  )
}
