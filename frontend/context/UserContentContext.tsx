import { createContext, useContext, useEffect, useState } from 'react'
import { supabase } from '../utils/supabaseClient'
import { useAuth } from './AuthContext'

export type ContentStatus = 'seen' | 'loved'

interface UserContentContextType {
  statuses: Record<string, ContentStatus>
  loading: boolean
  markContent: (
    contentId: string,
    contentType: string,
    status: ContentStatus
  ) => Promise<{ error: string | null }>
}

const UserContentContext = createContext<UserContentContextType>({
  statuses: {},
  loading: true,
  markContent: async () => ({ error: null })
})

export function UserContentProvider({ children }: { children: React.ReactNode }) {
  const { user } = useAuth()
  const [statuses, setStatuses] = useState<Record<string, ContentStatus>>({})
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    async function load() {
      if (!user) {
        setStatuses({})
        setLoading(false)
        return
      }
      setLoading(true)
      const { data, error } = await supabase
        .from('user_content')
        .select('content_id, status')
        .eq('id', user.id)
      if (!error && data) {
        const map: Record<string, ContentStatus> = {}
        for (const row of data) {
          map[row.content_id] = row.status as ContentStatus
        }
        setStatuses(map)
      } else if (error) {
        console.error('Failed to load content statuses', error)
      }
      setLoading(false)
    }
    load()
  }, [user])

  const markContent = async (
    contentId: string,
    contentType: string,
    status: ContentStatus
  ) => {
    if (!user) return { error: 'Not authenticated' }
    const previous = statuses[contentId]
    setStatuses((prev) => ({ ...prev, [contentId]: status }))
    const { error } = await supabase
      .from('user_content')
      .upsert(
        { id: user.id, content_id: contentId, content_type: contentType, status },
        { onConflict: 'id,content_id' }
      )
    if (error) {
      console.error('Failed to update content', error)
      setStatuses((prev) => ({ ...prev, [contentId]: previous }))
      return { error: error.message }
    }
    return { error: null }
  }

  return (
    <UserContentContext.Provider value={{ statuses, loading, markContent }}>
      {children}
    </UserContentContext.Provider>
  )
}

export const useUserContent = () => useContext(UserContentContext)
