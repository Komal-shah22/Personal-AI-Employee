# Skill: process-tasks

**Name**: process-tasks

**Description**: Processes pending tasks from Needs_Action folder and creates execution plans

**Version**: 1.0

**Trigger Phrases**:
- "process my tasks"
- "process pending actions"
- "check needs action"
- "process inbox items"

## Purpose
This skill processes pending tasks from the /Needs_Action folder by reading the Company_Handbook.md for rules, analyzing each task file, creating detailed execution plans, and updating the dashboard and logs.

## Behavior
1. Reads the Company_Handbook.md file first to understand processing rules
2. Scans the /Needs_Action folder for all .md files
3. For each file:
   - Parses the frontmatter to get priority, type, and metadata
   - Analyzes the content to understand what needs to be done
   - Creates a detailed plan with 3-5 actionable steps
   - Saves the plan in /Plans/PLAN_[original-filename].md
4. Updates the Dashboard.md file with:
   - Total pending tasks count
   - List of high-priority items
   - Activity log entry
   - Updated timestamp
5. Logs the activity in /Logs/[today's-date].txt

## Plan File Format
```markdown
---
task_id: [original filename without extension]
source_file: [path to original file]
created: [ISO 8601 timestamp]
priority: [high/medium/low from source]
status: planned
---

# Task: [Descriptive task name]

## Objective
[Clear 1-2 sentence description of what needs to be accomplished]

## Analysis
[Brief analysis of the task based on content]

## Action Steps
- [ ] Step 1: [Specific, actionable step]
- [ ] Step 2: [Specific, actionable step]
- [ ] Step 3: [Specific, actionable step]
- [ ] Step 4: [If needed]
- [ ] Step 5: [If needed]

## Success Criteria
[How to know this task is complete]

## Notes
[Any additional context or considerations]
```

## Error Handling
- If /Needs_Action is empty, respond with "No pending tasks found"
- If Company_Handbook.md is missing, create a basic one with default rules
- If a file is corrupted, skip it and log the error
- Always update Dashboard even if there are errors

## Constraints
- Never delete original files from Needs_Action
- Always respect priority levels from Company_Handbook.md
- Use clear, actionable language in steps
- Include timestamps in ISO 8601 format
- Keep plans concise (under 200 lines)

## Implementation Notes
The skill should use file system tools to read, write, and manipulate files in the Obsidian vault structure. It should properly parse YAML frontmatter from markdown files and generate well-formatted plan files with proper metadata.