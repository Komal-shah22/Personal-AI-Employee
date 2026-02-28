'use client';

import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Instagram, Linkedin, Twitter, BarChart3, TrendingUp, Users, MessageCircle } from 'lucide-react';
import { useState, useEffect } from 'react';

interface SocialMetrics {
  platform: string;
  followers: number;
  posts: number;
  engagement: number;
  growth: number;
}

export default function SocialMetrics() {
  const [metrics, setMetrics] = useState<SocialMetrics[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    // Simulate fetching social metrics
    const fetchSocialMetrics = async () => {
      try {
        setLoading(true);

        const mockMetrics: SocialMetrics[] = [
          {
            platform: 'instagram',
            followers: 1245,
            posts: 42,
            engagement: 4.8,
            growth: 12.3
          },
          {
            platform: 'linkedin',
            followers: 876,
            posts: 28,
            engagement: 3.2,
            growth: 8.7
          },
          {
            platform: 'twitter',
            followers: 543,
            posts: 67,
            engagement: 2.1,
            growth: 5.4
          }
        ];

        setMetrics(mockMetrics);
      } catch (error) {
        console.error('Error fetching social metrics:', error);
      } finally {
        setLoading(false);
      }
    };

    fetchSocialMetrics();
  }, []);

  const getPlatformIcon = (platform: string) => {
    switch (platform) {
      case 'instagram':
        return <Instagram className="w-5 h-5 bg-gradient-to-r from-purple-500 to-pink-500 text-transparent bg-clip-text" />;
      case 'linkedin':
        return <Linkedin className="w-5 h-5 text-blue-700" />;
      case 'twitter':
        return <Twitter className="w-5 h-5 text-blue-400" />;
      default:
        return <BarChart3 className="w-5 h-5" />;
    }
  };

  if (loading) {
    return (
      <Card className="h-full">
        <CardHeader>
          <CardTitle>Social Media Metrics</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="space-y-4">
            {[...Array(3)].map((_, i) => (
              <div key={i} className="animate-pulse flex justify-between items-center py-2">
                <div className="flex items-center gap-3">
                  <div className="w-8 h-8 rounded-full bg-gray-200"></div>
                  <div>
                    <div className="h-4 bg-gray-200 rounded w-20 mb-2"></div>
                    <div className="h-3 bg-gray-200 rounded w-16"></div>
                  </div>
                </div>
                <div className="h-4 bg-gray-200 rounded w-16"></div>
              </div>
            ))}
          </div>
        </CardContent>
      </Card>
    );
  }

  return (
    <Card className="h-full">
      <CardHeader>
        <CardTitle className="flex items-center gap-2">
          <BarChart3 className="w-5 h-5" />
          Social Media Metrics
        </CardTitle>
      </CardHeader>
      <CardContent>
        <div className="space-y-4">
          {metrics.map((metric, index) => (
            <div key={index} className="flex justify-between items-center py-2 border-b border-gray-100 last:border-0">
              <div className="flex items-center gap-3">
                <div className="p-2 rounded-lg bg-gray-50">
                  {getPlatformIcon(metric.platform)}
                </div>
                <div>
                  <div className="font-medium capitalize">{metric.platform}</div>
                  <div className="text-xs text-gray-500">
                    <Users className="w-3 h-3 inline mr-1" />
                    {metric.followers.toLocaleString()} followers
                  </div>
                </div>
              </div>
              <div className="text-right">
                <div className="font-semibold">{metric.engagement}% ER</div>
                <div className="text-xs text-green-500 flex items-center justify-end">
                  <TrendingUp className="w-3 h-3 mr-1" />
                  {metric.growth}%
                </div>
              </div>
            </div>
          ))}
        </div>

        <div className="mt-6 pt-4 border-t border-gray-100">
          <div className="grid grid-cols-2 gap-4">
            <div className="text-center">
              <div className="text-lg font-bold">{metrics.reduce((sum, m) => sum + m.posts, 0)}</div>
              <div className="text-xs text-gray-500">Total Posts</div>
            </div>
            <div className="text-center">
              <div className="text-lg font-bold">{(metrics.reduce((sum, m) => sum + m.followers, 0) / 1000).toFixed(1)}K</div>
              <div className="text-xs text-gray-500">Total Followers</div>
            </div>
          </div>
        </div>
      </CardContent>
    </Card>
  );
}