'use client'

import React from 'react'
import { motion } from 'framer-motion'
import { CpuChipIcon } from '@heroicons/react/24/outline'

export function TypingIndicator() {
  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.3 }}
      className="mb-8"
    >
      {/* Stanley's typing indicator - centered, no bubble */}
      <div className="max-w-4xl mx-auto px-6">
        <div className="text-center">
          <div className="inline-flex items-center space-x-2 mb-4">
            <div className="w-6 h-6 rounded-full bg-red-600 text-white flex items-center justify-center">
              <CpuChipIcon className="w-4 h-4" />
            </div>
            <span className="text-xs font-medium text-red-600 font-mono">STANLEY</span>
          </div>
          
          {/* Clean typing animation */}
          <div className="flex items-center justify-center space-x-2 mb-3">
            <span className="text-white text-base">
              Analyzing
            </span>
            <div className="flex space-x-1">
              {[0, 1, 2].map((i) => (
                <motion.div
                  key={i}
                  className="w-1.5 h-1.5 bg-red-600 rounded-full"
                  animate={{
                    scale: [1, 1.3, 1],
                    opacity: [0.4, 1, 0.4],
                  }}
                  transition={{
                    duration: 1.2,
                    repeat: Infinity,
                    delay: i * 0.15,
                  }}
                />
              ))}
            </div>
          </div>

          {/* Minimal progress indicator */}
          <div className="flex justify-center">
            <div className="w-32 h-0.5 bg-gray-800 rounded-full overflow-hidden">
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
          </div>
        </div>
      </div>
    </motion.div>
  )
}
