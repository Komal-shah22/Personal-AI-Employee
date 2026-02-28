'use client';

import { useState, useEffect } from 'react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import {
  Instagram,
  Linkedin,
  Twitter,
  Facebook,
  MessageCircle,
  Heart,
  Share2,
  Users,
  BarChart3,
  TrendingUp,
  Calendar,
  Target
} from 'lucide-react';

interface SocialStatusData {
  platform: string;
  status: 'active' | 'warning' | 'inactive';
  postsToday: number;
  scheduledPosts: number;
  engagementRate: number;
  reach: number;
  impressions: number;
  newFollowers: number;
  comments: number;
  shares: number;
}

interface SocialStatusProps {
  tier?: 'bronze' | 'silver' | 'gold' | 'platinum';
}

export default function SocialStatus({ tier = 'gold' }: SocialStatusProps) {
  const [socialData, setSocialData] = useState<SocialStatusData[]>([
    {
      platform: 'Instagram',
      status: 'active',
      postsToday: 2,
      scheduledPosts: 5,
      engagementRate: 4.8,
      reach: 1842,
      impressions: 2100,
      newFollowers: 12,
      comments: 24,
      shares: 7
    },
    {
      platform: 'LinkedIn',
      status: 'active',
      postsToday: 1,
      scheduledPosts: 3,
      engagementRate: 3.2,
      reach: 1520,
      impressions: 1800,
      newFollowers: 8,
      comments: 18,
      shares: 12
    },
    {
      platform: 'Twitter',
      status: 'active',
      postsToday: 3,
      scheduledPosts: 7,
      engagementRate: 2.1,
      reach: 2100,
      impressions: 2400,
      newFollowers: 15,
      comments: 22,
      shares: 31
    },
    {
      platform: 'Facebook',
      status: 'active',
      postsToday: 1,
      scheduledPosts: 2,
      engagementRate: 1.8,
      reach: 980,
      impressions: 1200,
      newFollowers: 5,
      comments: 8,
      shares: 4
    }
  ]);

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'active': return 'bg-green-500';
      case 'warning': return 'bg-yellow-500';
      case 'inactive': return 'bg-red-500';
      default: return 'bg-gray-500';
    }
  };

  const getStatusText = (status: string) => {
    switch (status) {
      case 'active': return 'Active';
      case 'warning': return 'Needs Attention';
      case 'inactive': return 'Inactive';
      default: return 'Unknown';
    }
  };

  const getPlatformIcon = (platform: string) => {
    switch (platform) {
      case 'Instagram':
        return <Instagram className="w-5 h-5 bg-gradient-to-r from-purple-500 to-pink-500 text-transparent bg-clip-text" />;
      case 'LinkedIn':
        return <Linkedin className="w-5 h-5 text-blue-700" />;
      case 'Twitter':
        return <Twitter className="w-5 h-5 text-blue-400" />;
      case 'Facebook':
        return <Facebook className="w-5 h-5 text-blue-600" />;
      default:
        return <BarChart3 className="w-5 h-5" />;
    }
  };

  // Calculate totals
  const totalPostsToday = socialData.reduce((sum, data) => sum + data.postsToday, 0);
  const totalScheduled = socialData.reduce((sum, data) => sum + data.scheduledPosts, 0);
  const totalNewFollowers = socialData.reduce((sum, data) => sum + data.newFollowers, 0);
  const avgEngagement = socialData.reduce((sum, data) => sum + data.engagementRate, 0) / socialData.length;

  return (
    <Card className="glass-card h-full">
      <CardHeader>
        <CardTitle className="flex items-center justify-between">
          <div className="flex items-center gap-2">
            <BarChart3 className="w-5 h-5" />
            <div>
              <div>Social Media Status</div>
              <div className="text-xs text-muted">Gold Tier - Full Automation</div>
            </div>
          </div>
          <div className="text-xs px-2 py-1 rounded-full bg-gradient-to-r from-yellow-500/20 to-yellow-600/20 text-yellow-400">
            Real-time
          </div>
        </CardTitle>
      </CardHeader>
      <CardContent>
        {/* Summary Stats */}
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-6">
          <div className="text-center p-3 bg-white/5 rounded-lg">
            <div className="text-2xl font-bold">{totalPostsToday}</div>
            <div className="text-xs text-muted">Posts Today</div>
          </div>
          <div className="text-center p-3 bg-white/5 rounded-lg">
            <div className="text-2xl font-bold">{totalScheduled}</div>
            <div className="text-xs text-muted">Scheduled</div>
          </div>
          <div className="text-center p-3 bg-white/5 rounded-lg">
            <div className="text-2xl font-bold">{totalNewFollowers}</div>
            <div className="text-xs text-muted">New Followers</div>
          </div>
          <div className="text-center p-3 bg-white/5 rounded-lg">
            <div className="text-2xl font-bold">{avgEngagement.toFixed(1)}%</div>
            <div className="text-xs text-muted">Avg Engagement</div>
          </div>
        </div>

        {/* Platform Status */}
        <div className="space-y-4">
          {socialData.map((data, index) => (
            <div key={index} className="border border-border rounded-lg p-4">
              <div className="flex items-center justify-between mb-3">
                <div className="flex items-center gap-3">
                  <div className="p-2 rounded-lg bg-gray-50">
                    {getPlatformIcon(data.platform)}
                  </div>
                  <div>
                    <h3 className="font-semibold">{data.platform}</h3>
                    <div className="flex items-center gap-2 text-xs">
                      <div className={`w-2 h-2 rounded-full ${getStatusColor(data.status)}`}></div>
                      <span className="text-muted">{getStatusText(data.status)}</span>
                    </div>
                  </div>
                </div>
                <div className="text-right">
                  <div className="font-semibold">{data.engagementRate}%</div>
                  <div className="text-xs text-muted">Engagement</div>
                </div>
              </div>

              <div className="grid grid-cols-2 md:grid-cols-4 gap-3">
                <div className="flex items-center gap-2 text-xs">
                  <Calendar className="w-3 h-3 text-muted" />
                  <span>{data.postsToday} today</span>
                </div>
                <div className="flex items-center gap-2 text-xs">
                  <Target className="w-3 h-3 text-muted" />
                  <span>{data.scheduledPosts} scheduled</span>
                </div>
                <div className="flex items-center gap-2 text-xs">
                  <Users className="w-3 h-3 text-muted" />
                  <span>+{data.newFollowers}</span>
                </div>
                <div className="flex items-center gap-2 text-xs">
                  <Heart className="w-3 h-3 text-muted" />
                  <span>{data.comments} comments</span>
                </div>
              </div>
            </div>
          ))}
        </div>

        {/* Platform Health Indicators */}
        <div className="mt-6 pt-4 border-t border-border">
          <h4 className="font-medium mb-3">Platform Health</h4>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
            <div className="flex items-center justify-between p-3 bg-green-50 border border-green-200 rounded-lg">
              <span className="text-sm">Instagram: High engagement</span>
              <TrendingUp className="w-4 h-4 text-green-600" />
            </div>
            <div className="flex items-center justify-between p-3 bg-blue-50 border border-blue-200 rounded-lg">
              <span className="text-sm">LinkedIn: Steady growth</span>
              <TrendingUp className="w-4 h-4 text-blue-600" />
            </div>
          </div>
        </div>
      </CardContent>
    </Card>
  );
}