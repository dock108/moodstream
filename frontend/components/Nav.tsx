import Link from 'next/link'

export default function Nav() {
  return (
    <nav style={{ marginBottom: '1rem' }}>
      <Link href="/">Home</Link> |{' '}
      <Link href="/mood">Mood</Link> |{' '}
      <Link href="/quiz">Quiz</Link> |{' '}
      <Link href="/results">Results</Link>
    </nav>
  )
}
