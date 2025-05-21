import type { AppProps } from 'next/app'
import '../styles/globals.css'
import { AuthProvider } from '../context/AuthContext'
import { UserContentProvider } from '../context/UserContentContext'
import DailyMoodPrompt from '../components/DailyMoodPrompt'

export default function App({ Component, pageProps }: AppProps) {
  return (
    <AuthProvider>
      <UserContentProvider>
        <DailyMoodPrompt />
        <Component {...pageProps} />
      </UserContentProvider>
    </AuthProvider>
  )
}
