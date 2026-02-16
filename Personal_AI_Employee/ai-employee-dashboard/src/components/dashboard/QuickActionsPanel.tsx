'use client';

import { motion } from 'framer-motion';
import { Zap, FileText, Mail, Linkedin, Activity, Loader2 } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { useState } from 'react';
import { toast } from 'sonner';

interface Action {
  id: string;
  label: string;
  description: string;
  icon: any;
  color: string;
  endpoint: string;
}

const actions: Action[] = [
  {
    id: 'process-queue',
    label: 'Process Needs Action',
    description: 'Trigger orchestrator to process pending items',
    icon: Zap,
    color: 'bg-primary hover:bg-primary/80',
    endpoint: '/api/actions/process-queue',
  },
  {
    id: 'generate-briefing',
    label: 'Generate CEO Briefing',
    description: 'Create executive summary report',
    icon: FileText,
    color: 'bg-secondary hover:bg-secondary/80',
    endpoint: '/api/briefing/generate',
  },
  {
    id: 'test-email',
    label: 'Test Email MCP',
    description: 'Send a test email via MCP',
    icon: Mail,
    color: 'bg-accent hover:bg-accent/80',
    endpoint: '/api/test/email',
  },
  {
    id: 'test-linkedin',
    label: 'Test LinkedIn Post',
    description: 'Create a test LinkedIn post draft',
    icon: Linkedin,
    color: 'bg-warning hover:bg-warning/80',
    endpoint: '/api/test/linkedin',
  },
  {
    id: 'health-check',
    label: 'Health Check All',
    description: 'Run health monitor on all services',
    icon: Activity,
    color: 'bg-success hover:bg-success/80',
    endpoint: '/api/health',
  },
];

export function QuickActionsPanel() {
  const [loadingAction, setLoadingAction] = useState<string | null>(null);

  const handleAction = async (action: Action) => {
    setLoadingAction(action.id);
    try {
      const res = await fetch(action.endpoint, {
        method: 'POST',
      });

      if (res.ok) {
        const data = await res.json();
        toast.success(data.message || `${action.label} completed successfully`);
      } else {
        toast.error(`Failed to execute ${action.label}`);
      }
    } catch (error) {
      toast.error(`Error: ${error}`);
    } finally {
      setLoadingAction(null);
    }
  };

  return (
    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-5 gap-4">
      {actions.map((action, index) => {
        const Icon = action.icon;
        const isLoading = loadingAction === action.id;

        return (
          <motion.div
            key={action.id}
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: index * 0.1 }}
            whileHover={{ scale: 1.05, y: -4 }}
            whileTap={{ scale: 0.98 }}
          >
            <Button
              onClick={() => handleAction(action)}
              disabled={isLoading}
              className={`w-full h-auto p-6 flex flex-col items-center gap-3 ${action.color} text-white border-0 shadow-lg hover:shadow-xl transition-all duration-300`}
            >
              {isLoading ? (
                <Loader2 className="w-8 h-8 animate-spin" />
              ) : (
                <Icon className="w-8 h-8" />
              )}
              <div className="text-center">
                <div className="font-semibold text-sm mb-1">{action.label}</div>
                <div className="text-xs opacity-90 font-normal">
                  {action.description}
                </div>
              </div>
            </Button>
          </motion.div>
        );
      })}
    </div>
  );
}
