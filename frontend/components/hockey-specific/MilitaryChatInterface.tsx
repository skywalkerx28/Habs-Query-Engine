'use client'

import React, { useState, useRef, useEffect } from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import { PaperAirplaneIcon } from '@heroicons/react/24/outline'
import { ChatMessage } from './ChatMessage'
import { TypingIndicator } from './TypingIndicator'
import { api } from '../../lib/api'

interface Message {
  id: string
  role: 'user' | 'stanley'
  content: string
  timestamp: Date
  analytics?: AnalyticsData[]
}

interface ClipData {
  clip_id: string
  title: string
  player_name: string
  game_info: string
  event_type: string
  description: string
  file_url: string
  thumbnail_url: string
  duration: number
  relevance_score?: number
}

interface AnalyticsData {
  type: 'stat' | 'chart' | 'table' | 'clips'
  title: string
  data: any
  clips?: ClipData[]
}

export function MilitaryChatInterface() {
  const [messages, setMessages] = useState<Message[]>([])
  const [inputValue, setInputValue] = useState('')
  const [isTyping, setIsTyping] = useState(false)
  const messagesEndRef = useRef<HTMLDivElement>(null)
  const inputRef = useRef<HTMLInputElement>(null)

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }

  useEffect(() => {
    scrollToBottom()
  }, [messages])

  const handleSendMessage = async () => {
    if (!inputValue.trim()) return

    const newMessage: Message = {
      id: Date.now().toString(),
      role: 'user',
      content: inputValue.trim(),
      timestamp: new Date(),
    }

    setMessages(prev => [...prev, newMessage])
    setInputValue('')
    setIsTyping(true)

    // Call real API for Stanley's response
    try {
      const queryResponse = await api.sendQuery({ query: newMessage.content })
      
      const stanleyResponse: Message = {
        id: (Date.now() + 1).toString(),
        role: 'stanley',
        content: queryResponse.response,
        timestamp: new Date(),
        analytics: queryResponse.analytics.length > 0 ? queryResponse.analytics.map(item => ({
          type: (item.type as any) ?? 'stat',
          title: item.title,
          data: item.data,
          clips: (item as any).clips || []
        })) : undefined
      }
      
      setMessages(prev => [...prev, stanleyResponse])
      setIsTyping(false)
    } catch (error) {
      console.error('Query error:', error)
      
      // Fallback response on error
      const errorResponse: Message = {
        id: (Date.now() + 1).toString(),
        role: 'stanley',
        content: "I apologize, but I'm experiencing technical difficulties. Please check your connection and try again.",
        timestamp: new Date(),
      }
      
      setMessages(prev => [...prev, errorResponse])
      setIsTyping(false)
    }
  }

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault()
      handleSendMessage()
    }
  }

  return (
    <div className="relative flex flex-col h-screen bg-gray-950">
      {/* Floating title */}
      <div className="absolute top-0 left-0 right-0 z-10 flex items-center justify-center px-6 py-6 pointer-events-none">
        <h1 className="text-xl font-bold text-white tracking-wider text-shadow-military font-military-display">
          HEARTBEAT
        </h1>
        <div className="absolute right-6 flex items-center space-x-2">
          <div className="w-2 h-2 bg-green-500 rounded-full animate-pulse" />
          <span className="text-xs text-gray-400 font-military-display">ONLINE</span>
        </div>
      </div>

      {/* Chat messages area */}
      <div className="flex-1 overflow-y-auto pt-20 pb-6">
        <AnimatePresence>
          {messages.map((message) => (
            <motion.div
              key={message.id}
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: -20 }}
              transition={{ duration: 0.3 }}
            >
              <ChatMessage message={message} />
            </motion.div>
          ))}
        </AnimatePresence>

        {isTyping && (
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: -20 }}
          >
            <TypingIndicator />
          </motion.div>
        )}

        <div ref={messagesEndRef} />
      </div>

      {/* Floating input area */}
      <div className="p-6">
        <div className="max-w-4xl mx-auto">
          <div className="relative flex items-end space-x-4">
            <div className="flex-1">
              <div className="relative">
                <input
                  ref={inputRef}
                  type="text"
                  value={inputValue}
                  onChange={(e) => setInputValue(e.target.value)}
                  onKeyPress={handleKeyPress}
                  placeholder="Enter your analytics query..."
                  className="w-full input-military text-white placeholder-gray-500 pr-12 resize-none font-military-chat"
                  disabled={isTyping}
                />
                <button
                  onClick={handleSendMessage}
                  disabled={!inputValue.trim() || isTyping}
                  className="absolute right-3 top-1/2 -translate-y-1/2 p-1.5 rounded-md text-gray-400 hover:text-white hover:bg-gray-800 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
                >
                  <PaperAirplaneIcon className="w-5 h-5" />
                </button>
              </div>
            </div>
          </div>
          
          {/* Military-style status bar */}
          <div className="flex items-center justify-center mt-3 text-xs text-gray-500">
            <div className="flex items-center space-x-4">
              <span className="font-military-display">SECURE CONNECTION</span>
              <span className="font-military-display">MTL-ANALYTICS-v2.1</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}
