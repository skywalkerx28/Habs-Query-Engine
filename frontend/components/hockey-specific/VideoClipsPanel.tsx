'use client'

import React, { useState } from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import { 
  VideoCameraIcon,
  FunnelIcon,
  ArrowsUpDownIcon,
  Squares2X2Icon,
  ListBulletIcon,
  MagnifyingGlassIcon
} from '@heroicons/react/24/outline'
import { VideoClipCard } from './VideoClipCard'

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

type ViewMode = 'grid' | 'list'
type SortBy = 'relevance' | 'duration' | 'player' | 'recent'
type FilterBy = 'all' | 'goals' | 'assists' | 'saves' | 'hits' | 'penalties'

export function VideoClipsPanel({ clips, title = "Video Highlights" }: VideoClipsPanelProps) {
  const [viewMode, setViewMode] = useState<ViewMode>('grid')
  const [sortBy, setSortBy] = useState<SortBy>('relevance')
  const [filterBy, setFilterBy] = useState<FilterBy>('all')
  const [searchTerm, setSearchTerm] = useState('')
  const [showControls, setShowControls] = useState(false)

  // Filter clips based on search and filter criteria
  const filteredClips = clips.filter(clip => {
    // Search filter
    if (searchTerm) {
      const searchLower = searchTerm.toLowerCase()
      const matchesSearch = 
        clip.title.toLowerCase().includes(searchLower) ||
        clip.player_name.toLowerCase().includes(searchLower) ||
        clip.event_type.toLowerCase().includes(searchLower) ||
        clip.game_info.toLowerCase().includes(searchLower)
      if (!matchesSearch) return false
    }

    // Event type filter
    if (filterBy !== 'all') {
      if (filterBy === 'goals' && !clip.event_type.toLowerCase().includes('goal')) return false
      if (filterBy === 'assists' && !clip.event_type.toLowerCase().includes('assist')) return false
      if (filterBy === 'saves' && !clip.event_type.toLowerCase().includes('save')) return false
      if (filterBy === 'hits' && !clip.event_type.toLowerCase().includes('hit')) return false
      if (filterBy === 'penalties' && !clip.event_type.toLowerCase().includes('penalt')) return false
    }

    return true
  })

  // Sort clips based on sort criteria
  const sortedClips = [...filteredClips].sort((a, b) => {
    switch (sortBy) {
      case 'relevance':
        return (b.relevance_score || 0) - (a.relevance_score || 0)
      case 'duration':
        return b.duration - a.duration
      case 'player':
        return a.player_name.localeCompare(b.player_name)
      case 'recent':
        return a.clip_id.localeCompare(b.clip_id) // Assuming clip_id has timestamp
      default:
        return 0
    }
  })

  if (clips.length === 0) {
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

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      className="bg-gray-900/50 border border-gray-800 rounded-lg backdrop-blur-sm overflow-hidden"
    >
      {/* Panel Header */}
      <div className="border-b border-gray-800 p-4">
        <div className="flex items-center justify-between mb-3">
          <div className="flex items-center space-x-3">
            <VideoCameraIcon className="w-5 h-5 text-red-500" />
            <h2 className="text-lg font-medium text-white font-military-display">
              {title}
            </h2>
            <span className="bg-red-600/20 text-red-400 text-xs px-2 py-1 rounded font-mono">
              {sortedClips.length} CLIPS
            </span>
          </div>
          
          <button
            onClick={() => setShowControls(!showControls)}
            className="text-gray-400 hover:text-white transition-colors"
          >
            <FunnelIcon className="w-4 h-4" />
          </button>
        </div>

        {/* Controls Panel */}
        <AnimatePresence>
          {showControls && (
            <motion.div
              initial={{ opacity: 0, height: 0 }}
              animate={{ opacity: 1, height: 'auto' }}
              exit={{ opacity: 0, height: 0 }}
              className="space-y-3"
            >
              {/* Search Bar */}
              <div className="relative">
                <MagnifyingGlassIcon className="absolute left-3 top-1/2 transform -translate-y-1/2 w-4 h-4 text-gray-500" />
                <input
                  type="text"
                  placeholder="Search clips..."
                  value={searchTerm}
                  onChange={(e) => setSearchTerm(e.target.value)}
                  className="w-full bg-gray-800/50 border border-gray-700 rounded pl-10 pr-4 py-2 text-sm text-white placeholder-gray-500 focus:border-gray-600 focus:outline-none font-military-chat"
                />
              </div>

              {/* Controls Row */}
              <div className="flex items-center justify-between space-x-4">
                {/* View Mode */}
                <div className="flex items-center space-x-2">
                  <span className="text-xs text-gray-400 font-mono">VIEW:</span>
                  <div className="flex border border-gray-700 rounded overflow-hidden">
                    <button
                      onClick={() => setViewMode('grid')}
                      className={`p-1.5 ${viewMode === 'grid' ? 'bg-gray-700 text-white' : 'text-gray-400 hover:text-white'}`}
                    >
                      <Squares2X2Icon className="w-4 h-4" />
                    </button>
                    <button
                      onClick={() => setViewMode('list')}
                      className={`p-1.5 border-l border-gray-700 ${viewMode === 'list' ? 'bg-gray-700 text-white' : 'text-gray-400 hover:text-white'}`}
                    >
                      <ListBulletIcon className="w-4 h-4" />
                    </button>
                  </div>
                </div>

                {/* Sort By */}
                <div className="flex items-center space-x-2">
                  <span className="text-xs text-gray-400 font-mono">SORT:</span>
                  <select
                    value={sortBy}
                    onChange={(e) => setSortBy(e.target.value as SortBy)}
                    className="bg-gray-800/50 border border-gray-700 rounded px-2 py-1 text-xs text-white font-mono focus:border-gray-600 focus:outline-none"
                  >
                    <option value="relevance">Relevance</option>
                    <option value="duration">Duration</option>
                    <option value="player">Player</option>
                    <option value="recent">Recent</option>
                  </select>
                </div>

                {/* Filter By */}
                <div className="flex items-center space-x-2">
                  <span className="text-xs text-gray-400 font-mono">FILTER:</span>
                  <select
                    value={filterBy}
                    onChange={(e) => setFilterBy(e.target.value as FilterBy)}
                    className="bg-gray-800/50 border border-gray-700 rounded px-2 py-1 text-xs text-white font-mono focus:border-gray-600 focus:outline-none"
                  >
                    <option value="all">All</option>
                    <option value="goals">Goals</option>
                    <option value="assists">Assists</option>
                    <option value="saves">Saves</option>
                    <option value="hits">Hits</option>
                    <option value="penalties">Penalties</option>
                  </select>
                </div>
              </div>
            </motion.div>
          )}
        </AnimatePresence>
      </div>

      {/* Clips Display */}
      <div className="p-4">
        {sortedClips.length === 0 ? (
          <div className="text-center py-8">
            <MagnifyingGlassIcon className="w-8 h-8 text-gray-600 mx-auto mb-2" />
            <p className="text-sm text-gray-400">
              No clips match your current filters
            </p>
          </div>
        ) : (
          <>
            {viewMode === 'grid' ? (
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                {sortedClips.map((clip, index) => (
                  <VideoClipCard
                    key={clip.clip_id}
                    clip={clip}
                    index={index}
                  />
                ))}
              </div>
            ) : (
              <div className="space-y-3">
                {sortedClips.map((clip, index) => (
                  <motion.div
                    key={clip.clip_id}
                    initial={{ opacity: 0, x: -20 }}
                    animate={{ opacity: 1, x: 0 }}
                    transition={{ delay: index * 0.05, duration: 0.2 }}
                    className="flex items-center space-x-3 bg-gray-800/30 border border-gray-700/50 rounded p-3 hover:bg-gray-800/50 transition-colors"
                  >
                    <div className="flex-shrink-0 w-16 h-12 bg-black rounded overflow-hidden">
                      <img 
                        src={clip.thumbnail_url} 
                        alt={clip.title}
                        className="w-full h-full object-cover"
                      />
                    </div>
                    <div className="flex-1 min-w-0">
                      <h4 className="text-sm font-medium text-white truncate">
                        {clip.title}
                      </h4>
                      <p className="text-xs text-gray-400 truncate">
                        {clip.player_name} • {clip.game_info} • {Math.round(clip.duration)}s
                      </p>
                    </div>
                    <div className="flex-shrink-0 text-right">
                      <span className="text-xs text-gray-500 font-mono">
                        {clip.event_type}
                      </span>
                    </div>
                  </motion.div>
                ))}
              </div>
            )}
          </>
        )}
      </div>
    </motion.div>
  )
}
