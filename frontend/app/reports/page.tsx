'use client'

import { DocumentTextIcon } from '@heroicons/react/24/outline'
import { BasePage } from '../../components/layout/BasePage'
import { PlaceholderPage } from '../../components/layout/PlaceholderPage'

export default function ReportsPage() {
  return (
    <BasePage loadingMessage="LOADING REPORTS...">
      <PlaceholderPage
        title="INTELLIGENCE REPORTS MODULE"
        description="Automated report generation, executive summaries, and detailed performance breakdowns for coaching staff and management."
        icon={DocumentTextIcon}
      />
    </BasePage>
  )
}
