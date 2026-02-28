'use client';

import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { TrendingUp, TrendingDown, Clock, Play, CheckCircle2, BarChart3 } from 'lucide-react';
import { motion } from 'framer-motion';
import { useState, useEffect } from 'react';
import { Badge } from '@/components/ui/badge';

interface StatCardProps {
  title: string;
  value: number;
  change: number;
  changeType: 'positive' | 'negative';
  icon: React.ReactNode;
  trendData: number[];
}

const StatCard = ({ title, value, change, changeType, icon, trendData }: StatCardProps) => {
  const IconComponent = icon;
  const TrendIcon = changeType === 'positive' ? TrendingUp : TrendingDown;
  const trendColor = changeType === 'positive' ? 'text-green-500' : 'text-red-500';

  return (
    <motion.div
      initial={{ opacity: 0, scale: 0.9 }}
      animate={{ opacity: 1, scale: 1 }}
      transition={{ duration: 0.3 }}
    >
      <Card className="glass-card hover:glow-on-hover transition-all duration-300 h-full">
        <CardHeader className="flex flex-row items-center justify-between pb-2">
          <CardTitle className="text-sm font-medium text-text-secondary">{title}</CardTitle>
          <div className="p-2 rounded-lg bg-primary/10 text-primary">
            {IconComponent}
          </div>
        </CardHeader>
        <CardContent>
          <div className="text-2xl font-bold">{value.toLocaleString()}</div>
          <div className="flex items-center gap-1 mt-2">
            <TrendIcon className={`w-4 h-4 ${trendColor}`} />
            <span className={`text-sm ${trendColor}`}>
              {Math.abs(change)}% vs last week
            </span>
          </div>
          {/* Mini chart visualization */}
          <div className="mt-3 h-8 flex items-end gap-1">
            {trendData.map((point, index) => (
              <div
                key={index}
                className="flex-1 bg-primary/30 rounded-t-sm min-h-[2px]"
                style={{ height: `${(point / Math.max(...trendData)) * 100}%` }}
              />
            ))}
          </div>
        </CardContent>
      </Card>
    </motion.div>
  );
};

