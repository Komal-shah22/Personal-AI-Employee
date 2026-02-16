'use client';

import { motion } from 'framer-motion';

interface TierNavProps {
  activeTier: 'bronze' | 'silver' | 'gold' | 'platinum';
  onTierChange: (tier: 'bronze' | 'silver' | 'gold' | 'platinum') => void;
}

const tiers = [
  { id: 'bronze' as const, label: '🥉 Bronze', color: 'bronze' },
  { id: 'silver' as const, label: '🥈 Silver (Missing Pieces)', color: 'silver' },
  { id: 'gold' as const, label: '🥇 Gold', color: 'gold' },
  { id: 'platinum' as const, label: '💎 Platinum', color: 'platinum' },
];

export default function TierNav({ activeTier, onTierChange }: TierNavProps) {
  return (
    <div className="flex flex-wrap gap-3 justify-center">
      {tiers.map((tier) => (
        <motion.button
          key={tier.id}
          whileHover={{ scale: 1.05 }}
          whileTap={{ scale: 0.95 }}
          onClick={() => onTierChange(tier.id)}
          className={`px-6 py-3 rounded-full font-semibold text-sm transition-all duration-200 ${
            activeTier === tier.id
              ? `bg-${tier.color} text-black border-2 border-${tier.color}`
              : 'bg-transparent text-muted border-2 border-border hover:border-accent'
          }`}
        >
          {tier.label}
        </motion.button>
      ))}
    </div>
  );
}
