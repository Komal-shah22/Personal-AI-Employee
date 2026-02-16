'use client';

import { useState, useEffect, useRef } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { formatDistanceToNow } from 'date-fns';

interface Activity {
  id: string;
  timestamp: string;
  agent: string;
  agentIcon: string;
  action: string;
  status: 'success' | 'pending' | 'error';
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
      const res = await fetch('/api/activity');
      const data = await res.json();
      setActivities(data.activities || []);
    } catch (error) {
      console.error('Failed to fetch activities:', error);
    } finally {
      setLoading(false);
    }
  };

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'success':
        return 'text-accent3 bg-accent3/10';
      case 'pending':
        return 'text-warn bg-warn/10';
      case 'error':
        return 'text-danger bg-danger/10';
      default:
        return 'text-muted bg-muted/10';
    }
  };

  if (loading) {
    return (
      <div className="card p-6">
        <div className="shimmer h-64 rounded-lg"></div>
      </div>
    );
  }

  return (
    <div className="card p-6 h-full">
      <h2 className="font-syne font-bold text-xl text-accent mb-6 flex items-center gap-2">
        <span>📊</span>
        Recent Activity
      </h2>

      <div
        ref={scrollRef}
        className="space-y-3 max-h-[400px] overflow-y-auto pr-2"
      >
        <AnimatePresence>
          {activities.map((activity, index) => (
            <motion.div
              key={activity.id}
              initial={{ opacity: 0, x: 20 }}
              animate={{ opacity: 1, x: 0 }}
              exit={{ opacity: 0, x: -20 }}
              transition={{ duration: 0.3, delay: index * 0.05 }}
              className="bg-surface2 border border-border rounded-lg p-3"
            >
              <div className="flex items-start gap-3">
                <div className="text-xl">{activity.agentIcon}</div>
                <div className="flex-1 min-w-0">
                  <div className="flex items-center gap-2 mb-1">
                    <span className="font-semibold text-sm">{activity.agent}</span>
                    <span
                      className={`text-[10px] px-2 py-0.5 rounded-full uppercase font-semibold ${getStatusColor(
                        activity.status
                      )}`}
                    >
                      {activity.status}
                    </span>
                  </div>
                  <p className="text-xs text-muted mb-1">{activity.action}</p>
                  <p className="text-[10px] text-muted">
                    {formatDistanceToNow(new Date(activity.timestamp), {
                      addSuffix: true,
                    })}
                  </p>
                </div>
              </div>
            </motion.div>
          ))}
        </AnimatePresence>

        {activities.length === 0 && (
          <div className="text-center py-8 text-muted">
            <p className="text-sm">No recent activity</p>
          </div>
        )}
      </div>
    </div>
  );
}
