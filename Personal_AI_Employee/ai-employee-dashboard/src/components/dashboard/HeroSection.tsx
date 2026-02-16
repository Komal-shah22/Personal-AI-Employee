'use client';

import { motion } from 'framer-motion';
import { Activity, Clock, CheckCircle, AlertCircle, Loader2 } from 'lucide-react';
import { formatDistanceToNow } from 'date-fns';
import { useEffect, useState } from 'react';

interface Stats {
  needsAction: number;
  inProgress: number;
  doneToday: number;
  pendingApproval: number;
}

export function HeroSection() {
  const [isOnline, setIsOnline] = useState(true);
  const [lastSync, setLastSync] = useState(new Date());
  const [stats, setStats] = useState<Stats>({
    needsAction: 0,
    inProgress: 0,
    doneToday: 0,
    pendingApproval: 0,
  });

  useEffect(() => {
    const fetchStats = async () => {
      try {
        const res = await fetch('/api/stats');
        const data = await res.json();
        setStats(data);
        setLastSync(new Date());
      } catch (error) {
        console.error('Failed to fetch stats:', error);
      }
    };

    fetchStats();
    const interval = setInterval(fetchStats, 5000);
    return () => clearInterval(interval);
  }, []);

  const statCards = [
    {
      label: 'Needs Action',
      value: stats.needsAction,
      icon: AlertCircle,
      color: 'text-warning',
      bgColor: 'bg-warning/10',
      borderColor: 'border-warning/20',
      urgent: stats.needsAction > 5,
    },
    {
      label: 'In Progress',
      value: stats.inProgress,
      icon: Loader2,
      color: 'text-primary',
      bgColor: 'bg-primary/10',
      borderColor: 'border-primary/20',
      spinning: true,
    },
    {
      label: 'Done Today',
      value: stats.doneToday,
      icon: CheckCircle,
      color: 'text-success',
      bgColor: 'bg-success/10',
      borderColor: 'border-success/20',
    },
    {
      label: 'Pending Approval',
      value: stats.pendingApproval,
      icon: Clock,
      color: 'text-secondary',
      bgColor: 'bg-secondary/10',
      borderColor: 'border-secondary/20',
    },
  ];

  return (
    <div className="space-y-6">
      {/* Status Badge and Time */}
      <motion.div
        initial={{ opacity: 0, y: -20 }}
        animate={{ opacity: 1, y: 0 }}
        className="flex items-center justify-between"
      >
        <div className="flex items-center gap-4">
          <div className="relative">
            <div
              className={`px-6 py-3 rounded-full border-2 ${
                isOnline
                  ? 'bg-success/10 border-success/30 text-success'
                  : 'bg-danger/10 border-danger/30 text-danger'
              } font-semibold text-lg flex items-center gap-3`}
            >
              <div className="relative">
                <Activity className="w-5 h-5" />
                {isOnline && (
                  <span className="absolute -top-1 -right-1 w-3 h-3 bg-success rounded-full animate-pulse-slow" />
                )}
              </div>
              AI Employee {isOnline ? 'Online' : 'Offline'}
            </div>
            {isOnline && (
              <div className="absolute inset-0 rounded-full bg-success/20 blur-xl animate-pulse-slow" />
            )}
          </div>
          <div className="text-text-secondary text-sm">
            <div className="font-mono">{new Date().toLocaleTimeString()}</div>
            <div className="text-xs">
              Last sync: {formatDistanceToNow(lastSync, { addSuffix: true })}
            </div>
          </div>
        </div>
      </motion.div>

      {/* Quick Stats Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
        {statCards.map((stat, index) => (
          <motion.div
            key={stat.label}
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: index * 0.1 }}
            whileHover={{ scale: 1.02, y: -2 }}
            className={`relative p-6 rounded-xl border ${stat.borderColor} ${stat.bgColor} backdrop-blur-sm transition-all duration-300 hover:shadow-lg cursor-pointer group`}
          >
            <div className="flex items-start justify-between">
              <div>
                <p className="text-text-secondary text-sm font-medium mb-2">
                  {stat.label}
                </p>
                <p className="text-3xl font-bold text-text-primary">
                  {stat.value}
                </p>
              </div>
              <div
                className={`p-3 rounded-lg ${stat.bgColor} ${stat.color} group-hover:scale-110 transition-transform`}
              >
                <stat.icon
                  className={`w-6 h-6 ${stat.spinning ? 'animate-spin-slow' : ''}`}
                />
              </div>
            </div>
            {stat.urgent && (
              <div className="absolute top-2 right-2">
                <span className="px-2 py-1 text-xs font-bold bg-danger text-white rounded-full animate-pulse">
                  URGENT
                </span>
              </div>
            )}
          </motion.div>
        ))}
      </div>
    </div>
  );
}
