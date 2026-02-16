"""
CEO Briefing Automation
Gold Tier Feature

Generates daily/weekly executive summaries with key metrics,
action items, and system health status.
"""

import os
import json
from pathlib import Path
from datetime import datetime, timedelta
from typing import Dict, List
import logging

class CEOBriefingGenerator:
    """Generate executive briefings with key metrics and insights"""

    def __init__(self, config_path="config.json"):
        self.config = self.load_config(config_path)
        self.setup_logging()
        self.briefings_dir = Path('AI_Employee_Vault/Briefings')
        self.briefings_dir.mkdir(parents=True, exist_ok=True)

    def load_config(self, config_path):
        """Load configuration"""
        with open(config_path, 'r') as f:
            return json.load(f)

    def setup_logging(self):
        """Setup logging"""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        self.logger = logging.getLogger(__name__)

    def get_daily_metrics(self, date: datetime = None) -> Dict:
        """Get metrics for a specific day"""
        if date is None:
            date = datetime.now()

        date_str = date.strftime('%Y-%m-%d')
        log_file = Path(f'AI_Employee_Vault/Logs/{date_str}.json')

        metrics = {
            'date': date_str,
            'total_actions': 0,
            'by_type': {},
            'by_intent': {},
            'by_priority': {},
            'requires_approval': 0,
            'auto_processed': 0
        }

        if not log_file.exists():
            return metrics

        try:
            with open(log_file, 'r') as f:
                log_data = json.load(f)

            actions = log_data.get('actions', [])
            metrics['total_actions'] = len(actions)

            for action in actions:
                # Count by type
                action_type = action.get('type', 'unknown')
                metrics['by_type'][action_type] = metrics['by_type'].get(action_type, 0) + 1

                # Count by intent
                intent = action.get('intent', 'unknown')
                metrics['by_intent'][intent] = metrics['by_intent'].get(intent, 0) + 1

                # Count by priority
                priority = action.get('priority', 'medium')
                metrics['by_priority'][priority] = metrics['by_priority'].get(priority, 0) + 1

                # Count approval requirements
                if action.get('requires_approval', False):
                    metrics['requires_approval'] += 1
                else:
                    metrics['auto_processed'] += 1

        except Exception as e:
            self.logger.error(f"Error reading log file: {e}")

        return metrics

    def get_weekly_metrics(self, end_date: datetime = None) -> Dict:
        """Get aggregated metrics for the past week"""
        if end_date is None:
            end_date = datetime.now()

        weekly_metrics = {
            'period': f"{(end_date - timedelta(days=6)).strftime('%Y-%m-%d')} to {end_date.strftime('%Y-%m-%d')}",
            'total_actions': 0,
            'by_type': {},
            'by_intent': {},
            'by_priority': {},
            'requires_approval': 0,
            'auto_processed': 0,
            'daily_breakdown': []
        }

        for i in range(7):
            date = end_date - timedelta(days=i)
            daily = self.get_daily_metrics(date)
            weekly_metrics['daily_breakdown'].append(daily)

            # Aggregate
            weekly_metrics['total_actions'] += daily['total_actions']
            weekly_metrics['requires_approval'] += daily['requires_approval']
            weekly_metrics['auto_processed'] += daily['auto_processed']

            for type_name, count in daily['by_type'].items():
                weekly_metrics['by_type'][type_name] = weekly_metrics['by_type'].get(type_name, 0) + count

            for intent, count in daily['by_intent'].items():
                weekly_metrics['by_intent'][intent] = weekly_metrics['by_intent'].get(intent, 0) + count

            for priority, count in daily['by_priority'].items():
                weekly_metrics['by_priority'][priority] = weekly_metrics['by_priority'].get(priority, 0) + count

        return weekly_metrics

    def get_pending_approvals(self) -> List[Dict]:
        """Get list of pending approval requests"""
        pending_dir = Path(self.config['directories']['pending_approval'])
        pending_files = list(pending_dir.glob('*.md'))

        approvals = []
        for file in pending_files:
            try:
                with open(file, 'r', encoding='utf-8') as f:
                    content = f.read()

                # Parse frontmatter
                if content.startswith('---'):
                    parts = content.split('---', 2)
                    if len(parts) >= 3:
                        frontmatter_text = parts[1].strip()
                        frontmatter = {}
                        for line in frontmatter_text.split('\n'):
                            if ':' in line:
                                key, value = line.split(':', 1)
                                frontmatter[key.strip()] = value.strip()

                        approvals.append({
                            'file': file.name,
                            'action_type': frontmatter.get('action_type', 'unknown'),
                            'priority': frontmatter.get('priority', 'medium'),
                            'created': frontmatter.get('created', 'unknown')
                        })
            except Exception as e:
                self.logger.error(f"Error reading approval file {file}: {e}")

        return approvals

    def get_error_stats(self) -> Dict:
        """Get error recovery statistics"""
        error_log = Path('AI_Employee_Vault/Logs/errors.json')

        stats = {
            'total_errors': 0,
            'last_24h': 0,
            'by_category': {}
        }

        if not error_log.exists():
            return stats

        try:
            with open(error_log, 'r') as f:
                error_data = json.load(f)

            errors = error_data.get('errors', [])
            stats['total_errors'] = len(errors)

            # Count errors in last 24 hours
            cutoff = datetime.now() - timedelta(hours=24)
            for error in errors:
                try:
                    error_time = datetime.fromisoformat(error['timestamp'])
                    if error_time > cutoff:
                        stats['last_24h'] += 1

                    category = error.get('category', 'unknown')
                    stats['by_category'][category] = stats['by_category'].get(category, 0) + 1
                except Exception:
                    pass

        except Exception as e:
            self.logger.error(f"Error reading error log: {e}")

        return stats

    def get_system_health(self) -> Dict:
        """Get current system health status"""
        health = {
            'status': 'healthy',
            'checks': {}
        }

        # Check disk space
        try:
            import shutil
            total, used, free = shutil.disk_usage('.')
            free_percent = (free / total) * 100
            health['checks']['disk_space'] = {
                'status': 'ok' if free_percent > 10 else 'warning',
                'free_percent': round(free_percent, 1),
                'free_gb': round(free / (1024**3), 2)
            }
        except Exception as e:
            health['checks']['disk_space'] = {'status': 'error', 'message': str(e)}

        # Check pending items
        try:
            needs_action_dir = Path(self.config['directories']['needs_action'])
            pending_count = len(list(needs_action_dir.glob('*.md')))
            health['checks']['pending_items'] = {
                'status': 'ok' if pending_count < 50 else 'warning',
                'count': pending_count
            }
        except Exception as e:
            health['checks']['pending_items'] = {'status': 'error', 'message': str(e)}

        # Check error rate
        error_stats = self.get_error_stats()
        health['checks']['error_rate'] = {
            'status': 'ok' if error_stats['last_24h'] < 10 else 'warning',
            'errors_24h': error_stats['last_24h']
        }

        # Overall status
        if any(check['status'] == 'warning' for check in health['checks'].values()):
            health['status'] = 'warning'
        if any(check['status'] == 'error' for check in health['checks'].values()):
            health['status'] = 'error'

        return health

    def generate_daily_briefing(self, date: datetime = None) -> str:
        """Generate daily briefing"""
        if date is None:
            date = datetime.now()

        self.logger.info(f"Generating daily briefing for {date.strftime('%Y-%m-%d')}")

        metrics = self.get_daily_metrics(date)
        pending = self.get_pending_approvals()
        errors = self.get_error_stats()
        health = self.get_system_health()

        # Generate briefing content
        briefing = f"""# CEO Daily Briefing
**Date:** {date.strftime('%A, %B %d, %Y')}
**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

---

## Executive Summary

The AI Employee processed **{metrics['total_actions']} actions** today.

- **Auto-processed:** {metrics['auto_processed']} actions
- **Awaiting approval:** {metrics['requires_approval']} actions
- **System health:** {health['status'].upper()}

---

## Activity Breakdown

### By Type
"""

        for action_type, count in sorted(metrics['by_type'].items(), key=lambda x: x[1], reverse=True):
            briefing += f"- **{action_type.title()}:** {count}\n"

        briefing += "\n### By Intent\n"
        for intent, count in sorted(metrics['by_intent'].items(), key=lambda x: x[1], reverse=True):
            briefing += f"- **{intent.replace('_', ' ').title()}:** {count}\n"

        briefing += "\n### By Priority\n"
        for priority, count in sorted(metrics['by_priority'].items(), key=lambda x: x[1], reverse=True):
            briefing += f"- **{priority.title()}:** {count}\n"

        briefing += f"\n---\n\n## Pending Approvals ({len(pending)})\n\n"

        if pending:
            for approval in pending[:10]:  # Show top 10
                briefing += f"- **{approval['action_type'].replace('_', ' ').title()}** (Priority: {approval['priority']})\n"
            if len(pending) > 10:
                briefing += f"\n*...and {len(pending) - 10} more*\n"
        else:
            briefing += "*No pending approvals*\n"

        briefing += f"\n---\n\n## System Health\n\n**Status:** {health['status'].upper()}\n\n"

        for check_name, check_data in health['checks'].items():
            status_icon = {'ok': '[OK]', 'warning': '[WARN]', 'error': '[ERROR]'}.get(check_data['status'], '[?]')
            briefing += f"- {status_icon} **{check_name.replace('_', ' ').title()}**"

            if 'free_percent' in check_data:
                briefing += f": {check_data['free_percent']}% free ({check_data['free_gb']} GB)\n"
            elif 'count' in check_data:
                briefing += f": {check_data['count']} items\n"
            elif 'errors_24h' in check_data:
                briefing += f": {check_data['errors_24h']} errors in last 24h\n"
            elif 'message' in check_data:
                briefing += f": {check_data['message']}\n"
            else:
                briefing += "\n"

        briefing += f"\n---\n\n## Error Recovery\n\n"
        briefing += f"- **Total errors (all time):** {errors['total_errors']}\n"
        briefing += f"- **Errors (last 24h):** {errors['last_24h']}\n"

        if errors['by_category']:
            briefing += "\n**By Category:**\n"
            for category, count in sorted(errors['by_category'].items(), key=lambda x: x[1], reverse=True):
                briefing += f"- {category.title()}: {count}\n"

        briefing += "\n---\n\n## Next Steps\n\n"

        if len(pending) > 0:
            briefing += f"1. Review and approve {len(pending)} pending action(s)\n"

        if health['status'] != 'healthy':
            briefing += "2. Address system health warnings\n"

        if errors['last_24h'] > 5:
            briefing += "3. Investigate recent error spike\n"

        if len(pending) == 0 and health['status'] == 'healthy' and errors['last_24h'] < 5:
            briefing += "*No immediate action required - system operating normally*\n"

        briefing += "\n---\n\n*Generated by Personal AI Employee - CEO Briefing Automation*\n"

        return briefing

    def generate_weekly_briefing(self, end_date: datetime = None) -> str:
        """Generate weekly briefing"""
        if end_date is None:
            end_date = datetime.now()

        self.logger.info(f"Generating weekly briefing ending {end_date.strftime('%Y-%m-%d')}")

        metrics = self.get_weekly_metrics(end_date)
        pending = self.get_pending_approvals()
        errors = self.get_error_stats()
        health = self.get_system_health()

        start_date = end_date - timedelta(days=6)

        briefing = f"""# CEO Weekly Briefing
**Period:** {start_date.strftime('%B %d')} - {end_date.strftime('%B %d, %Y')}
**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

---

## Executive Summary

The AI Employee processed **{metrics['total_actions']} actions** this week.

- **Auto-processed:** {metrics['auto_processed']} actions ({round(metrics['auto_processed']/max(metrics['total_actions'],1)*100, 1)}%)
- **Required approval:** {metrics['requires_approval']} actions ({round(metrics['requires_approval']/max(metrics['total_actions'],1)*100, 1)}%)
- **Daily average:** {round(metrics['total_actions']/7, 1)} actions/day

---

## Weekly Activity

### By Type
"""

        for action_type, count in sorted(metrics['by_type'].items(), key=lambda x: x[1], reverse=True):
            percent = round(count/max(metrics['total_actions'],1)*100, 1)
            briefing += f"- **{action_type.title()}:** {count} ({percent}%)\n"

        briefing += "\n### By Intent\n"
        for intent, count in sorted(metrics['by_intent'].items(), key=lambda x: x[1], reverse=True):
            percent = round(count/max(metrics['total_actions'],1)*100, 1)
            briefing += f"- **{intent.replace('_', ' ').title()}:** {count} ({percent}%)\n"

        briefing += "\n### Daily Breakdown\n\n"
        for daily in reversed(metrics['daily_breakdown']):
            briefing += f"- **{daily['date']}:** {daily['total_actions']} actions\n"

        briefing += f"\n---\n\n## Current Status\n\n"
        briefing += f"- **Pending approvals:** {len(pending)}\n"
        briefing += f"- **System health:** {health['status'].upper()}\n"
        briefing += f"- **Errors (last 24h):** {errors['last_24h']}\n"

        briefing += "\n---\n\n## Insights & Trends\n\n"

        # Calculate trends
        if len(metrics['daily_breakdown']) >= 2:
            recent_avg = sum(d['total_actions'] for d in metrics['daily_breakdown'][:3]) / 3
            older_avg = sum(d['total_actions'] for d in metrics['daily_breakdown'][3:]) / 4

            if recent_avg > older_avg * 1.2:
                briefing += "- Activity trending UP (20%+ increase in recent days)\n"
            elif recent_avg < older_avg * 0.8:
                briefing += "- Activity trending DOWN (20%+ decrease in recent days)\n"
            else:
                briefing += "- Activity levels STABLE\n"

        # Approval rate
        if metrics['total_actions'] > 0:
            approval_rate = (metrics['requires_approval'] / metrics['total_actions']) * 100
            if approval_rate > 50:
                briefing += f"- High approval rate ({round(approval_rate, 1)}%) - consider automation opportunities\n"
            else:
                briefing += f"- Good automation rate ({round(100-approval_rate, 1)}% auto-processed)\n"

        briefing += "\n---\n\n*Generated by Personal AI Employee - CEO Briefing Automation*\n"

        return briefing

    def save_briefing(self, content: str, briefing_type: str = 'daily') -> Path:
        """Save briefing to file"""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"CEO_BRIEFING_{briefing_type.upper()}_{timestamp}.md"
        filepath = self.briefings_dir / filename

        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)

        self.logger.info(f"Briefing saved: {filepath}")
        return filepath


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description='CEO Briefing Generator')
    parser.add_argument('--type', choices=['daily', 'weekly'], default='daily', help='Briefing type')
    parser.add_argument('--save', action='store_true', help='Save briefing to file')
    args = parser.parse_args()

    generator = CEOBriefingGenerator()

    if args.type == 'daily':
        briefing = generator.generate_daily_briefing()
    else:
        briefing = generator.generate_weekly_briefing()

    print(briefing)

    if args.save:
        filepath = generator.save_briefing(briefing, args.type)
        print(f"\nBriefing saved to: {filepath}")
