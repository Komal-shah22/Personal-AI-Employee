'use client';

import { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { Mail, CheckCircle, Clock, FileText, Calendar } from 'lucide-react';
import { formatDistanceToNow } from 'date-fns';

interface ActivityItem {
  id: string;
  title: string;
  description: string;
  time: string;
  type: 'email' | 'task' | 'approval' | 'plan';
  icon: React.ReactNode;
}

const getActivityIcon = (type: string) => {
  switch (type) {
    case 'email':
      return <Mail className="w-4 h-4 text-primary" />;
    case 'task':
      return <CheckCircle className="w-4 h-4 text-accent" />;
    case 'approval':
      return <Clock className="w-4 h-4 text-warning" />;
    case 'plan':
      return <FileText className="w-4 h-4 text-secondary" />;
    default:
      return <Calendar className="w-4 h-4 text-text-secondary" />;
  }
};

const getActivityColor = (type: string) => {
  switch (type) {
    case 'email':
      return 'bg-primary/20';
    case 'task':
      return 'bg-accent/20';
    case 'approval':
      return 'bg-warning/20';
    case 'plan':
      return 'bg-secondary/20';
    default:
      return 'bg-text-secondary/20';
  }
};

export const ActivityFeed = () => {
  const [activities, setActivities] = useState<ActivityItem[]>([]);
  const [loading, setLoading] = useState(true);

  const fetchActivities = async () => {
    try {
      setLoading(true);

      // Fetch from the API
      const response = await fetch('/api/activity');
      if (!response.ok) throw new Error('Failed to fetch activities');

      const data = await response.json();
      setActivities(data.activities);
    } catch (error) {
      console.error('Error fetching activities:', error);
      // Fallback to empty array
      setActivities([]);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    // Fetch activities on mount
    fetchActivities();

    // Set up interval to fetch activities every 5 seconds for real-time updates
    const interval = setInterval(fetchActivities, 5000);

    // Clean up interval on unmount
    return () => clearInterval(interval);
  }, []);

  if (loading) {
    return (
      <div className="space-y-4">
        {[...Array(5)].map((_, i) => (
          <div key={i} className="flex items-start gap-3 p-3 rounded-lg bg-surface animate-pulse">
            <div className="w-8 h-8 rounded-full bg-border flex items-center justify-center"></div>
            <div className="flex-1">
              <div className="h-4 bg-border rounded w-3/4 mb-2"></div>
              <div className="h-3 bg-border rounded w-1/2"></div>
            </div>
          </div>
        ))}
      </div>
    );
  }

  return (
    <div className="space-y-4 max-h-96 overflow-y-auto">
      <AnimatePresence>
        {activities.map((activity) => (
          <motion.div
            key={activity.id}
            initial={{ opacity: 0, x: -20 }}
            animate={{ opacity: 1, x: 0 }}
            exit={{ opacity: 0, x: 20 }}
            transition={{ duration: 0.3 }}
            className="flex items-start gap-3 p-3 rounded-lg hover:bg-surface transition-colors"
          >
            <div className={`w-8 h-8 rounded-full ${getActivityColor(activity.type)} flex items-center justify-center`}>
              {getActivityIcon(activity.type)}
            </div>
            <div className="flex-1 min-w-0">
              <p className="font-medium truncate">{activity.title}</p>
              <p className="text-sm text-text-secondary truncate">{activity.description}</p>
            </div>
            <div className="text-xs text-text-tertiary whitespace-nowrap">
              {formatDistanceToNow(new Date(activity.time), { addSuffix: true })}
            </div>
          </motion.div>
        ))}
      </AnimatePresence>

      {activities?.length === 0 && (
        <div className="text-center py-8 text-text-secondary">
          <p>No recent activity</p>
        </div>
      )}
    </div>
  );
};