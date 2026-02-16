'use client';

import { useState, useEffect } from 'react';
import { Play, Square, RotateCw, BarChart2, Loader2 } from 'lucide-react';
import { motion } from 'framer-motion';
import { toast } from 'sonner';

interface Agent {
  id: string;
  name: string;
  icon: string;
  status: 'running' | 'stopped' | 'starting' | 'error';
  lastActive: string;
  stats: {
    processed: number;
    label: string;
  };
}

export default function AgentGrid() {
  const [agents, setAgents] = useState<Agent[]>([]);
  const [loading, setLoading] = useState(true);
  const [actionLoading, setActionLoading] = useState<string | null>(null);

  useEffect(() => {
    fetchAgents();
    const interval = setInterval(fetchAgents, 3000);
    return () => clearInterval(interval);
  }, []);

  const fetchAgents = async () => {
    try {
      const res = await fetch('/api/dashboard');
      const data = await res.json();
      setAgents(data.agents || []);
    } catch (error) {
      console.error('Failed to fetch agents:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleAction = async (agentId: string, action: 'start' | 'stop' | 'restart') => {
    setActionLoading(`${agentId}-${action}`);
    try {
      const res = await fetch(`/api/agents/${agentId}/control`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ action }),
      });

      if (res.ok) {
        toast.success(`Agent ${action}ed successfully`);
        fetchAgents();
      } else {
        toast.error(`Failed to ${action} agent`);
      }
    } catch (error) {
      toast.error(`Error: ${error}`);
    } finally {
      setActionLoading(null);
    }
  };

  if (loading) {
    return (
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        {[1, 2, 3, 4, 5, 6].map((i) => (
          <div key={i} className="agent-card h-[200px]">
            <div className="skeleton h-full" />
          </div>
        ))}
      </div>
    );
  }

  return (
    <div>
      <div className="flex items-center justify-between mb-4">
        <h2 className="text-lg font-display font-semibold">Agent Status</h2>
        <div className="flex items-center gap-2 text-sm text-text-tertiary">
          <div className="status-dot status-running" />
          <span>{agents.filter(a => a.status === 'running').length} running</span>
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        {agents.map((agent, index) => (
          <AgentCard
            key={agent.id}
            agent={agent}
            index={index}
            onAction={handleAction}
            actionLoading={actionLoading}
          />
        ))}
      </div>
    </div>
  );
}

function AgentCard({
  agent,
  index,
  onAction,
  actionLoading,
}: {
  agent: Agent;
  index: number;
  onAction: (id: string, action: 'start' | 'stop' | 'restart') => void;
  actionLoading: string | null;
}) {
  return (
    <motion.div
      initial={{ opacity: 0, scale: 0.95 }}
      animate={{ opacity: 1, scale: 1 }}
      transition={{ duration: 0.3, delay: index * 0.05 }}
      className="agent-card"
    >
      {/* Header */}
      <div className="flex items-start justify-between mb-4">
        <div className="flex items-center gap-3">
          <div className="relative">
            <div className="w-12 h-12 rounded-xl bg-surface-2 flex items-center justify-center text-2xl">
              {agent.icon}
            </div>
            <div className="absolute -top-1 -right-1">
              {agent.status === 'running' && (
                <div className="relative">
                  <div className="status-dot status-running" />
                  <div className="absolute inset-0 status-dot bg-success animate-ping" />
                </div>
              )}
              {agent.status === 'stopped' && (
                <div className="status-dot status-stopped" />
              )}
              {agent.status === 'starting' && (
                <div className="status-dot status-starting" />
              )}
              {agent.status === 'error' && (
                <div className="status-dot bg-error animate-scale-pulse" />
              )}
            </div>
          </div>
          <div>
            <h3 className="font-semibold text-sm">{agent.name}</h3>
            <p className="text-xs text-text-tertiary">{agent.lastActive}</p>
          </div>
        </div>
        {agent.status === 'running' && (
          <span className="badge badge-success text-[10px]">LIVE</span>
        )}
      </div>

      {/* Stats */}
      <div className="mb-4 p-3 bg-surface-2 rounded-lg">
        <div className="flex items-center justify-between">
          <span className="text-xs text-text-tertiary">{agent.stats.label}</span>
          <span className="text-lg font-display font-bold">{agent.stats.processed}</span>
        </div>
      </div>

      {/* Actions */}
      <div className="grid grid-cols-4 gap-2">
        <button
          onClick={() => onAction(agent.id, 'start')}
          disabled={agent.status === 'running' || actionLoading === `${agent.id}-start`}
          className="btn btn-ghost p-2 disabled:opacity-50 disabled:cursor-not-allowed"
          title="Start"
        >
          {actionLoading === `${agent.id}-start` ? (
            <Loader2 className="w-4 h-4 animate-spin" />
          ) : (
            <Play className="w-4 h-4" />
          )}
        </button>
        <button
          onClick={() => onAction(agent.id, 'stop')}
          disabled={agent.status === 'stopped' || actionLoading === `${agent.id}-stop`}
          className="btn btn-ghost p-2 disabled:opacity-50 disabled:cursor-not-allowed"
          title="Stop"
        >
          {actionLoading === `${agent.id}-stop` ? (
            <Loader2 className="w-4 h-4 animate-spin" />
          ) : (
            <Square className="w-4 h-4" />
          )}
        </button>
        <button
          onClick={() => onAction(agent.id, 'restart')}
          disabled={actionLoading === `${agent.id}-restart`}
          className="btn btn-ghost p-2 disabled:opacity-50 disabled:cursor-not-allowed"
          title="Restart"
        >
          {actionLoading === `${agent.id}-restart` ? (
            <Loader2 className="w-4 h-4 animate-spin" />
          ) : (
            <RotateCw className="w-4 h-4" />
          )}
        </button>
        <button
          className="btn btn-ghost p-2"
          title="View Logs"
        >
          <BarChart2 className="w-4 h-4" />
        </button>
      </div>
    </motion.div>
  );
}
