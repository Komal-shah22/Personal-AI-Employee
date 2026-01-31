'use client';

import { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, Legend } from 'recharts';
import { format } from 'date-fns';

interface ChartDataPoint {
  date: string;
  completed: number;
  pending: number;
  inProgress: number;
}

export const TaskCompletionChart = () => {
  const [data, setData] = useState<ChartDataPoint[]>([]);
  const [loading, setLoading] = useState(true);

  const fetchChartData = async () => {
    try {
      setLoading(true);

      const response = await fetch('/api/chart-data');
      if (!response.ok) throw new Error('Failed to fetch chart data');

      const chartData = await response.json();
      setData(chartData);
    } catch (error) {
      console.error('Error fetching chart data:', error);
      // Fallback to empty array if API fails
      setData([]);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    // Fetch chart data on mount
    fetchChartData();

    // Set up interval to fetch chart data every 10 seconds for real-time updates
    const interval = setInterval(fetchChartData, 10000);

    // Clean up interval on unmount
    return () => clearInterval(interval);
  }, []);

  if (loading) {
    return (
      <div className="h-64 w-full flex items-center justify-center">
        <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-primary"></div>
      </div>
    );
  }

  return (
    <motion.div
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      transition={{ duration: 0.5 }}
      className="h-80 w-full"
    >
      <ResponsiveContainer width="100%" height="100%">
        <LineChart
          data={data}
          margin={{
            top: 5,
            right: 30,
            left: 20,
            bottom: 5,
          }}
        >
          <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.1)" />
          <XAxis
            dataKey="date"
            stroke="rgba(255,255,255,0.6)"
            tick={{ fontSize: 12 }}
          />
          <YAxis
            stroke="rgba(255,255,255,0.6)"
            tick={{ fontSize: 12 }}
          />
          <Tooltip
            contentStyle={{
              backgroundColor: 'var(--surface)',
              borderColor: 'var(--border)',
              borderRadius: '0.5rem',
              color: 'var(--text-primary)'
            }}
            itemStyle={{ color: 'var(--text-primary)' }}
            labelStyle={{ color: 'var(--text-primary)', fontWeight: 'bold' }}
          />
          <Legend />
          <Line
            type="monotone"
            dataKey="completed"
            stroke="#10B981"
            strokeWidth={2}
            dot={{ r: 4 }}
            activeDot={{ r: 6 }}
            name="Completed"
          />
          <Line
            type="monotone"
            dataKey="inProgress"
            stroke="#F59E0B"
            strokeWidth={2}
            dot={{ r: 4 }}
            activeDot={{ r: 6 }}
            name="In Progress"
          />
          <Line
            type="monotone"
            dataKey="pending"
            stroke="#3B82F6"
            strokeWidth={2}
            dot={{ r: 4 }}
            activeDot={{ r: 6 }}
            name="Pending"
          />
        </LineChart>
      </ResponsiveContainer>
    </motion.div>
  );
};