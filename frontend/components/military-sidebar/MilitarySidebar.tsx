'use client'

import * as Headless from '@headlessui/react'
import clsx from 'clsx'
import { motion, AnimatePresence } from 'framer-motion'
import React, { forwardRef } from 'react'
import { 
  ChartBarIcon, 
  UserGroupIcon, 
  TrophyIcon,
  ClockIcon,
  CogIcon,
  ArrowRightOnRectangleIcon,
  ChevronLeftIcon,
  ChevronRightIcon,
  HomeIcon,
  DocumentTextIcon,
  BeakerIcon
} from '@heroicons/react/24/outline'

interface SidebarProps {
  isOpen: boolean
  onToggle: () => void
  userInfo?: {
    username: string
    name: string
    role: string
    email: string
    team_access: string[]
  }
  onLogout?: () => void
}

export function MilitarySidebar({ isOpen, onToggle, userInfo, onLogout }: SidebarProps) {
  return (
    <>
      {/* Sidebar */}
      <AnimatePresence mode="wait">
        {isOpen && (
          <>
            {/* Mobile backdrop */}
            <motion.div
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              exit={{ opacity: 0 }}
              className="fixed inset-0 bg-black/50 backdrop-blur-sm z-40 lg:hidden"
              onClick={onToggle}
            />
            
            {/* Sidebar panel */}
            <motion.aside
              initial={{ x: -320 }}
              animate={{ x: 0 }}
              exit={{ x: -320 }}
              transition={{ type: "spring", damping: 30, stiffness: 300 }}
              className="fixed left-0 top-0 bottom-0 w-80 bg-gray-900 border-r border-gray-800 z-50 flex flex-col"
            >
              {/* Sidebar header */}
              <div className="flex items-center justify-between px-6 py-6 border-b border-gray-800">
                <div className="flex items-center space-x-3">
                  <div className="w-2 h-2 bg-red-600 rounded-full animate-pulse" />
                  <h2 className="text-lg font-military-display text-white">COMMAND CENTER</h2>
                </div>
                <button
                  onClick={onToggle}
                  className="p-1.5 rounded-md text-gray-400 hover:text-white hover:bg-gray-800 transition-colors"
                >
                  <ChevronLeftIcon className="w-5 h-5" />
                </button>
              </div>

              {/* Sidebar navigation */}
              <nav className="flex-1 overflow-y-auto py-6">
                {/* Main section */}
                <div className="px-3 mb-6">
                  <h3 className="mb-3 px-3 text-xs font-military-display text-gray-500">
                    MAIN OPERATIONS
                  </h3>
                  <div className="space-y-1">
                    <SidebarItem href="/" icon={HomeIcon} current>
                      Dashboard
                    </SidebarItem>
                    <SidebarItem href="/analytics" icon={ChartBarIcon}>
                      Analytics
                    </SidebarItem>
                    <SidebarItem href="/players" icon={UserGroupIcon}>
                      Player Stats
                    </SidebarItem>
                    <SidebarItem href="/games" icon={TrophyIcon}>
                      Game Analysis
                    </SidebarItem>
                  </div>
                </div>

                {/* Advanced section */}
                <div className="px-3 mb-6">
                  <h3 className="mb-3 px-3 text-xs font-military-display text-gray-500">
                    ADVANCED INTEL
                  </h3>
                  <div className="space-y-1">
                    <SidebarItem href="/predictions" icon={ClockIcon}>
                      Predictions
                    </SidebarItem>
                    <SidebarItem href="/reports" icon={DocumentTextIcon}>
                      Reports
                    </SidebarItem>
                    <SidebarItem href="/lab" icon={BeakerIcon}>
                      Research Lab
                    </SidebarItem>
                  </div>
                </div>

                {/* System section */}
                <div className="px-3">
                  <h3 className="mb-3 px-3 text-xs font-military-display text-gray-500">
                    SYSTEM
                  </h3>
                  <div className="space-y-1">
                    <SidebarItem href="/settings" icon={CogIcon}>
                      Settings
                    </SidebarItem>
                    <button
                      onClick={onLogout}
                      className="group flex items-center gap-3 rounded-lg px-3 py-2.5 text-sm font-military-chat transition-all text-gray-300 hover:text-white hover:bg-gray-800 w-full text-left"
                    >
                      <ArrowRightOnRectangleIcon className="w-5 h-5 flex-shrink-0 text-gray-500 group-hover:text-gray-300" />
                      <span>Logout</span>
                    </button>
                  </div>
                </div>
              </nav>

              {/* User info section */}
              {userInfo && (
                <div className="px-6 py-4 border-t border-gray-800">
                  <div className="flex items-center space-x-3 mb-3">
                    <div className="w-8 h-8 rounded-full bg-red-600 text-white flex items-center justify-center text-sm font-military-display">
                      {userInfo.name.split(' ').map(n => n[0]).join('')}
                    </div>
                    <div className="flex-1 min-w-0">
                      <p className="text-sm font-military-chat text-white truncate">
                        {userInfo.name}
                      </p>
                      <p className="text-xs font-military-display text-red-600 uppercase">
                        {userInfo.role}
                      </p>
                    </div>
                  </div>
                  
                  {/* System info */}
                  <div className="flex items-center justify-between text-xs text-gray-500 pt-3 border-t border-gray-800">
                    <span className="font-military-display">HEARTBEAT ENGINE</span>
                    <span className="font-military-display">V2.1</span>
                  </div>
                </div>
              )}
            </motion.aside>
          </>
        )}
      </AnimatePresence>

      {/* Toggle button when sidebar is closed */}
      <AnimatePresence>
        {!isOpen && (
          <motion.button
            initial={{ opacity: 0, x: -10 }}
            animate={{ opacity: 1, x: 0 }}
            exit={{ opacity: 0, x: -10 }}
            onClick={onToggle}
            className="fixed left-4 top-6 z-40 p-2 rounded-md bg-gray-900 border border-gray-800 text-gray-400 hover:text-white hover:bg-gray-800 transition-colors"
          >
            <ChevronRightIcon className="w-5 h-5" />
          </motion.button>
        )}
      </AnimatePresence>
    </>
  )
}

interface SidebarItemProps {
  href: string
  icon: React.ComponentType<{ className?: string }>
  current?: boolean
  children: React.ReactNode
}

const SidebarItem = forwardRef<HTMLAnchorElement, SidebarItemProps>(
  function SidebarItem({ href, icon: Icon, current = false, children }, ref) {
    return (
      <a
        ref={ref}
        href={href}
        className={clsx(
          'group flex items-center gap-3 rounded-lg px-3 py-2.5 text-sm font-military-chat transition-all',
          current
            ? 'bg-red-600/20 text-white border-l-2 border-red-600 -ml-[2px] pl-[14px]'
            : 'text-gray-300 hover:text-white hover:bg-gray-800'
        )}
      >
        <Icon className={clsx(
          'w-5 h-5 flex-shrink-0',
          current ? 'text-red-600' : 'text-gray-500 group-hover:text-gray-300'
        )} />
        <span>{children}</span>
      </a>
    )
  }
)
