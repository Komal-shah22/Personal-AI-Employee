'use client';

import { useState, useEffect } from 'react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { BarChart3, TrendingUp, Users, Heart, MessageCircle, Share2, Calendar, Target } from 'lucide-react';

interface AnalyticsData {
  date: string;
  instagram: number;
  linkedin: number;
  twitter: number;
  facebook: number;
}

interface SocialAnalyticsProps {
  tier?: 'bronze' | 'silver' | 'gold' | 'platinum';
}

export default function SocialAnalytics({ tier = 'gold' }: SocialAnalyticsProps) {
  const [analyticsData, setAnalyticsData] = useState<AnalyticsData[]>([
    { date: 'Feb 14', instagram: 3200, linkedin: 2400, twitter: 1800, facebook: 1200 },
    { date: 'Feb 15', instagram: 3800, linkedin: 2800, twitter: 2200, facebook: 1500 },
    { date: 'Feb 16', instagram: 4300, linkedin: 3200, twitter: 2500, facebook: 1700 },
    { date: 'Feb 17', instagram: 3900, linkedin: 3000, twitter: 2100, facebook: 1400 },
    { date: 'Feb 18', instagram: 4500, linkedin: 3500, twitter: 2700, facebook: 1900 },
    { date: 'Feb 19', instagram: 5200, linkedin: 3800, twitter: 3100, facebook: 2200 },
    { date: 'Feb 20', instagram: 4800, linkedin: 3600, twitter: 2900, facebook: 2100 },
  ]);

  const [selectedMetric, setSelectedMetric] = useState<'impressions' | 'engagement' | 'reach'>('impressions');
  const [timeRange, setTimeRange] = useState<'7d' | '30d' | '90d'>('7d');

  // Calculate totals and metrics
  const totalImpressions = analyticsData.reduce((sum, day) =>
    sum + day.instagram + day.linkedin + day.twitter + day.facebook, 0);

  const avgEngagementRate = 4.2; // Simulated average
  const totalFollowers = 3240;   // Simulated total

  // Get the latest day's data for comparison
  const latestDay = analyticsData[analyticsData.length - 1];
  const previousDay = analyticsData[analyticsData.length - 2];

  const impressionsChange = previousDay
    ? ((latestDay.instagram + latestDay.linkedin + latestDay.twitter + latestDay.facebook) -
       (previousDay.instagram + previousDay.linkedin + previousDay.twitter + previousDay.facebook)) /
       (previousDay.instagram + previousDay.linkedin + previousDay.twitter + previousDay.facebook) * 100
    : 0;

  return (
    <Card className="glass-card">
      <CardHeader className="flex flex-col sm:flex-row sm:items-center sm:justify-between">
        <CardTitle className="flex items-center gap-2">
          <BarChart3 className="w-5 h-5" />
          Social Media Analytics
        </CardTitle>

        <div className="flex gap-2 mt-2 sm:mt-0">
          <select
            value={selectedMetric}
            onChange={(e) => setSelectedMetric(e.target.value as any)}
            className="bg-surface2 border border-border rounded-md px-3 py-1 text-sm"
          >
            <option value="impressions">Impressions</option>
            <option value="engagement">Engagement</option>
            <option value="reach">Reach</option>
          </select>

          <select
            value={timeRange}
            onChange={(e) => setTimeRange(e.target.value as any)}
            className="bg-surface2 border border-border rounded-md px-3 py-1 text-sm"
          >
            <option value="7d">7 Days</option>
            <option value="30d">30 Days</option>
            <option value="90d">90 Days</option>
          </select>
        </div>
      </CardHeader>

      <CardContent>
        {/* Summary Stats */}
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-6">
          <div className="text-center p-4 bg-white/5 rounded-lg">
            <div className="flex justify-center mb-2">
              <Target className="w-6 h-6 text-accent" />
            </div>
            <div className="text-xl font-bold">{totalImpressions.toLocaleString()}</div>
            <div className="text-xs text-muted">Total Impressions</div>
            <div className="text-xs mt-1 flex items-center justify-center gap-1">
              <TrendingUp className="w-3 h-3 text-green-500" />
              <span className="text-green-500">{impressionsChange.toFixed(1)}%</span>
              <span className="text-muted">vs last day</span>
            </div>
          </div>

          <div className="text-center p-4 bg-white/5 rounded-lg">
            <div className="flex justify-center mb-2">
              <Heart className="w-6 h-6 text-pink-500" />
            </div>
            <div className="text-xl font-bold">{avgEngagementRate}%</div>
            <div className="text-xs text-muted">Avg Engagement</div>
            <div className="text-xs mt-1 text-muted">Rate</div>
          </div>

          <div className="text-center p-4 bg-white/5 rounded-lg">
            <div className="flex justify-center mb-2">
              <Users className="w-6 h-6 text-blue-500" />
            </div>
            <div className="text-xl font-bold">{totalFollowers.toLocaleString()}</div>
            <div className="text-xs text-muted">Total Followers</div>
            <div className="text-xs mt-1 text-muted">Across all platforms</div>
          </div>

          <div className="text-center p-4 bg-white/5 rounded-lg">
            <div className="flex justify-center mb-2">
              <Calendar className="w-6 h-6 text-green-500" />
            </div>
            <div className="text-xl font-bold">{analyticsData.length}</div>
            <div className="text-xs text-muted">Days Tracked</div>
            <div className="text-xs mt-1 text-muted">Period</div>
          </div>
        </div>

        {/* Chart Visualization */}
        <div className="mb-6">
          <h4 className="text-sm font-medium mb-3">Impressions Over Time</h4>
          <div className="space-y-2">
            {analyticsData.map((day, index) => (
              <div key={index} className="flex items-center">
                <div className="w-12 text-xs text-muted">{day.date}</div>
                <div className="flex-1 flex gap-1">
                  <div
                    className="bg-gradient-to-r from-purple-500/80 to-pink-500/80 rounded-sm min-h-6 flex items-center justify-end pr-2 text-[10px] text-white"
                    style={{ width: `${(day.instagram / Math.max(...analyticsData.map(d => d.instagram))) * 80}%` }}
                  >
                    {day.instagram >= 4000 ? 'IG' : ''}
                  </div>
                  <div
                    className="bg-blue-700/80 rounded-sm min-h-6 flex items-center justify-end pr-2 text-[10px] text-white"
                    style={{ width: `${(day.linkedin / Math.max(...analyticsData.map(d => d.linkedin))) * 70}%` }}
                  >
                    {day.linkedin >= 3000 ? 'LI' : ''}
                  </div>
                  <div
                    className="bg-blue-400/80 rounded-sm min-h-6 flex items-center justify-end pr-2 text-[10px] text-white"
                    style={{ width: `${(day.twitter / Math.max(...analyticsData.map(d => d.twitter))) * 60}%` }}
                  >
                    {day.twitter >= 2500 ? 'TW' : ''}
                  </div>
                  <div
                    className="bg-blue-600/80 rounded-sm min-h-6 flex items-center justify-end pr-2 text-[10px] text-white"
                    style={{ width: `${(day.facebook / Math.max(...analyticsData.map(d => d.facebook))) * 50}%` }}
                  >
                    {day.facebook >= 1800 ? 'FB' : ''}
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Platform Comparison */}
        <div>
          <h4 className="text-sm font-medium mb-3">Platform Comparison</h4>
          <div className="grid grid-cols-2 md:grid-cols-4 gap-3">
            <div className="p-3 bg-gradient-to-r from-purple-500/10 to-pink-500/10 border border-purple-500/20 rounded-lg">
              <div className="font-semibold text-purple-600">Instagram</div>
              <div className="text-lg font-bold">{(analyticsData.reduce((sum, d) => sum + d.instagram, 0) / analyticsData.length).toLocaleString()}</div>
              <div className="text-xs text-muted">avg/day</div>
            </div>

            <div className="p-3 bg-blue-700/10 border border-blue-700/20 rounded-lg">
              <div className="font-semibold text-blue-700">LinkedIn</div>
              <div className="text-lg font-bold">{(analyticsData.reduce((sum, d) => sum + d.linkedin, 0) / analyticsData.length).toLocaleString()}</div>
              <div className="text-xs text-muted">avg/day</div>
            </div>

            <div className="p-3 bg-blue-400/10 border border-blue-400/20 rounded-lg">
              <div className="font-semibold text-blue-400">Twitter</div>
              <div className="text-lg font-bold">{(analyticsData.reduce((sum, d) => sum + d.twitter, 0) / analyticsData.length).toLocaleString()}</div>
              <div className="text-xs text-muted">avg/day</div>
            </div>

            <div className="p-3 bg-blue-600/10 border border-blue-600/20 rounded-lg">
              <div className="font-semibold text-blue-600">Facebook</div>
              <div className="text-lg font-bold">{(analyticsData.reduce((sum, d) => sum + d.facebook, 0) / analyticsData.length).toLocaleString()}</div>
              <div className="text-xs text-muted">avg/day</div>
            </div>
          </div>
        </div>
      </CardContent>
    </Card>
  );
}