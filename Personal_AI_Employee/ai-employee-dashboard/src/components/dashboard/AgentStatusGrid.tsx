'use client';

import { motion } from 'framer-motion';
import { Mail, MessageCircle, Briefcase, FileText, Settings, Play, Square, RotateCw, Eye } from 'lucide-react';
import { useState, useEffect } from 'react';
import { Button } from '@/components/ui/button';
import { toast } from 'sonner';
import { formatDistanceToNow } from 'date-fns';

interface Agent {
  id: string;
  name: string;
  icon: string;
  status: 'running' | 'stopped' | 'starting';
  lastActivity: Date;
}

const agentIcons = {
  gmail: Mail,
  whatsapp: MessageCircle,
  linkedin: Briefcase,
  file: FileText,
  orchestrator: Settings,
};

export function AgentStatusGrid() {
  const [agents, setAgents] = useState<Agent[]>([
    { id: 'gmail', name: 'Gmail Watcher', icon: '📧', status: 'running', lastActivity: new Date() },
    { id: 'whatsapp', name: 'WhatsApp Monitor', icon: '💬', status: 'running', lastActivity: new Date() },
    { id: 'linkedin', name: 'LinkedIn Agent', icon: '💼', status: 'stopped', lastActivity: new Date(Date.now() - 3600000) },
    { id: 'file', name: 'File Watcher', icon: '📂', status: 'running', lastActivity: new Date() },
    { id: 'orchestrator', name: 'Orchestrator', icon: '🎛️', status: 'running', lastActivity: new Date() },
  ]);

  const [loadingAgent, setLoadingAgent] = useState<string | null>(null);

  const handleAgentAction = async (agentId: string, action: 'start' | 'stop' | 'restart') => {
    setLoadingAgent(agentId);
    try {
      const res = await fetch(`/api/agents/${agentId}/action`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ action }),
      });

      if (res.ok) {
        toast.success(`Agent ${action}ed successfully`);
        // Update agent status
        setAgents(prev =>
          prev.map(agent =>
            agent.id === agentId
              ? { ...agent, status: action === 'stop' ? 'stopped' : 'starting' }
              : agent
          )
        );
      } else {
        toast.error(`Failed to ${action} agent`);
      }
    } catch (error) {
      toast.error(`Error: ${error}`);
    } finally {
      setLoadingAgent(null);
    }
  };

  return (
    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
      {agents.map((agent, index) => {
        const IconComponent = agentIcons[agent.id as keyof typeof agentIcons];
        const isLoading = loadingAgent === agent.id;

        return (
          <motion.div
            key={agent.id}
            initial={{ opacity: 0, scale: 0.9 }}
            animate={{ opacity: 1, scale: 1 }}
            transition={{ delay: index * 0.1 }}
            whileHover={{ scale: 1.02 }}
            className="relative p-6 rounded-xl border border-border bg-surface backdrop-blur-sm hover:shadow-glow transition-all duration-300"
          >
            {/* Status Indicator */}
            <div className="absolute top-4 right-4">
              {agent.status === 'running' && (
                <div className="relative">
                  <div className="w-3 h-3 bg-success rounded-full animate-pulse-slow" />
                  <div className="absolute inset-0 w-3 h-3 bg-success rounded-full animate-ping opacity-75" />
                </div>
              )}
              {agent.status === 'stopped' && (
                <div className="w-3 h-3 bg-danger rounded-full" />
              )}
              {agent.status === 'starting' && (
                <div className="w-3 h-3 bg-warning rounded-full animate-pulse" />
              )}
            </div>

            {/* Agent Info */}
            <div className="flex items-start gap-4 mb-4">
              <div className="text-4xl">{agent.icon}</div>
              <div className="flex-1">
                <h3 className="text-lg font-semibold text-text-primary mb-1">
                  {agent.name}
                </h3>
                <p className="text-sm text-text-secondary">
                  {agent.status === 'running' && (
                    <span className="text-success">● Running</span>
                  )}
                  {agent.status === 'stopped' && (
                    <span className="text-danger">● Stopped</span>
                  )}
                  {agent.status === 'starting' && (
                    <span className="text-warning">● Starting...</span>
                  )}
                </p>
                <p className="text-xs text-text-tertiary mt-1 font-mono">
                  {formatDistanceToNow(agent.lastActivity, { addSuffix: true })}
                </p>
              </div>
            </div>

            {/* Action Buttons */}
            <div className="flex gap-2">
              {agent.status === 'stopped' ? (
                <Button
                  size="sm"
                  onClick={() => handleAgentAction(agent.id, 'start')}
                  disabled={isLoading}
                  className="flex-1 bg-success hover:bg-success/80"
                >
                  {isLoading ? (
                    <RotateCw className="w-4 h-4 animate-spin" />
                  ) : (
                    <>
                      <Play className="w-4 h-4 mr-1" />
                      Start
                    </>
                  )}
                </Button>
              ) : (
                <>
                  <Button
                    size="sm"
                    variant="outline"
                    onClick={() => handleAgentAction(agent.id, 'stop')}
                    disabled={isLoading}
                    className="flex-1"
                  >
                    {isLoading ? (
                      <RotateCw className="w-4 h-4 animate-spin" />
                    ) : (
                      <>
                        <Square className="w-4 h-4 mr-1" />
                        Stop
                      </>
                    )}
                  </Button>
                  <Button
                    size="sm"
                    variant="outline"
                    onClick={() => handleAgentAction(agent.id, 'restart')}
                    disabled={isLoading}
                    className="flex-1"
                  >
                    <RotateCw className="w-4 h-4 mr-1" />
                    Restart
                  </Button>
                </>
              )}
              <Button size="sm" variant="ghost" className="px-3">
                <Eye className="w-4 h-4" />
              </Button>
            </div>
          </motion.div>
        );
      })}
    </div>
  );
}
