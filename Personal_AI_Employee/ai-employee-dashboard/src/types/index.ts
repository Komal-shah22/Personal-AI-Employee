export interface StatCard {
  title: string;
  value: number;
  change: number;
  changeType: 'positive' | 'negative';
  icon: string;
  trendData: number[];
}

export interface ActivityItem {
  id: string;
  title: string;
  description: string;
  time: string;
  type: 'email' | 'task' | 'approval' | 'plan';
  icon: string;
}

export interface EmailItem {
  id: string;
  from: string;
  subject: string;
  preview: string;
  priority: 'urgent' | 'high' | 'normal';
  time: string;
  unread: boolean;
}

export interface TaskItem {
  id: string;
  title: string;
  description: string;
  status: 'inbox' | 'progress' | 'review' | 'done';
  priority: 'high' | 'medium' | 'low';
  assignee: string;
  dueDate: string;
}

export interface ApprovalItem {
  id: string;
  title: string;
  description: string;
  status: 'pending' | 'approved' | 'rejected';
  requestedBy: string;
  requestedAt: string;
  expiresAt: string;
}

export interface ChartDataPoint {
  date: string;
  value: number;
}

export interface DashboardStats {
  pending: number;
  inProgress: number;
  completed: number;
  total: number;
  trends: {
    pendingChange: number;
    inProgressChange: number;
    completedChange: number;
    totalChange: number;
  };
}