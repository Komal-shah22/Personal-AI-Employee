# 🚀 AI Employee Dashboard - Quick Start Guide

## ⚡ 5-Minute Setup

### Step 1: Install Dependencies
```bash
cd ai-employee-dashboard
npm install
```

### Step 2: Configure Environment
```bash
cp .env.example .env.local
```

Edit `.env.local` with your paths:
```env
VAULT_PATH=E:/hackathon-0/Personal_AI_Employee/AI_Employee_Vault
SCRIPTS_PATH=E:/hackathon-0/Personal_AI_Employee
PM2_PATH=C:/Users/YourUser/.pm2
PORT=3000
```

### Step 3: Start Dashboard
```bash
npm run dev
```

### Step 4: Open Browser
Navigate to: **http://localhost:3000**

---

## 🎯 What You'll See

### Hero Section (Top)
- **AI Employee Status Badge** - Green pulse = Online, Red = Offline
- **4 Stat Cards**: Needs Action, In Progress, Done Today, Pending Approval

### Agent Status Grid
5 agent cards with Start/Stop/Restart buttons and live status indicators.

### Quick Actions Panel
5 colorful action buttons for common tasks.

### Performance Chart
Line chart showing 7-day trends for completed, in progress, and pending tasks.

### Activity Feed
Real-time stream of recent actions with color-coded icons.

---

## 🐛 Troubleshooting

### Dashboard shows "0" for all stats
- Check that `VAULT_PATH` in `.env.local` is correct
- Verify the vault folders exist

### Agents won't start/stop
- Ensure PM2 is installed: `npm install -g pm2`
- Check that agent scripts are running: `pm2 list`

---

**Enjoy your beautiful dashboard!** 🎨✨
