'use client';

import { useState, useEffect } from 'react';
import { Search, Bell, User, Moon, Sun } from 'lucide-react';

function getTimeBasedGreeting() {
  const hour = new Date().getHours();
  if (hour < 12) return 'Good morning';
  if (hour < 18) return 'Good afternoon';
  return 'Good evening';
}

export default function TopBar() {
  const [greeting, setGreeting] = useState('');
  const [time, setTime] = useState('');

  useEffect(() => {
    const updateTime = () => {
      setGreeting(getTimeBasedGreeting());
      setTime(new Date().toLocaleTimeString('en-US', {
        hour: '2-digit',
        minute: '2-digit'
      }));
    };

    updateTime();
    const interval = setInterval(updateTime, 60000); // Update every minute

    return () => clearInterval(interval);
  }, []);

  return (
    <header className="h-16 border-b border-border bg-surface-1/80 backdrop-blur-xl sticky top-0 z-40">
      <div className="h-full px-6 flex items-center justify-between">
        {/* Left: Greeting */}
        <div>
          <h2 className="text-lg font-display font-semibold">
            {greeting}, <span className="gradient-text">Admin</span>
          </h2>
          <p className="text-xs text-text-tertiary">{time}</p>
        </div>

        {/* Right: Actions */}
        <div className="flex items-center gap-3">
          {/* Search */}
          <button className="flex items-center gap-2 px-3 py-1.5 bg-surface-2 hover:bg-surface-3 rounded-lg transition-colors group">
            <Search className="w-4 h-4 text-text-tertiary group-hover:text-text-secondary" />
            <span className="text-sm text-text-tertiary">Search</span>
            <kbd className="px-1.5 py-0.5 text-xs bg-surface-3 rounded border border-border">
              ⌘K
            </kbd>
          </button>

          {/* Notifications */}
          <button className="relative p-2 hover:bg-surface-2 rounded-lg transition-colors">
            <Bell className="w-5 h-5 text-text-secondary" />
            <span className="absolute top-1 right-1 w-2 h-2 bg-error rounded-full" />
          </button>

          {/* Theme Toggle */}
          <button className="p-2 hover:bg-surface-2 rounded-lg transition-colors">
            <Moon className="w-5 h-5 text-text-secondary" />
          </button>

          {/* Profile */}
          <button className="flex items-center gap-2 px-3 py-1.5 hover:bg-surface-2 rounded-lg transition-colors">
            <div className="w-7 h-7 rounded-full bg-brand-gradient flex items-center justify-center">
              <User className="w-4 h-4 text-white" />
            </div>
            <span className="text-sm font-medium">Admin</span>
          </button>
        </div>
      </div>
    </header>
  );
}
