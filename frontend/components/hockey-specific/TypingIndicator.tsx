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
      className="mb-8 grid grid-cols-12"
    >
      {/* Left empty column */}
      <div className="col-span-3"></div>
      
      {/* Center column with typing indicator bubble */}
      <div className="col-span-6 px-4">
        {/* Thinking bubble - only appears while processing, no avatar */}
        <div className="bg-gray-900 border border-gray-800 rounded-2xl px-6 py-4 inline-block">
          <div className="flex items-center space-x-3">
            <span className="text-xs font-medium text-red-600 font-military-display">STANLEY</span>
            <span className="text-white text-sm font-military-chat">THINKING</span>
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
        </div>
      </div>
      
      {/* Right empty column */}
      <div className="col-span-3"></div>
    </motion.div>
  )
}
