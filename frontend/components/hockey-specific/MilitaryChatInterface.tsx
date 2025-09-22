'use client'

import React, { useState, useRef, useEffect } from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import { PaperAirplaneIcon } from '@heroicons/react/24/outline'
import { ChatMessage } from './ChatMessage'
import { TypingIndicator } from './TypingIndicator'

interface Message {
  id: string
  role: 'user' | 'stanley'
  content: string
  timestamp: Date
  analytics?: AnalyticsData[]
}

interface AnalyticsData {
  type: 'stat' | 'chart' | 'table'
  title: string
  data: any
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

    // Simulate Stanley's response (replace with actual API call)
    setTimeout(() => {
      const stanleyResponse: Message = {
        id: (Date.now() + 1).toString(),
        role: 'stanley',
        content: `Analyzing query: "${newMessage.content}"\n\nBased on current Montreal Canadiens data, I can provide detailed insights. Processing through advanced analytics pipeline...`,
        timestamp: new Date(),
        analytics: [
          {
            type: 'stat',
            title: 'Player Performance',
            data: { goals: 12, assists: 8, points: 20 }
          }
        ]
      }
      setMessages(prev => [...prev, stanleyResponse])
      setIsTyping(false)
    }, 2000)
  }

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault()
      handleSendMessage()
    }
  }

  return (
    <div className="flex flex-col h-screen bg-gray-950">
      {/* Military-style header */}
      <header className="border-b border-gray-800 bg-gray-900/50 backdrop-blur-sm">
        <div className="flex items-center justify-center px-6 py-4 relative">
          <h1 className="text-xl font-bold text-white tracking-wider">
            HEARTBEAT
          </h1>
          <div className="absolute right-6 flex items-center space-x-2">
            <div className="w-2 h-2 bg-green-500 rounded-full animate-pulse" />
            <span className="text-xs text-gray-400 font-mono">ONLINE</span>
          </div>
        </div>
      </header>

      {/* Chat messages area */}
      <div className="flex-1 overflow-y-auto px-6 py-6 space-y-6">
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
                  className="w-full input-military text-white placeholder-gray-500 pr-12 resize-none"
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
          <div className="flex items-center justify-between mt-3 text-xs text-gray-500">
            <div className="flex items-center space-x-4">
              <span className="font-mono">SECURE CONNECTION</span>
              <span className="font-mono">MTL-ANALYTICS-v2.1</span>
            </div>
            <div className="flex items-center space-x-2">
              <span>Press Enter to send</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}
