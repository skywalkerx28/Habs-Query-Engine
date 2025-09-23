'use client'

import { TrophyIcon } from '@heroicons/react/24/outline'
import { BasePage } from '../../components/layout/BasePage'
import { PlaceholderPage } from '../../components/layout/PlaceholderPage'

export default function GamesPage() {
  return (
    <BasePage loadingMessage="LOADING GAME ANALYSIS...">
      <PlaceholderPage
        title="GAME ANALYSIS MODULE"
        description="Deep dive into game-by-game performance metrics, tactical analysis, and strategic insights for team optimization."
        icon={TrophyIcon}
      />
    </BasePage>
  )
}
