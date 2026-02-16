'use client';

import { motion } from 'framer-motion';

export default function Header() {
  return (
    <div className="text-center space-y-4">
      {/* Badge */}
      <motion.div
        initial={{ opacity: 0, y: -10 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.3 }}
        className="flex justify-center"
      >
        <span className="badge-hackathon">
          🤖 HACKATHON 0 - AGENT REFERENCE
        </span>
      </motion.div>

      {/* Main Title */}
      <motion.h1
        initial={{ opacity: 0, scale: 0.95 }}
        animate={{ opacity: 1, scale: 1 }}
        transition={{ duration: 0.4, delay: 0.1 }}
        className="font-syne font-extrabold text-5xl md:text-7xl gradient-text leading-tight"
      >
        Personal AI Employee
      </motion.h1>

      {/* Subtitle */}
      <motion.p
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ duration: 0.4, delay: 0.2 }}
        className="text-muted text-base md:text-lg"
      >
        Current Tier: <span className="text-accent font-semibold">Bronze → Silver (In Progress)</span>
      </motion.p>
    </div>
  );
}
