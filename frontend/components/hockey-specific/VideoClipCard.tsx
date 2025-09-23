'use client'

import React, { useState, useRef } from 'react'
import { motion } from 'framer-motion'
import { 
  PlayIcon,
  PauseIcon,
  SpeakerWaveIcon,
  SpeakerXMarkIcon
} from '@heroicons/react/24/outline'

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

interface VideoClipCardProps {
  clip: ClipData
  index?: number
}

export function VideoClipCard({ clip, index = 0 }: VideoClipCardProps) {
  const [isPlaying, setIsPlaying] = useState(false)
  const [isMuted, setIsMuted] = useState(true)
  const [currentTime, setCurrentTime] = useState(0)
  const [isHovered, setIsHovered] = useState(false)
  const videoRef = useRef<HTMLVideoElement>(null)

  const handlePlayPause = () => {
    if (videoRef.current) {
      if (isPlaying) {
        videoRef.current.pause()
      } else {
        videoRef.current.play()
      }
      setIsPlaying(!isPlaying)
    }
  }

  const handleMuteToggle = () => {
    if (videoRef.current) {
      videoRef.current.muted = !isMuted
      setIsMuted(!isMuted)
    }
  }

  const handleTimeUpdate = () => {
    if (videoRef.current) {
      setCurrentTime(videoRef.current.currentTime)
    }
  }

  const formatTime = (seconds: number) => {
    const mins = Math.floor(seconds / 60)
    const secs = Math.floor(seconds % 60)
    return `${mins}:${secs.toString().padStart(2, '0')}`
  }

  const formatDuration = (seconds: number) => {
    if (seconds < 60) return `${Math.round(seconds)}s`
    const mins = Math.floor(seconds / 60)
    const secs = Math.floor(seconds % 60)
    return `${mins}:${secs.toString().padStart(2, '0')}`
  }

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ delay: index * 0.1, duration: 0.3 }}
      className="relative bg-black/80 border border-red-900/30 rounded-sm overflow-hidden backdrop-blur-sm group hover:border-red-600/50 hover:shadow-lg hover:shadow-red-900/20 transition-all duration-300"
      onMouseEnter={() => setIsHovered(true)}
      onMouseLeave={() => setIsHovered(false)}
    >
      {/* Full Height Video Player Container */}
      <div className="relative h-64 bg-black">
        {/* Video Element */}
        <video
          ref={videoRef}
          className="w-full h-full object-cover"
          poster={clip.thumbnail_url}
          muted={isMuted}
          onTimeUpdate={handleTimeUpdate}
          onPlay={() => setIsPlaying(true)}
          onPause={() => setIsPlaying(false)}
          onEnded={() => setIsPlaying(false)}
          onLoadedData={() => {
            // When video data loads, hide any fallback image
            const img = videoRef.current?.parentElement?.querySelector('img')
            if (img) img.style.display = 'none'
          }}
          preload="metadata"
        >
          <source src={clip.file_url} type="video/mp4" />
          Your browser does not support the video tag.
        </video>

        {/* Fallback Thumbnail Image (when video poster fails) */}
        {!isPlaying && clip.thumbnail_url && (
          <img
            src={clip.thumbnail_url}
            alt={`${clip.player_name} - ${clip.game_info}`}
            className="absolute inset-0 w-full h-full object-cover"
            onError={(e) => {
              // Hide the image if it fails to load
              (e.target as HTMLImageElement).style.display = 'none'
            }}
            onLoad={() => {
              // Hide video poster when our fallback image loads successfully
              if (videoRef.current) {
                videoRef.current.poster = ''
              }
            }}
          />
        )}

        {/* Video Overlay Controls */}
        <div className={`absolute inset-0 transition-opacity duration-300 ${
          isHovered ? 'opacity-100' : 'opacity-0'
        }`}>
          
          {/* Center Play Button */}
          <div className="absolute inset-0 flex items-center justify-center">
            <motion.button
              whileHover={{ scale: 1.05 }}
              whileTap={{ scale: 0.95 }}
              onClick={handlePlayPause}
              className="bg-red-600/80 border border-red-500 rounded-sm p-4 hover:bg-red-600 transition-colors backdrop-blur-sm"
            >
              {isPlaying ? (
                <PauseIcon className="w-8 h-8 text-white" />
              ) : (
                <PlayIcon className="w-8 h-8 text-white ml-0.5" />
              )}
            </motion.button>
          </div>

          {/* Top Controls Bar */}
          <div className="absolute top-3 left-3 right-3 flex items-center justify-between">
            <div className="flex items-center space-x-2">
              <span className="bg-red-600/90 text-white text-xs px-2 py-1 font-mono uppercase tracking-wider">
                {clip.event_type || 'CLIP'}
              </span>
              <span className="bg-black/70 text-gray-300 text-xs px-2 py-1 font-mono">
                {formatDuration(clip.duration)}
              </span>
            </div>
            
            <button
              onClick={handleMuteToggle}
              className="bg-black/70 p-2 rounded-sm hover:bg-black/90 transition-colors"
            >
              {isMuted ? (
                <SpeakerXMarkIcon className="w-4 h-4 text-gray-300" />
              ) : (
                <SpeakerWaveIcon className="w-4 h-4 text-white" />
              )}
            </button>
          </div>

          {/* Bottom Progress Bar */}
          <div className="absolute bottom-0 left-0 right-0 bg-gradient-to-t from-black/80 via-black/40 to-transparent p-3">
            <div className="bg-gray-700/60 h-0.5 rounded-full overflow-hidden mb-2">
              <div 
                className="bg-red-500 h-full transition-all duration-100"
                style={{ 
                  width: clip.duration > 0 ? `${(currentTime / clip.duration) * 100}%` : '0%' 
                }}
              />
            </div>
            <div className="flex items-center justify-between text-xs text-gray-300 font-mono">
              <span>{formatTime(currentTime)}</span>
              <span>{formatTime(clip.duration)}</span>
            </div>
          </div>
        </div>

        {/* Essential Info Overlay */}
        <div className={`absolute bottom-0 left-0 right-0 bg-gradient-to-t from-black/90 via-black/50 to-transparent p-3 transition-opacity duration-300 ${
          isHovered ? 'opacity-0' : 'opacity-100'
        }`}>
          <div className="text-white">
            <h3 className="text-sm font-medium font-military-display leading-tight mb-1 truncate">
              {clip.player_name.toUpperCase()}
            </h3>
            <p className="text-xs text-gray-300 font-mono truncate">
              {clip.game_info}
            </p>
          </div>
        </div>
      </div>
    </motion.div>
  )
}
