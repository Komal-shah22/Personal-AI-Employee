# 🚀 AI Employee Dashboard - Enterprise Edition

An **ultra-professional, enterprise-grade** dashboard for monitoring and controlling your Personal AI Employee system. Built with Next.js 14, TypeScript, and Tailwind CSS.

![Next.js](https://img.shields.io/badge/Next.js-14-black) ![TypeScript](https://img.shields.io/badge/TypeScript-5.4-blue) ![Tailwind CSS](https://img.shields.io/badge/Tailwind-3.4-38bdf8)

---

## ✨ Features

### 🎨 Refined Design System
- **Professional Color Palette**: Deep void background (#030712), refined surfaces, brand gradients
- **Premium Typography**: Inter Variable, JetBrains Mono for code
- **Smooth Animations**: Framer Motion with 60fps performance
- **Responsive Design**: Mobile, tablet, desktop optimized

### 🎯 Dashboard Components

#### 1. Hero Metrics (4 Cards)
- **Tasks Processed Today** - Animated counter with sparkline chart
- **Active Agents** - Real-time status with uptime percentage
- **Pending Approvals** - Count with average response time
- **System Health** - Score with trend visualization

Each metric card features:
- Animated number counters
- Mini trend charts (sparklines)
- Change indicators (↑ 12% vs yesterday)
- Hover effects with glow

#### 2. Agent Status Grid (6 Agents)
- Gmail Watcher 📧
- WhatsApp Monitor 💬
- LinkedIn Agent 💼
- File Watcher 📂
- Orchestrator 🎛️

Each agent card shows:
- Real-time status (🟢 Running, 🔴 Stopped, 🟡 Starting)
- Last activity timestamp
- Quick stats (emails processed, etc.)
- Control buttons: Start, Stop, Restart, Logs

#### 3. Real-time Activity Feed
- Live stream of agent actions
- Timeline view with agent icons
- Color-coded status badges
- Auto-scroll to latest
- Updates every 5 seconds

#### 4. Quick Actions Panel
- Process Queue → Trigger orchestrator
- CEO Briefing → Generate report
- Test Email → Send via MCP
- Test LinkedIn → Create post
- Health Check → Monitor services
- Sync Data → Refresh all

Each action button features:
- Loading states with progress bars
- Success/error indicators
- Ripple effects on click

#### 5. Interactive Charts
- **Tasks Over Time** - Line chart with 7-day trends
- **Agent Activity** - Horizontal bar chart
- Time range selector (1D, 7D, 30D)
- Gradient fills and smooth animations

#### 6. Approval Queue
- Expandable approval cards
- Preview of action content
- One-click Approve/Reject
- Priority badges (High, Normal, Low)
- File moving to Approved/Rejected folders

### 🎭 Advanced Features

#### Micro-interactions
- Ripple effects on button clicks
- Smooth hover animations (scale, glow)
- Loading skeletons (not spinners)
- Success/error states with animations

#### Real-time Updates
- Polling every 3-5 seconds
- Optimistic UI updates
- Auto-scroll in activity feed
- Live status indicators

#### Professional UI
- Glass-morphism effects
- Gradient mesh backgrounds
- Custom scrollbars
- Focus-visible states
- Accessible (WCAG AA)

---

## 🚀 Quick Start

### Prerequisites
- Node.js 18+ installed
- Python 3.8+ (for backend scripts)
- PM2 installed globally (optional): `npm install -g pm2`

### Installation

1. **Navigate to dashboard directory**
```bash
cd ai-employee-dashboard
```

2. **Install dependencies**
```bash
npm install
```

3. **Configure environment**
```bash
cp .env.local.example .env.local
```

Edit `.env.local` with your paths:
```env
VAULT_PATH=E:/hackathon-0/Personal_AI_Employee/AI_Employee_Vault
SCRIPTS_PATH=E:/hackathon-0/Personal_AI_Employee
PM2_HOME=C:/Users/YourUser/.pm2
PORT=3000
```

4. **Run development server**
```bash
npm run dev
```

5. **Open browser**
```
http://localhost:3000
```

---

## 📁 Project Structure

```
ai-employee-dashboard/
├── src/
│   ├── app/
│   │   ├── api/                          # API Routes
│   │   │   ├── dashboard/route.ts        # Main dashboard data
│   │   │   ├── activity/stream/route.ts  # Real-time activity
│   │   │   ├── approvals/
│   │   │   │   ├── route.ts              # List approvals
│   │   │   │   └── [id]/action/route.ts  # Approve/reject
│   │   │   ├── agents/[id]/control/route.ts  # Agent control
│   │   │   ├── chart-data/route.ts       # Chart data
│   │   │   └── test/                     # Test endpoints
│   │   ├── layout.tsx                    # Root layout
│   │   ├── page.tsx                      # Main dashboard
│   │   └── globals.css                   # Global styles
│   │
│   └── components/
│       ├── layout/
│       │   ├── Sidebar.tsx               # Navigation sidebar
│       │   └── TopBar.tsx                # Time-aware greeting
│       ├── dashboard/
│       │   ├── HeroMetrics.tsx           # 4 metric cards
│       │   ├── AgentGrid.tsx             # Agent status cards
│       │   ├── ActivityFeed.tsx          # Real-time feed
│       │   ├── QuickActions.tsx          # Action buttons
│       │   ├── ApprovalQueue.tsx         # Approval list
│       │   └── Charts.tsx                # Data visualization
│       └── ui/
│           └── LoadingSkeleton.tsx       # Loading states
│
├── .env.local.example                    # Environment template
├── package.json                          # Dependencies
├── tailwind.config.js                    # Tailwind config
├── tsconfig.json                         # TypeScript config
└── README.md                             # This file
```

---

## 🎨 Design System

### Color Palette (Refined Dark)
```css
--void: #030712          /* Deepest background */
--surface-1: #0f1419     /* Cards */
--surface-2: #1a1f2e     /* Nested elements */
--surface-3: #252b3b     /* Hover states */

--border-subtle: #1e293b
--border-default: #334155
--border-strong: #475569

--text-primary: #f1f5f9
--text-secondary: #94a3b8
--text-tertiary: #64748b

--success: #10b981
--warning: #f59e0b
--error: #ef4444
--info: #3b82f6

--brand-primary: #6366f1  /* Indigo */
--brand-secondary: #8b5cf6 /* Purple */
```

### Typography
- **Sans**: Inter Variable (body text)
- **Display**: Inter (headings, bold weights)
- **Mono**: JetBrains Mono (code, data)

### Animations
- Page load: Staggered slide-up (50ms delay)
- Hover: Scale 1.02 + glow
- Status pulse: 2s ease-in-out infinite
- Transitions: 200-300ms ease-in-out

---

## 🔌 API Endpoints

### Dashboard Data
```typescript
GET /api/dashboard
Response: {
  metrics: { tasksToday, activeAgents, pendingApprovals, systemHealth },
  agents: [{ id, name, icon, status, lastActive, stats }]
}
```

### Agent Control
```typescript
POST /api/agents/[id]/control
Body: { action: "start" | "stop" | "restart" }
Response: { success: true, status: "running" }
```

### Activity Stream
```typescript
GET /api/activity/stream
Response: {
  activities: [{ id, timestamp, agent, action, status }]
}
```

### Approvals
```typescript
GET /api/approvals
Response: [{ id, type, title, preview, priority, requestedAt }]

POST /api/approvals/[id]/action
Body: { action: "approve" | "reject" }
Response: { success: true }
```

### Chart Data
```typescript
GET /api/chart-data?range=7D
Response: [{ date, completed, pending, agent, tasks }]
```

---

## 🛠️ Development

### Run Development Server
```bash
npm run dev
```
Dashboard available at `http://localhost:3000`

### Build for Production
```bash
npm run build
```

### Start Production Server
```bash
npm run start
```

### Type Check
```bash
npm run type-check
```

---

## 📊 Performance

- **Page Load**: < 2 seconds
- **Animations**: 60fps
- **Bundle Size**: Optimized with Next.js
- **Real-time Updates**: 3-5 second polling
- **Responsive**: Mobile, tablet, desktop

---

## 🎯 Key Features

### Real-time Updates
- All sections poll every 3-5 seconds
- Optimistic UI updates
- Auto-scroll in activity feed
- Live status indicators

### Professional Design
- Glass-morphism cards
- Gradient mesh backgrounds
- Smooth animations
- Custom scrollbars
- Focus-visible states

### Enterprise-Ready
- TypeScript type safety
- Error handling with toasts
- Loading skeletons
- Responsive design
- Accessible (WCAG AA)

---

## 🐛 Troubleshooting

### Dashboard won't start
```bash
rm -rf .next node_modules
npm install
npm run dev
```

### API endpoints returning errors
- Check `.env.local` paths are correct
- Verify vault folders exist
- Ensure Python scripts are in SCRIPTS_PATH

### Agents won't start/stop
- Install PM2: `npm install -g pm2`
- Check PM2 is running: `pm2 list`

---

## 🚀 Deployment

### Vercel (Recommended)
```bash
npm install -g vercel
vercel
```

### Docker
```dockerfile
FROM node:18-alpine
WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .
RUN npm run build
EXPOSE 3000
CMD ["npm", "start"]
```

---

## 📄 License

MIT License - feel free to use this in your projects!

---

## 🙏 Credits

Built with:
- [Next.js 14](https://nextjs.org/)
- [Tailwind CSS](https://tailwindcss.com/)
- [Framer Motion](https://www.framer.com/motion/)
- [Recharts](https://recharts.org/)
- [Lucide Icons](https://lucide.dev/)
- [Sonner](https://sonner.emilkowal.ski/)

---

**Made with ❤️ for the Personal AI Employee Project**

🎨 **ENTERPRISE-GRADE** | ⚡ **FAST** | 🚀 **PRODUCTION-READY**
