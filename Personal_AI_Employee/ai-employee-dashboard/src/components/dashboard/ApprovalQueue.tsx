'use client';

import { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { Check, X, ChevronDown, ChevronUp, Mail, CreditCard, FileText, Loader2, CheckCircle } from 'lucide-react';
import { toast } from 'sonner';
import { formatDistanceToNow } from 'date-fns';

interface Approval {
  id: string;
  type: 'email' | 'payment' | 'post' | 'file';
  title: string;
  preview: string;
  priority: 'high' | 'normal' | 'low';
  requestedAt: string;
  amount?: string;
}

export default function ApprovalQueue() {
  const [approvals, setApprovals] = useState<Approval[]>([]);
  const [loading, setLoading] = useState(true);
  const [expandedId, setExpandedId] = useState<string | null>(null);
  const [actionLoading, setActionLoading] = useState<string | null>(null);

  useEffect(() => {
    fetchApprovals();
    const interval = setInterval(fetchApprovals, 5000);
    return () => clearInterval(interval);
  }, []);

  const fetchApprovals = async () => {
    try {
      const res = await fetch('/api/approvals');
      const data = await res.json();
      setApprovals(data || []);
    } catch (error) {
      console.error('Failed to fetch approvals:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleAction = async (id: string, action: 'approve' | 'reject') => {
    setActionLoading(`${id}-${action}`);
    try {
      const res = await fetch(`/api/approvals/${id}/action`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ action }),
      });

      if (res.ok) {
        toast.success(`Item ${action}d successfully`);
        setApprovals(approvals.filter((a) => a.id !== id));
      } else {
        toast.error(`Failed to ${action} item`);
      }
    } catch (error) {
      toast.error(`Error: ${error}`);
    } finally {
      setActionLoading(null);
    }
  };

  const getTypeIcon = (type: string) => {
    switch (type) {
      case 'email':
        return <Mail className="w-4 h-4" />;
      case 'payment':
        return <CreditCard className="w-4 h-4" />;
      case 'post':
        return <FileText className="w-4 h-4" />;
      case 'file':
        return <FileText className="w-4 h-4" />;
      default:
        return <FileText className="w-4 h-4" />;
    }
  };

  const getPriorityBadge = (priority: string) => {
    const classes = {
      high: 'badge-error',
      normal: 'badge-info',
      low: 'badge-success',
    };
    return classes[priority as keyof typeof classes] || 'badge-info';
  };

  if (loading) {
    return (
      <div className="card p-6">
        <div className="skeleton h-64" />
      </div>
    );
  }

  return (
    <div className="card p-6">
      <div className="flex items-center justify-between mb-4">
        <h2 className="text-lg font-display font-semibold">Approval Queue</h2>
        <span className="badge badge-warning">{approvals.length} pending</span>
      </div>

      {approvals.length === 0 ? (
        <div className="text-center py-12 text-text-tertiary">
          <CheckCircle className="w-12 h-12 mx-auto mb-3 opacity-50" />
          <p className="text-sm">No pending approvals</p>
        </div>
      ) : (
        <div className="space-y-2">
          <AnimatePresence>
            {approvals.map((approval, index) => (
              <motion.div
                key={approval.id}
                initial={{ opacity: 0, y: 10 }}
                animate={{ opacity: 1, y: 0 }}
                exit={{ opacity: 0, x: -20 }}
                transition={{ duration: 0.2, delay: index * 0.05 }}
                className="border border-border rounded-lg overflow-hidden"
              >
                {/* Header */}
                <button
                  onClick={() =>
                    setExpandedId(expandedId === approval.id ? null : approval.id)
                  }
                  className="w-full flex items-center gap-3 p-4 hover:bg-surface-2 transition-colors"
                >
                  <div className="w-10 h-10 rounded-lg bg-surface-2 flex items-center justify-center flex-shrink-0">
                    {getTypeIcon(approval.type)}
                  </div>
                  <div className="flex-1 text-left min-w-0">
                    <div className="flex items-center gap-2 mb-1">
                      <span className="font-semibold text-sm truncate">
                        {approval.title}
                      </span>
                      <span className={`badge ${getPriorityBadge(approval.priority)}`}>
                        {approval.priority}
                      </span>
                    </div>
                    <p className="text-xs text-text-tertiary">
                      {formatDistanceToNow(new Date(approval.requestedAt), {
                        addSuffix: true,
                      })}
                    </p>
                  </div>
                  {approval.amount && (
                    <span className="font-mono font-semibold text-sm">
                      {approval.amount}
                    </span>
                  )}
                  {expandedId === approval.id ? (
                    <ChevronUp className="w-4 h-4 text-text-tertiary" />
                  ) : (
                    <ChevronDown className="w-4 h-4 text-text-tertiary" />
                  )}
                </button>

                {/* Expanded Content */}
                <AnimatePresence>
                  {expandedId === approval.id && (
                    <motion.div
                      initial={{ height: 0, opacity: 0 }}
                      animate={{ height: 'auto', opacity: 1 }}
                      exit={{ height: 0, opacity: 0 }}
                      transition={{ duration: 0.2 }}
                      className="border-t border-border"
                    >
                      <div className="p-4 space-y-4">
                        {/* Preview */}
                        <div className="bg-surface-2 rounded-lg p-3">
                          <p className="text-sm text-text-secondary font-mono whitespace-pre-wrap">
                            {approval.preview}
                          </p>
                        </div>

                        {/* Actions */}
                        <div className="flex gap-2">
                          <button
                            onClick={() => handleAction(approval.id, 'approve')}
                            disabled={actionLoading === `${approval.id}-approve`}
                            className="btn btn-primary flex-1 disabled:opacity-50 disabled:cursor-not-allowed"
                          >
                            {actionLoading === `${approval.id}-approve` ? (
                              <Loader2 className="w-4 h-4 animate-spin" />
                            ) : (
                              <>
                                <Check className="w-4 h-4" />
                                Approve
                              </>
                            )}
                          </button>
                          <button
                            onClick={() => handleAction(approval.id, 'reject')}
                            disabled={actionLoading === `${approval.id}-reject`}
                            className="btn btn-secondary flex-1 disabled:opacity-50 disabled:cursor-not-allowed border border-error text-error hover:bg-error hover:text-white"
                          >
                            {actionLoading === `${approval.id}-reject` ? (
                              <Loader2 className="w-4 h-4 animate-spin" />
                            ) : (
                              <>
                                <X className="w-4 h-4" />
                                Reject
                              </>
                            )}
                          </button>
                        </div>
                      </div>
                    </motion.div>
                  )}
                </AnimatePresence>
              </motion.div>
            ))}
          </AnimatePresence>
        </div>
      )}
    </div>
  );
}
