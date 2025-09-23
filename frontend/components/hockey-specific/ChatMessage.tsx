'use client'

import React from 'react'
import { motion } from 'framer-motion'
import { UserIcon, CpuChipIcon } from '@heroicons/react/24/outline'
import { AnalyticsPanel } from './AnalyticsPanel'

interface Message {
  id: string
  role: 'user' | 'stanley'
  content: string
  timestamp: Date
  analytics?: AnalyticsData[]
}

interface AnalyticsData {
  type: 'stat' | 'chart' | 'table' | 'clips'
  title: string
  data: any
  clips?: {
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
  }[]
}

interface ChatMessageProps {
  message: Message
}

export function ChatMessage({ message }: ChatMessageProps) {
  const isStanley = message.role === 'stanley'
  
  if (isStanley) {
    // Stanley's messages: Plain text aligned to far left of center column
    return (
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.3 }}
        className="mb-8 grid grid-cols-12"
      >
        {/* Left empty column */}
        <div className="col-span-3"></div>
        
        {/* Center column with Stanley's plain text response */}
        <div className="col-span-6 px-4">
          {/* Small Stanley indicator - no avatar */}
          <div className="mb-3">
            <span className="text-xs font-medium text-red-600 font-military-display">STANLEY</span>
          </div>
          
          {/* Plain text response - aligned to far left, no bubble, just text */}
          <div className="text-white text-base leading-relaxed text-left font-military-chat">
            {message.content.split('\n').map((line, index) => (
              <p key={index} className={index > 0 ? 'mt-3' : ''}>
                {line}
              </p>
            ))}
          </div>
          
          {/* Analytics panel if present */}
          {message.analytics && (
            <motion.div
              initial={{ opacity: 0, y: 10 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.3, duration: 0.3 }}
              className="mt-6"
            >
              <AnalyticsPanel analytics={message.analytics} />
            </motion.div>
          )}
        </div>
        
        {/* Right empty column */}
        <div className="col-span-3"></div>
      </motion.div>
    )
  }

  // User messages: Aligned to far right of center column
  return (
    <div className="mb-6 grid grid-cols-12">
      {/* Left empty column */}
      <div className="col-span-3"></div>
      
      {/* Center column with user message */}
      <div className="col-span-6 px-4">
        <div className="flex justify-end">
          {/* User message bubble - no avatar, aligned to far right */}
          <motion.div
            initial={{ scale: 0.95, opacity: 0 }}
            animate={{ scale: 1, opacity: 1 }}
            transition={{ duration: 0.2 }}
            className="px-4 py-3 rounded-2xl bg-gray-800 border border-gray-700 text-white inline-block max-w-xs"
          >
            <div className="text-sm leading-relaxed font-military-chat">
              {message.content}
            </div>
          </motion.div>
        </div>
      </div>
      
      {/* Right empty column */}
      <div className="col-span-3"></div>
    </div>
  )
}
