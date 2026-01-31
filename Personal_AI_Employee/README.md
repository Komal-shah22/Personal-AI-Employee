# Personal AI Employee

An autonomous AI agent powered by Claude Code and Obsidian that proactively manages personal and business affairs 24/7.

## Overview

The Personal AI Employee is designed to act as a "Smart Consultant" or senior employee who figures out how to solve problems autonomously. It monitors various inputs (Gmail, file systems) and takes appropriate actions based on your Company Handbook and business rules. The system features a complete workflow from task detection to completion with human-in-the-loop approval for sensitive actions.

## Architecture

- **The Brain**: Claude Code acts as the reasoning engine with custom skills
- **The Memory/GUI**: Obsidian-style Markdown vault as the dashboard
- **The Senses (Watchers)**: Lightweight Python scripts monitoring inputs
- **The Hands (MCP)**: Model Context Protocol servers for external actions
- **The Vault**: Structured directory system for task management

## Directory Structure

```
├── AI_Employee_Vault/           # Main vault directory
│   ├── Inbox/                   # Incoming files and data
│   ├── Needs_Action/            # Items requiring processing
│   ├── Plans/                   # Generated action plans
│   ├── Done/                    # Completed items
│   ├── Pending_Approval/        # Actions requiring human approval
│   ├── Approved/                # Approved actions
│   ├── Rejected/                # Rejected actions
│   └── Logs/                    # System logs
├── .claude/skills/             # Claude Code custom skills
│   ├── process-tasks/          # Process pending tasks
│   ├── update-dashboard/       # Update dashboard statistics
│   ├── complete-task/          # Mark tasks as completed
│   ├── request-approval/       # Handle approval workflows
│   └── process-emails/         # Process incoming emails (NEW!)
├── watchers/                   # Watcher scripts
│   ├── gmail_watcher.py        # Gmail monitoring
│   └── filesystem_watcher.py   # File system monitoring
├── scripts/                    # Utility scripts
├── Dashboard.md               # Main dashboard
├── Company_Handbook.md        # Business rules and guidelines
├── Business_Goals.md          # Business objectives
├── orchestrator.py            # Main orchestrator
├── config.json                # Configuration
├── credentials.json           # API credentials (keep secure!)
├── requirements.txt           # Python dependencies
└── README.md                  # This file
```

## Setup

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Set up your Claude Code environment with appropriate permissions

3. Configure your Gmail API credentials:
   - Go to Google Cloud Console
   - Create a new project or select existing one
   - Enable the Gmail API
   - Create credentials (OAuth 2.0 client ID)
   - Download credentials.json and place in root directory

4. Update `Company_Handbook.md` with your specific rules

## Usage

1. Start the orchestrator:
   ```bash
   python orchestrator.py
   ```

2. Start the watchers:
   ```bash
   python watchers/gmail_watcher.py
   python filesystem_watcher.py
   ```

3. Place files in the `AI_Employee_Vault/Inbox/` directory or simulate incoming data

4. Monitor the `Dashboard.md` for system status

## Claude Skills

The system includes several Claude Code skills:

- **process-tasks**: Process pending tasks from Needs_Action folder
- **update-dashboard**: Refresh Dashboard with current stats
- **complete-task**: Mark tasks as complete and archive
- **request-approval**: Create approval requests for sensitive actions
- **process-emails**: Process incoming emails and create responses (NEW!)

Run skills with:
```bash
claude skill process-tasks
claude skill update-dashboard
claude skill complete-task
claude skill request-approval
claude skill process-emails
```

## Testing

Create test data with:
```bash
python test_data.py
```

This will create sample email and file drop items for the system to process.

## Security

- API credentials stored in `credentials.json` (excluded in .gitignore)
- Human-in-the-loop approval for sensitive actions
- Comprehensive audit logging in `AI_Employee_Vault/Logs/`
- Local-first architecture for privacy
- Approval workflow for email responses and sensitive actions

## Contributing

This project is part of a hackathon challenge to create autonomous AI employees. Contributions and improvements are welcome!

## Hackathon Progress

- ✅ **Bronze Tier**: Complete - Basic vault, watchers, and skills
- ✅ **Silver Tier**: Complete - Enhanced watchers, approval workflows, email processing
- 🔄 **Gold Tier**: In progress - Advanced integrations and automation
- 🚀 **Platinum Tier**: Planned - Cloud deployment and advanced features