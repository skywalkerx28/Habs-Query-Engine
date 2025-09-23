'use client'

import { useState, useEffect } from 'react'
import clsx from 'clsx'
import { MilitaryChatInterface } from '../components/hockey-specific/MilitaryChatInterface'
import { MilitarySidebar } from '../components/military-sidebar/MilitarySidebar'
import { MilitaryAuthView } from '../components/auth/MilitaryAuthView'
import { api } from '../lib/api'

export default function HomePage() {
  const [isAuthenticated, setIsAuthenticated] = useState(false)
  const [sidebarOpen, setSidebarOpen] = useState(false)
  const [userInfo, setUserInfo] = useState<any>(null)

  // Check for existing authentication on component mount
  useEffect(() => {
    const storedUser = localStorage.getItem('heartbeat_user')
    const storedToken = localStorage.getItem('heartbeat_token')
    
    if (storedUser && storedToken) {
      try {
        const userData = JSON.parse(storedUser)
        setUserInfo(userData)
        setIsAuthenticated(true)
        
        // Set the API token for subsequent requests
        api.setAccessToken(storedToken)
      } catch (error) {
        console.error('Error parsing stored user data:', error)
        localStorage.removeItem('heartbeat_user')
        localStorage.removeItem('heartbeat_token')
      }
    }
  }, [])

  const handleLogin = (userInfo: any) => {
    // Store user info from successful API authentication
    setUserInfo(userInfo)
    setIsAuthenticated(true)
    localStorage.setItem('heartbeat_user', JSON.stringify(userInfo))
  }

  const handleLogout = () => {
    // Clear authentication state
    setIsAuthenticated(false)
    setUserInfo(null)
    setSidebarOpen(false)
    localStorage.removeItem('heartbeat_user')
    localStorage.removeItem('heartbeat_token')
    
    // Clear API token
    api.clearAccessToken()
  }

  // Show auth view if not authenticated
  if (!isAuthenticated) {
    return <MilitaryAuthView onLogin={handleLogin} />
  }

  // Show main app if authenticated
  return (
    <main className="min-h-screen bg-gray-950 relative">
      <MilitarySidebar 
        isOpen={sidebarOpen} 
        onToggle={() => setSidebarOpen(!sidebarOpen)}
        userInfo={userInfo}
        onLogout={handleLogout}
      />
      <div className={clsx(
        'transition-all duration-300',
        sidebarOpen ? 'ml-80' : 'ml-16'
      )}>
        <MilitaryChatInterface />
      </div>
    </main>
  )
}
