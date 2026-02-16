'use client'

import { useState } from 'react'
import Header from '@/components/Header'
import StatsStrip from '@/components/StatsStrip'
import ArchitectureDiagram from '@/components/ArchitectureDiagram'
import LiveStatus from '@/components/LiveStatus'
import ActivityFeed from '@/components/ActivityFeed'
import QuickActions from '@/components/QuickActions'
import ApprovalQueue from '@/components/ApprovalQueue'
import TierNav from '@/components/TierNav'
import AgentCard from '@/components/AgentCard'

type Tier = 'bronze' | 'silver' | 'gold' | 'platinum'

export default function Dashboard() {
  const [activeTier, setActiveTier] = useState<Tier>('bronze')

  return (
    <main className="container mx-auto px-4 py-8 max-w-7xl">
      {/* Header */}
      <Header />

      {/* Stats Strip */}
      <div className="mt-8">
        <StatsStrip />
      </div>

      {/* System Architecture */}
      <div className="mt-8">
        <ArchitectureDiagram />
      </div>

      {/* Live Control Panel */}
      <div className="mt-8 grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Live Status - Takes 2 columns */}
        <div className="lg:col-span-2">
          <LiveStatus />
        </div>

        {/* Activity Feed - Takes 1 column */}
        <div className="lg:col-span-1">
          <ActivityFeed />
        </div>
      </div>

      {/* Quick Actions & Approval Queue */}
      <div className="mt-8 grid grid-cols-1 lg:grid-cols-2 gap-6">
        <QuickActions />
        <ApprovalQueue />
      </div>

      {/* Tier Navigation */}
      <div className="mt-12">
        <TierNav activeTier={activeTier} onTierChange={setActiveTier} />
      </div>

      {/* Agent Cards by Tier */}
      <div className="mt-8">
        <AgentCard tier={activeTier} />
      </div>
    </main>
  )
}
