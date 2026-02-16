# Generate Reports Skill

The `generate-reports` skill generates comprehensive business intelligence reports and CEO briefings from your Personal AI Employee vault data.

## Overview

This skill analyzes your AI employee's activities and generates professional reports including daily summaries, weekly CEO briefings, monthly metrics, revenue analysis, and task performance metrics.

## Capabilities

- **Daily Summaries**: Executive overview of daily activities
- **Weekly CEO Briefings**: Comprehensive weekly analysis
- **Monthly Metrics**: Performance and efficiency tracking
- **Revenue Analysis**: Financial impact estimation
- **Task Performance**: Efficiency and throughput metrics
- **Automated Scheduling**: Regular report generation
- **Dashboard Integration**: Automatic statistics updates

## Usage

### Basic Usage
```bash
claude skill generate-reports
```

### With Parameters
```bash
claude skill generate-reports --report_type weekly --include_revenue true
```

## Input Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `report_type` | string | No | Type of report (daily, weekly, monthly, all) |
| `period` | string | No | Time period for analysis |
| `include_revenue` | boolean | No | Include revenue analysis (default: true) |
| `include_performance` | boolean | No | Include task performance (default: true) |

## Generated Reports

The skill creates these report types in the `Reports` folder:

### Daily Summary
- Daily activity overview
- Task completion counts
- Recent activity log

### Weekly CEO Briefing
- Executive summary
- Revenue tracking
- Bottleneck identification
- Proactive suggestions

### Monthly Metrics
- Performance indicators
- Trend analysis
- Efficiency metrics

### Revenue Analysis
- Revenue breakdown by category
- Task categorization
- Growth opportunities

### Task Performance
- Completion statistics
- Performance by category
- Efficiency insights

## Integration

- **Automatic**: Runs weekly on Mondays at 7 AM
- **Daily**: Runs at 8 AM for daily summaries
- **Trigger**: Processes REPORT_*.md files in Needs_Action
- **Dashboard**: Updates statistics after generation
- **Vault**: Saves reports to Reports folder

## Security

- Read-only access to vault data
- No external data transmission
- Local report generation
- Secure file handling

## Best Practices

- Review reports regularly for insights
- Use CEO briefings for strategic planning
- Monitor performance metrics for optimization
- Schedule regular review cycles
- Adjust parameters based on needs

## Troubleshooting

- If reports aren't generating, check vault folder structure
- Verify that the Reports folder has write permissions
- Check logs in the Logs folder for errors
- Ensure vault contains sufficient data for analysis

## Dependencies

- Built-in Python libraries only
- Access to vault directories
- Dashboard update permissions