'use client'

import React, { useState, useRef } from 'react'
import { motion } from 'framer-motion'
import { 
  PlayIcon,
  PauseIcon,
  SpeakerWaveIcon,
  SpeakerXMarkIcon,
  ArrowsPointingOutIcon,
  ClockIcon,
  UserIcon
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
      className="relative bg-gray-900/50 border border-gray-800 rounded-lg overflow-hidden backdrop-blur-sm group hover:border-gray-600 transition-all duration-200"
      onMouseEnter={() => setIsHovered(true)}
      onMouseLeave={() => setIsHovered(false)}
    >
      {/* Video Player Container */}
      <div className="relative aspect-video bg-black">
        <video
          ref={videoRef}
          className="w-full h-full object-cover"
          poster={clip.thumbnail_url}
          muted={isMuted}
          onTimeUpdate={handleTimeUpdate}
          onPlay={() => setIsPlaying(true)}
          onPause={() => setIsPlaying(false)}
          onEnded={() => setIsPlaying(false)}
          preload="metadata"
        >
          <source src={clip.file_url} type="video/mp4" />
          Your browser does not support the video tag.
        </video>

        {/* Video Overlay Controls */}
        <div className={`absolute inset-0 bg-black/20 transition-opacity duration-200 ${
          isHovered ? 'opacity-100' : 'opacity-0'
        }`}>
          
          {/* Center Play Button */}
          <div className="absolute inset-0 flex items-center justify-center">
            <motion.button
              whileHover={{ scale: 1.1 }}
              whileTap={{ scale: 0.95 }}
              onClick={handlePlayPause}
              className="bg-black/70 border border-gray-600 rounded-full p-3 hover:bg-black/90 transition-colors"
            >
              {isPlaying ? (
                <PauseIcon className="w-6 h-6 text-white" />
              ) : (
                <PlayIcon className="w-6 h-6 text-white ml-0.5" />
              )}
            </motion.button>
          </div>

          {/* Top Controls Bar */}
          <div className="absolute top-2 left-2 right-2 flex items-center justify-between">
            <div className="flex items-center space-x-1">
              <span className="bg-red-600 text-white text-xs px-2 py-0.5 rounded font-mono">
                LIVE
              </span>
              {clip.event_type && (
                <span className="bg-gray-800/80 text-gray-300 text-xs px-2 py-0.5 rounded font-mono uppercase">
                  {clip.event_type}
                </span>
              )}
            </div>
            
            <button
              onClick={handleMuteToggle}
              className="bg-gray-800/80 p-1.5 rounded hover:bg-gray-700/80 transition-colors"
            >
              {isMuted ? (
                <SpeakerXMarkIcon className="w-4 h-4 text-gray-300" />
              ) : (
                <SpeakerWaveIcon className="w-4 h-4 text-white" />
              )}
            </button>
          </div>

          {/* Bottom Progress Bar */}
          <div className="absolute bottom-0 left-0 right-0 bg-gradient-to-t from-black/60 to-transparent p-2">
            <div className="bg-gray-700 h-1 rounded-full overflow-hidden">
              <div 
                className="bg-red-500 h-full transition-all duration-100"
                style={{ 
                  width: clip.duration > 0 ? `${(currentTime / clip.duration) * 100}%` : '0%' 
                }}
              />
            </div>
            <div className="flex items-center justify-between mt-1 text-xs text-gray-300 font-mono">
              <span>{formatTime(currentTime)}</span>
              <span>{formatDuration(clip.duration)}</span>
            </div>
          </div>
        </div>

        {/* Duration Badge (when not playing) */}
        {!isPlaying && (
          <div className="absolute top-2 right-2 bg-black/70 text-white text-xs px-2 py-1 rounded font-mono flex items-center space-x-1">
            <ClockIcon className="w-3 h-3" />
            <span>{formatDuration(clip.duration)}</span>
          </div>
        )}
      </div>

      {/* Clip Information */}
      <div className="p-3 space-y-2">
        {/* Title and Player */}
        <div className="space-y-1">
          <h3 className="text-sm font-medium text-white font-military-display leading-tight">
            {clip.title}
          </h3>
          <div className="flex items-center space-x-2 text-xs text-gray-400">
            <UserIcon className="w-3 h-3" />
            <span className="font-mono">{clip.player_name}</span>
            {clip.game_info && (
              <>
                <span>•</span>
                <span className="font-mono">{clip.game_info}</span>
              </>
            )}
          </div>
        </div>

        {/* Description */}
        {clip.description && clip.description !== clip.title && (
          <p className="text-xs text-gray-500 leading-relaxed">
            {clip.description}
          </p>
        )}

        {/* Footer with metadata */}
        <div className="flex items-center justify-between pt-2 border-t border-gray-800/50">
          <div className="flex items-center space-x-3 text-xs text-gray-500 font-mono">
            <span>ID: {clip.clip_id.slice(-8)}</span>
            {clip.relevance_score && (
              <span>RELEVANCE: {Math.round(clip.relevance_score * 100)}%</span>
            )}
          </div>
          
          {/* Expand button */}
          <button
            className="p-1 text-gray-500 hover:text-white transition-colors"
            title="Expand video"
          >
            <ArrowsPointingOutIcon className="w-3 h-3" />
          </button>
        </div>
      </div>
    </motion.div>
  )
}
