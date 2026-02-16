'use client';

import { useState } from 'react';

export default function QuickActionForms() {
  const [activeTab, setActiveTab] = useState<'email' | 'whatsapp' | 'linkedin'>('email');
  const [loading, setLoading] = useState(false);
  const [message, setMessage] = useState('');

  // Email Form State
  const [emailData, setEmailData] = useState({
    to: '',
    subject: '',
    body: ''
  });

  // WhatsApp Form State
  const [whatsappData, setWhatsappData] = useState({
    phone: '',
    message: ''
  });

  // LinkedIn Form State
  const [linkedinData, setLinkedinData] = useState({
    content: '',
    imageUrl: ''
  });

  const handleEmailSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setMessage('');

    try {
      const response = await fetch('/api/actions/send-email-direct', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(emailData)
      });

      const result = await response.json();

      if (response.ok) {
        if (result.fallback) {
          setMessage('✅ Email queued for sending (direct send unavailable)');
        } else {
          setMessage('✅ Email sent successfully via Gmail!');
        }
        setEmailData({ to: '', subject: '', body: '' });
      } else {
        setMessage(`❌ Error: ${result.error}`);
      }
    } catch (error) {
      setMessage('❌ Failed to send email');
    } finally {
      setLoading(false);
    }
  };

  const handleWhatsAppSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setMessage('');

    try {
      const response = await fetch('/api/actions/send-whatsapp', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(whatsappData)
      });

      const result = await response.json();

      if (response.ok) {
        setMessage('✅ WhatsApp message sent successfully!');
        setWhatsappData({ phone: '', message: '' });
      } else {
        setMessage(`❌ Error: ${result.error}`);
      }
    } catch (error) {
      setMessage('❌ Failed to send WhatsApp message');
    } finally {
      setLoading(false);
    }
  };

  const handleLinkedInSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setMessage('');

    try {
      const response = await fetch('/api/actions/post-linkedin', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(linkedinData)
      });

      const result = await response.json();

      if (response.ok) {
        setMessage('✅ LinkedIn post created successfully!');
        setLinkedinData({ content: '', imageUrl: '' });
      } else {
        setMessage(`❌ Error: ${result.error}`);
      }
    } catch (error) {
      setMessage('❌ Failed to post to LinkedIn');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="bg-white rounded-lg shadow-md p-6">
      <h2 className="text-2xl font-bold mb-6">Quick Actions</h2>

      {/* Tabs */}
      <div className="flex space-x-4 mb-6 border-b">
        <button
          onClick={() => setActiveTab('email')}
          className={`pb-2 px-4 font-medium transition-colors ${
            activeTab === 'email'
              ? 'border-b-2 border-blue-500 text-blue-600'
              : 'text-gray-500 hover:text-gray-700'
          }`}
        >
          📧 Email
        </button>
        <button
          onClick={() => setActiveTab('whatsapp')}
          className={`pb-2 px-4 font-medium transition-colors ${
            activeTab === 'whatsapp'
              ? 'border-b-2 border-green-500 text-green-600'
              : 'text-gray-500 hover:text-gray-700'
          }`}
        >
          💬 WhatsApp
        </button>
        <button
          onClick={() => setActiveTab('linkedin')}
          className={`pb-2 px-4 font-medium transition-colors ${
            activeTab === 'linkedin'
              ? 'border-b-2 border-blue-700 text-blue-700'
              : 'text-gray-500 hover:text-gray-700'
          }`}
        >
          💼 LinkedIn
        </button>
      </div>

      {/* Message Display */}
      {message && (
        <div className={`mb-4 p-3 rounded ${
          message.includes('✅') ? 'bg-green-50 text-green-800' : 'bg-red-50 text-red-800'
        }`}>
          {message}
        </div>
      )}

      {/* Email Form */}
      {activeTab === 'email' && (
        <form onSubmit={handleEmailSubmit} className="space-y-4">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              To Email Address
            </label>
            <input
              type="email"
              required
              value={emailData.to}
              onChange={(e) => setEmailData({ ...emailData, to: e.target.value })}
              className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
              placeholder="recipient@example.com"
            />
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Subject
            </label>
            <input
              type="text"
              required
              value={emailData.subject}
              onChange={(e) => setEmailData({ ...emailData, subject: e.target.value })}
              className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
              placeholder="Email subject"
            />
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Message
            </label>
            <textarea
              required
              value={emailData.body}
              onChange={(e) => setEmailData({ ...emailData, body: e.target.value })}
              rows={6}
              className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
              placeholder="Email body..."
            />
          </div>

          <button
            type="submit"
            disabled={loading}
            className="w-full bg-blue-600 text-white py-2 px-4 rounded-md hover:bg-blue-700 disabled:bg-gray-400 disabled:cursor-not-allowed transition-colors"
          >
            {loading ? 'Sending...' : 'Send Email'}
          </button>
        </form>
      )}

      {/* WhatsApp Form */}
      {activeTab === 'whatsapp' && (
        <form onSubmit={handleWhatsAppSubmit} className="space-y-4">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Phone Number
            </label>
            <input
              type="tel"
              required
              value={whatsappData.phone}
              onChange={(e) => setWhatsappData({ ...whatsappData, phone: e.target.value })}
              className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-green-500"
              placeholder="+1234567890"
            />
            <p className="text-xs text-gray-500 mt-1">Include country code (e.g., +92 for Pakistan)</p>
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Message
            </label>
            <textarea
              required
              value={whatsappData.message}
              onChange={(e) => setWhatsappData({ ...whatsappData, message: e.target.value })}
              rows={6}
              className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-green-500"
              placeholder="WhatsApp message..."
            />
          </div>

          <button
            type="submit"
            disabled={loading}
            className="w-full bg-green-600 text-white py-2 px-4 rounded-md hover:bg-green-700 disabled:bg-gray-400 disabled:cursor-not-allowed transition-colors"
          >
            {loading ? 'Sending...' : 'Send WhatsApp Message'}
          </button>
        </form>
      )}

      {/* LinkedIn Form */}
      {activeTab === 'linkedin' && (
        <form onSubmit={handleLinkedInSubmit} className="space-y-4">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Post Content
            </label>
            <textarea
              required
              value={linkedinData.content}
              onChange={(e) => setLinkedinData({ ...linkedinData, content: e.target.value })}
              rows={6}
              className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-700"
              placeholder="What do you want to share on LinkedIn?"
            />
            <p className="text-xs text-gray-500 mt-1">Max 3000 characters</p>
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Image URL (Optional)
            </label>
            <input
              type="url"
              value={linkedinData.imageUrl}
              onChange={(e) => setLinkedinData({ ...linkedinData, imageUrl: e.target.value })}
              className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-700"
              placeholder="https://example.com/image.jpg"
            />
          </div>

          <button
            type="submit"
            disabled={loading}
            className="w-full bg-blue-700 text-white py-2 px-4 rounded-md hover:bg-blue-800 disabled:bg-gray-400 disabled:cursor-not-allowed transition-colors"
          >
            {loading ? 'Posting...' : 'Post to LinkedIn'}
          </button>
        </form>
      )}
    </div>
  );
}
