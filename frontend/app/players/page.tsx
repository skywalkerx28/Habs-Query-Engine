'use client'

import { UserGroupIcon } from '@heroicons/react/24/outline'
import { BasePage } from '../../components/layout/BasePage'
import { PlaceholderPage } from '../../components/layout/PlaceholderPage'

export default function PlayersPage() {
  return (
    <BasePage loadingMessage="LOADING PLAYER STATS...">
      <PlaceholderPage
        title="PLAYER STATISTICS MODULE"
        description="Comprehensive player performance analytics, individual metrics tracking, and comparative analysis tools will be available here."
        icon={UserGroupIcon}
      />
    </BasePage>
  )
}
