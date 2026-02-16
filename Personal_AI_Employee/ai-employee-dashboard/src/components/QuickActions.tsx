'use client';

import { useState } from 'react';
import { motion } from 'framer-motion';
import { Inbox, FileText, Mail, Linkedin, Activity, RefreshCw, Loader2, CheckCircle, XCircle } from 'lucide-react';
import { toast } from 'sonner';

interface Action {
  id: string;
  icon: any;
  label: string;
  description: string;
  endpoint: string;
  color: string;
}

const actions: Action[] = [
  {
    id: 'process-queue',
    icon: Inbox,
    label: 'Process Queue',
    description: 'Trigger orchestrator',
    endpoint: '/api/actions/process-queue',
    color: 'bg-accent text-black',
  },
  {
    id: 'generate-briefing',
    icon: FileText,
    label: 'CEO Briefing',
    description: 'Generate report',
    endpoint: '/api/briefing/generate',
    color: 'bg-accent2 text-white',
  },
  {
    id: 'test-email',
    icon: Mail,
    label: 'Test Email',
    description: 'Send test via MCP',
    endpoint: '/api/test/email',
    color: 'bg-accent3 text-black',
  },
  {
    id: 'test-linkedin',
    icon: Linkedin,
    label: 'Test LinkedIn',
    description: 'Create test post',
    endpoint: '/api/test/linkedin',
    color: 'bg-warn text-black',
  },
  {
    id: 'health-check',
    icon: Activity,
    label: 'Health Check',
    description: 'Monitor services',
    endpoint: '/api/health',
    color: 'bg-accent3 text-black',
  },
  {
    id: 'sync-dashboard',
    icon: RefreshCw,
    label: 'Sync Dashboard',
    description: 'Refresh all data',
    endpoint: '/api/status',
    color: 'bg-accent text-black',
  },
];

export default function QuickActions() {
  const [loadingAction, setLoadingAction] = useState<string | null>(null);
  const [actionStatus, setActionStatus] = useState<Record<string, 'success' | 'error' | null>>({});

  const handleAction = async (action: Action) => {
    setLoadingAction(action.id);
    setActionStatus({ ...actionStatus, [action.id]: null });

    try {
      const res = await fetch(action.endpoint, {
        method: 'POST',
      });

      if (res.ok) {
        setActionStatus({ ...actionStatus, [action.id]: 'success' });
        toast.success(`${action.label} completed successfully`);
        setTimeout(() => {
          setActionStatus({ ...actionStatus, [action.id]: null });
        }, 2000);
      } else {
        setActionStatus({ ...actionStatus, [action.id]: 'error' });
        toast.error(`Failed to execute ${action.label}`);
      }
    } catch (error) {
      setActionStatus({ ...actionStatus, [action.id]: 'error' });
      toast.error(`Error: ${error}`);
    } finally {
      setLoadingAction(null);
    }
  };

  return (
    <div className="card p-6">
      <h2 className="font-syne font-bold text-xl text-accent mb-6 flex items-center gap-2">
        <span>⚡</span>
        Quick Actions
      </h2>

      <div className="grid grid-cols-2 gap-4">
        {actions.map((action) => {
          const Icon = action.icon;
          const isLoading = loadingAction === action.id;
          const status = actionStatus[action.id];

          return (
            <motion.button
              key={action.id}
              whileHover={{ scale: 1.02, y: -2 }}
              whileTap={{ scale: 0.98 }}
              onClick={() => handleAction(action)}
              disabled={isLoading}
              className={`${action.color} rounded-lg p-4 text-left transition-all duration-200 hover:shadow-lg disabled:opacity-50 disabled:cursor-not-allowed relative overflow-hidden`}
            >
              <div className="flex items-start gap-3">
                <div className="mt-1">
                  {isLoading ? (
                    <Loader2 className="w-5 h-5 animate-spin" />
                  ) : status === 'success' ? (
                    <CheckCircle className="w-5 h-5" />
                  ) : status === 'error' ? (
                    <XCircle className="w-5 h-5" />
                  ) : (
                    <Icon className="w-5 h-5" />
                  )}
                </div>
                <div className="flex-1">
                  <div className="font-semibold text-sm mb-1">{action.label}</div>
                  <div className="text-xs opacity-80">{action.description}</div>
                </div>
              </div>

              {isLoading && (
                <div className="absolute bottom-0 left-0 right-0 h-1 bg-white/20">
                  <motion.div
                    initial={{ width: 0 }}
                    animate={{ width: '100%' }}
                    transition={{ duration: 2 }}
                    className="h-full bg-white/50"
                  />
                </div>
              )}
            </motion.button>
          );
        })}
      </div>
    </div>
  );
}
