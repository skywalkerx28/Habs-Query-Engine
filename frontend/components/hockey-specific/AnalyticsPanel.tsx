'use client'

import React from 'react'
import { motion } from 'framer-motion'
import { 
  ChartBarIcon, 
  TableCellsIcon, 
  ArrowTrendingUpIcon,
  ArrowTrendingDownIcon 
} from '@heroicons/react/24/outline'

interface AnalyticsData {
  type: 'stat' | 'chart' | 'table'
  title: string
  data: any
}

interface AnalyticsPanelProps {
  analytics: AnalyticsData[]
}

export function AnalyticsPanel({ analytics }: AnalyticsPanelProps) {
  return (
    <div className="space-y-4">
      {analytics.map((item, index) => (
        <motion.div
          key={index}
          initial={{ opacity: 0, y: 10 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: index * 0.1, duration: 0.3 }}
          className="bg-gray-900/50 border border-gray-800 rounded-lg p-4 backdrop-blur-sm"
        >
          {/* Panel header */}
          <div className="flex items-center justify-between mb-3">
            <div className="flex items-center space-x-2">
              {item.type === 'stat' && <ChartBarIcon className="w-4 h-4 text-gray-400" />}
              {item.type === 'chart' && <ArrowTrendingUpIcon className="w-4 h-4 text-white" />}
              {item.type === 'table' && <TableCellsIcon className="w-4 h-4 text-gray-400" />}
              <h3 className="text-sm font-medium text-white">
                {item.title}
              </h3>
            </div>
            <span className="text-xs font-mono text-gray-400">
              LIVE DATA
            </span>
          </div>

          {/* Panel content based on type */}
          {item.type === 'stat' && (
            <StatCard data={item.data} />
          )}
          
          {item.type === 'chart' && (
            <ChartPreview data={item.data} />
          )}
          
          {item.type === 'table' && (
            <TablePreview data={item.data} />
          )}
        </motion.div>
      ))}
    </div>
  )
}

function StatCard({ data }: { data: any }) {
  return (
    <div className="grid grid-cols-3 gap-4">
      {Object.entries(data).map(([key, value], index) => (
        <div key={key} className="text-center">
          <div className="text-lg font-bold text-white font-mono">
            {value as string}
          </div>
          <div className="text-xs text-gray-400 uppercase tracking-wide">
            {key}
          </div>
        </div>
      ))}
    </div>
  )
}

function ChartPreview({ data }: { data: any }) {
  return (
    <div className="h-24 bg-gray-800/30 rounded border border-gray-800/50 flex items-center justify-center">
      <div className="text-center">
        <ArrowTrendingUpIcon className="w-8 h-8 text-white mx-auto mb-1" />
        <div className="text-xs text-gray-400">
          Chart visualization will render here
        </div>
      </div>
    </div>
  )
}

function TablePreview({ data }: { data: any }) {
  return (
    <div className="space-y-2">
      {/* Table header */}
      <div className="grid grid-cols-4 gap-2 pb-2 border-b border-gray-800/50">
        <div className="text-xs font-medium text-gray-400 uppercase">Player</div>
        <div className="text-xs font-medium text-gray-400 uppercase">Goals</div>
        <div className="text-xs font-medium text-gray-400 uppercase">Assists</div>
        <div className="text-xs font-medium text-gray-400 uppercase">Points</div>
      </div>
      
      {/* Sample rows */}
      {[1, 2, 3].map((row) => (
        <div key={row} className="grid grid-cols-4 gap-2 py-1">
          <div className="text-xs text-white font-mono">Player {row}</div>
          <div className="text-xs text-white font-mono">{10 + row}</div>
          <div className="text-xs text-white font-mono">{8 + row}</div>
          <div className="text-xs text-white font-mono">{18 + row * 2}</div>
        </div>
      ))}
    </div>
  )
}
