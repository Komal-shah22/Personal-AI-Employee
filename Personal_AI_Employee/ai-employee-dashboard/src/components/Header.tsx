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

      {/* Professional Subtitle */}
      <motion.p
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ duration: 0.4, delay: 0.2 }}
        className="text-muted text-base md:text-lg"
      >
        <span className="text-accent font-semibold">Personal AI Employee</span> •
        <span className="ml-2 px-2 py-1 bg-gradient-to-r from-yellow-500/20 to-yellow-600/20 text-yellow-400 rounded-full text-sm font-medium">
          Gold Tier - Social Media Automation
        </span>
      </motion.p>

      {/* Professional Status Indicators */}
      <motion.div
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ duration: 0.4, delay: 0.3 }}
        className="flex flex-wrap justify-center gap-6 mt-4"
      >
        <div className="flex items-center gap-2 text-sm">
          <div className="w-2 h-2 rounded-full bg-green-500 animate-pulse"></div>
          <span className="text-green-300">System: Operational</span>
        </div>
        <div className="flex items-center gap-2 text-sm">
          <div className="w-2 h-2 rounded-full bg-green-500 animate-pulse"></div>
          <span className="text-green-300">Social Media: Active</span>
        </div>
        <div className="flex items-center gap-2 text-sm">
          <div className="w-2 h-2 rounded-full bg-green-500 animate-pulse"></div>
          <span className="text-green-300">Watchers: Running</span>
        </div>
      </motion.div>
    </div>
  );
}
