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
  type: 'stat' | 'chart' | 'table'
  title: string
  data: any
}

interface ChatMessageProps {
  message: Message
}

export function ChatMessage({ message }: ChatMessageProps) {
  const isStanley = message.role === 'stanley'
  
  return (
    <div className={`flex ${isStanley ? 'justify-start' : 'justify-end'} mb-6`}>
      <div className={`flex max-w-4xl ${isStanley ? 'flex-row' : 'flex-row-reverse'} items-start space-x-3`}>
        {/* Avatar */}
        <div className={`flex-shrink-0 ${isStanley ? 'mr-3' : 'ml-3 mr-0'}`}>
          <div className={`w-8 h-8 rounded-full flex items-center justify-center ${
            isStanley 
              ? 'bg-red-600 text-white' 
              : 'bg-gray-800 text-white'
          }`}>
            {isStanley ? (
              <CpuChipIcon className="w-5 h-5" />
            ) : (
              <UserIcon className="w-5 h-5" />
            )}
          </div>
        </div>

        {/* Message content */}
        <div className={`flex flex-col ${isStanley ? 'items-start' : 'items-end'} max-w-3xl`}>
          {/* Message bubble */}
          <motion.div
            initial={{ scale: 0.95, opacity: 0 }}
            animate={{ scale: 1, opacity: 1 }}
            transition={{ duration: 0.2 }}
            className={`px-6 py-4 rounded-2xl ${
              isStanley
                ? 'bg-gray-900 border border-gray-800 text-white'
                : 'bg-blue-500 text-white'
            } shadow-lg`}
          >
            {/* Message header */}
            <div className="flex items-center justify-between mb-2">
              <span className={`text-xs font-medium ${
                isStanley ? 'text-red-600' : 'text-white/70'
              }`}>
                {isStanley ? 'STANLEY' : 'USER'}
              </span>
              <span className={`text-xs font-mono ${
                isStanley ? 'text-gray-400' : 'text-white/50'
              }`}>
                {message.timestamp.toLocaleTimeString([], { 
                  hour: '2-digit', 
                  minute: '2-digit' 
                })}
              </span>
            </div>

            {/* Message text */}
            <div className="text-sm leading-relaxed text-white">
              {message.content.split('\n').map((line, index) => (
                <p key={index} className={index > 0 ? 'mt-2' : ''}>
                  {line}
                </p>
              ))}
            </div>
          </motion.div>

          {/* Analytics panel for Stanley messages */}
          {isStanley && message.analytics && (
            <motion.div
              initial={{ opacity: 0, y: 10 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.3, duration: 0.3 }}
              className="mt-4 w-full"
            >
              <AnalyticsPanel analytics={message.analytics} />
            </motion.div>
          )}
        </div>
      </div>
    </div>
  )
}
