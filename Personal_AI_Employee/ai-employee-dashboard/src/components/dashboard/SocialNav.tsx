'use client';

import { useState, useEffect } from 'react';
import { BarChart3, Instagram, Linkedin, Twitter, Facebook, MessageCircle, Users, Settings, Activity, FileText, Calendar, Mail } from 'lucide-react';
import Link from 'next/link';

interface NavItem {
  id: string;
  label: string;
  icon: React.ReactNode;
  href: string;
}

export default function SocialNav({ onTabChange }: { onTabChange: (tab: string) => void }) {
  const [activeTab, setActiveTab] = useState('dashboard');

  const navItems: NavItem[] = [
    {
      id: 'dashboard',
      label: 'Dashboard',
      icon: <BarChart3 className="w-5 h-5" />,
      href: '#'
    },
    {
      id: 'email',
      label: 'Email',
      icon: <Mail className="w-5 h-5 text-red-500" />,
      href: '#'
    },
    {
      id: 'whatsapp',
      label: 'WhatsApp',
      icon: <MessageCircle className="w-5 h-5 text-green-500" />,
      href: '#'
    },
    {
      id: 'instagram',
      label: 'Instagram',
      icon: <Instagram className="w-5 h-5 bg-gradient-to-r from-purple-500 to-pink-500 text-transparent bg-clip-text" />,
      href: '#'
    },
    {
      id: 'linkedin',
      label: 'LinkedIn',
      icon: <Linkedin className="w-5 h-5 text-blue-700" />,
      href: '#'
    },
    {
      id: 'twitter',
      label: 'Twitter',
      icon: <Twitter className="w-5 h-5 text-blue-400" />,
      href: '#'
    },
    {
      id: 'facebook',
      label: 'Facebook',
      icon: <Facebook className="w-5 h-5 text-blue-600" />,
      href: '#'
    },
    {
      id: 'analytics',
      label: 'Analytics',
      icon: <BarChart3 className="w-5 h-5" />,
      href: '#'
    },
    {
      id: 'audience',
      label: 'Audience',
      icon: <Users className="w-5 h-5" />,
      href: '#'
    },
    {
      id: 'scheduling',
      label: 'Scheduling',
      icon: <Calendar className="w-5 h-5" />,
      href: '#'
    },
    {
      id: 'content',
      label: 'Content',
      icon: <FileText className="w-5 h-5" />,
      href: '#'
    },
    {
      id: 'activity',
      label: 'Activity',
      icon: <Activity className="w-5 h-5" />,
      href: '#'
    },
    {
      id: 'settings',
      label: 'Settings',
      icon: <Settings className="w-5 h-5" />,
      href: '#'
    }
  ];

  // Update the parent when the local activeTab changes
  useEffect(() => {
    onTabChange(activeTab);
  }, [activeTab, onTabChange]);

  return (
    <div className="fixed left-0 top-0 h-full w-64 bg-white/10 backdrop-blur-lg border-r border-border p-4 flex flex-col">
      <div className="mb-8">
        <h1 className="text-xl font-bold flex items-center gap-2">
          <MessageCircle className="w-8 h-8" />
          <span>Social Media</span>
        </h1>
        <p className="text-sm text-muted mt-1">AI Employee Dashboard</p>
      </div>

      <nav className="flex-1">
        <ul className="space-y-1">
          {navItems.map((item) => (
            <li key={item.id}>
              <button
                onClick={() => setActiveTab(item.id)}
                className={`w-full flex items-center gap-3 px-3 py-2 rounded-lg text-left transition-colors ${
                  activeTab === item.id
                    ? 'bg-primary text-primary-foreground'
                    : 'text-foreground hover:bg-white/10'
                }`}
              >
                <span>{item.icon}</span>
                <span className="text-sm">{item.label}</span>
              </button>
            </li>
          ))}
        </ul>
      </nav>

      <div className="mt-auto pt-4 border-t border-border">
        <div className="text-xs text-muted flex items-center gap-2 p-2">
          <div className="w-2 h-2 rounded-full bg-green-500"></div>
          <span>AI Employee Active</span>
        </div>
        <div className="text-xs text-muted mt-1">Gold Tier v2.0</div>
      </div>
    </div>
  );
}