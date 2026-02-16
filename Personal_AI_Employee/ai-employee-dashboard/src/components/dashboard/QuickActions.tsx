'use client';

import { useState } from 'react';
import { motion } from 'framer-motion';
import {
  Inbox,
  FileText,
  Mail,
  Linkedin,
  Activity,
  RefreshCw,
  Loader2,
  CheckCircle,
  XCircle,
} from 'lucide-react';
import { toast } from 'sonner';

interface Action {
  id: string;
  icon: any;
  label: string;
  description: string;
  endpoint: string;
}

const actions: Action[] = [
  {
    id: 'process-queue',
    icon: Inbox,
    label: 'Process Queue',
    description: 'Trigger orchestrator',
    endpoint: '/api/actions/process-queue',
  },
  {
    id: 'generate-briefing',
    icon: FileText,
    label: 'CEO Briefing',
    description: 'Generate report',
    endpoint: '/api/briefing/generate',
  },
  {
    id: 'test-email',
    icon: Mail,
    label: 'Test Email',
    description: 'Send via MCP',
    endpoint: '/api/test/email',
  },
  {
    id: 'test-linkedin',
    icon: Linkedin,
    label: 'Test LinkedIn',
    description: 'Create post',
    endpoint: '/api/test/linkedin',
  },
  {
    id: 'health-check',
    icon: Activity,
    label: 'Health Check',
    description: 'Monitor services',
    endpoint: '/api/health',
  },
  {
    id: 'sync-dashboard',
    icon: RefreshCw,
    label: 'Sync Data',
    description: 'Refresh all',
    endpoint: '/api/dashboard',
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
        toast.success(`${action.label} completed`);
        setTimeout(() => {
          setActionStatus({ ...actionStatus, [action.id]: null });
        }, 2000);
      } else {
        setActionStatus({ ...actionStatus, [action.id]: 'error' });
        toast.error(`Failed: ${action.label}`);
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
      <h2 className="text-lg font-display font-semibold mb-4">Quick Actions</h2>

      <div className="space-y-2">
        {actions.map((action, index) => {
          const Icon = action.icon;
          const isLoading = loadingAction === action.id;
          const status = actionStatus[action.id];

          return (
            <motion.button
              key={action.id}
              initial={{ opacity: 0, y: 10 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.2, delay: index * 0.05 }}
              onClick={() => handleAction(action)}
              disabled={isLoading}
              className="w-full flex items-center gap-3 p-3 rounded-lg bg-surface-2 hover:bg-surface-3 transition-all duration-200 disabled:opacity-50 disabled:cursor-not-allowed group relative overflow-hidden"
            >
              {/* Icon */}
              <div className="w-10 h-10 rounded-lg bg-surface-3 flex items-center justify-center flex-shrink-0 group-hover:scale-110 transition-transform">
                {isLoading ? (
                  <Loader2 className="w-5 h-5 animate-spin text-brand-primary" />
                ) : status === 'success' ? (
                  <CheckCircle className="w-5 h-5 text-success" />
                ) : status === 'error' ? (
                  <XCircle className="w-5 h-5 text-error" />
                ) : (
                  <Icon className="w-5 h-5 text-text-secondary group-hover:text-brand-primary transition-colors" />
                )}
              </div>

              {/* Content */}
              <div className="flex-1 text-left">
                <div className="font-semibold text-sm">{action.label}</div>
                <div className="text-xs text-text-tertiary">{action.description}</div>
              </div>

              {/* Progress Bar */}
              {isLoading && (
                <motion.div
                  initial={{ width: 0 }}
                  animate={{ width: '100%' }}
                  transition={{ duration: 2 }}
                  className="absolute bottom-0 left-0 h-0.5 bg-brand-primary"
                />
              )}
            </motion.button>
          );
        })}
      </div>
    </div>
  );
}
