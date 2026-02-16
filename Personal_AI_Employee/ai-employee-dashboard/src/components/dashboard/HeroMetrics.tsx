'use client';

import { useState, useEffect } from 'react';
import { TrendingUp, TrendingDown, Info, ArrowRight } from 'lucide-react';
import { motion } from 'framer-motion';

interface Metric {
  label: string;
  value: number;
  change: number;
  trend: number[];
  unit?: string;
  info: string;
}

export default function HeroMetrics() {
  const [metrics, setMetrics] = useState<Metric[]>([
    {
      label: 'Tasks Processed',
      value: 0,
      change: 12,
      trend: [45, 52, 48, 61, 58, 67, 73],
      info: 'Total tasks completed today',
    },
    {
      label: 'Active Agents',
      value: 0,
      change: 0,
      trend: [5, 5, 4, 5, 5, 5, 5],
      unit: '/5',
      info: 'Currently running agents',
    },
    {
      label: 'Pending Approvals',
      value: 0,
      change: -25,
      trend: [12, 10, 8, 6, 5, 4, 3],
      info: 'Items awaiting approval',
    },
    {
      label: 'System Health',
      value: 0,
      change: 2,
      trend: [94, 95, 96, 97, 97, 98, 98],
      unit: '%',
      info: 'Overall system performance',
    },
  ]);

  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchMetrics = async () => {
      try {
        const res = await fetch('/api/dashboard');
        const data = await res.json();

        setMetrics([
          {
            label: 'Tasks Processed',
            value: data.metrics.tasksToday || 73,
            change: 12,
            trend: [45, 52, 48, 61, 58, 67, 73],
            info: 'Total tasks completed today',
          },
          {
            label: 'Active Agents',
            value: data.metrics.activeAgents || 5,
            change: 0,
            trend: [5, 5, 4, 5, 5, 5, 5],
            unit: '/5',
            info: 'Currently running agents',
          },
          {
            label: 'Pending Approvals',
            value: data.metrics.pendingApprovals || 3,
            change: -25,
            trend: [12, 10, 8, 6, 5, 4, 3],
            info: 'Items awaiting approval',
          },
          {
            label: 'System Health',
            value: data.metrics.systemHealth || 98,
            change: 2,
            trend: [94, 95, 96, 97, 97, 98, 98],
            unit: '%',
            info: 'Overall system performance',
          },
        ]);
      } catch (error) {
        console.error('Failed to fetch metrics:', error);
      } finally {
        setLoading(false);
      }
    };

    fetchMetrics();
    const interval = setInterval(fetchMetrics, 10000);
    return () => clearInterval(interval);
  }, []);

  if (loading) {
    return (
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        {[1, 2, 3, 4].map((i) => (
          <div key={i} className="metric-card h-[280px]">
            <div className="skeleton h-full" />
          </div>
        ))}
      </div>
    );
  }

  return (
    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
      {metrics.map((metric, index) => (
        <MetricCard key={metric.label} metric={metric} index={index} />
      ))}
    </div>
  );
}

function MetricCard({ metric, index }: { metric: Metric; index: number }) {
  const [displayValue, setDisplayValue] = useState(0);

  useEffect(() => {
    let start = 0;
    const end = metric.value;
    const duration = 1000;
    const increment = end / (duration / 16);

    const timer = setInterval(() => {
      start += increment;
      if (start >= end) {
        setDisplayValue(end);
        clearInterval(timer);
      } else {
        setDisplayValue(Math.floor(start));
      }
    }, 16);

    return () => clearInterval(timer);
  }, [metric.value]);

  const maxTrend = Math.max(...metric.trend);
  const minTrend = Math.min(...metric.trend);

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.4, delay: index * 0.1 }}
      className="metric-card h-[280px] group"
    >
      {/* Header */}
      <div className="flex items-start justify-between mb-6">
        <div>
          <div className="flex items-center gap-2 mb-1">
            <span className="text-xs uppercase tracking-wider text-text-tertiary font-semibold">
              {metric.label}
            </span>
            <div className="relative group/info">
              <Info className="w-3 h-3 text-text-quaternary hover:text-text-tertiary cursor-help" />
              <div className="tooltip opacity-0 group-hover/info:opacity-100 transition-opacity -top-8 left-0">
                {metric.info}
              </div>
            </div>
          </div>
        </div>
        <div
          className={`flex items-center gap-1 text-xs font-semibold ${
            metric.change > 0
              ? 'text-success'
              : metric.change < 0
              ? 'text-error'
              : 'text-text-tertiary'
          }`}
        >
          {metric.change > 0 ? (
            <TrendingUp className="w-3 h-3" />
          ) : metric.change < 0 ? (
            <TrendingDown className="w-3 h-3" />
          ) : null}
          {metric.change !== 0 && `${Math.abs(metric.change)}%`}
        </div>
      </div>

      {/* Value */}
      <div className="mb-6">
        <div className="text-5xl font-display font-bold mb-2">
          {displayValue}
          {metric.unit && (
            <span className="text-2xl text-text-tertiary">{metric.unit}</span>
          )}
        </div>
      </div>

      {/* Sparkline */}
      <div className="mb-4">
        <svg width="100%" height="40" className="overflow-visible">
          <defs>
            <linearGradient id={`gradient-${index}`} x1="0%" y1="0%" x2="0%" y2="100%">
              <stop offset="0%" stopColor="rgb(99, 102, 241)" stopOpacity="0.3" />
              <stop offset="100%" stopColor="rgb(99, 102, 241)" stopOpacity="0" />
            </linearGradient>
          </defs>

          {/* Area */}
          <path
            d={`M 0 40 ${metric.trend
              .map((value, i) => {
                const x = (i / (metric.trend.length - 1)) * 100;
                const y = 40 - ((value - minTrend) / (maxTrend - minTrend)) * 30;
                return `${i === 0 ? 'M' : 'L'} ${x}% ${y}`;
              })
              .join(' ')} L 100% 40 Z`}
            fill={`url(#gradient-${index})`}
          />

          {/* Line */}
          <path
            d={metric.trend
              .map((value, i) => {
                const x = (i / (metric.trend.length - 1)) * 100;
                const y = 40 - ((value - minTrend) / (maxTrend - minTrend)) * 30;
                return `${i === 0 ? 'M' : 'L'} ${x}% ${y}`;
              })
              .join(' ')}
            fill="none"
            stroke="rgb(99, 102, 241)"
            strokeWidth="2"
            className="animate-draw-line"
          />
        </svg>
      </div>

      {/* Footer */}
      <div className="flex items-center justify-between text-xs">
        <span className="text-text-tertiary">
          {metric.change > 0 ? '↑' : metric.change < 0 ? '↓' : '→'} vs yesterday
        </span>
        <button className="flex items-center gap-1 text-brand-primary hover:text-brand-secondary transition-colors group/link">
          <span>Details</span>
          <ArrowRight className="w-3 h-3 group-hover/link:translate-x-0.5 transition-transform" />
        </button>
      </div>
    </motion.div>
  );
}
