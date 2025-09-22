'use client'

import React from 'react'
import { motion } from 'framer-motion'
import { CpuChipIcon } from '@heroicons/react/24/outline'

export function TypingIndicator() {
  return (
    <div className="flex justify-start mb-6">
      <div className="flex flex-row items-start space-x-3 max-w-4xl">
        {/* Stanley avatar */}
        <div className="flex-shrink-0">
          <div className="w-8 h-8 rounded-full bg-red-600 text-white flex items-center justify-center">
            <CpuChipIcon className="w-5 h-5" />
          </div>
        </div>

        {/* Typing bubble */}
        <motion.div
          initial={{ scale: 0.95, opacity: 0 }}
          animate={{ scale: 1, opacity: 1 }}
          transition={{ duration: 0.2 }}
          className="bg-gray-900 border border-gray-800 rounded-2xl px-6 py-4 shadow-lg"
        >
          {/* Header */}
          <div className="flex items-center justify-between mb-2">
            <span className="text-xs font-medium text-red-600">
              STANLEY
            </span>
            <span className="text-xs font-mono text-gray-400">
              PROCESSING
            </span>
          </div>

          {/* Typing animation */}
          <div className="flex items-center space-x-2">
            <span className="text-sm text-white">
              Analyzing data
            </span>
            <div className="flex space-x-1">
              {[0, 1, 2].map((i) => (
                <motion.div
                  key={i}
                  className="w-2 h-2 bg-red-600 rounded-full"
                  animate={{
                    scale: [1, 1.2, 1],
                    opacity: [0.5, 1, 0.5],
                  }}
                  transition={{
                    duration: 1.5,
                    repeat: Infinity,
                    delay: i * 0.2,
                  }}
                />
              ))}
            </div>
          </div>

          {/* Military-style progress indicator */}
          <div className="mt-3">
            <div className="flex items-center space-x-2">
              <div className="flex-1 h-1 bg-gray-800 rounded-full overflow-hidden">
                <motion.div
                  className="h-full bg-red-600"
                  animate={{
                    width: ['0%', '100%', '0%'],
                  }}
                  transition={{
                    duration: 2,
                    repeat: Infinity,
                    ease: 'easeInOut',
                  }}
                />
              </div>
              <span className="text-xs font-mono text-gray-400">
                ANALYZING
              </span>
            </div>
          </div>
        </motion.div>
      </div>
    </div>
  )
}
