'use client';

import { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import { Play, Square, RotateCw, FileText, Loader2 } from 'lucide-react';
import { toast } from 'sonner';

interface Agent {
  id: string;
  name: string;
  icon: string;
  status: 'running' | 'stopped' | 'starting';
  lastActive: string;
}

export default function LiveStatus() {
  const [agents, setAgents] = useState<Agent[]>([]);
  const [loading, setLoading] = useState(true);
  const [actionLoading, setActionLoading] = useState<string | null>(null);

  useEffect(() => {
    fetchStatus();
    const interval = setInterval(fetchStatus, 5000);
    return () => clearInterval(interval);
  }, []);

  const fetchStatus = async () => {
    try {
      const res = await fetch('/api/status');
      const data = await res.json();
      setAgents(data.agents || []);
    } catch (error) {
      console.error('Failed to fetch status:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleAction = async (agentId: string, action: 'start' | 'stop' | 'restart') => {
    setActionLoading(`${agentId}-${action}`);
    try {
      const res = await fetch(`/api/agents/${agentId}`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ action }),
      });

      if (res.ok) {
        toast.success(`Agent ${action}ed successfully`);
        fetchStatus();
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
      <div className="card p-6">
        <div className="shimmer h-64 rounded-lg"></div>
      </div>
    );
  }

  return (
    <div className="card p-6">
      <h2 className="font-syne font-bold text-xl text-accent mb-6 flex items-center gap-2">
        <span>🎛️</span>
        Live System Status
      </h2>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        {agents.map((agent) => (
          <motion.div
            key={agent.id}
            whileHover={{ scale: 1.02 }}
            className="bg-surface2 border border-border rounded-lg p-4"
          >
            {/* Agent Header */}
            <div className="flex items-center gap-3 mb-3">
              <div className="text-3xl">{agent.icon}</div>
              <div className="flex-1">
                <div className="font-semibold text-sm">{agent.name}</div>
                <div className="flex items-center gap-2 text-xs mt-1">
                  {agent.status === 'running' && (
                    <span className="flex items-center gap-1 text-accent3">
                      <span className="w-2 h-2 bg-accent3 rounded-full animate-pulse"></span>
                      RUNNING
                    </span>
                  )}
                  {agent.status === 'stopped' && (
                    <span className="flex items-center gap-1 text-danger">
                      <span className="w-2 h-2 bg-danger rounded-full"></span>
                      STOPPED
                    </span>
                  )}
                  {agent.status === 'starting' && (
                    <span className="flex items-center gap-1 text-warn">
                      <Loader2 className="w-3 h-3 animate-spin" />
                      STARTING
                    </span>
                  )}
                </div>
              </div>
            </div>

            {/* Last Active */}
            <div className="text-xs text-muted mb-3">
              Last active: {agent.lastActive}
            </div>

            {/* Control Buttons */}
            <div className="grid grid-cols-4 gap-2">
              <button
                onClick={() => handleAction(agent.id, 'start')}
                disabled={agent.status === 'running' || actionLoading === `${agent.id}-start`}
                className="flex items-center justify-center gap-1 px-2 py-1.5 text-xs bg-accent3/10 text-accent3 rounded hover:bg-accent3/20 disabled:opacity-50 disabled:cursor-not-allowed transition-all"
              >
                {actionLoading === `${agent.id}-start` ? (
                  <Loader2 className="w-3 h-3 animate-spin" />
                ) : (
                  <Play className="w-3 h-3" />
                )}
              </button>
              <button
                onClick={() => handleAction(agent.id, 'stop')}
                disabled={agent.status === 'stopped' || actionLoading === `${agent.id}-stop`}
                className="flex items-center justify-center gap-1 px-2 py-1.5 text-xs bg-danger/10 text-danger rounded hover:bg-danger/20 disabled:opacity-50 disabled:cursor-not-allowed transition-all"
              >
                {actionLoading === `${agent.id}-stop` ? (
                  <Loader2 className="w-3 h-3 animate-spin" />
                ) : (
                  <Square className="w-3 h-3" />
                )}
              </button>
              <button
                onClick={() => handleAction(agent.id, 'restart')}
                disabled={actionLoading === `${agent.id}-restart`}
                className="flex items-center justify-center gap-1 px-2 py-1.5 text-xs bg-accent/10 text-accent rounded hover:bg-accent/20 disabled:opacity-50 disabled:cursor-not-allowed transition-all"
              >
                {actionLoading === `${agent.id}-restart` ? (
                  <Loader2 className="w-3 h-3 animate-spin" />
                ) : (
                  <RotateCw className="w-3 h-3" />
                )}
              </button>
              <button
                className="flex items-center justify-center gap-1 px-2 py-1.5 text-xs bg-muted/10 text-muted rounded hover:bg-muted/20 transition-all"
              >
                <FileText className="w-3 h-3" />
              </button>
            </div>
          </motion.div>
        ))}
      </div>
    </div>
  );
}
