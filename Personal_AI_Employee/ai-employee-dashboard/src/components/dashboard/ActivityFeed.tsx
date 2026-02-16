'use client';

import { useState, useEffect, useRef } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { formatDistanceToNow } from 'date-fns';
import { CheckCircle, Clock, XCircle, AlertCircle } from 'lucide-react';

interface Activity {
  id: string;
  timestamp: string;
  agent: string;
  agentIcon: string;
  action: string;
  status: 'success' | 'pending' | 'error' | 'info';
  details?: string;
}

export default function ActivityFeed() {
  const [activities, setActivities] = useState<Activity[]>([]);
  const [loading, setLoading] = useState(true);
  const scrollRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    fetchActivities();
    const interval = setInterval(fetchActivities, 5000);
    return () => clearInterval(interval);
  }, []);

  useEffect(() => {
    if (scrollRef.current) {
      scrollRef.current.scrollTop = scrollRef.current.scrollHeight;
    }
  }, [activities]);

  const fetchActivities = async () => {
    try {
      const res = await fetch('/api/activity/stream');
      const data = await res.json();
      setActivities(data.activities || []);
    } catch (error) {
      console.error('Failed to fetch activities:', error);
    } finally {
      setLoading(false);
    }
  };

  const getStatusIcon = (status: string) => {
    switch (status) {
      case 'success':
        return <CheckCircle className="w-4 h-4 text-success" />;
      case 'pending':
        return <Clock className="w-4 h-4 text-warning" />;
      case 'error':
        return <XCircle className="w-4 h-4 text-error" />;
      case 'info':
        return <AlertCircle className="w-4 h-4 text-info" />;
      default:
        return null;
    }
  };

  const getStatusBadge = (status: string) => {
    const classes = {
      success: 'badge-success',
      pending: 'badge-warning',
      error: 'badge-error',
      info: 'badge-info',
    };
    return classes[status as keyof typeof classes] || 'badge-info';
  };

  if (loading) {
    return (
      <div className="card p-6 h-[500px]">
        <div className="skeleton h-full" />
      </div>
    );
  }

  return (
    <div className="card p-6 h-[500px] flex flex-col">
      {/* Header */}
      <div className="flex items-center justify-between mb-4">
        <h2 className="text-lg font-display font-semibold">Real-time Activity</h2>
        <div className="flex items-center gap-2">
          <div className="w-2 h-2 rounded-full bg-success animate-scale-pulse" />
          <span className="text-xs text-text-tertiary">Live</span>
        </div>
      </div>

      {/* Activity Stream */}
      <div
        ref={scrollRef}
        className="flex-1 overflow-y-auto custom-scrollbar space-y-3"
      >
        <AnimatePresence>
          {activities.map((activity, index) => (
            <motion.div
              key={activity.id}
              initial={{ opacity: 0, x: -20 }}
              animate={{ opacity: 1, x: 0 }}
              exit={{ opacity: 0, x: 20 }}
              transition={{ duration: 0.3, delay: index * 0.05 }}
              className="activity-item"
            >
              {/* Timeline Connector */}
              <div className="flex flex-col items-center">
                <div className="w-8 h-8 rounded-full bg-surface-2 flex items-center justify-center text-lg flex-shrink-0">
                  {activity.agentIcon}
                </div>
                {index < activities.length - 1 && (
                  <div className="w-px h-full bg-border-subtle mt-2" />
                )}
              </div>

              {/* Content */}
              <div className="flex-1 min-w-0">
                <div className="flex items-start justify-between gap-2 mb-1">
                  <div className="flex items-center gap-2">
                    <span className="font-semibold text-sm">{activity.agent}</span>
                    <span className={`badge ${getStatusBadge(activity.status)}`}>
                      {activity.status}
                    </span>
                  </div>
                  <span className="text-xs text-text-tertiary whitespace-nowrap">
                    {formatDistanceToNow(new Date(activity.timestamp), {
                      addSuffix: true,
                    })}
                  </span>
                </div>
                <p className="text-sm text-text-secondary">{activity.action}</p>
                {activity.details && (
                  <p className="text-xs text-text-tertiary mt-1 font-mono">
                    {activity.details}
                  </p>
                )}
              </div>

              {/* Status Icon */}
              <div className="flex-shrink-0">{getStatusIcon(activity.status)}</div>
            </motion.div>
          ))}
        </AnimatePresence>

        {activities.length === 0 && (
          <div className="flex items-center justify-center h-full text-text-tertiary">
            <p className="text-sm">No recent activity</p>
          </div>
        )}
      </div>
    </div>
  );
}
