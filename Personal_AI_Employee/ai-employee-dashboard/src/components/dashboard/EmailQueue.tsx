'use client';

import { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { Badge } from '@/components/ui/badge';
import { Button } from '@/components/ui/button';
import { Mail, Send, Archive, Trash2, MoreHorizontal } from 'lucide-react';
import { formatDistanceToNow } from 'date-fns';

interface EmailItem {
  id: string;
  from: string;
  subject: string;
  preview: string;
  priority: 'urgent' | 'high' | 'normal';
  time: string;
  unread: boolean;
}

const getPriorityVariant = (priority: string) => {
  switch (priority) {
    case 'urgent':
      return 'destructive';
    case 'high':
      return 'warning';
    case 'normal':
      return 'success';
    default:
      return 'default';
  }
};

const getPriorityLabel = (priority: string) => {
  switch (priority) {
    case 'urgent':
      return 'Urgent';
    case 'high':
      return 'High';
    case 'normal':
      return 'Normal';
    default:
      return 'Normal';
  }
};

export const EmailQueue = () => {
  const [emails, setEmails] = useState<EmailItem[]>([]);
  const [loading, setLoading] = useState(true);

  const fetchEmails = async () => {
    try {
      setLoading(true);

      // Fetch from the API
      const response = await fetch('/api/emails');
      if (!response.ok) throw new Error('Failed to fetch emails');

      const data = await response.json();
      setEmails(data.emails);
    } catch (error) {
      console.error('Error fetching emails:', error);
      // Fallback to empty array
      setEmails([]);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    // Fetch emails on mount
    fetchEmails();

    // Set up interval to fetch emails every 5 seconds for real-time updates
    const interval = setInterval(fetchEmails, 5000);

    // Clean up interval on unmount
    return () => clearInterval(interval);
  }, []);

  const handleAction = (action: string, id: string) => {
    console.log(`${action} email ${id}`);
    // In a real app, this would trigger an API call
  };

  const urgentCount = emails?.filter(e => e.priority === 'urgent').length || 0;
  const highCount = emails?.filter(e => e.priority === 'high').length || 0;
  const normalCount = emails?.filter(e => e.priority === 'normal').length || 0;

  if (loading) {
    return (
      <div className="space-y-4">
        <div className="flex justify-between items-center mb-4">
          <div className="h-6 w-40 bg-border rounded"></div>
          <div className="h-8 w-20 bg-border rounded"></div>
        </div>
        {[...Array(5)].map((_, i) => (
          <div key={i} className="flex items-center gap-4 p-3 rounded-lg bg-surface animate-pulse">
            <div className="w-3 h-3 rounded-full bg-border"></div>
            <div className="flex-1">
              <div className="h-4 bg-border rounded w-1/4 mb-2"></div>
              <div className="h-3 bg-border rounded w-3/4"></div>
            </div>
          </div>
        ))}
      </div>
    );
  }

  return (
    <div className="space-y-4">
      <div className="flex justify-between items-center mb-4">
        <h3 className="font-medium">Priority Queue</h3>
        <div className="flex gap-2">
          <Badge variant={urgentCount > 0 ? 'destructive' : 'default'} className="gap-1">
            <div className="w-2 h-2 rounded-full bg-red-500"></div>
            {urgentCount}
          </Badge>
          <Badge variant={highCount > 0 ? 'warning' : 'default'} className="gap-1">
            <div className="w-2 h-2 rounded-full bg-yellow-500"></div>
            {highCount}
          </Badge>
          <Badge variant={normalCount > 0 ? 'success' : 'default'} className="gap-1">
            <div className="w-2 h-2 rounded-full bg-green-500"></div>
            {normalCount}
          </Badge>
        </div>
      </div>

      <div className="space-y-3 max-h-80 overflow-y-auto">
        <AnimatePresence>
          {emails?.map((email) => (
            <motion.div
              key={email.id}
              initial={{ opacity: 0, y: 10 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: -10 }}
              transition={{ duration: 0.2 }}
              className={`flex items-center gap-3 p-3 rounded-lg hover:bg-surface transition-colors ${
                email.unread ? 'bg-surface-elevated' : ''
              }`}
            >
              <div className={`w-2 h-2 rounded-full ${email.unread ? 'bg-primary' : 'bg-transparent'}`}></div>
              <div className="flex-1 min-w-0">
                <div className="flex items-center gap-2">
                  <p className={`font-medium truncate ${email.unread ? 'text-text-primary' : 'text-text-secondary'}`}>
                    {email.from}
                  </p>
                  <Badge variant={getPriorityVariant(email.priority)} className="text-xs">
                    {getPriorityLabel(email.priority)}
                  </Badge>
                </div>
                <p className="truncate text-sm font-medium">{email.subject}</p>
                <p className="truncate text-xs text-text-tertiary">{email.preview}</p>
              </div>
              <div className="text-xs text-text-tertiary whitespace-nowrap">
                {formatDistanceToNow(new Date(email.time), { addSuffix: true })}
              </div>
              <Button variant="ghost" size="icon" className="h-8 w-8">
                <MoreHorizontal className="w-4 h-4" />
              </Button>
            </motion.div>
          ))}
        </AnimatePresence>

        {emails && emails.length === 0 && (
          <div className="text-center py-8 text-text-secondary">
            <Mail className="w-12 h-12 mx-auto mb-3 text-border" />
            <p>No emails in queue</p>
          </div>
        )}
      </div>
    </div>
  );
};