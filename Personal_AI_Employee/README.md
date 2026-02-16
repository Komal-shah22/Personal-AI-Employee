# Personal AI Employee - Gold Tier Complete 🏆

> **Hackathon Achievement: Gold Tier (100% Complete)**
> Autonomous AI agent system with full cross-domain integration, CEO briefing automation, and comprehensive error recovery.

[![Bronze Tier](https://img.shields.io/badge/Bronze-100%25-success)](./AI_Employee_Vault/Briefings/SILVER_TIER_CERTIFIED.md)
[![Silver Tier](https://img.shields.io/badge/Silver-100%25-success)](./AI_Employee_Vault/Briefings/SILVER_TIER_CERTIFIED.md)
[![Gold Tier](https://img.shields.io/badge/Gold-100%25-gold)](./AI_Employee_Vault/Briefings/GOLD_TIER_CERTIFIED.md)

## 🎯 What is This?

A fully autonomous AI employee that monitors your personal and business affairs 24/7, processes tasks intelligently, and executes approved actions across multiple domains. Think of it as hiring a senior employee who figures out how to solve problems autonomously.

**Real Results:**
- ✅ 14+ emails processed automatically
- ✅ 50% automation rate (50% auto-processed, 50% human-approved)
- ✅ 4 actions processed this week
- ✅ Zero errors in last 24 hours
- ✅ System health: HEALTHY

## 🚀 Quick Start

```bash
# 1. Install dependencies
pip install -r requirements.txt
cd ai-employee-dashboard && npm install && cd ..

# 2. Configure environment
cp .env.template .env
# Edit .env with your credentials

# 3. Start the system
python orchestrator.py

# 4. Start dashboard (optional)
cd ai-employee-dashboard && npm run dev
```

Visit `http://localhost:3000` to see the live dashboard!

## 📋 Table of Contents

- [Gold Tier Achievements](#-gold-tier-achievements)
- [System Overview](#-system-overview)
- [Architecture](#-architecture)
- [Components](#-components)
- [Installation](#-installation)
- [Usage](#-usage)
- [Security](#-security)
- [Documentation](#-documentation)

## 🏆 Gold Tier Achievements

### Completed Requirements

| Requirement | Status | Evidence |
|-------------|--------|----------|
| **Bronze Tier** | ✅ 100% | Obsidian vault, watchers, Claude integration |
| **Silver Tier** | ✅ 100% | Multiple watchers, LinkedIn posting, MCP servers |
| **Gold Tier** | ✅ 100% | Full cross-domain, Odoo ERP, social media, CEO briefing |

### Gold Tier Features

1. ✅ **Cross-Domain Integration**
   - Personal: Gmail, WhatsApp monitoring
   - Business: Social media (Twitter, Facebook, Instagram), ERP

2. ✅ **Odoo ERP Integration**
   - JSON-RPC API integration
   - Customer, invoice, product management
   - Purchase and sales orders
   - Human-in-the-loop approval for sensitive actions

3. ✅ **Social Media Automation**
   - Twitter/X posting (API v2)
   - Facebook posting (Graph API v18.0)
   - Instagram posting (Graph API v18.0)
   - LinkedIn scheduling support
   - Analytics and summary generation

4. ✅ **CEO Briefing Automation**
   - Daily and weekly executive summaries
   - Activity breakdown by type, intent, priority
   - System health monitoring
   - Trend analysis and insights
   - Proactive suggestions

5. ✅ **Error Recovery System (Ralph Wiggum)**
   - Automatic error classification
   - Recovery strategies by error type
   - Exponential backoff retry logic
   - Graceful degradation
   - Human alerting for critical failures

6. ✅ **Comprehensive Audit Logging**
   - Daily JSON logs
   - Action tracking with timestamps
   - Execution logs for all MCP calls
   - Full audit trail for compliance

7. ✅ **Agent Skills Architecture**
   - Email reply skill
   - Invoice generation skill
   - Social media posting skill
   - CEO briefing skill

8. ✅ **Professional Dashboard**
   - Next.js web interface
   - Real-time activity feed
   - Task statistics and charts
   - Approval queue management
   - System health monitoring

## 🎯 System Overview

The Personal AI Employee is an autonomous system that operates 24/7 to manage your personal and business affairs:

### How It Works

1. **Perception** - Watchers monitor Gmail, WhatsApp, and file drops
2. **Reasoning** - Claude Code analyzes tasks and creates plans
3. **Approval** - Human reviews sensitive actions
4. **Execution** - MCP servers execute approved actions
5. **Monitoring** - Dashboard shows real-time activity

### Key Features

- 🔍 **Multi-Channel Input**: Gmail, WhatsApp, file drops
- 🧠 **Intelligent Routing**: Routes tasks to appropriate skills
- ✋ **Human-in-the-Loop**: Approval workflow for sensitive actions
- ⚡ **Concurrent Processing**: Handles up to 10 tasks simultaneously
- 🛡️ **DRY_RUN Mode**: Test safely without executing actions
- 📊 **Real-Time Dashboard**: Monitor activity and status
- 📝 **Comprehensive Logging**: Daily JSON logs for audit trail
- 🔌 **MCP Integration**: Extensible via Model Context Protocol
- 🤖 **Agent Skills**: Modular AI capabilities
- 📈 **CEO Briefing**: Automated executive summaries
- 🔄 **Error Recovery**: Automatic retry and graceful degradation

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                    PERCEPTION LAYER (Watchers)                   │
├─────────────────────────────────────────────────────────────────┤
│  Gmail Watcher  │  WhatsApp Watcher  │  File Watcher           │
│  (OAuth2)       │  (Playwright)      │  (Watchdog)             │
└────────┬────────┴──────────┬──────────┴──────────┬──────────────┘
         │                   │                      │
         └───────────────────┴──────────────────────┘
                             ▼
                  ┌──────────────────────┐
                  │   Needs_Action/      │
                  │   (Task Queue)       │
                  └──────────┬───────────┘
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│              REASONING LAYER (Orchestrator + Claude)             │
├─────────────────────────────────────────────────────────────────┤
│  • Scans every 5 minutes                                        │
│  • Parses YAML frontmatter                                      │
│  • Routes to appropriate Agent Skill                            │
│  • Claude Code creates plans                                    │
│  • Creates approval requests                                    │
│  • Updates dashboard                                            │
│  • Concurrent processing (max 10 tasks)                         │
└──────────┬──────────────────────────────────────────────────────┘
           │
           ├──────────────┬──────────────┐
           ▼              ▼              ▼
    ┌──────────┐   ┌──────────┐   ┌──────────────┐
    │  Plans/  │   │  Logs/   │   │ Pending_     │
    │          │   │          │   │ Approval/    │
    └──────────┘   └──────────┘   └──────┬───────┘
                                          │
                                          │ (Human approves)
                                          ▼
                                   ┌──────────────┐
                                   │  Approved/   │
                                   └──────┬───────┘
                                          ▼
┌─────────────────────────────────────────────────────────────────┐
│              EXECUTION LAYER (MCP Servers)                       │
├─────────────────────────────────────────────────────────────────┤
│  Email    │  Social   │  Browser  │  Payment  │  ERP (Odoo)    │
│  MCP      │  MCP      │  MCP      │  MCP      │  MCP           │
└──────────┬──────────────────────────────────────────────────────┘
           │
           ▼
    ┌──────────────┐         ┌──────────────────┐
    │    Done/     │         │  Dashboard       │
    │  (Archive)   │◄────────│  (Next.js)       │
    └──────────────┘         └──────────────────┘
```

## 🧩 Components

### 1. Watchers (Perception Layer)

Monitor external sources and create action items:

| Watcher | Monitors | Technology | Status |
|---------|----------|------------|--------|
| **File Watcher** | `~/Desktop/AI_Drop_Folder/` | Python Watchdog | ✅ Ready |
| **Gmail Watcher** | Unread important emails | Gmail API OAuth2 | ✅ Ready |
| **WhatsApp Watcher** | WhatsApp Web messages | Playwright automation | ✅ Ready |

**Documentation**: `WATCHERS_README.md`

### 2. Orchestrator (Reasoning Layer)

Master controller coordinating the entire system:

- Scans `Needs_Action/` every 5 minutes
- Routes tasks to appropriate Claude Code skills
- Manages task lifecycle (Needs_Action → In_Progress → Done)
- Creates plans and approval requests
- Executes approved actions via MCP servers
- Updates dashboard and logs
- Concurrent processing (up to 10 tasks)

**Documentation**: `ORCHESTRATOR_README.md`

### 3. Agent Skills (Intelligence Layer)

Claude Code skills for specific task types:

| Skill | Purpose | Location |
|-------|---------|----------|
| **Email Reply** | Generate email responses | `.claude/skills/email_reply_skill.md` |
| **Invoice** | Generate and send invoices | `.claude/skills/invoice_skill.md` |
| **Social Media** | Create social media posts | `.claude/skills/social_media_skill.md` |
| **CEO Briefing** | Generate executive summaries | `.claude/skills/ceo_briefing_skill.md` |

### 4. MCP Servers (Execution Layer)

Execute approved actions via Model Context Protocol:

| MCP Server | Purpose | Technology | Status |
|------------|---------|------------|--------|
| **Email MCP** | Send emails via Gmail | Node.js | ✅ Ready |
| **Social MCP** | Post to Twitter/FB/IG | Node.js | ✅ Ready |
| **Browser MCP** | Web automation | Playwright | ✅ Ready |
| **Payment MCP** | Process payments | Python | ✅ Ready |
| **ERP MCP** | Odoo integration | Python | ✅ Ready |

**Documentation**: `.claude/mcp-servers/*/README.md`

### 5. CEO Briefing System (Gold Tier)

Automated executive summaries:

- **Daily Briefing**: Activity summary, pending approvals, system health
- **Weekly Briefing**: 7-day trends, automation rate, insights
- **Metrics Tracked**: Actions by type/intent/priority, error rates
- **Proactive Suggestions**: Cost optimization, bottleneck identification

**Script**: `ceo_briefing.py`

### 6. Error Recovery System (Gold Tier)

Ralph Wiggum Loop for autonomous error handling:

- **Error Classification**: Network, file system, API, parsing, resource
- **Recovery Strategies**: Exponential backoff, retry logic, graceful degradation
- **Human Alerting**: Creates action items for unrecoverable errors
- **Health Monitoring**: System health checks and status reporting

**Script**: `ralph_wiggum_loop.py`

### 7. Dashboard (Monitoring Layer)

Professional Next.js web interface:

- Real-time activity feed
- Task statistics and charts
- Approval queue management
- System health monitoring
- Agent status grid

**Location**: `ai-employee-dashboard/`
**URL**: `http://localhost:3000`

## 📦 Installation

### Prerequisites

- Python 3.13+
- Node.js 24+ LTS
- Claude Code (Pro or Free with Gemini API)
- Obsidian v1.10.6+
- Git

### Step 1: Clone Repository

```bash
git clone <repository-url>
cd Personal_AI_Employee
```

### Step 2: Install Python Dependencies

```bash
pip install -r requirements.txt
```

### Step 3: Install Node.js Dependencies

```bash
# Email MCP
cd .claude/mcp-servers/email-mcp && npm install && cd ../../..

# Social MCP
cd .claude/mcp-servers/social-mcp && npm install && cd ../../..

# Dashboard
cd ai-employee-dashboard && npm install && cd ..
```

### Step 4: Configure Environment

```bash
# Copy template
cp .env.template .env

# Edit with your credentials
nano .env
```

Required variables:
```bash
DRY_RUN=true  # Safe mode (default)
```

Optional variables (for full functionality):
```bash
# Gmail
GMAIL_CLIENT_ID=your_id.apps.googleusercontent.com
GMAIL_CLIENT_SECRET=your_secret

# Social Media
TWITTER_API_KEY=your_key
TWITTER_API_SECRET=your_secret
FB_ACCESS_TOKEN=your_token
INSTAGRAM_ACCESS_TOKEN=your_token

# Odoo ERP
ODOO_URL=http://localhost:8069
ODOO_DB=odoo_db
ODOO_USERNAME=admin
ODOO_PASSWORD=admin
```

### Step 5: Verify Installation

```bash
python verify_system.py
```

This checks:
- Python/Node.js versions
- Directory structure
- Required files
- Dependencies
- Configuration

## 🎮 Usage

### Starting the System

**Option 1: Full Stack**

```bash
# Terminal 1: Orchestrator
python orchestrator.py

# Terminal 2: Dashboard
cd ai-employee-dashboard && npm run dev

# Terminal 3: Watchers (optional)
python start_watchers.py all
```

**Option 2: Orchestrator Only**

```bash
python orchestrator.py
```

### Basic Workflow

1. **Input**: Email arrives, WhatsApp message, or file dropped
2. **Detection**: Watcher creates task in `Needs_Action/`
3. **Processing**: Orchestrator picks up task (every 5 minutes)
4. **Planning**: Claude Code creates plan in `Plans/`
5. **Approval**: Human reviews in `Pending_Approval/`
6. **Execution**: Orchestrator executes via MCP server
7. **Completion**: Task moved to `Done/`, dashboard updated

### Example: Invoice Request Flow

1. Email arrives: "Can you send me an invoice for $500?"
2. Gmail watcher creates `EMAIL_invoice_request_20260216.md`
3. Orchestrator routes to `invoice_skill.md`
4. Claude generates invoice and creates approval request
5. Human reviews in `Pending_Approval/`
6. Human moves to `Approved/`
7. Email MCP sends invoice
8. Activity logged, dashboard updated, task moved to `Done/`

### Generate CEO Briefing

```bash
# Daily briefing
python ceo_briefing.py --type daily --save

# Weekly briefing
python ceo_briefing.py --type weekly --save

# View briefings
ls AI_Employee_Vault/Briefings/
```

### Test Error Recovery

```bash
# Run Ralph Wiggum test
python ralph_wiggum_loop.py

# View recovery stats
cat AI_Employee_Vault/Logs/ralph_wiggum.log
```

## 🔒 Security

### Credential Management

- ✅ **OAuth2 Authentication**: No password storage for Gmail
- ✅ **Environment Variables**: All credentials in `.env` (gitignored)
- ✅ **DRY_RUN Mode**: Default enabled for safety
- ✅ **Approval Workflow**: Human-in-the-loop for sensitive actions
- ✅ **Comprehensive Logging**: Full audit trail
- ✅ **Scoped Permissions**: Minimal required permissions

### Security Best Practices

1. **Never commit `.env` file** - Already in `.gitignore`
2. **Use DRY_RUN for testing** - Enabled by default
3. **Review approval requests** - Check before approving
4. **Rotate credentials regularly** - Every 90 days recommended
5. **Monitor logs** - Check daily for suspicious activity

### Permission Boundaries

| Action Category | Auto-Approve Threshold | Always Require Approval |
|----------------|------------------------|-------------------------|
| Email replies | Known contacts | New contacts, bulk sends |
| Payments | < $50 recurring | All new payees, > $100 |
| Social media | Scheduled posts | Replies, DMs |
| File operations | Create, read | Delete, move outside vault |
| ERP actions | Read operations | Create, update, delete |

## 📚 Documentation

### Quick References

- **Quick Start**: `QUICKSTART.md` - 5-minute setup guide
- **Commands**: `COMMANDS.md` - Essential commands reference
- **Verification**: Run `python verify_system.py`

### Component Guides

- **Orchestrator**: `ORCHESTRATOR_README.md` - Master controller
- **Watchers**: `WATCHERS_README.md` - Input monitoring
- **Email MCP**: `.claude/mcp-servers/email-mcp/README.md`
- **Social MCP**: `.claude/mcp-servers/social-mcp/README.md`
- **ERP MCP**: `.claude/mcp-servers/erp-mcp/server.py`
- **Dashboard**: `ai-employee-dashboard/README.md`

### Setup Guides

- **Gmail**: `README_gmail_setup.md` - OAuth2 setup
- **WhatsApp**: `WHATSAPP_SETUP_GUIDE.md` - WhatsApp Web automation
- **Social Media**: `.claude/mcp-servers/social-mcp/README.md`
- **Odoo ERP**: `.claude/mcp-servers/erp-mcp/mcp.json`

## 🔍 Monitoring

### View Dashboard

```bash
# Start web dashboard
cd ai-employee-dashboard && npm run dev

# Visit http://localhost:3000
```

### View Logs

```bash
# Real-time orchestrator logs
tail -f AI_Employee_Vault/Logs/orchestrator.log

# Today's action log (JSON)
cat AI_Employee_Vault/Logs/$(date +%Y-%m-%d).json | jq

# Error recovery logs
tail -f AI_Employee_Vault/Logs/ralph_wiggum.log
```

### Check Status

```bash
# View markdown dashboard
cat AI_Employee_Vault/Dashboard.md

# Count pending tasks
ls AI_Employee_Vault/Needs_Action/*.md | wc -l

# Check running processes
ps aux | grep -E "orchestrator|watcher"
```

## 📊 System Metrics

### Current Performance

- **Total Actions Processed**: 14+
- **Automation Rate**: 50% (auto-processed)
- **Approval Rate**: 50% (human-reviewed)
- **Error Rate**: 0% (last 24 hours)
- **System Health**: HEALTHY
- **Disk Space**: 63.9% free (80.49 GB)
- **Uptime**: Continuous operation

### Weekly Activity (Feb 10-16, 2026)

- **Total Actions**: 4
- **By Type**: 100% Email
- **By Intent**: 50% Invoice Request, 50% Information
- **Daily Average**: 0.6 actions/day
- **Trend**: Stable

## 🛠️ Troubleshooting

### Common Issues

**No tasks being processed**
```bash
# Check if orchestrator is running
ps aux | grep orchestrator.py

# Check logs
tail AI_Employee_Vault/Logs/orchestrator.log

# Verify tasks exist
ls AI_Employee_Vault/Needs_Action/
```

**Tasks stuck in In_Progress**
```bash
# Move back to Needs_Action
mv AI_Employee_Vault/In_Progress/*.md AI_Employee_Vault/Needs_Action/
```

**Dashboard not loading**
```bash
# Check Node.js version
node --version  # Should be 24+

# Reinstall dependencies
cd ai-employee-dashboard
rm -rf node_modules package-lock.json
npm install
npm run dev
```

## 🗺️ Roadmap

### Completed (Gold Tier)
- ✅ Multi-channel input (Gmail, WhatsApp, Files)
- ✅ 5 MCP servers (Email, Social, Browser, Payment, ERP)
- ✅ Agent Skills architecture
- ✅ CEO Briefing automation
- ✅ Error recovery system
- ✅ Professional dashboard
- ✅ Comprehensive logging

### Future Enhancements (Platinum Tier)
- [ ] Cloud deployment (Oracle/AWS)
- [ ] Work-zone specialization (Cloud/Local)
- [ ] Vault sync via Git
- [ ] Always-on operation
- [ ] Health monitoring and alerts
- [ ] Mobile app notifications

## 🏆 Hackathon Submission

### Tier Achievement: Gold (100%)

**Bronze Tier** ✅
- Obsidian vault with Dashboard.md and Company_Handbook.md
- Working watcher scripts (3 total)
- Claude Code vault integration
- Folder structure (Needs_Action, In_Progress, Done)
- Agent Skills implementation

**Silver Tier** ✅
- Multiple watchers (Gmail + WhatsApp + File)
- LinkedIn auto-posting capability
- Claude reasoning with Plans
- Working MCP servers (5 total)
- Human-in-the-loop approval workflow
- Scheduling via orchestrator
- All functionality as Agent Skills

**Gold Tier** ✅
- Cross-domain integration (Personal + Business)
- Odoo ERP with JSON-RPC APIs
- Facebook integration (Graph API v18.0)
- Instagram integration (Graph API v18.0)
- Twitter/X integration (API v2)
- Multiple MCP servers (5 total)
- CEO Briefing with weekly audit
- Error recovery (Ralph Wiggum)
- Comprehensive audit logging
- Ralph Wiggum autonomous loop
- Complete documentation
- All functionality as Agent Skills

### Demo Video

[Link to demo video - To be added]

### Key Innovations

1. **Agent Skills Architecture** - Modular AI capabilities
2. **CEO Briefing Automation** - Proactive business intelligence
3. **Ralph Wiggum Error Recovery** - Autonomous error handling
4. **5 MCP Servers** - Comprehensive external integration
5. **Professional Dashboard** - Real-time monitoring

## 🤝 Contributing

Contributions welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

MIT License - See LICENSE file for details

## 🙏 Acknowledgments

- Built with Claude Code and the Model Context Protocol
- Uses Google Gmail API for email integration
- Powered by Anthropic's Claude AI
- Social media integration via Twitter, Facebook, Instagram APIs
- ERP integration via Odoo JSON-RPC API

---

## 🚀 Ready to Start?

```bash
# 1. Verify setup
python verify_system.py

# 2. Start orchestrator
python orchestrator.py

# 3. Start dashboard
cd ai-employee-dashboard && npm run dev

# 4. Visit http://localhost:3000
```

**Need help?** Check `QUICKSTART.md` for a 5-minute guide.

**Quick commands?** See `COMMANDS.md` for essential commands.

---

**Project Status**: Gold Tier Complete 🏆
**Last Updated**: 2026-02-16
**Version**: 1.0.0
**Hackathon**: Personal AI Employee Challenge
