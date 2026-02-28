'use client';

import { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { ChevronDown, Copy, CheckCircle, XCircle, AlertCircle, Shield, Zap, BarChart3, Settings, User, TrendingUp, Mail, MessageCircle } from 'lucide-react';
import { toast } from 'sonner';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';

interface Agent {
  id: string;
  name: string;
  icon: React.ReactNode;
  description: string;
  tags: string[];
  status: 'done' | 'missing' | 'partial' | 'running' | 'scheduled';
  tier: 'bronze' | 'silver' | 'gold' | 'platinum';
  flow: string;
  uptime: string;
  lastActivity: string;
  capabilities: string[];
  prompts?: {
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
    icon: <Mail className="w-5 h-5" />,
    description: 'Monitors Gmail inbox for new emails and creates action items',
    tags: ['MCP', 'Email', 'Watcher'],
    status: 'running',
    tier: 'bronze',
    flow: 'Gmail API → Parse Email → Create Markdown → Save to Vault',
    uptime: '99.8%',
    lastActivity: '2 minutes ago',
    capabilities: ['Email monitoring', 'Urgent detection', 'Basic filtering'],
    prompts: {
      create: 'Create a Gmail watcher agent that monitors inbox every 5 minutes...',
      verify: 'Test the Gmail watcher by sending a test email...',
      test: 'Send test email to verify agent is working correctly...',
    },
  },
  {
    id: 'whatsapp-watcher',
    name: 'WhatsApp Monitor',
    icon: <MessageCircle className="w-5 h-5" />,
    description: 'Monitors WhatsApp Web for incoming messages',
    tags: ['Puppeteer', 'WhatsApp', 'Watcher'],
    status: 'running',
    tier: 'bronze',
    flow: 'WhatsApp Web → Puppeteer → Parse Message → Save to Vault',
    uptime: '99.7%',
    lastActivity: '1 minute ago',
    capabilities: ['Message detection', 'Keyword filtering', 'Reply scheduling'],
    warnings: ['Requires WhatsApp Web to be logged in', 'May break if WhatsApp UI changes'],
    prompts: {
      create: 'Create a WhatsApp watcher using Puppeteer to monitor messages...',
      verify: 'Test WhatsApp watcher by sending a test message...',
    },
  },
  {
    id: 'linkedin-agent',
    name: 'LinkedIn Agent',
    icon: <BarChart3 className="w-5 h-5" />,
    description: 'Creates and schedules LinkedIn posts',
    tags: ['MCP', 'LinkedIn', 'Social'],
    status: 'running',
    tier: 'silver',
    flow: 'Read Draft → Format Post → LinkedIn API → Publish',
    uptime: '99.9%',
    lastActivity: '3 minutes ago',
    capabilities: ['Post automation', 'Engagement tracking', 'Analytics'],
    prompts: {
      create: 'Create a LinkedIn agent that can post content via API...',
      verify: 'Test LinkedIn agent with a draft post...',
    },
  },
  {
    id: 'instagram-agent',
    name: 'Instagram Agent',
    icon: <Zap className="w-5 h-5 bg-gradient-to-r from-purple-500 to-pink-500 text-transparent bg-clip-text" />,
    description: 'Creates and manages Instagram posts and stories',
    tags: ['MCP', 'Instagram', 'Social', 'Media'],
    status: 'running',
    tier: 'gold',
    flow: 'Content → Image Processing → Instagram API → Publish',
    uptime: '99.9%',
    lastActivity: '45 seconds ago',
    capabilities: ['Post automation', 'Story management', 'Engagement tracking'],
    prompts: {
      create: 'Create an Instagram agent that can post content via API...',
      verify: 'Test Instagram agent with a draft post...',
    },
  },
  {
    id: 'orchestrator',
    name: 'Orchestrator',
    icon: <Settings className="w-5 h-5" />,
    description: 'Main coordinator that processes the queue and delegates tasks',
    tags: ['Core', 'Orchestrator', 'Claude', 'Coordination'],
    status: 'running',
    tier: 'bronze',
    flow: 'Read Needs_Action → Analyze → Create Plan → Execute → Move to Done',
    uptime: '100%',
    lastActivity: '30 seconds ago',
    capabilities: ['Task coordination', 'Multi-step execution', 'Error recovery'],
    prompts: {
      create: 'Create an orchestrator that reads from Needs_Action folder...',
      verify: 'Test orchestrator by adding a test file to Needs_Action...',
    },
  },
  {
    id: 'ceo-briefing',
    name: 'CEO Briefing',
    icon: <TrendingUp className="w-5 h-5" />,
    description: 'Automated business reporting and analytics',
    tags: ['Reporting', 'Analytics', 'CEO', 'Business'],
    status: 'scheduled',
    tier: 'gold',
    flow: 'Data Aggregation → Analysis → Report Generation → Delivery',
    uptime: '100%',
    lastActivity: 'Last briefing: 2 days ago',
    capabilities: ['Revenue analysis', 'Bottleneck detection', 'Proactive suggestions'],
    prompts: {
      create: 'Create a CEO briefing generator that analyzes business metrics...',
    },
  },
  {
    id: 'odoo-accounting',
    name: 'Odoo Accounting',
    icon: <BarChart3 className="w-5 h-5" />,
    description: 'Integration with Odoo for accounting and financial management',
    tags: ['Accounting', 'Odoo', 'Finance', 'ERP'],
    status: 'running',
    tier: 'gold',
    flow: 'Transaction Data → Odoo API → Accounting Records → Reports',
    uptime: '99.6%',
    lastActivity: '1 minute ago',
    capabilities: ['Invoice processing', 'Payment tracking', 'Financial reporting'],
    prompts: {
      create: 'Create an Odoo integration for accounting automation...',
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
        return 'from-amber-600 to-amber-800';
      case 'silver':
        return 'from-gray-400 to-gray-600';
      case 'gold':
        return 'from-yellow-400 to-yellow-600';
      case 'platinum':
        return 'from-blue-400 to-cyan-500';
      default:
        return 'from-gray-500 to-gray-700';
    }
  };

  const getStatusBadge = (status: string) => {
    switch (status) {
      case 'done':
        return (
          <Badge className="bg-green-500/20 text-green-400">
            <CheckCircle className="w-3 h-3 mr-1" />
            DONE
          </Badge>
        );
      case 'missing':
        return (
          <Badge className="bg-red-500/20 text-red-400">
            <XCircle className="w-3 h-3 mr-1" />
            MISSING
          </Badge>
        );
      case 'partial':
        return (
          <Badge className="bg-yellow-500/20 text-yellow-400">
            <AlertCircle className="w-3 h-3 mr-1" />
            PARTIAL
          </Badge>
        );
      case 'running':
        return (
          <Badge className="bg-blue-500/20 text-blue-400">
            <div className="w-2 h-2 rounded-full bg-blue-400 animate-pulse mr-1"></div>
            RUNNING
          </Badge>
        );
      case 'scheduled':
        return (
          <Badge className="bg-purple-500/20 text-purple-400">
            <div className="w-2 h-2 rounded-full bg-purple-400 mr-1"></div>
            SCHEDULED
          </Badge>
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
    <Card className="glass-card">
      <CardHeader>
        <CardTitle className="flex items-center justify-between">
          <div>
            <span className="text-lg font-bold capitalize">{tier} Tier Agents</span>
            <p className="text-sm text-muted mt-1">AI Employee automation components</p>
          </div>
          <Badge className={`bg-gradient-to-r ${getTierColor(tier)}`}>
            {tier.toUpperCase()}
          </Badge>
        </CardTitle>
      </CardHeader>
      <CardContent>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          {filteredAgents.map((agent) => {
            const isExpanded = expandedId === agent.id;
            const statusIcon = agent.status === 'running' ? <div className="w-2 h-2 rounded-full bg-green-500 animate-pulse"></div> :
                             agent.status === 'scheduled' ? <div className="w-2 h-2 rounded-full bg-blue-500"></div> :
                             <div className="w-2 h-2 rounded-full bg-gray-500"></div>;

            return (
              <div key={agent.id} className="border border-border rounded-lg">
                {/* Card Header */}
                <button
                  onClick={() => setExpandedId(isExpanded ? null : agent.id)}
                  className="w-full p-4 flex items-start gap-3 text-left hover:bg-white/5 transition-colors"
                >
                  {/* Icon */}
                  <div className="p-2 rounded-lg bg-white/10">
                    {agent.icon}
                  </div>

                  {/* Content */}
                  <div className="flex-1">
                    <div className="flex items-center justify-between mb-1">
                      <h3 className="font-semibold text-sm">{agent.name}</h3>
                      {getStatusBadge(agent.status)}
                    </div>
                    <p className="text-xs text-muted mb-2">{agent.description}</p>

                    {/* Stats */}
                    <div className="flex items-center gap-4 text-xs text-muted mb-2">
                      <div className="flex items-center gap-1">
                        <span className="font-medium">Uptime:</span>
                        <span>{agent.uptime}</span>
                      </div>
                      <div className="flex items-center gap-1">
                        <span className="font-medium">Last:</span>
                        <span>{agent.lastActivity}</span>
                      </div>
                    </div>

                    {/* Tags */}
                    <div className="flex flex-wrap gap-1">
                      {agent.tags.map((tag, index) => (
                        <span
                          key={index}
                          className="text-xs px-2 py-0.5 bg-white/5 text-muted rounded font-medium"
                        >
                          {tag}
                        </span>
                      ))}
                    </div>
                  </div>

                  {/* Expand Arrow */}
                  <ChevronDown
                    className={`w-4 h-4 text-muted transition-transform flex-shrink-0 ${
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
                      <div className="p-4 space-y-4">
                        {/* Capabilities */}
                        <div>
                          <h4 className="text-xs font-semibold uppercase text-muted mb-2">Capabilities</h4>
                          <div className="space-y-1">
                            {agent.capabilities.map((capability, index) => (
                              <div key={index} className="flex items-center gap-2 text-xs">
                                <div className="w-1 h-1 rounded-full bg-gray-400"></div>
                                <span>{capability}</span>
                              </div>
                            ))}
                          </div>
                        </div>

                        {/* Flow */}
                        <div>
                          <h4 className="text-xs font-semibold uppercase text-muted mb-2">Process Flow</h4>
                          <p className="text-xs text-muted">{agent.flow}</p>
                        </div>

                        {/* Prompts */}
                        {agent.prompts && Object.keys(agent.prompts).length > 0 && (
                          <div>
                            <div className="flex gap-2 mb-3">
                              {Object.keys(agent.prompts).map((tab) => (
                                <button
                                  key={tab}
                                  onClick={() => setActiveTab(tab as any)}
                                  className={`px-3 py-1 text-xs font-semibold rounded transition-all ${
                                    activeTab === tab
                                      ? 'bg-accent text-black'
                                      : 'bg-white/5 text-muted hover:text-text'
                                  }`}
                                >
                                  {tab}
                                </button>
                              ))}
                            </div>

                            {/* Prompt Box */}
                            <div className="relative">
                              <div className="p-3 bg-white/5 rounded text-xs whitespace-pre-wrap font-mono">
                                {agent.prompts?.[activeTab]}
                              </div>
                              <button
                                onClick={() => copyToClipboard(agent.prompts?.[activeTab] || '')}
                                className="absolute top-2 right-2 p-1.5 bg-white/10 hover:bg-white/20 rounded transition-all"
                              >
                                <Copy className="w-3 h-3" />
                              </button>
                            </div>
                          </div>
                        )}

                        {/* Warnings */}
                        {agent.warnings && agent.warnings.length > 0 && (
                          <div className="bg-yellow-500/10 border border-yellow-500/30 rounded p-3">
                            <div className="flex items-start gap-2">
                              <AlertCircle className="w-4 h-4 text-yellow-500 flex-shrink-0 mt-0.5" />
                              <div className="space-y-1">
                                {agent.warnings.map((warning, index) => (
                                  <p key={index} className="text-xs text-yellow-500">
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
              </div>
            );
          })}
        </div>

        {filteredAgents.length === 0 && (
          <div className="text-center py-8 text-muted">
            <p>No agents configured for this tier yet</p>
          </div>
        )}
      </CardContent>
    </Card>
  );
}
