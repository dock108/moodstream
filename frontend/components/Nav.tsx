import Link from 'next/link'
import { useAuth } from '../context/AuthContext'

export default function Nav() {
  const { user, signOut } = useAuth()

  return (
    <nav style={{ marginBottom: '1rem' }}>
      <Link href="/">Home</Link> |{' '}
      <Link href="/mood">Mood</Link> |{' '}
      <Link href="/quiz">Quiz</Link> |{' '}
      {user ? (
        <>
          <button onClick={signOut}>Logout</button> |{' '}
          <span>You are logged in as {user.email}</span>
        </>
      ) : (
        <Link href="/login">Login</Link>
      )}
      <Link href="/results">Results</Link>
    </nav>
  )
}
