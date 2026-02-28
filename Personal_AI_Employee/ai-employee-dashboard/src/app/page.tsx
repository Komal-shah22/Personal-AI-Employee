'use client'

import { useState } from 'react'
import Header from '@/components/Header'
import StatsStrip from '@/components/StatsStrip'
import ArchitectureDiagram from '@/components/ArchitectureDiagram'
import LiveStatus from '@/components/LiveStatus'
import ActivityFeed from '@/components/ActivityFeed'
import QuickActions from '@/components/QuickActions'
import ApprovalQueue from '@/components/ApprovalQueue'
import TierNav from '@/components/TierNav'
import AgentCard from '@/components/AgentCard'
import SocialDashboard from '@/components/dashboard/SocialDashboard'
import SocialNav from '@/components/dashboard/SocialNav'
import TierStatus from '@/components/dashboard/TierStatus'

type Tier = 'bronze' | 'silver' | 'gold' | 'platinum'

export default function Dashboard() {
  const [activeTier, setActiveTier] = useState<Tier>('gold')
  const [activeTab, setActiveTab] = useState('dashboard')

  const handleTabChange = (tab: string) => {
    setActiveTab(tab);
  }

  // Email/Gmail Form Component
  const EmailForm = () => {
    const [to, setTo] = useState('');
    const [subject, setSubject] = useState('');
    const [message, setMessage] = useState('');
    const [isSubmitting, setIsSubmitting] = useState(false);
    const [status, setStatus] = useState<{type: string, message: string} | null>(null);

    const handleSubmit = async (e: React.FormEvent) => {
      e.preventDefault();
      setIsSubmitting(true);
      setStatus(null);

      try {
        // Call the direct email API endpoint
        const response = await fetch('/api/actions/send-email-direct', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({
            to: to,
            subject: subject,
            body: message
          }),
        });

        const result = await response.json();

        if (response.ok) {
          // Show success message
          setStatus({ type: 'success', message: result.message || 'Email sent successfully!' });
          // Reset form
          setTo('');
          setSubject('');
          setMessage('');
        } else {
          throw new Error(result.error || 'Failed to send email');
        }
      } catch (error: any) {
        console.error('Email send error:', error);
        setStatus({ type: 'error', message: error.message || 'Failed to send email. Please try again.' });
      } finally {
        setIsSubmitting(false);
      }
    };

    return (
      <div className="p-6 rounded-lg bg-surface border border-border">
        <div className="flex items-center gap-3 mb-4 pb-4 border-b border-border-subtle">
          <div className="w-10 h-10 rounded-lg bg-[#EA4335]/10 flex items-center justify-center">
            <svg className="w-5 h-5 text-[#EA4335]" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M3 8l7.89 4.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z"></path>
            </svg>
          </div>
          <div>
            <h3 className="font-semibold font-syne">Gmail</h3>
            <p className="text-xs text-muted">Send email</p>
          </div>
          <div className="ml-auto">
            <span className="px-3 py-1 rounded-full bg-green-500/20 text-green-400 text-xs font-medium">
              Connected
            </span>
          </div>
        </div>

        {status && (
          <div className={`mb-4 p-3 rounded-lg ${status.type === 'success' ? 'bg-green-500/20 text-green-400' : 'bg-red-500/20 text-red-400'}`}>
            {status.message}
          </div>
        )}

        <form onSubmit={handleSubmit} className="space-y-4">
          <div>
            <label className="block text-sm font-medium mb-2">To</label>
            <input
              type="email"
              value={to}
              onChange={(e) => setTo(e.target.value)}
              placeholder="recipient@example.com"
              className="w-full px-4 py-3 rounded-lg bg-surface2 border border-border focus:border-[#EA4335] focus:ring-2 focus:ring-[#EA4335]/20 outline-none transition-all"
              required
            />
          </div>

          <div>
            <label className="block text-sm font-medium mb-2">Subject</label>
            <input
              type="text"
              value={subject}
              onChange={(e) => setSubject(e.target.value)}
              placeholder="Email subject..."
              className="w-full px-4 py-3 rounded-lg bg-surface2 border border-border focus:border-[#EA4335] focus:ring-2 focus:ring-[#EA4335]/20 outline-none transition-all"
              required
            />
          </div>

          <div>
            <label className="block text-sm font-medium mb-2">Message</label>
            <textarea
              rows={4}
              value={message}
              onChange={(e) => setMessage(e.target.value)}
              placeholder="Type your message..."
              className="w-full px-4 py-3 rounded-lg bg-surface2 border border-border focus:border-[#EA4335] focus:ring-2 focus:ring-[#EA4335]/20 outline-none transition-all resize-none"
              required
            ></textarea>
          </div>

          <div className="flex gap-3 pt-2">
            <button
              type="button"
              className="flex-1 px-4 py-3 rounded-lg bg-surface2 border border-border hover:bg-surface/50 font-medium transition-all"
            >
              Save Draft
            </button>
            <button
              type="submit"
              disabled={isSubmitting}
              className="flex-1 px-4 py-3 rounded-lg bg-[#EA4335] hover:bg-[#EA4335]/90 text-white font-medium transition-all flex items-center justify-center gap-2 disabled:opacity-50"
            >
              {isSubmitting ? (
                <svg className="w-4 h-4 animate-spin" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15"></path>
                </svg>
              ) : (
                <>
                  <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M12 19l9 2-9-18-9 18 9-2zm0 0v-8"></path>
                  </svg>
                  Send
                </>
              )}
            </button>
          </div>
        </form>
      </div>
    );
  }

  // WhatsApp Form Component
  const WhatsAppForm = () => {
    const [contact, setContact] = useState('');
    const [message, setMessage] = useState('');
    const [isSubmitting, setIsSubmitting] = useState(false);
    const [status, setStatus] = useState<{type: string, message: string} | null>(null);

    const handleSubmit = async (e: React.FormEvent) => {
      e.preventDefault();
      setIsSubmitting(true);
      setStatus(null);

      try {
        // Call the WhatsApp API endpoint
        const response = await fetch('/api/actions/send-whatsapp-direct', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({
            phone: contact,
            message: message
          }),
        });

        const result = await response.json();

        if (response.ok) {
          // Show success message
          setStatus({ type: 'success', message: result.message || 'WhatsApp message sent successfully!' });
          // Reset form
          setContact('');
          setMessage('');
        } else {
          if (result.action_required === 'qr_scan') {
            throw new Error('WhatsApp Web not authenticated. Please scan QR code first.');
          } else {
            throw new Error(result.error || 'Failed to send WhatsApp message');
          }
        }
      } catch (error: any) {
        console.error('WhatsApp send error:', error);
        setStatus({ type: 'error', message: error.message || 'Failed to send WhatsApp message. Please try again.' });
      } finally {
        setIsSubmitting(false);
      }
    };

    return (
      <div className="p-6 rounded-lg bg-surface border border-border">
        <div className="flex items-center gap-3 mb-4 pb-4 border-b border-border-subtle">
          <div className="w-10 h-10 rounded-lg bg-[#25D366]/10 flex items-center justify-center">
            <svg className="w-5 h-5 text-[#25D366]" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z"></path>
            </svg>
          </div>
          <div>
            <h3 className="font-semibold font-syne">WhatsApp</h3>
            <p className="text-xs text-muted">Send message</p>
          </div>
          <div className="ml-auto">
            <span className="px-3 py-1 rounded-full bg-green-500/20 text-green-400 text-xs font-medium flex items-center gap-1">
              <div className="w-2 h-2 rounded-full bg-green-500 animate-pulse"></div>
              Online
            </span>
          </div>
        </div>

        {status && (
          <div className={`mb-4 p-3 rounded-lg ${status.type === 'success' ? 'bg-green-500/20 text-green-400' : 'bg-red-500/20 text-red-400'}`}>
            {status.message}
          </div>
        )}

        <form onSubmit={handleSubmit} className="space-y-4">
          <div>
            <label className="block text-sm font-medium mb-2">Contact</label>
            <input
              type="tel"
              value={contact}
              onChange={(e) => setContact(e.target.value)}
              placeholder="+92 300 1234567"
              className="w-full px-4 py-3 rounded-lg bg-surface2 border border-border focus:border-[#25D366] focus:ring-2 focus:ring-[#25D366]/20 outline-none transition-all"
              required
            />
          </div>

          <div>
            <label className="block text-sm font-medium mb-2">Message</label>
            <textarea
              rows={5}
              value={message}
              onChange={(e) => setMessage(e.target.value)}
              placeholder="Type your WhatsApp message..."
              className="w-full px-4 py-3 rounded-lg bg-surface2 border border-border focus:border-[#25D366] focus:ring-2 focus:ring-[#25D366]/20 outline-none transition-all resize-none"
              required
            ></textarea>
            <p className="text-xs text-muted mt-2">Max 4096 characters</p>
          </div>

          <div className="flex gap-3 pt-2">
            <button
              type="button"
              className="flex-1 px-4 py-3 rounded-lg bg-surface2 border border-border hover:bg-surface/50 font-medium transition-all"
            >
              Schedule
            </button>
            <button
              type="submit"
              disabled={isSubmitting}
              className="flex-1 px-4 py-3 rounded-lg bg-[#25D366] hover:bg-[#25D366]/90 text-white font-medium transition-all flex items-center justify-center gap-2 disabled:opacity-50"
            >
              {isSubmitting ? (
                <svg className="w-4 h-4 animate-spin" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15"></path>
                </svg>
              ) : (
                <>
                  <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M12 19l9 2-9-18-9 18 9-2zm0 0v-8"></path>
                  </svg>
                  Send Now
                </>
              )}
            </button>
          </div>
        </form>
      </div>
    );
  }

  // Instagram Form Component
  const InstagramForm = () => {
    const [caption, setCaption] = useState('');
    const [image, setImage] = useState<File | null>(null);
    const [isSubmitting, setIsSubmitting] = useState(false);
    const [status, setStatus] = useState<{type: string, message: string} | null>(null);

    const handleSubmit = async (e: React.FormEvent) => {
      e.preventDefault();
      setIsSubmitting(true);
      setStatus(null);

      try {
        // Prepare form data
        const formData = new FormData();
        formData.append('caption', caption);

        if (image) {
          formData.append('image', image);
        }

        // Call the Instagram API endpoint
        const response = await fetch('/api/actions/post-instagram', {
          method: 'POST',
          body: formData,
        });

        const result = await response.json();

        if (response.ok) {
          // Show success message
          setStatus({ type: 'success', message: result.message || 'Instagram post created successfully!' });
          // Reset form
          setCaption('');
          setImage(null);
        } else {
          throw new Error(result.error || 'Failed to create Instagram post');
        }
      } catch (error: any) {
        console.error('Instagram post error:', error);
        setStatus({ type: 'error', message: error.message || 'Failed to create Instagram post. Please try again.' });
      } finally {
        setIsSubmitting(false);
      }
    };

    const handleImageUpload = (e: React.ChangeEvent<HTMLInputElement>) => {
      if (e.target.files && e.target.files[0]) {
        setImage(e.target.files[0]);
      }
    };

    return (
      <div className="p-6 rounded-lg bg-surface border border-border">
        <div className="flex items-center gap-3 mb-4 pb-4 border-b border-border-subtle">
          <div className="w-10 h-10 rounded-lg bg-gradient-to-br from-[#f09433] via-[#e6683c] to-[#bc1888] flex items-center justify-center">
            <svg className="w-5 h-5 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M12 16a4 4 0 100-8 4 4 0 000 8z"></path>
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M3 16V8a5 5 0 015-5h8a5 5 0 015 5v8a5 5 0 01-5 5H8a5 5 0 01-5-5z"></path>
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M17.5 6.5h.01"></path>
            </svg>
          </div>
          <div>
            <h3 className="font-semibold font-syne">Instagram</h3>
            <p className="text-xs text-muted">Create post</p>
          </div>
          <div className="ml-auto">
            <span className="px-3 py-1 rounded-full bg-green-500/20 text-green-400 text-xs font-medium">
              Connected
            </span>
          </div>
        </div>

        {status && (
          <div className={`mb-4 p-3 rounded-lg ${status.type === 'success' ? 'bg-green-500/20 text-green-400' : 'bg-red-500/20 text-red-400'}`}>
            {status.message}
          </div>
        )}

        <form onSubmit={handleSubmit} className="space-y-4">
          <div>
            <label className="block text-sm font-medium mb-2">Image</label>
            <label className="border-2 border-dashed border-border rounded-lg p-8 text-center hover:border-[#bc1888] transition-all cursor-pointer block">
              <input
                type="file"
                className="hidden"
                accept="image/*"
                onChange={handleImageUpload}
              />
              <svg className="mx-auto mb-2 text-muted" fill="none" stroke="currentColor" viewBox="0 0 24 24" width="32" height="32" xmlns="http://www.w3.org/2000/svg">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12"></path>
              </svg>
              <p className="text-sm text-muted">Click to upload or drag and drop</p>
              <p className="text-xs text-muted mt-1">JPG, PNG up to 10MB</p>
              {image && (
                <div className="mt-2 text-xs text-green-400">Selected: {image.name}</div>
              )}
            </label>
          </div>

          <div>
            <label className="block text-sm font-medium mb-2">Caption</label>
            <textarea
              rows={5}
              value={caption}
              onChange={(e) => setCaption(e.target.value)}
              placeholder="Write an engaging caption..."
              className="w-full px-4 py-3 rounded-lg bg-surface2 border border-border focus:border-[#bc1888] focus:ring-2 focus:ring-[#bc1888]/20 outline-none transition-all resize-none"
              required
            ></textarea>
            <div className="flex justify-between mt-2">
              <p className="text-xs text-muted">{caption.length} / 2200 characters</p>
              <p className="text-xs text-muted">Max 30 hashtags</p>
            </div>
          </div>

          <div className="flex gap-3 pt-2">
            <button
              type="button"
              className="flex-1 px-4 py-3 rounded-lg bg-surface2 border border-border hover:bg-surface/50 font-medium transition-all"
            >
              Schedule
            </button>
            <button
              type="submit"
              disabled={isSubmitting}
              className="flex-1 px-4 py-3 rounded-lg bg-gradient-to-r from-[#f09433] to-[#bc1888] hover:bg-gradient-to-r hover:from-[#f09433]/90 hover:to-[#bc1888]/90 text-white font-medium transition-all flex items-center justify-center gap-2 disabled:opacity-50"
            >
              {isSubmitting ? (
                <svg className="w-4 h-4 animate-spin" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15"></path>
                </svg>
              ) : (
                <>
                  <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M12 19l9 2-9-18-9 18 9-2zm0 0v-8"></path>
                  </svg>
                  Post Now
                </>
              )}
            </button>
          </div>
        </form>

        <div className="mt-4 p-3 rounded-lg bg-surface2 border border-border-subtle">
          <p className="text-xs text-muted">
            <strong>Note:</strong> This will open your browser and post directly to Instagram using your saved session.
            The process takes about 30-60 seconds.
          </p>
        </div>
      </div>
    );
  }

  // Analytics View Component
  const AnalyticsView = () => (
    <div className="space-y-6">
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        <div className="p-4 rounded-lg bg-surface border border-border">
          <h4 className="text-sm font-medium text-muted mb-1">Total Followers</h4>
          <p className="text-2xl font-bold font-syne">24.8K</p>
          <p className="text-xs text-green-500">↑ 12% this month</p>
        </div>
        <div className="p-4 rounded-lg bg-surface border border-border">
          <h4 className="text-sm font-medium text-muted mb-1">Engagement Rate</h4>
          <p className="text-2xl font-bold font-syne">4.8%</p>
          <p className="text-xs text-green-500">↑ 1.2% this month</p>
        </div>
        <div className="p-4 rounded-lg bg-surface border border-border">
          <h4 className="text-sm font-medium text-muted mb-1">Avg. Reach</h4>
          <p className="text-2xl font-bold font-syne">12.4K</p>
          <p className="text-xs text-green-500">↑ 8% this month</p>
        </div>
        <div className="p-4 rounded-lg bg-surface border border-border">
          <h4 className="text-sm font-medium text-muted mb-1">Posts This Month</h4>
          <p className="text-2xl font-bold font-syne">32</p>
          <p className="text-xs text-green-500">↑ 5% this month</p>
        </div>
      </div>

      <div className="p-4 rounded-lg bg-surface border border-border">
        <h3 className="font-semibold font-syne mb-4">Engagement Overview</h3>
        <div className="h-64 flex items-center justify-center text-muted">
          Engagement chart would go here
        </div>
      </div>

      <div className="p-4 rounded-lg bg-surface border border-border">
        <h3 className="font-semibold font-syne mb-4">Top Performing Posts</h3>
        <div className="space-y-3">
          {[1, 2, 3, 4, 5].map((item) => (
            <div key={item} className="flex items-center justify-between p-3 hover:bg-surface2 rounded">
              <div className="flex items-center gap-3">
                <div className="w-10 h-10 bg-surface2 rounded flex items-center justify-center">
                  <svg className="w-4 h-4 text-muted" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z"></path>
                  </svg>
                </div>
                <div>
                  <p className="text-sm font-medium">Post #{item}</p>
                  <p className="text-xs text-muted">2 days ago</p>
                </div>
              </div>
              <div className="text-right">
                <p className="text-sm font-bold">1.2K</p>
                <p className="text-xs text-muted">likes</p>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  )

  // LinkedIn Form Component
  const LinkedInForm = () => {
    const [content, setContent] = useState('');
    const [postType, setPostType] = useState('Business Insight');
    const [topic, setTopic] = useState('');
    const [isSubmitting, setIsSubmitting] = useState(false);
    const [status, setStatus] = useState<{type: string, message: string} | null>(null);

    const handleSubmit = async (e: React.FormEvent) => {
      e.preventDefault();
      setIsSubmitting(true);
      setStatus(null);

      try {
        // Combine topic and content if topic is provided
        const fullContent = topic ? `${topic}\n\n${content}` : content;

        // Call the LinkedIn API endpoint
        const response = await fetch('/api/actions/post-linkedin', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({
            content: fullContent,
            postType: postType
          }),
        });

        const result = await response.json();

        if (response.ok && result.success) {
          // Show success message
          setStatus({ type: 'success', message: result.message || 'LinkedIn post published successfully!' });
          // Reset form
          setContent('');
          setTopic('');
        } else if (result.fallback) {
          // Posted to queue instead
          setStatus({
            type: 'success',
            message: `Post queued for publishing. ${result.note || ''}`
          });
          setContent('');
          setTopic('');
        } else {
          throw new Error(result.error || 'Failed to post to LinkedIn');
        }
      } catch (error: any) {
        console.error('LinkedIn post error:', error);
        setStatus({ type: 'error', message: error.message || 'Failed to post to LinkedIn. Please try again.' });
      } finally {
        setIsSubmitting(false);
      }
    };

    const charCount = content.length;
    const maxChars = 3000;

    return (
      <div className="p-6 rounded-lg bg-surface border border-border">
        <div className="flex items-center gap-3 mb-4 pb-4 border-b border-border-subtle">
          <div className="w-10 h-10 rounded-lg bg-[#0A66C2]/10 flex items-center justify-center">
            <svg className="w-5 h-5 text-[#0A66C2]" fill="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
              <path d="M20.447 20.452h-3.554v-5.569c0-1.328-.027-3.037-1.852-3.037-1.853 0-2.136 1.445-2.136 2.939v5.667H9.351V9h3.414v1.561h.046c.477-.9 1.637-1.85 3.37-1.85 3.601 0 4.267 2.37 4.267 5.455v6.286zM5.337 7.433c-1.144 0-2.063-.926-2.063-2.065 0-1.138.92-2.063 2.063-2.063 1.14 0 2.064.925 2.064 2.063 0 1.139-.925 2.065-2.064 2.065zm1.782 13.019H3.555V9h3.564v11.452zM22.225 0H1.771C.792 0 0 .774 0 1.729v20.542C0 23.227.792 24 1.771 24h20.451C23.2 24 24 23.227 24 22.271V1.729C24 .774 23.2 0 22.222 0h.003z"/>
            </svg>
          </div>
          <div>
            <h3 className="font-semibold font-syne">LinkedIn</h3>
            <p className="text-xs text-muted">Create professional post</p>
          </div>
          <div className="ml-auto">
            <span className="px-3 py-1 rounded-full bg-green-500/20 text-green-400 text-xs font-medium flex items-center gap-1">
              <div className="w-2 h-2 rounded-full bg-green-500 animate-pulse"></div>
              Ready to post
            </span>
          </div>
        </div>

        {status && (
          <div className={`mb-4 p-3 rounded-lg ${status.type === 'success' ? 'bg-green-500/20 text-green-400' : 'bg-red-500/20 text-red-400'}`}>
            {status.message}
          </div>
        )}

        <form onSubmit={handleSubmit} className="space-y-4">
          <div className="grid grid-cols-2 gap-4">
            <div>
              <label className="block text-sm font-medium mb-2">Post Type</label>
              <select
                value={postType}
                onChange={(e) => setPostType(e.target.value)}
                className="w-full px-4 py-3 rounded-lg bg-surface2 border border-border focus:border-[#0A66C2] focus:ring-2 focus:ring-[#0A66C2]/20 outline-none transition-all"
              >
                <option>Business Insight</option>
                <option>Client Success Story</option>
                <option>Industry Tip</option>
                <option>Personal Update</option>
                <option>Company News</option>
                <option>Thought Leadership</option>
              </select>
            </div>

            <div>
              <label className="block text-sm font-medium mb-2">Topic (Optional)</label>
              <input
                type="text"
                value={topic}
                onChange={(e) => setTopic(e.target.value)}
                placeholder="AI automation benefits..."
                className="w-full px-4 py-3 rounded-lg bg-surface2 border border-border focus:border-[#0A66C2] focus:ring-2 focus:ring-[#0A66C2]/20 outline-none transition-all"
              />
            </div>
          </div>

          <div>
            <label className="block text-sm font-medium mb-2">Content</label>
            <textarea
              rows={8}
              value={content}
              onChange={(e) => setContent(e.target.value)}
              placeholder="Share your professional thoughts, insights, or updates with your LinkedIn network..."
              className="w-full px-4 py-3 rounded-lg bg-surface2 border border-border focus:border-[#0A66C2] focus:ring-2 focus:ring-[#0A66C2]/20 outline-none transition-all resize-none"
              required
            ></textarea>
            <div className="flex justify-between mt-2">
              <p className={`text-xs ${charCount > maxChars ? 'text-red-400' : 'text-muted'}`}>
                {charCount} / {maxChars} characters
              </p>
              <p className="text-xs text-muted">Tip: Add 3-5 relevant hashtags</p>
            </div>
          </div>

          <div className="flex gap-3 pt-2">
            <button
              type="button"
              onClick={() => { setContent(''); setTopic(''); }}
              className="flex-1 px-4 py-3 rounded-lg bg-surface2 border border-border hover:bg-surface/50 font-medium transition-all"
            >
              Clear
            </button>
            <button
              type="submit"
              disabled={isSubmitting || charCount === 0 || charCount > maxChars}
              className="flex-1 px-4 py-3 rounded-lg bg-[#0A66C2] hover:bg-[#0A66C2]/90 text-white font-medium transition-all flex items-center justify-center gap-2 disabled:opacity-50 disabled:cursor-not-allowed"
            >
              {isSubmitting ? (
                <>
                  <svg className="w-4 h-4 animate-spin" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15"></path>
                  </svg>
                  Posting...
                </>
              ) : (
                <>
                  <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M12 19l9 2-9-18-9 18 9-2zm0 0v-8"></path>
                  </svg>
                  Post to LinkedIn
                </>
              )}
            </button>
          </div>
        </form>

        <div className="mt-4 p-3 rounded-lg bg-surface2 border border-border-subtle">
          <p className="text-xs text-muted">
            <strong>Note:</strong> This will open your browser and post directly to LinkedIn using your saved session.
            The process takes about 30-60 seconds.
          </p>
        </div>
      </div>
    );
  }

  // Render content based on active tab
  const renderContent = () => {
    switch (activeTab) {
      case 'dashboard':
        return (
          <>
            {/* Stats Strip */}
            <div className="mt-8">
              <StatsStrip />
            </div>

            {/* System Architecture */}
            <div className="mt-8">
              <ArchitectureDiagram />
            </div>

            {/* Professional Dashboard Overview */}
            <div className="grid grid-cols-1 lg:grid-cols-4 gap-6">
              <div className="lg:col-span-1">
                {/* Tier Status */}
                <TierStatus currentTier={activeTier} />
              </div>
              <div className="lg:col-span-3">
                {/* Social Media Dashboard */}
                <SocialDashboard />
              </div>
            </div>

            {/* Live Control Panel */}
            <div className="mt-8 grid grid-cols-1 lg:grid-cols-3 gap-6">
              {/* Live Status - Takes 2 columns */}
              <div className="lg:col-span-2">
                <LiveStatus />
              </div>

              {/* Activity Feed - Takes 1 column */}
              <div className="lg:col-span-1">
                <ActivityFeed />
              </div>
            </div>

            {/* Quick Actions & Approval Queue */}
            <div className="mt-8 grid grid-cols-1 lg:grid-cols-2 gap-6">
              <QuickActions />
              <ApprovalQueue />
            </div>

            {/* Tier Navigation */}
            <div className="mt-12">
              <TierNav activeTier={activeTier} onTierChange={setActiveTier} />
            </div>

            {/* Agent Cards by Tier */}
            <div className="mt-8">
              <AgentCard tier={activeTier} />
            </div>
          </>
        );
      case 'email':
      case 'gmail':
        return (
          <div className="mt-8">
            <h2 className="text-2xl font-bold font-syne mb-6">Gmail Actions</h2>
            <EmailForm />
          </div>
        );
      case 'whatsapp':
        return (
          <div className="mt-8">
            <h2 className="text-2xl font-bold font-syne mb-6">WhatsApp Actions</h2>
            <WhatsAppForm />
          </div>
        );
      case 'instagram':
        return (
          <div className="mt-8">
            <h2 className="text-2xl font-bold font-syne mb-6">Instagram Actions</h2>
            <InstagramForm />
          </div>
        );
      case 'analytics':
        return (
          <div className="mt-8">
            <h2 className="text-2xl font-bold font-syne mb-6">Analytics Dashboard</h2>
            <AnalyticsView />
          </div>
        );
      case 'linkedin':
        return (
          <div className="mt-8">
            <h2 className="text-2xl font-bold font-syne mb-6">LinkedIn Actions</h2>
            <LinkedInForm />
          </div>
        );
      case 'twitter':
        return (
          <div className="mt-8">
            <h2 className="text-2xl font-bold font-syne mb-6">Twitter Actions</h2>
            <div className="p-6 rounded-lg bg-surface border border-border">
              <div className="flex items-center gap-3 mb-4 pb-4 border-b border-border-subtle">
                <div className="w-10 h-10 rounded-lg bg-[#1DA1F2]/10 flex items-center justify-center">
                  <svg className="w-5 h-5 text-[#1DA1F2]" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M12 16a4 4 0 100-8 4 4 0 000 8z"></path>
                  </svg>
                </div>
                <div>
                  <h3 className="font-semibold font-syne">Twitter</h3>
                  <p className="text-xs text-muted">Create tweet</p>
                </div>
                <div className="ml-auto">
                  <span className="px-3 py-1 rounded-full bg-green-500/20 text-green-400 text-xs font-medium">
                    Connected
                  </span>
                </div>
              </div>

              <form onSubmit={(e) => {
                e.preventDefault();
                alert('Twitter post functionality would be implemented here');
              }} className="space-y-4">
                <div>
                  <label className="block text-sm font-medium mb-2">Tweet Content</label>
                  <textarea
                    rows={5}
                    placeholder="What's happening?"
                    className="w-full px-4 py-3 rounded-lg bg-surface2 border border-border focus:border-[#1DA1F2] focus:ring-2 focus:ring-[#1DA1F2]/20 outline-none transition-all resize-none"
                  ></textarea>
                  <div className="flex justify-between mt-2">
                    <p className="text-xs text-muted">0 / 280 characters</p>
                    <p className="text-xs text-muted">Max 4 images</p>
                  </div>
                </div>

                <div className="flex gap-3 pt-2">
                  <button
                    type="button"
                    className="flex-1 px-4 py-3 rounded-lg bg-surface2 border border-border hover:bg-surface/50 font-medium transition-all"
                  >
                    Schedule
                  </button>
                  <button
                    type="submit"
                    className="flex-1 px-4 py-3 rounded-lg bg-[#1DA1F2] hover:bg-[#1DA1F2]/90 text-white font-medium transition-all flex items-center justify-center gap-2"
                  >
                    <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M12 19l9 2-9-18-9 18 9-2zm0 0v-8"></path>
                    </svg>
                    Tweet
                  </button>
                </div>
              </form>
            </div>
          </div>
        );
      case 'facebook':
        return (
          <div className="mt-8">
            <h2 className="text-2xl font-bold font-syne mb-6">Facebook Actions</h2>
            <div className="p-6 rounded-lg bg-surface border border-border">
              <div className="flex items-center gap-3 mb-4 pb-4 border-b border-border-subtle">
                <div className="w-10 h-10 rounded-lg bg-[#1877F2]/10 flex items-center justify-center">
                  <svg className="w-5 h-5 text-[#1877F2]" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M18 9v3m0 0v3m0-3h3m-3 0h-3m-2-5a4 4 0 11-8 0 4 4 0 018 0zM3 20a6 6 0 0112 0v1H3v-1z"></path>
                  </svg>
                </div>
                <div>
                  <h3 className="font-semibold font-syne">Facebook</h3>
                  <p className="text-xs text-muted">Create post</p>
                </div>
                <div className="ml-auto">
                  <span className="px-3 py-1 rounded-full bg-green-500/20 text-green-400 text-xs font-medium">
                    Connected
                  </span>
                </div>
              </div>

              <form onSubmit={(e) => {
                e.preventDefault();
                alert('Facebook post functionality would be implemented here');
              }} className="space-y-4">
                <div>
                  <label className="block text-sm font-medium mb-2">Post Content</label>
                  <textarea
                    rows={5}
                    placeholder="What's on your mind?"
                    className="w-full px-4 py-3 rounded-lg bg-surface2 border border-border focus:border-[#1877F2] focus:ring-2 focus:ring-[#1877F2]/20 outline-none transition-all resize-none"
                  ></textarea>
                </div>

                <div>
                  <label className="block text-sm font-medium mb-2">Image/Video</label>
                  <div className="border-2 border-dashed border-border rounded-lg p-8 text-center hover:border-[#1877F2] transition-all cursor-pointer">
                    <svg className="mx-auto mb-2 text-muted" fill="none" stroke="currentColor" viewBox="0 0 24 24" width="32" height="32" xmlns="http://www.w3.org/2000/svg">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M12 6v6m0 0v6m0-6h6m-6 0H6"></path>
                    </svg>
                    <p className="text-sm text-muted">Add photos or videos</p>
                  </div>
                </div>

                <div className="flex gap-3 pt-2">
                  <button
                    type="button"
                    className="flex-1 px-4 py-3 rounded-lg bg-surface2 border border-border hover:bg-surface/50 font-medium transition-all"
                  >
                    Save Draft
                  </button>
                  <button
                    type="submit"
                    className="flex-1 px-4 py-3 rounded-lg bg-[#1877F2] hover:bg-[#1877F2]/90 text-white font-medium transition-all flex items-center justify-center gap-2"
                  >
                    <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M12 19l9 2-9-18-9 18 9-2zm0 0v-8"></path>
                    </svg>
                    Post
                  </button>
                </div>
              </form>
            </div>
          </div>
        );
      default:
        return (
          <>
            {/* Stats Strip */}
            <div className="mt-8">
              <StatsStrip />
            </div>

            {/* System Architecture */}
            <div className="mt-8">
              <ArchitectureDiagram />
            </div>

            {/* Professional Dashboard Overview */}
            <div className="grid grid-cols-1 lg:grid-cols-4 gap-6">
              <div className="lg:col-span-1">
                {/* Tier Status */}
                <TierStatus currentTier={activeTier} />
              </div>
              <div className="lg:col-span-3">
                {/* Social Media Dashboard */}
                <SocialDashboard />
              </div>
            </div>

            {/* Live Control Panel */}
            <div className="mt-8 grid grid-cols-1 lg:grid-cols-3 gap-6">
              {/* Live Status - Takes 2 columns */}
              <div className="lg:col-span-2">
                <LiveStatus />
              </div>

              {/* Activity Feed - Takes 1 column */}
              <div className="lg:col-span-1">
                <ActivityFeed />
              </div>
            </div>

            {/* Quick Actions & Approval Queue */}
            <div className="mt-8 grid grid-cols-1 lg:grid-cols-2 gap-6">
              <QuickActions />
              <ApprovalQueue />
            </div>

            {/* Tier Navigation */}
            <div className="mt-12">
              <TierNav activeTier={activeTier} onTierChange={setActiveTier} />
            </div>

            {/* Agent Cards by Tier */}
            <div className="mt-8">
              <AgentCard tier={activeTier} />
            </div>
          </>
        );
    }
  };

  return (
    <div className="flex">
      <div className="hidden lg:block">
        <SocialNav onTabChange={handleTabChange} />
      </div>
      <main className="flex-1 container mx-auto px-4 py-8 max-w-7xl">
        <Header />
        {renderContent()}
      </main>
    </div>
  )
}