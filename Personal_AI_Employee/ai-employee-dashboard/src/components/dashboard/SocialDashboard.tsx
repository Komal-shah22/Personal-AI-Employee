'use client';

import { useState, useEffect } from 'react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { BarChart3, Users, TrendingUp, Instagram, Linkedin, Twitter, Facebook, Heart } from 'lucide-react';
import SocialAnalytics from './SocialAnalytics';

interface SocialPlatform {
  name: string;
  icon: React.ReactNode;
  followers: number;
  following: number;
  posts: number;
  engagement: number;
  growth: number;
  status: 'active' | 'warning' | 'inactive';
}

export default function SocialDashboard() {
  const [platforms, setPlatforms] = useState<SocialPlatform[]>([
    {
      name: 'Instagram',
      icon: <Instagram className="w-5 h-5 bg-gradient-to-r from-purple-500 to-pink-500 text-transparent bg-clip-text" />,
      followers: 1245,
      following: 56,
      posts: 42,
      engagement: 4.8,
      growth: 12.3,
      status: 'active'
    },
    {
      name: 'LinkedIn',
      icon: <Linkedin className="w-5 h-5 text-blue-700" />,
      followers: 876,
      following: 234,
      posts: 28,
      engagement: 3.2,
      growth: 8.7,
      status: 'active'
    },
    {
      name: 'Twitter',
      icon: <Twitter className="w-5 h-5 text-blue-400" />,
      followers: 543,
      following: 432,
      posts: 67,
      engagement: 2.1,
      growth: 5.4,
      status: 'active'
    },
    {
      name: 'Facebook',
      icon: <Facebook className="w-5 h-5 text-blue-600" />,
      followers: 632,
      following: 89,
      posts: 31,
      engagement: 1.8,
      growth: 3.2,
      status: 'active'
    }
  ]);

  const [totalStats, setTotalStats] = useState({
    followers: 0,
    posts: 0,
    engagement: 0,
    growth: 0
  });

  useEffect(() => {
    // Calculate total stats
    const totalFollowers = platforms.reduce((sum, p) => sum + p.followers, 0);
    const totalPosts = platforms.reduce((sum, p) => sum + p.posts, 0);
    const avgEngagement = platforms.reduce((sum, p) => sum + p.engagement, 0) / platforms.length;
    const avgGrowth = platforms.reduce((sum, p) => sum + p.growth, 0) / platforms.length;

    setTotalStats({
      followers: totalFollowers,
      posts: totalPosts,
      engagement: parseFloat(avgEngagement.toFixed(1)),
      growth: parseFloat(avgGrowth.toFixed(1))
    });
  }, [platforms]);

  return (
    <div className="space-y-8">
      {/* Social Media Overview Stats */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        <Card className="glass-card hover:glow-on-hover transition-all duration-300 h-full">
          <CardHeader className="flex flex-row items-center justify-between pb-2">
            <CardTitle className="text-sm font-medium text-text-secondary">Total Followers</CardTitle>
            <div className="p-2 rounded-lg bg-primary/10 text-primary">
              <Users className="w-5 h-5" />
            </div>
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{totalStats.followers.toLocaleString()}</div>
            <div className="flex items-center gap-1 mt-2">
              <TrendingUp className="w-4 h-4 text-green-500" />
              <span className="text-sm text-green-500">
                +{totalStats.growth}% this month
              </span>
            </div>
          </CardContent>
        </Card>

        <Card className="glass-card hover:glow-on-hover transition-all duration-300 h-full">
          <CardHeader className="flex flex-row items-center justify-between pb-2">
            <CardTitle className="text-sm font-medium text-text-secondary">Total Posts</CardTitle>
            <div className="p-2 rounded-lg bg-primary/10 text-primary">
              <BarChart3 className="w-5 h-5" />
            </div>
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{totalStats.posts}</div>
            <div className="flex items-center gap-1 mt-2">
              <TrendingUp className="w-4 h-4 text-green-500" />
              <span className="text-sm text-green-500">
                +12% this month
              </span>
            </div>
          </CardContent>
        </Card>

        <Card className="glass-card hover:glow-on-hover transition-all duration-300 h-full">
          <CardHeader className="flex flex-row items-center justify-between pb-2">
            <CardTitle className="text-sm font-medium text-text-secondary">Avg Engagement</CardTitle>
            <div className="p-2 rounded-lg bg-primary/10 text-primary">
              <Heart className="w-5 h-5" />
            </div>
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{totalStats.engagement}%</div>
            <div className="flex items-center gap-1 mt-2">
              <TrendingUp className="w-4 h-4 text-green-500" />
              <span className="text-sm text-green-500">
                +0.5% this month
              </span>
            </div>
          </CardContent>
        </Card>

        <Card className="glass-card hover:glow-on-hover transition-all duration-300 h-full">
          <CardHeader className="flex flex-row items-center justify-between pb-2">
            <CardTitle className="text-sm font-medium text-text-secondary">Active Platforms</CardTitle>
            <div className="p-2 rounded-lg bg-primary/10 text-primary">
              <BarChart3 className="w-5 h-5" />
            </div>
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{platforms.length}</div>
            <div className="flex items-center gap-1 mt-2">
              <div className="w-2 h-2 rounded-full bg-green-500 mr-1"></div>
              <span className="text-sm text-green-500">
                All active
              </span>
            </div>
          </CardContent>
        </Card>
      </div>

      {/* Analytics Chart */}
      <SocialAnalytics tier="gold" />
    </div>
  );
}