'use client';

import { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { Check, X, ChevronDown, Loader2 } from 'lucide-react';
import { toast } from 'sonner';

interface Approval {
  id: string;
  title: string;
  description: string;
  type: 'email' | 'payment' | 'post' | 'file';
  requestedAt: string;
  preview: string;
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
        return '📧';
      case 'payment':
        return '💳';
      case 'post':
        return '💼';
      case 'file':
        return '📄';
      default:
        return '📋';
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
        <span>⏳</span>
        Pending Approvals
        <span className="text-sm font-normal text-muted">({approvals.length})</span>
      </h2>

      <div className="space-y-3 max-h-[400px] overflow-y-auto pr-2">
        <AnimatePresence>
          {approvals.map((approval) => (
            <motion.div
              key={approval.id}
              initial={{ opacity: 0, y: 10 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, x: -20 }}
              className="bg-surface2 border border-border rounded-lg overflow-hidden"
            >
              {/* Header */}
              <button
                onClick={() =>
                  setExpandedId(expandedId === approval.id ? null : approval.id)
                }
                className="w-full p-4 flex items-center gap-3 hover:bg-surface transition-colors"
              >
                <div className="text-2xl">{getTypeIcon(approval.type)}</div>
                <div className="flex-1 text-left">
                  <div className="font-semibold text-sm mb-1">{approval.title}</div>
                  <div className="text-xs text-muted">{approval.description}</div>
                </div>
                <ChevronDown
                  className={`w-4 h-4 text-muted transition-transform ${
                    expandedId === approval.id ? 'rotate-180' : ''
                  }`}
                />
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
                      <div className="bg-bg rounded-lg p-3 text-xs text-muted font-mono">
                        {approval.preview}
                      </div>

                      {/* Action Buttons */}
                      <div className="flex gap-2">
                        <button
                          onClick={() => handleAction(approval.id, 'approve')}
                          disabled={actionLoading === `${approval.id}-approve`}
                          className="flex-1 flex items-center justify-center gap-2 px-4 py-2 bg-accent3 text-black rounded-lg hover:bg-accent3/80 transition-all disabled:opacity-50 disabled:cursor-not-allowed font-semibold text-sm"
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
                          className="flex-1 flex items-center justify-center gap-2 px-4 py-2 bg-danger text-white rounded-lg hover:bg-danger/80 transition-all disabled:opacity-50 disabled:cursor-not-allowed font-semibold text-sm"
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

        {approvals.length === 0 && (
          <div className="text-center py-8 text-muted">
            <p className="text-sm">No pending approvals</p>
          </div>
        )}
      </div>
    </div>
  );
}
