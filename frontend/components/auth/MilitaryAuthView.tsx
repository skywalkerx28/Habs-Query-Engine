'use client'

import React, { useState } from 'react'
import { motion } from 'framer-motion'
import { LockClosedIcon, UserIcon, ShieldCheckIcon } from '@heroicons/react/24/outline'
import { EyeIcon, EyeSlashIcon } from '@heroicons/react/24/solid'
import { api } from '../../lib/api'

interface MilitaryAuthViewProps {
  onLogin: (userInfo: any) => void
}

export function MilitaryAuthView({ onLogin }: MilitaryAuthViewProps) {
  const [username, setUsername] = useState('')
  const [password, setPassword] = useState('')
  const [showPassword, setShowPassword] = useState(false)
  const [isLoading, setIsLoading] = useState(false)
  const [error, setError] = useState('')

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setError('')
    
    if (!username || !password) {
      setError('AUTHENTICATION REQUIRED')
      return
    }

    setIsLoading(true)
    
    try {
      // Call real API authentication
      const loginResponse = await api.login({ username, password })
      
      if (loginResponse.success && loginResponse.user_info && loginResponse.access_token) {
        // Store the token for API requests
        localStorage.setItem('heartbeat_token', loginResponse.access_token)
        onLogin(loginResponse.user_info)
      } else {
        setError('AUTHENTICATION FAILED')
      }
    } catch (error) {
      console.error('Login error:', error)
      setError('AUTHENTICATION FAILED')
    } finally {
      setIsLoading(false)
    }
  }

  return (
    <div className="min-h-screen bg-gray-950 flex flex-col items-center justify-center px-4 relative overflow-hidden">
      {/* Background grid pattern */}
      <div className="absolute inset-0 bg-grid-pattern opacity-10 pointer-events-none" />
      
      {/* Top status bar */}
      <div className="absolute top-0 left-0 right-0 px-6 py-4 flex items-center justify-between">
        <div className="flex items-center space-x-2">
          <div className="w-2 h-2 bg-green-500 rounded-full animate-pulse" />
          <span className="text-xs text-gray-400 font-military-display">SECURE ACCESS POINT</span>
        </div>
        <span className="text-xs text-gray-400 font-military-display">MTL-AUTH-V2.1</span>
      </div>

      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5 }}
        className="w-full max-w-md"
      >
        {/* Logo and Title */}
        <div className="text-center mb-14">
          <h1 className="text-3xl font-bold text-white tracking-wider font-military-display mb-2">
            HEARTBEAT
          </h1>
          <p className="text-xs text-gray-400 font-military-chat">
            MONTREAL CANADIENS ANALYTICS ENGINE
          </p>
        </div>

        {/* Auth Form */}
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ delay: 0.3, duration: 0.5 }}
          className="bg-gray-900/50 backdrop-blur-sm border border-gray-800 rounded-lg p-6"
        >
          <h2 className="text-base font-military-display text-white mb-5 text-center">
            AUTHENTICATION REQUIRED
          </h2>

          <form onSubmit={handleSubmit} className="space-y-5">
            {/* Username Field */}
            <div>
              <label htmlFor="username" className="block text-xs font-military-display text-gray-400 mb-1.5">
                USERNAME
              </label>
              <div className="relative">
                <div className="absolute inset-y-0 left-0 pl-2.5 flex items-center pointer-events-none">
                  <UserIcon className="h-4 w-4 text-gray-500" />
                </div>
                <input
                  id="username"
                  type="text"
                  value={username}
                  onChange={(e) => setUsername(e.target.value)}
                  className="block w-full pl-9 pr-3 py-2.5 bg-gray-950 border border-gray-700 rounded-lg text-white placeholder-gray-500 font-military-chat text-base focus:outline-none focus:ring-2 focus:ring-red-600 focus:border-transparent transition-all"
                  placeholder="Enter username"
                  disabled={isLoading}
                  autoComplete="username"
                />
              </div>
            </div>

            {/* Password Field */}
            <div>
              <label htmlFor="password" className="block text-xs font-military-display text-gray-400 mb-1.5">
                ACCESS CODE
              </label>
              <div className="relative">
                <div className="absolute inset-y-0 left-0 pl-2.5 flex items-center pointer-events-none">
                  <LockClosedIcon className="h-4 w-4 text-gray-500" />
                </div>
                <input
                  id="password"
                  type={showPassword ? 'text' : 'password'}
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  className="block w-full pl-9 pr-10 py-2.5 bg-gray-950 border border-gray-700 rounded-lg text-white placeholder-gray-500 font-military-chat text-base focus:outline-none focus:ring-2 focus:ring-red-600 focus:border-transparent transition-all"
                  placeholder="Enter access code"
                  disabled={isLoading}
                  autoComplete="current-password"
                />
                <button
                  type="button"
                  onClick={() => setShowPassword(!showPassword)}
                  className="absolute inset-y-0 right-0 pr-2.5 flex items-center"
                  tabIndex={-1}
                >
                  {showPassword ? (
                    <EyeSlashIcon className="h-4 w-4 text-gray-500 hover:text-gray-400 transition-colors" />
                  ) : (
                    <EyeIcon className="h-4 w-4 text-gray-500 hover:text-gray-400 transition-colors" />
                  )}
                </button>
              </div>
            </div>

            {/* Error Message */}
            {error && (
              <motion.div
                initial={{ opacity: 0, y: -10 }}
                animate={{ opacity: 1, y: 0 }}
                className="bg-red-600/10 border border-red-600/30 rounded-lg px-3 py-2"
              >
                <p className="text-xs text-red-600 font-military-chat text-center">
                  {error}
                </p>
              </motion.div>
            )}

            {/* Submit Button */}
            <button
              type="submit"
              disabled={isLoading}
              className="w-full py-2.5 px-4 bg-red-600 hover:bg-red-700 disabled:bg-gray-800 disabled:cursor-not-allowed text-white font-military-display text-base rounded-lg transition-all duration-200 focus:outline-none focus:ring-2 focus:ring-red-600 focus:ring-offset-2 focus:ring-offset-gray-950"
            >
              {isLoading ? (
                <span className="flex items-center justify-center">
                  <svg className="animate-spin -ml-1 mr-2 h-4 w-4 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                    <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                    <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                  </svg>
                  AUTHENTICATING...
                </span>
              ) : (
                'INITIATE ACCESS'
              )}
            </button>
          </form>

          {/* Security Notice */}
          <div className="mt-5 pt-5 border-t border-gray-800">
            <p className="text-xs text-gray-500 text-center font-military-chat">
              RESTRICTED ACCESS • AUTHORIZED PERSONNEL ONLY
            </p>
            <p className="text-xs text-gray-600 text-center font-military-chat mt-1">
              ALL ACCESS ATTEMPTS ARE MONITORED AND LOGGED
            </p>
          </div>
        </motion.div>
      </motion.div>

      {/* Bottom status bar */}
      <div className="absolute bottom-0 left-0 right-0 px-6 py-4 flex items-center justify-between">
        <span className="text-xs text-gray-500 font-military-display">SECURE CONNECTION</span>
        <span className="text-xs text-gray-500 font-military-display">HEARTBEAT ENGINE V2.1</span>
      </div>
    </div>
  )
}
