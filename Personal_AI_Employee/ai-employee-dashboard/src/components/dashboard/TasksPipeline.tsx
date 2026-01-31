'use client';

import { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { Badge } from '@/components/ui/badge';
import { Button } from '@/components/ui/button';
import { MoreHorizontal, Plus, User, Calendar } from 'lucide-react';
import { format } from 'date-fns';

interface TaskItem {
  id: string;
  title: string;
  description: string;
  status: 'inbox' | 'progress' | 'review' | 'done';
  priority: 'high' | 'medium' | 'low';
  assignee: string;
  dueDate: string;
}

const getStatusColor = (status: string) => {
  switch (status) {
    case 'inbox':
      return 'border-l-blue-500';
    case 'progress':
      return 'border-l-yellow-500';
    case 'review':
      return 'border-l-purple-500';
    case 'done':
      return 'border-l-green-500';
    default:
      return 'border-l-gray-500';
  }
};

const getPriorityVariant = (priority: string) => {
  switch (priority) {
    case 'high':
      return 'destructive';
    case 'medium':
      return 'warning';
    case 'low':
      return 'success';
    default:
      return 'default';
  }
};

const getStatusTitle = (status: string) => {
  switch (status) {
    case 'inbox':
      return 'Inbox';
    case 'progress':
      return 'In Progress';
    case 'review':
      return 'Review';
    case 'done':
      return 'Done';
    default:
      return status;
  }
};

export const TasksPipeline = () => {
  const [tasks, setTasks] = useState<TaskItem[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    // Simulate API call to fetch tasks
    const fetchTasks = async () => {
      setLoading(true);

      // Simulate API delay
      await new Promise(resolve => setTimeout(resolve, 500));

      // Mock data - in a real app this would come from an API
      const mockTasks: TaskItem[] = [
        {
          id: '1',
          title: 'Update customer database',
          description: 'Clean and update customer records with new contact information',
          status: 'inbox',
          priority: 'high',
          assignee: 'AI Employee',
          dueDate: new Date(Date.now() + 1000 * 60 * 60 * 24 * 3).toISOString(),
        },
        {
          id: '2',
          title: 'Process weekly reports',
          description: 'Compile and analyze weekly sales reports',
          status: 'inbox',
          priority: 'medium',
          assignee: 'AI Employee',
          dueDate: new Date(Date.now() + 1000 * 60 * 60 * 24 * 1).toISOString(),
        },
        {
          id: '3',
          title: 'Send newsletter',
          description: 'Prepare and send monthly company newsletter',
          status: 'progress',
          priority: 'medium',
          assignee: 'AI Employee',
          dueDate: new Date(Date.now() + 1000 * 60 * 60 * 24 * 5).toISOString(),
        },
        {
          id: '4',
          title: 'Review vendor contracts',
          description: 'Review and renew vendor agreements',
          status: 'review',
          priority: 'high',
          assignee: 'AI Employee',
          dueDate: new Date(Date.now() + 1000 * 60 * 60 * 24 * 7).toISOString(),
        },
        {
          id: '5',
          title: 'Update inventory system',
          description: 'Integrate new inventory tracking system',
          status: 'done',
          priority: 'low',
          assignee: 'AI Employee',
          dueDate: new Date(Date.now() - 1000 * 60 * 60 * 24 * 2).toISOString(),
        },
      ];

      setTasks(mockTasks);
      setLoading(false);
    };

    fetchTasks();
  }, []);

  const columns = ['inbox', 'progress', 'review', 'done'];

  const getTasksByStatus = (status: string) => {
    return tasks.filter(task => task.status === status);
  };

  if (loading) {
    return (
      <div className="grid grid-cols-4 gap-4">
        {columns.map((col, idx) => (
          <div key={idx} className="bg-surface rounded-lg p-4">
            <div className="h-6 w-24 bg-border rounded mb-4"></div>
            <div className="space-y-3">
              {[...Array(2)].map((_, i) => (
                <div key={i} className="p-3 bg-surface-elevated rounded animate-pulse">
                  <div className="h-4 bg-border rounded w-3/4 mb-2"></div>
                  <div className="h-3 bg-border rounded w-1/2"></div>
                </div>
              ))}
            </div>
          </div>
        ))}
      </div>
    );
  }

  return (
    <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
      <AnimatePresence>
        {columns.map((column) => (
          <motion.div
            key={column}
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: -20 }}
            transition={{ duration: 0.3 }}
            className="bg-surface rounded-lg p-4"
          >
            <div className="flex items-center justify-between mb-4">
              <h3 className="font-medium">{getStatusTitle(column)}</h3>
              <Badge variant="outline" className="rounded-full">
                {getTasksByStatus(column).length}
              </Badge>
            </div>

            <div className="space-y-3">
              {getTasksByStatus(column).map((task) => (
                <motion.div
                  key={task.id}
                  layout
                  initial={{ opacity: 0, scale: 0.9 }}
                  animate={{ opacity: 1, scale: 1 }}
                  exit={{ opacity: 0, scale: 0.9 }}
                  transition={{ duration: 0.2 }}
                  className={`p-3 rounded-lg border-l-4 ${getStatusColor(task.status)} bg-surface-elevated hover:bg-surface transition-colors cursor-pointer`}
                >
                  <div className="flex items-start justify-between">
                    <div className="flex-1 min-w-0">
                      <p className="font-medium truncate">{task.title}</p>
                      <p className="text-xs text-text-tertiary mt-1 line-clamp-2">{task.description}</p>

                      <div className="flex items-center gap-2 mt-2">
                        <Badge variant={getPriorityVariant(task.priority)} className="text-xs">
                          {task.priority.charAt(0).toUpperCase() + task.priority.slice(1)}
                        </Badge>

                        <div className="flex items-center text-xs text-text-tertiary gap-1">
                          <Calendar className="w-3 h-3" />
                          {format(new Date(task.dueDate), 'MMM dd')}
                        </div>
                      </div>
                    </div>

                    <Button variant="ghost" size="icon" className="h-6 w-6 flex-shrink-0 ml-2">
                      <MoreHorizontal className="w-3 h-3" />
                    </Button>
                  </div>

                  <div className="flex items-center gap-1 mt-2">
                    <User className="w-3 h-3 text-text-tertiary" />
                    <span className="text-xs text-text-tertiary">{task.assignee}</span>
                  </div>
                </motion.div>
              ))}

              {getTasksByStatus(column).length === 0 && (
                <div className="text-center py-4 text-text-secondary text-sm">
                  <p>No tasks</p>
                </div>
              )}
            </div>

            <Button variant="outline" className="w-full mt-3 gap-1 text-sm">
              <Plus className="w-4 h-4" />
              Add Task
            </Button>
          </motion.div>
        ))}
      </AnimatePresence>
    </div>
  );
};