'use client';

import { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { Badge } from '@/components/ui/badge';
import { Button } from '@/components/ui/button';
import { Check, X, MoreHorizontal, Clock, User, Calendar } from 'lucide-react';
import { formatDistanceToNow, format } from 'date-fns';

interface ApprovalItem {
  id: string;
  title: string;
  description: string;
  status: 'pending' | 'approved' | 'rejected';
  requestedBy: string;
  requestedAt: string;
  expiresAt: string;
}

const getStatusVariant = (status: string) => {
  switch (status) {
    case 'pending':
      return 'warning';
    case 'approved':
      return 'success';
    case 'rejected':
      return 'destructive';
    default:
      return 'default';
  }
};

const getStatusIcon = (status: string) => {
  switch (status) {
    case 'pending':
      return <Clock className="w-4 h-4" />;
    case 'approved':
      return <Check className="w-4 h-4" />;
    case 'rejected':
      return <X className="w-4 h-4" />;
    default:
      return <Clock className="w-4 h-4" />;
  }
};

export const ApprovalCenter = () => {
  const [approvals, setApprovals] = useState<ApprovalItem[]>([]);
  const [loading, setLoading] = useState(true);

  const fetchApprovals = async () => {
    try {
      setLoading(true);

      const response = await fetch('/api/approvals');
      if (!response.ok) {
        throw new Error('Failed to fetch approvals');
      }

      const data = await response.json();
      setApprovals(data);
    } catch (error) {
      console.error('Error fetching approvals:', error);
      // Fallback to empty array if API fails
      setApprovals([]);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    // Fetch approvals on mount
    fetchApprovals();

    // Set up interval to fetch approvals every 5 seconds for real-time updates
    const interval = setInterval(fetchApprovals, 5000);

    // Clean up interval on unmount
    return () => clearInterval(interval);
  }, []);

  const handleApprove = async (id: string) => {
    try {
      const response = await fetch('/api/approvals', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ id, action: 'approve' }),
      });

      if (response.ok) {
        // Update local state to reflect the change
        setApprovals(prev => prev.map(item =>
          item.id === id ? { ...item, status: 'approved' } : item
        ));
      } else {
        console.error('Failed to approve item');
      }
    } catch (error) {
      console.error('Error approving item:', error);
    }
  };

  const handleReject = async (id: string) => {
    try {
      const response = await fetch('/api/approvals', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ id, action: 'reject' }),
      });

      if (response.ok) {
        // Update local state to reflect the change
        setApprovals(prev => prev.map(item =>
          item.id === id ? { ...item, status: 'rejected' } : item
        ));
      } else {
        console.error('Failed to reject item');
      }
    } catch (error) {
      console.error('Error rejecting item:', error);
    }
  };

  const pendingApprovals = approvals?.filter(a => a.status === 'pending') || [];

  if (loading) {
    return (
      <div className="space-y-4">
        <div className="flex justify-between items-center mb-4">
          <div className="h-6 w-40 bg-border rounded"></div>
          <div className="h-8 w-20 bg-border rounded"></div>
        </div>
        {[...Array(3)].map((_, i) => (
          <div key={i} className="flex items-center gap-4 p-4 rounded-lg bg-surface animate-pulse">
            <div className="w-10 h-10 rounded-lg bg-border"></div>
            <div className="flex-1">
              <div className="h-4 bg-border rounded w-1/3 mb-2"></div>
              <div className="h-3 bg-border rounded w-2/3"></div>
            </div>
          </div>
        ))}
      </div>
    );
  }

  return (
    <div className="space-y-4">
      <div className="flex justify-between items-center mb-4">
        <h3 className="font-medium">Pending Approvals</h3>
        <Badge variant="outline" className="gap-1">
          <Clock className="w-3 h-3" />
          {pendingApprovals.length}
        </Badge>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        <AnimatePresence>
          {approvals.map((approval) => (
            <motion.div
              key={approval.id}
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: -20 }}
              transition={{ duration: 0.3 }}
              className="glass-card p-4 rounded-lg border"
            >
              <div className="flex items-start justify-between">
                <div className="flex-1 min-w-0">
                  <div className="flex items-center gap-2 mb-2">
                    <div className={`p-1 rounded-full ${approval.status === 'pending' ? 'bg-warning/20 text-warning' : approval.status === 'approved' ? 'bg-accent/20 text-accent' : 'bg-danger/20 text-danger'}`}>
                      {getStatusIcon(approval.status)}
                    </div>
                    <h4 className="font-medium truncate">{approval.title}</h4>
                    <Badge variant={getStatusVariant(approval.status)}>
                      {approval.status.charAt(0).toUpperCase() + approval.status.slice(1)}
                    </Badge>
                  </div>

                  <p className="text-sm text-text-secondary mb-3 line-clamp-2">{approval.description}</p>

                  <div className="flex items-center justify-between text-xs text-text-tertiary">
                    <div className="flex items-center gap-1">
                      <User className="w-3 h-3" />
                      <span>{approval.requestedBy}</span>
                    </div>
                    <div className="flex items-center gap-1">
                      <Calendar className="w-3 h-3" />
                      <span>{formatDistanceToNow(new Date(approval.requestedAt), { addSuffix: true })}</span>
                    </div>
                  </div>
                </div>

                <Button variant="ghost" size="icon" className="h-8 w-8 flex-shrink-0 ml-2">
                  <MoreHorizontal className="w-4 h-4" />
                </Button>
              </div>

              {approval.status === 'pending' && (
                <div className="flex gap-2 mt-4">
                  <Button
                    variant="outline"
                    size="sm"
                    className="flex-1 gap-1"
                    onClick={() => handleApprove(approval.id)}
                  >
                    <Check className="w-4 h-4" />
                    Approve
                  </Button>
                  <Button
                    variant="outline"
                    size="sm"
                    className="flex-1 gap-1"
                    onClick={() => handleReject(approval.id)}
                  >
                    <X className="w-4 h-4" />
                    Reject
                  </Button>
                </div>
              )}

              <div className="mt-3 text-xs text-text-tertiary flex items-center gap-1">
                <Clock className="w-3 h-3" />
                Expires {format(new Date(approval.expiresAt), 'MMM dd, yyyy')}
              </div>
            </motion.div>
          ))}
        </AnimatePresence>
      </div>

      {approvals.length === 0 && (
        <div className="text-center py-8 text-text-secondary">
          <Clock className="w-12 h-12 mx-auto mb-3 text-border" />
          <p>No pending approvals</p>
        </div>
      )}
    </div>
  );
};