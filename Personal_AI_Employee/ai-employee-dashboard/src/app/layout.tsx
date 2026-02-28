import './globals.css'
import type { Metadata } from 'next'
import { Toaster } from 'sonner'

export const metadata: Metadata = {
  title: 'Personal AI Employee Dashboard',
  description: 'Production-ready dashboard for managing AI agents and workflows',
  icons: {
    icon: '/favicon.ico',
  },
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en">
      <body className="antialiased">
        <div className="min-h-screen animated-gradient grid-pattern">
          <div className="flex">
            <div className="hidden lg:block">
              <div className="fixed left-0 top-0 h-full w-64">
                <div className="h-full overflow-y-auto">
                  {/* Navigation will be implemented separately */}
                  <div className="p-4">
                    <h1 className="text-xl font-bold flex items-center gap-2">
                      <svg className="w-8 h-8" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z"></path>
                      </svg>
                      <span>Social Media</span>
                    </h1>
                    <p className="text-sm text-muted mt-1">AI Employee Dashboard</p>
                  </div>
                </div>
              </div>
            </div>

            <div className="flex-1 lg:ml-64">
              {children}
            </div>
          </div>
        </div>
        <Toaster
          position="top-right"
          theme="dark"
          toastOptions={{
            style: {
              background: 'var(--surface)',
              border: '1px solid var(--border)',
              color: 'var(--text)',
            },
          }}
        />
      </body>
    </html>
  )
}
