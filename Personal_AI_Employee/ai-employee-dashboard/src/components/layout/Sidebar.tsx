'use client';

import { useState } from 'react';
import Link from 'next/link';
import { usePathname } from 'next/navigation';
import {
  Home,
  Bot,
  BarChart3,
  Activity,
  Clock,
  FileText,
  Settings,
  ChevronLeft,
  ChevronRight
} from 'lucide-react';

import { Route } from 'next';

const navigation: Array<{
  name: string;
  href: Route;
  icon: any;
}> = [
  { name: 'Overview', href: '/' as Route, icon: Home },
  { name: 'Agents', href: '/agents' as Route, icon: Bot },
  { name: 'Analytics', href: '/analytics' as Route, icon: BarChart3 },
  { name: 'Activity', href: '/activity' as Route, icon: Activity },
  { name: 'Approvals', href: '/approvals' as Route, icon: Clock },
  { name: 'Logs', href: '/logs' as Route, icon: FileText },
  { name: 'Settings', href: '/settings' as Route, icon: Settings },
];

export default function Sidebar() {
  const pathname = usePathname();
  const [collapsed, setCollapsed] = useState(false);

  return (
    <aside
      className={`${
        collapsed ? 'w-20' : 'w-72'
      } bg-surface-1 border-r border-border flex flex-col transition-all duration-300`}
    >
      {/* Logo */}
      <div className="h-16 flex items-center justify-between px-6 border-b border-border">
        {!collapsed && (
          <div className="flex items-center gap-3">
            <div className="w-8 h-8 rounded-lg bg-brand-gradient flex items-center justify-center">
              <Bot className="w-5 h-5 text-white" />
            </div>
            <div>
              <h1 className="font-display font-bold text-sm">AI Employee</h1>
              <p className="text-xs text-text-tertiary">Control Center</p>
            </div>
          </div>
        )}
        <button
          onClick={() => setCollapsed(!collapsed)}
          className="p-1.5 hover:bg-surface-2 rounded-lg transition-colors"
        >
          {collapsed ? (
            <ChevronRight className="w-4 h-4 text-text-secondary" />
          ) : (
            <ChevronLeft className="w-4 h-4 text-text-secondary" />
          )}
        </button>
      </div>

      {/* Navigation */}
      <nav className="flex-1 px-3 py-4 space-y-1">
        {navigation.map((item) => {
          const isActive = pathname === item.href;
          const Icon = item.icon;

          return (
            <Link
              key={item.name}
              href={item.href}
              className={`
                flex items-center gap-3 px-3 py-2.5 rounded-lg transition-all duration-200
                ${isActive
                  ? 'bg-brand-gradient text-white shadow-glow'
                  : 'text-text-secondary hover:text-text-primary hover:bg-surface-2'
                }
                ${collapsed ? 'justify-center' : ''}
              `}
            >
              <Icon className="w-5 h-5 flex-shrink-0" />
              {!collapsed && (
                <span className="text-sm font-medium">{item.name}</span>
              )}
              {!collapsed && isActive && (
                <div className="ml-auto w-1.5 h-1.5 rounded-full bg-white" />
              )}
            </Link>
          );
        })}
      </nav>

      {/* System Health Summary */}
      {!collapsed && (
        <div className="p-4 border-t border-border">
          <div className="bg-surface-2 rounded-lg p-3 space-y-2">
            <div className="flex items-center justify-between">
              <span className="text-xs text-text-tertiary">System Health</span>
              <span className="text-xs font-semibold text-success">98%</span>
            </div>
            <div className="h-1.5 bg-surface-3 rounded-full overflow-hidden">
              <div className="h-full w-[98%] bg-success rounded-full" />
            </div>
            <div className="flex items-center gap-2 text-xs text-text-tertiary">
              <div className="status-dot status-running" />
              <span>5 agents running</span>
            </div>
          </div>
        </div>
      )}

      {/* Current Tier */}
      {!collapsed && (
        <div className="p-4 border-t border-border">
          <div className="flex items-center gap-2">
            <div className="w-2 h-2 rounded-full bg-silver" />
            <span className="text-xs text-text-tertiary">Silver Tier</span>
          </div>
        </div>
      )}
    </aside>
  );
}
