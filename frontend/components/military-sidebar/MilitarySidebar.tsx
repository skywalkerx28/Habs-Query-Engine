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
      {/* Mobile backdrop */}
      <AnimatePresence>
        {isOpen && (
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            className="fixed inset-0 bg-black/50 backdrop-blur-sm z-40 lg:hidden"
            onClick={onToggle}
          />
        )}
      </AnimatePresence>

      {/* Unified sidebar that expands/collapses */}
      <motion.aside
        initial={false}
        animate={{ width: isOpen ? 320 : 64 }}
        transition={{ type: "spring", damping: 30, stiffness: 300 }}
        className="fixed left-0 top-0 bottom-0 bg-gray-900 border-r border-gray-800 z-50 flex flex-col overflow-hidden"
      >
        {/* Sidebar header */}
        <div className="flex items-center justify-between h-[72px] px-3 border-b border-gray-800">
          <AnimatePresence mode="wait">
            {isOpen ? (
              <motion.div
                key="expanded-header"
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
                exit={{ opacity: 0 }}
                transition={{ duration: 0.2 }}
                className="flex items-center space-x-3 flex-1"
              >
                <div className="w-2 h-2 bg-red-600 rounded-full animate-pulse" />
                <h2 className="text-lg font-military-display text-white whitespace-nowrap">COMMAND CENTER</h2>
              </motion.div>
            ) : (
              <motion.div
                key="collapsed-header"
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
                exit={{ opacity: 0 }}
                transition={{ duration: 0.2 }}
                className="w-full flex justify-center"
              >
                <button
                  onClick={onToggle}
                  className="p-2 rounded-md text-gray-400 hover:text-white hover:bg-gray-800 transition-colors"
                >
                  <ChevronRightIcon className="w-5 h-5" />
                </button>
              </motion.div>
            )}
          </AnimatePresence>
          
          {isOpen && (
            <motion.button
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              exit={{ opacity: 0 }}
              onClick={onToggle}
              className="p-1.5 rounded-md text-gray-400 hover:text-white hover:bg-gray-800 transition-colors ml-auto"
            >
              <ChevronLeftIcon className="w-5 h-5" />
            </motion.button>
          )}
        </div>

        {/* Sidebar navigation */}
        <nav className="flex-1 overflow-y-auto py-6">
          {/* Main section */}
          <div className={clsx("mb-6", isOpen ? "px-3" : "px-2")}>
            <AnimatePresence mode="wait">
              {isOpen && (
                <motion.h3
                  initial={{ opacity: 0, height: 0 }}
                  animate={{ opacity: 1, height: "auto" }}
                  exit={{ opacity: 0, height: 0 }}
                  transition={{ duration: 0.2 }}
                  className="mb-3 px-3 text-xs font-military-display text-gray-500 overflow-hidden"
                >
                  MAIN OPERATIONS
                </motion.h3>
              )}
            </AnimatePresence>
            <div className="space-y-1">
              <UnifiedSidebarItem href="/" icon={HomeIcon} current isOpen={isOpen}>
                Dashboard
              </UnifiedSidebarItem>
              <UnifiedSidebarItem href="/analytics" icon={ChartBarIcon} isOpen={isOpen}>
                Analytics
              </UnifiedSidebarItem>
              <UnifiedSidebarItem href="/players" icon={UserGroupIcon} isOpen={isOpen}>
                Player Stats
              </UnifiedSidebarItem>
              <UnifiedSidebarItem href="/games" icon={TrophyIcon} isOpen={isOpen}>
                Game Analysis
              </UnifiedSidebarItem>
            </div>
          </div>

          {/* Divider */}
          <div className={clsx("my-4 border-t border-gray-800", isOpen ? "mx-3" : "mx-2")} />

          {/* Advanced section */}
          <div className={clsx("mb-6", isOpen ? "px-3" : "px-2")}>
            <AnimatePresence mode="wait">
              {isOpen && (
                <motion.h3
                  initial={{ opacity: 0, height: 0 }}
                  animate={{ opacity: 1, height: "auto" }}
                  exit={{ opacity: 0, height: 0 }}
                  transition={{ duration: 0.2 }}
                  className="mb-3 px-3 text-xs font-military-display text-gray-500 overflow-hidden"
                >
                  ADVANCED INTEL
                </motion.h3>
              )}
            </AnimatePresence>
            <div className="space-y-1">
              <UnifiedSidebarItem href="/predictions" icon={ClockIcon} isOpen={isOpen}>
                Predictions
              </UnifiedSidebarItem>
              <UnifiedSidebarItem href="/reports" icon={DocumentTextIcon} isOpen={isOpen}>
                Reports
              </UnifiedSidebarItem>
              <UnifiedSidebarItem href="/lab" icon={BeakerIcon} isOpen={isOpen}>
                Research Lab
              </UnifiedSidebarItem>
            </div>
          </div>

          {/* Divider */}
          <div className={clsx("my-4 border-t border-gray-800", isOpen ? "mx-3" : "mx-2")} />

          {/* System section */}
          <div className={clsx(isOpen ? "px-3" : "px-2")}>
            <AnimatePresence mode="wait">
              {isOpen && (
                <motion.h3
                  initial={{ opacity: 0, height: 0 }}
                  animate={{ opacity: 1, height: "auto" }}
                  exit={{ opacity: 0, height: 0 }}
                  transition={{ duration: 0.2 }}
                  className="mb-3 px-3 text-xs font-military-display text-gray-500 overflow-hidden"
                >
                  SYSTEM
                </motion.h3>
              )}
            </AnimatePresence>
            <div className="space-y-1">
              <UnifiedSidebarItem href="/settings" icon={CogIcon} isOpen={isOpen}>
                Settings
              </UnifiedSidebarItem>
              <button
                onClick={onLogout}
                className={clsx(
                  "group relative flex items-center w-full rounded-md transition-all",
                  isOpen 
                    ? "gap-3 px-3 py-2.5 text-sm font-military-chat text-gray-300 hover:text-white hover:bg-gray-800 text-left"
                    : "justify-center p-2 text-gray-500 hover:text-white hover:bg-gray-800"
                )}
              >
                <ArrowRightOnRectangleIcon className={clsx(
                  "flex-shrink-0",
                  isOpen ? "w-5 h-5 text-gray-500 group-hover:text-gray-300" : "w-5 h-5"
                )} />
                {isOpen && <span>Logout</span>}
                {!isOpen && (
                  <span className="absolute left-full ml-2 px-2 py-1 text-xs bg-gray-800 text-white rounded opacity-0 group-hover:opacity-100 transition-opacity whitespace-nowrap pointer-events-none z-50">
                    Logout
                  </span>
                )}
              </button>
            </div>
          </div>
        </nav>

        {/* User info section */}
        {userInfo && (
          <div className={clsx(
            "py-4 border-t border-gray-800 transition-all",
            isOpen ? "px-6" : "px-2"
          )}>
            <AnimatePresence mode="wait">
              {isOpen ? (
                <motion.div
                  key="expanded-user"
                  initial={{ opacity: 0 }}
                  animate={{ opacity: 1 }}
                  exit={{ opacity: 0 }}
                  transition={{ duration: 0.2 }}
                >
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
                </motion.div>
              ) : (
                <motion.div
                  key="collapsed-user"
                  initial={{ opacity: 0 }}
                  animate={{ opacity: 1 }}
                  exit={{ opacity: 0 }}
                  transition={{ duration: 0.2 }}
                  className="w-full flex justify-center"
                >
                  <div className="w-8 h-8 rounded-full bg-red-600 text-white flex items-center justify-center text-xs font-military-display">
                    {userInfo.name.split(' ').map(n => n[0]).join('')}
                  </div>
                </motion.div>
              )}
            </AnimatePresence>
          </div>
        )}
      </motion.aside>
    </>
  )
}

