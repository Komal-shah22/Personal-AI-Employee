'use client';

import { motion } from 'framer-motion';

interface TierNavProps {
  activeTier: 'bronze' | 'silver' | 'gold' | 'platinum';
  onTierChange: (tier: 'bronze' | 'silver' | 'gold' | 'platinum') => void;
}

const tiers = [
  { id: 'bronze' as const, label: 'Bronze', color: 'from-amber-500 to-amber-700', icon: '🥉' },
  { id: 'silver' as const, label: 'Silver', color: 'from-gray-400 to-gray-600', icon: '🥈' },
  { id: 'gold' as const, label: 'Gold', color: 'from-yellow-400 to-yellow-600', icon: '🥇' },
  { id: 'platinum' as const, label: 'Platinum', color: 'from-blue-400 to-cyan-500', icon: '💎' },
];

export default function TierNav({ activeTier, onTierChange }: TierNavProps) {
  return (
    <div className="bg-white/5 backdrop-blur-lg border border-border rounded-xl p-2">
      <div className="flex flex-wrap justify-center gap-1">
        {tiers.map((tier) => (
          <motion.button
            key={tier.id}
            whileHover={{ scale: 1.02 }}
            whileTap={{ scale: 0.98 }}
            onClick={() => onTierChange(tier.id)}
            className={`px-4 py-3 rounded-lg font-semibold text-sm transition-all duration-200 flex items-center gap-2 min-w-[120px] ${
              activeTier === tier.id
                ? `bg-gradient-to-r ${tier.color} text-white shadow-lg`
                : 'text-muted hover:bg-white/10'
            }`}
          >
            <span>{tier.icon}</span>
            <span>{tier.label}</span>
          </motion.button>
        ))}
      </div>
    </div>
  );
}