export const StatsCards = () => {
  const [stats, setStats] = useState<StatCardProps[]>([
    { title: 'Pending Tasks', value: 0, change: 0, changeType: 'positive', icon: <Clock className="w-5 h-5" />, trendData: [65, 59, 80, 81, 56, 55, 40] },
    { title: 'In Progress', value: 0, change: 0, changeType: 'positive', icon: <Play className="w-5 h-5" />, trendData: [28, 48, 40, 19, 86, 27, 90] },
    { title: 'Completed', value: 0, change: 0, changeType: 'positive', icon: <CheckCircle2 className="w-5 h-5" />, trendData: [12, 19, 3, 5, 2, 3, 20] },
    { title: 'Total Tasks', value: 0, change: 0, changeType: 'positive', icon: <BarChart3 className="w-5 h-5" />, trendData: [45, 55, 48, 52, 60, 58, 65] },
    { title: 'Instagram Followers', value: 0, change: 0, changeType: 'positive', icon: <div className="w-5 h-5 bg-gradient-to-r from-purple-500 to-pink-500 rounded-sm"></div>, trendData: [45, 52, 48, 61, 55, 67, 72] },
    { title: 'LinkedIn Followers', value: 0, change: 0, changeType: 'positive', icon: <div className="w-5 h-5 bg-blue-700 rounded-sm"></div>, trendData: [32, 38, 45, 42, 50, 55, 62] },
    { title: 'Social Posts', value: 0, change: 0, changeType: 'positive', icon: <div className="w-5 h-5 bg-gradient-to-r from-blue-500 to-purple-600 rounded-sm"></div>, trendData: [12, 15, 18, 22, 19, 25, 30] },
    { title: 'Engagement Rate', value: 0, change: 0, changeType: 'positive', icon: <div className="w-5 h-5 bg-pink-500 rounded-sm"></div>, trendData: [3.2, 3.8, 4.1, 4.5, 4.2, 5.0, 5.3] },
  ]);

  const [loading, setLoading] = useState(true);

  const fetchStats = async () => {
    try {
      setLoading(true);
      const response = await fetch('/api/stats');
      if (!response.ok) throw new Error('Failed to fetch stats');

      const data = await response.json();

      setStats([
        {
          title: 'Pending Tasks',
          value: data.pending || 0,
          change: data.trends?.pendingChange || 0,
          changeType: (data.trends?.pendingChange >= 0 ? 'positive' : 'negative') as 'positive' | 'negative',
          icon: <Clock className="w-5 h-5" />,
          trendData: [65, 59, 80, 81, 56, 55, 40]
        },
        {
          title: 'In Progress',
          value: data.inProgress || 0,
          change: data.trends?.inProgressChange || 0,
          changeType: (data.trends?.inProgressChange >= 0 ? 'positive' : 'negative') as 'positive' | 'negative',
          icon: <Play className="w-5 h-5" />,
          trendData: [28, 48, 40, 19, 86, 27, 90]
        },
        {
          title: 'Completed',
          value: data.completed || 0,
          change: data.trends?.completedChange || 0,
          changeType: (data.trends?.completedChange >= 0 ? 'positive' : 'negative') as 'positive' | 'negative',
          icon: <CheckCircle2 className="w-5 h-5" />,
          trendData: [12, 19, 3, 5, 2, 3, 20]
        },
        {
          title: 'Total Tasks',
          value: data.total || 0,
          change: data.trends?.totalChange || 0,
          changeType: (data.trends?.totalChange >= 0 ? 'positive' : 'negative') as 'positive' | 'negative',
          icon: <BarChart3 className="w-5 h-5" />,
          trendData: [45, 55, 48, 52, 60, 58, 65]
        },
        {
          title: 'Instagram Followers',
          value: data.social?.instagramFollowers || 0,
          change: data.social?.instagramGrowth || 0,
          changeType: (data.social?.instagramGrowth >= 0 ? 'positive' : 'negative') as 'positive' | 'negative',
          icon: <div className="w-5 h-5 bg-gradient-to-r from-purple-500 to-pink-500 rounded-sm"></div>,
          trendData: [45, 52, 48, 61, 55, 67, 72]
        },
        {
          title: 'LinkedIn Followers',
          value: data.social?.linkedinFollowers || 0,
          change: data.social?.linkedinGrowth || 0,
          changeType: (data.social?.linkedinGrowth >= 0 ? 'positive' : 'negative') as 'positive' | 'negative',
          icon: <div className="w-5 h-5 bg-blue-700 rounded-sm"></div>,
          trendData: [32, 38, 45, 42, 50, 55, 62]
        },
        {
          title: 'Social Posts',
          value: data.social?.totalPosts || 0,
          change: data.social?.postGrowth || 0,
          changeType: (data.social?.postGrowth >= 0 ? 'positive' : 'negative') as 'positive' | 'negative',
          icon: <div className="w-5 h-5 bg-gradient-to-r from-blue-500 to-purple-600 rounded-sm"></div>,
          trendData: [12, 15, 18, 22, 19, 25, 30]
        },
        {
          title: 'Engagement Rate',
          value: data.social?.engagementRate || 0,
          change: data.social?.engagementChange || 0,
          changeType: (data.social?.engagementChange >= 0 ? 'positive' : 'negative') as 'positive' | 'negative',
          icon: <div className="w-5 h-5 bg-pink-500 rounded-sm"></div>,
          trendData: [3.2, 3.8, 4.1, 4.5, 4.2, 5.0, 5.3]
        },
      ]);
    } catch (error) {
      console.error('Error fetching stats:', error);
      // Set default values in case of error
      setStats([
        { title: 'Pending Tasks', value: 0, change: 0, changeType: 'positive' as const, icon: <Clock className="w-5 h-5" />, trendData: [65, 59, 80, 81, 56, 55, 40] },
        { title: 'In Progress', value: 0, change: 0, changeType: 'positive' as const, icon: <Play className="w-5 h-5" />, trendData: [28, 48, 40, 19, 86, 27, 90] },
        { title: 'Completed', value: 0, change: 0, changeType: 'positive' as const, icon: <CheckCircle2 className="w-5 h-5" />, trendData: [12, 19, 3, 5, 2, 3, 20] },
        { title: 'Total Tasks', value: 0, change: 0, changeType: 'positive' as const, icon: <BarChart3 className="w-5 h-5" />, trendData: [45, 55, 48, 52, 60, 58, 65] },
        { title: 'Instagram Followers', value: 0, change: 0, changeType: 'positive' as const, icon: <div className="w-5 h-5 bg-gradient-to-r from-purple-500 to-pink-500 rounded-sm"></div>, trendData: [45, 52, 48, 61, 55, 67, 72] },
        { title: 'LinkedIn Followers', value: 0, change: 0, changeType: 'positive' as const, icon: <div className="w-5 h-5 bg-blue-700 rounded-sm"></div>, trendData: [32, 38, 45, 42, 50, 55, 62] },
        { title: 'Social Posts', value: 0, change: 0, changeType: 'positive' as const, icon: <div className="w-5 h-5 bg-gradient-to-r from-blue-500 to-purple-600 rounded-sm"></div>, trendData: [12, 15, 18, 22, 19, 25, 30] },
        { title: 'Engagement Rate', value: 0, change: 0, changeType: 'positive' as const, icon: <div className="w-5 h-5 bg-pink-500 rounded-sm"></div>, trendData: [3.2, 3.8, 4.1, 4.5, 4.2, 5.0, 5.3] },
      ]);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    // Fetch stats on mount
    fetchStats();

    // Set up interval to fetch stats every 5 seconds for real-time updates
    const interval = setInterval(fetchStats, 5000);

    // Clean up interval on unmount
    return () => clearInterval(interval);
  }, []);

  if (loading) {
    return (
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        {[...Array(8)].map((_, i) => (
          <Card key={i} className="glass-card h-32 animate-pulse">
            <CardHeader className="pb-2">
              <div className="h-4 bg-border rounded w-3/4 mb-2"></div>
            </CardHeader>
            <CardContent>
              <div className="h-6 bg-border rounded w-1/2 mb-3"></div>
              <div className="h-3 bg-border rounded w-2/3"></div>
            </CardContent>
          </Card>
        ))}
      </div>
    );
  }

  return (
    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
      {stats.map((stat, index) => (
        <StatCard
          key={index}
          title={stat.title}
          value={stat.value}
          change={stat.change}
          changeType={stat.changeType}
          icon={stat.icon}
          trendData={stat.trendData}
        />
      ))}
    </div>
  );
};