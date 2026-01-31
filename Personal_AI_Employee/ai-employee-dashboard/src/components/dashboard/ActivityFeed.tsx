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

  useEffect(() => {
    // Simulate API call to fetch activities
    const fetchActivities = async () => {
      setLoading(true);

      // Simulate API delay
      await new Promise(resolve => setTimeout(resolve, 500));

      // Mock data - in a real app this would come from an API
      const mockActivities: ActivityItem[] = [
        {
          id: '1',
          title: 'Email processed',
          description: 'Processed marketing campaign email',
          time: new Date(Date.now() - 1000 * 60 * 5).toISOString(),
          type: 'email',
          icon: <Mail className="w-4 h-4 text-primary" />,
        },
        {
          id: '2',
          title: 'Plan created',
          description: 'Created Q1 marketing strategy plan',
          time: new Date(Date.now() - 1000 * 60 * 15).toISOString(),
          type: 'plan',
          icon: <FileText className="w-4 h-4 text-secondary" />,
        },
        {
          id: '3',
          title: 'Task completed',
          description: 'Updated customer database',
          time: new Date(Date.now() - 1000 * 60 * 30).toISOString(),
          type: 'task',
          icon: <CheckCircle className="w-4 h-4 text-accent" />,
        },
        {
          id: '4',
          title: 'Approval requested',
          description: 'New vendor contract pending approval',
          time: new Date(Date.now() - 1000 * 60 * 45).toISOString(),
          type: 'approval',
          icon: <Clock className="w-4 h-4 text-warning" />,
        },
        {
          id: '5',
          title: 'Email sent',
          description: 'Sent monthly newsletter',
          time: new Date(Date.now() - 1000 * 60 * 60).toISOString(),
          type: 'email',
          icon: <Mail className="w-4 h-4 text-primary" />,
        },
      ];

      setActivities(mockActivities);
      setLoading(false);
    };

    fetchActivities();

    // Simulate real-time updates
    const interval = setInterval(() => {
      if (activities.length > 0) {
        const newActivity: ActivityItem = {
          id: (parseInt(activities[0].id) + 1).toString(),
          title: 'New activity',
          description: 'A new task was completed',
          time: new Date().toISOString(),
          type: ['email', 'task', 'approval', 'plan'][Math.floor(Math.random() * 4)] as any,
          icon: getActivityIcon(['email', 'task', 'approval', 'plan'][Math.floor(Math.random() * 4)]),
        };

        setActivities(prev => [newActivity, ...prev.slice(0, 4)]);
      }
    }, 10000); // Update every 10 seconds

    return () => clearInterval(interval);
  }, [activities.length]);

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

      {activities.length === 0 && (
        <div className="text-center py-8 text-text-secondary">
          <p>No recent activity</p>
        </div>
      )}
    </div>
  );
};