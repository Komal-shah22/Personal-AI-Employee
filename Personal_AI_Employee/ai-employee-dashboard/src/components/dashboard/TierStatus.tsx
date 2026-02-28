'use client';

import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import {
  Medal,
  BadgeCheck,
  Star,
  Crown,
  Target,
  TrendingUp,
  CheckCircle,
  BarChart3
} from 'lucide-react';

interface TierStatusProps {
  currentTier: 'bronze' | 'silver' | 'gold' | 'platinum';
}

export default function TierStatus({ currentTier }: TierStatusProps) {
  const tierInfo = {
    bronze: {
      name: 'Bronze Tier',
      color: 'from-amber-600 to-amber-800',
      icon: <Medal className="w-6 h-6 text-amber-500" />,
      features: [
        'Basic automation',
        'Email & WhatsApp monitoring',
        'Simple task processing',
        'Basic file operations'
      ],
      progress: 25,
      nextTier: 'silver'
    },
    silver: {
      name: 'Silver Tier',
      color: 'from-gray-400 to-gray-600',
      icon: <Medal className="w-6 h-6 text-gray-400" />,
      features: [
        'Advanced automation',
        'Social media posting',
        'Multi-platform monitoring',
        'Task planning capabilities',
        'Basic MCP integration'
      ],
      progress: 50,
      nextTier: 'gold'
    },
    gold: {
      name: 'Gold Tier',
      color: 'from-yellow-400 to-yellow-600',
      icon: <Medal className="w-6 h-6 text-yellow-400" />,
      features: [
        'Full cross-domain integration',
        'Odoo accounting system',
        'Multi-platform social media',
        'Advanced error recovery',
        'CEO briefing automation',
        'Ralph Wiggum loops'
      ],
      progress: 75,
      nextTier: 'platinum'
    },
    platinum: {
      name: 'Platinum Tier',
      color: 'from-blue-400 to-cyan-500',
      icon: <Crown className="w-6 h-6 text-blue-400" />,
      features: [
        '24/7 cloud operations',
        'Work-zone specialization',
        'Vault sync infrastructure',
        'Multi-agent coordination',
        'Advanced security protocols',
        'Production-ready systems'
      ],
      progress: 100,
      nextTier: null
    }
  };

  const current = tierInfo[currentTier];
  const nextTier = currentTier !== 'platinum' ? tierInfo[current.nextTier as keyof typeof tierInfo] : null;

  return (
    <Card className="glass-card">
      <CardHeader>
        <CardTitle className="flex items-center gap-3">
          <div className={`p-2 rounded-lg bg-gradient-to-r ${current.color} bg-opacity-10`}>
            {current.icon}
          </div>
          <div>
            <div className="flex items-center gap-2">
              <span className="text-lg font-bold">{current.name}</span>
              <Badge className={`bg-gradient-to-r ${current.color}`}>
                {currentTier.toUpperCase()}
              </Badge>
            </div>
            <p className="text-sm text-muted">AI Employee Status</p>
          </div>
        </CardTitle>
      </CardHeader>
      <CardContent>
        <div className="mb-4">
          <div className="flex justify-between text-sm mb-1">
            <span>Progress</span>
            <span>{current.progress}%</span>
          </div>
          <div className="w-full bg-gray-200 rounded-full h-2">
            <div
              className={`h-2 rounded-full bg-gradient-to-r ${current.color}`}
              style={{ width: `${current.progress}%` }}
            ></div>
          </div>
        </div>

        <div className="mb-4">
          <h4 className="font-medium mb-2 flex items-center gap-2">
            <Target className="w-4 h-4" />
            Achievements
          </h4>
          <div className="space-y-2">
            {current.features.map((feature, index) => (
              <div key={index} className="flex items-center gap-2 text-sm">
                <CheckCircle className="w-4 h-4 text-green-500" />
                <span>{feature}</span>
              </div>
            ))}
          </div>
        </div>

        {nextTier && (
          <div>
            <h4 className="font-medium mb-2 flex items-center gap-2">
              <TrendingUp className="w-4 h-4" />
              Next: {nextTier.name}
            </h4>
            <div className="text-xs text-muted space-y-1">
              {nextTier.features.slice(0, 3).map((feature, index) => (
                <div key={index} className="flex items-center gap-1">
                  <div className="w-1 h-1 rounded-full bg-gray-400"></div>
                  <span>{feature}</span>
                </div>
              ))}
            </div>
          </div>
        )}
      </CardContent>
    </Card>
  );
}