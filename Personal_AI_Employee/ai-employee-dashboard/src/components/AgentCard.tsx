'use client';

import { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { ChevronDown, Copy, CheckCircle, XCircle, AlertCircle } from 'lucide-react';
import { toast } from 'sonner';

interface Agent {
  id: string;
  name: string;
  icon: string;
  description: string;
  tags: string[];
  status: 'done' | 'missing' | 'partial';
  tier: 'bronze' | 'silver' | 'gold' | 'platinum';
  flow: string;
  prompts: {
    create?: string;
    verify?: string;
    test?: string;
  };
  warnings?: string[];
}

const agentsData: Agent[] = [
  {
    id: 'gmail-watcher',
    name: 'Gmail Watcher',
    icon: '📧',
    description: 'Monitors Gmail inbox for new emails and creates action items',
    tags: ['MCP', 'Email', 'Watcher'],
    status: 'done',
    tier: 'bronze',
    flow: 'Gmail API → Parse Email → Create Markdown → Save to Vault',
    prompts: {
      create: 'Create a Gmail watcher agent that monitors inbox every 5 minutes...',
      verify: 'Test the Gmail watcher by sending a test email...',
      test: 'Send test email to verify agent is working correctly...',
    },
  },
  {
    id: 'whatsapp-watcher',
    name: 'WhatsApp Watcher',
    icon: '💬',
    description: 'Monitors WhatsApp Web for incoming messages',
    tags: ['Puppeteer', 'WhatsApp', 'Watcher'],
    status: 'done',
    tier: 'bronze',
    flow: 'WhatsApp Web → Puppeteer → Parse Message → Save to Vault',
    prompts: {
      create: 'Create a WhatsApp watcher using Puppeteer to monitor messages...',
      verify: 'Test WhatsApp watcher by sending a test message...',
    },
    warnings: ['Requires WhatsApp Web to be logged in', 'May break if WhatsApp UI changes'],
  },
  {
    id: 'linkedin-agent',
    name: 'LinkedIn Agent',
    icon: '💼',
    description: 'Creates and schedules LinkedIn posts',
    tags: ['MCP', 'LinkedIn', 'Social'],
    status: 'partial',
    tier: 'silver',
    flow: 'Read Draft → Format Post → LinkedIn API → Publish',
    prompts: {
      create: 'Create a LinkedIn agent that can post content via API...',
      verify: 'Test LinkedIn agent with a draft post...',
    },
  },
  {
    id: 'orchestrator',
    name: 'Orchestrator',
    icon: '🎛️',
    description: 'Main coordinator that processes the queue and delegates tasks',
    tags: ['Core', 'Orchestrator', 'Claude'],
    status: 'done',
    tier: 'bronze',
    flow: 'Read Needs_Action → Analyze → Create Plan → Execute → Move to Done',
    prompts: {
      create: 'Create an orchestrator that reads from Needs_Action folder...',
      verify: 'Test orchestrator by adding a test file to Needs_Action...',
    },
  },
];

interface AgentCardProps {
  tier: 'bronze' | 'silver' | 'gold' | 'platinum';
}

export default function AgentCard({ tier }: AgentCardProps) {
  const [expandedId, setExpandedId] = useState<string | null>(null);
  const [activeTab, setActiveTab] = useState<'create' | 'verify' | 'test'>('create');

  const filteredAgents = agentsData.filter((agent) => agent.tier === tier);

  const getTierColor = (tier: string) => {
    switch (tier) {
      case 'bronze':
        return 'bronze';
      case 'silver':
        return 'silver';
      case 'gold':
        return 'gold';
      case 'platinum':
        return 'platinum';
      default:
        return 'accent';
    }
  };

  const getStatusBadge = (status: string) => {
    switch (status) {
      case 'done':
        return (
          <span className="flex items-center gap-1 text-xs px-2 py-1 bg-accent3/10 text-accent3 rounded-full">
            <CheckCircle className="w-3 h-3" />
            DONE
          </span>
        );
      case 'missing':
        return (
          <span className="flex items-center gap-1 text-xs px-2 py-1 bg-danger/10 text-danger rounded-full">
            <XCircle className="w-3 h-3" />
            MISSING
          </span>
        );
      case 'partial':
        return (
          <span className="flex items-center gap-1 text-xs px-2 py-1 bg-warn/10 text-warn rounded-full">
            <AlertCircle className="w-3 h-3" />
            PARTIAL
          </span>
        );
      default:
        return null;
    }
  };

  const copyToClipboard = (text: string) => {
    navigator.clipboard.writeText(text);
    toast.success('Copied to clipboard!');
  };

  return (
    <div className="space-y-4">
      {filteredAgents.map((agent) => {
        const tierColor = getTierColor(agent.tier);
        const isExpanded = expandedId === agent.id;

        return (
          <motion.div
            key={agent.id}
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            className="agent-card"
          >
            {/* Card Header */}
            <button
              onClick={() => setExpandedId(isExpanded ? null : agent.id)}
              className="w-full p-6 flex items-start gap-4 hover:bg-surface2 transition-colors"
            >
              {/* Icon */}
              <div
                className={`w-11 h-11 rounded-lg bg-${tierColor}/10 flex items-center justify-center text-2xl flex-shrink-0`}
              >
                {agent.icon}
              </div>

              {/* Content */}
              <div className="flex-1 text-left">
                <div className="flex items-center gap-2 mb-2">
                  <h3 className="font-syne font-bold text-base">{agent.name}</h3>
                  {getStatusBadge(agent.status)}
                </div>
                <p className="text-xs text-muted mb-3">{agent.description}</p>
                <div className="flex flex-wrap gap-2">
                  {agent.tags.map((tag) => (
                    <span
                      key={tag}
                      className="text-[10px] px-2 py-1 bg-surface2 text-muted rounded uppercase font-semibold"
                    >
                      {tag}
                    </span>
                  ))}
                </div>
              </div>

              {/* Expand Arrow */}
              <ChevronDown
                className={`w-5 h-5 text-muted transition-transform flex-shrink-0 ${
                  isExpanded ? 'rotate-180' : ''
                }`}
              />
            </button>

            {/* Card Body */}
            <AnimatePresence>
              {isExpanded && (
                <motion.div
                  initial={{ height: 0, opacity: 0 }}
                  animate={{ height: 'auto', opacity: 1 }}
                  exit={{ height: 0, opacity: 0 }}
                  transition={{ duration: 0.3 }}
                  className="border-t border-border overflow-hidden"
                >
                  <div className="p-6 space-y-6">
                    {/* Flow */}
                    <div>
                      <div className="flex items-center gap-2 mb-3">
                        <div className={`w-2 h-2 rounded-full bg-${tierColor}`}></div>
                        <span className="text-xs text-muted uppercase font-semibold">
                          Flow
                        </span>
                      </div>
                      <p className="text-sm text-text">{agent.flow}</p>
                    </div>

                    {/* Tabs */}
                    <div>
                      <div className="flex gap-2 mb-4">
                        {Object.keys(agent.prompts).map((tab) => (
                          <button
                            key={tab}
                            onClick={() => setActiveTab(tab as any)}
                            className={`px-4 py-2 text-xs font-semibold uppercase rounded-lg transition-all ${
                              activeTab === tab
                                ? 'bg-accent text-black'
                                : 'bg-surface2 text-muted hover:text-text'
                            }`}
                          >
                            {tab}
                          </button>
                        ))}
                      </div>

                      {/* Prompt Box */}
                      <div className="relative">
                        <div className="prompt-box">
                          <pre className="whitespace-pre-wrap">
                            {agent.prompts[activeTab]}
                          </pre>
                        </div>
                        <button
                          onClick={() => copyToClipboard(agent.prompts[activeTab] || '')}
                          className="absolute top-3 right-3 p-2 bg-accent/10 hover:bg-accent hover:text-black text-accent rounded transition-all"
                        >
                          <Copy className="w-4 h-4" />
                        </button>
                      </div>
                    </div>

                    {/* Warnings */}
                    {agent.warnings && agent.warnings.length > 0 && (
                      <div className="bg-warn/10 border border-warn/30 rounded-lg p-4">
                        <div className="flex items-start gap-2">
                          <AlertCircle className="w-4 h-4 text-warn flex-shrink-0 mt-0.5" />
                          <div className="space-y-1">
                            {agent.warnings.map((warning, index) => (
                              <p key={index} className="text-xs text-warn">
                                {warning}
                              </p>
                            ))}
                          </div>
                        </div>
                      </div>
                    )}
                  </div>
                </motion.div>
              )}
            </AnimatePresence>
          </motion.div>
        );
      })}

      {filteredAgents.length === 0 && (
        <div className="card p-12 text-center">
          <p className="text-muted">No agents in this tier yet</p>
        </div>
      )}
    </div>
  );
}
