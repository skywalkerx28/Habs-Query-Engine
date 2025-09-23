'use client'

import React from 'react'
import { motion } from 'framer-motion'
import { VideoCameraIcon } from '@heroicons/react/24/outline'
import { VideoClipCard } from './VideoClipCard'
import { API_BASE_URL, api } from '../../lib/api'

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

interface VideoClipsPanelProps {
  clips: ClipData[]
  title?: string
}

export function VideoClipsPanel({ clips, title = "Video Highlights" }: VideoClipsPanelProps) {
  // Build absolute URLs with token for media requests
  const token = api.getAccessToken()
  const toAbsolute = (path: string) => {
    if (!path) return path
    // If already absolute, return as-is
    if (path.startsWith('http://') || path.startsWith('https://')) return path
    const tokenParam = token ? `?token=${encodeURIComponent(token)}` : ''
    // Only append token to media endpoints
    if (path.startsWith('/api/v1/clips/')) {
      return `${API_BASE_URL}${path}${tokenParam}`
    }
    return `${API_BASE_URL}${path}`
  }

  const normalizedClips = (clips || []).map((c) => ({
    ...c,
    file_url: toAbsolute(c.file_url),
    thumbnail_url: toAbsolute(c.thumbnail_url),
  }))

  // If no clips, show empty state
  if (normalizedClips.length === 0) {
    return (
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        className="bg-gray-900/50 border border-gray-800 rounded-lg p-6 backdrop-blur-sm text-center"
      >
        <VideoCameraIcon className="w-12 h-12 text-gray-600 mx-auto mb-3" />
        <h3 className="text-lg font-medium text-white font-military-display mb-2">
          No Video Clips Available
        </h3>
        <p className="text-sm text-gray-400">
          No clips were found for your query. Try adjusting your search terms or check back later.
        </p>
      </motion.div>
    )
  }

  // Simply render the video clips without any titles or wrapper panels
  return (
    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4 mt-3">
      {normalizedClips.map((clip, index) => (
        <VideoClipCard
          key={clip.clip_id}
          clip={clip}
          index={index}
        />
      ))}
    </div>
  )
}