interface UnifiedSidebarItemProps {
  href: string
  icon: React.ComponentType<{ className?: string }>
  current?: boolean
  isOpen: boolean
  children: React.ReactNode
}

const UnifiedSidebarItem = forwardRef<HTMLAnchorElement, UnifiedSidebarItemProps>(
  function UnifiedSidebarItem({ href, icon: Icon, current = false, isOpen, children }, ref) {
    return (
      <a
        ref={ref}
        href={href}
        className={clsx(
          'group relative flex items-center rounded-md transition-all',
          isOpen
            ? clsx(
                'gap-3 px-3 py-2.5 text-sm font-military-chat',
                current
                  ? 'bg-red-600/20 text-white border-l-2 border-red-600 -ml-[2px] pl-[14px]'
                  : 'text-gray-300 hover:text-white hover:bg-gray-800'
              )
            : clsx(
                'justify-center p-2',
                current
                  ? 'bg-red-600/20 text-red-600'
                  : 'text-gray-500 hover:text-white hover:bg-gray-800'
              )
        )}
      >
        <Icon className={clsx(
          'flex-shrink-0 w-5 h-5',
          current 
            ? (isOpen ? 'text-red-600' : '') 
            : (isOpen ? 'text-gray-500 group-hover:text-gray-300' : '')
        )} />
        
        {isOpen ? (
          <motion.span
            initial={{ opacity: 0, width: 0 }}
            animate={{ opacity: 1, width: "auto" }}
            exit={{ opacity: 0, width: 0 }}
            transition={{ duration: 0.2 }}
            className="whitespace-nowrap overflow-hidden"
          >
            {children}
          </motion.span>
        ) : (
          <span className="absolute left-full ml-2 px-2 py-1 text-xs bg-gray-800 text-white rounded opacity-0 group-hover:opacity-100 transition-opacity whitespace-nowrap pointer-events-none z-50">
            {children}
          </span>
        )}
      </a>
    )
  }
)