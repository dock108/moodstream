import { useState } from 'react'
import { useRouter } from 'next/router'
import Nav from '../components/Nav'
import { useAuth } from '../context/AuthContext'

export default function Login() {
  const { signUp, signIn, user } = useAuth()
  const router = useRouter()
  const [isSignUp, setIsSignUp] = useState(false)
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [error, setError] = useState<string | null>(null)

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setError(null)
    if (!email || !password) {
      setError('Email and password are required')
      return
    }

    const fn = isSignUp ? signUp : signIn
    const { error } = await fn(email, password)
    if (error) {
      setError(error)
    } else {
      router.push('/')
    }
  }

  return (
    <div>
      <Nav />
      {user ? (
        <p>You are logged in as {user.email}</p>
      ) : (
        <form onSubmit={handleSubmit}>
          <h1>{isSignUp ? 'Sign Up' : 'Login'}</h1>
          {error && <p style={{ color: 'red' }}>{error}</p>}
          <div>
            <label>
              Email
              <input
                type="email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
              />
            </label>
          </div>
          <div>
            <label>
              Password
              <input
                type="password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
              />
            </label>
          </div>
          <button type="submit">{isSignUp ? 'Sign Up' : 'Login'}</button>
          <p
            style={{ cursor: 'pointer', textDecoration: 'underline' }}
            onClick={() => setIsSignUp(!isSignUp)}
          >
            {isSignUp ? 'Already have an account? Login' : 'Need an account? Sign Up'}
          </p>
        </form>
      )}
    </div>
  )
}
