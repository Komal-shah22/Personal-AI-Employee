'use client';

import { motion } from 'framer-motion';

const stats = [
  { label: 'Bronze Agents', value: 5, color: 'text-bronze' },
  { label: 'Silver Agents', value: 4, color: 'text-silver' },
  { label: 'Gold Agents', value: 5, color: 'text-gold' },
  { label: 'Platinum Agents', value: 3, color: 'text-platinum' },
  { label: 'Total Agents', value: 17, color: 'text-accent' },
];

export default function StatsStrip() {
  return (
    <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-5 gap-4">
      {stats.map((stat, index) => (
        <motion.div
          key={stat.label}
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.3, delay: index * 0.05 }}
          whileHover={{ scale: 1.02, y: -2 }}
          className="stat-card"
        >
          <div className="text-center">
            <div className={`font-syne font-extrabold text-4xl mb-2 ${stat.color}`}>
              {stat.value}
            </div>
            <div className="text-muted text-[11px] uppercase tracking-wider font-medium">
              {stat.label}
            </div>
          </div>
        </motion.div>
      ))}
    </div>
  );
}
