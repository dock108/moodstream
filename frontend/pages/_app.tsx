import type { AppProps } from 'next/app'
import '../styles/globals.css'
import { AuthProvider } from '../context/AuthContext'
import { UserContentProvider } from '../context/UserContentContext'

export default function App({ Component, pageProps }: AppProps) {
  return (
    <AuthProvider>
      <UserContentProvider>
        <Component {...pageProps} />
      </UserContentProvider>
    </AuthProvider>
  )
}
