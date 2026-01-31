# Skill: complete-task

**Name**: complete-task

**Description**: Marks a task as completed and moves it to Done folder

**Version**: 1.0

**Parameters**: Takes task identifier as argument

**Trigger Phrases**:
- "complete task [name]"
- "mark [name] as done"
- "finish task [name]"
- "archive task [name]"

**Usage Examples**:
- User: "complete task invoice_reminder"
- User: "mark email_client_request as done"
- User: "finish urgent_payment"

## Purpose
This skill marks a task as completed by locating all related files, updating their metadata, creating a completion summary, and moving them to the Done folder.

## Behavior
1. Accept task identifier from user (filename without extension or task ID)
2. Locate all related files:
   - /Needs_Action/ACTION_[task-id].md
   - /Plans/PLAN_[task-id].md
   - Any other files matching task-id
3. For each file found:
   - Read current content
   - Update frontmatter:
     * status: completed
     * completed_at: [ISO timestamp]
     * completed_by: claude_skill
   - Add completion note at bottom
   - Move to /Done folder with same filename
4. Create completion summary:
   - Original task description
   - Time taken (if created timestamp available)
   - Steps completed
   - Final outcome
5. Update Dashboard.md:
   - Increment completed count
   - Add to "Recently Completed" section
   - Remove from pending lists
6. Log to /Logs/[today].txt:
   - Format: "[HH:MM:SS] COMPLETED: [task-id] - [brief description]"

## Completion Summary Format
```markdown
# ✅ Task Completion Summary

**Task:** [task name]
**Completed:** [ISO timestamp]
**Duration:** [time from creation to completion, if available]

## Original Objective
[Original task description]

## Steps Taken
- ✓ [Step 1 from plan]
- ✓ [Step 2 from plan]
- ✓ [Step 3 from plan]

## Outcome
[Brief description of result]

## Notes
[Any additional observations or learnings]

---
*Task archived by AI Employee on [date]*
```

## Error Handling
- If task not found:
  * Search in all folders (/Needs_Action, /Plans, /Pending_Approval)
  * Suggest similar task names if close match
  * Response: "Task '[name]' not found. Did you mean: [suggestions]?"

- If task already completed:
  * Check /Done folder
  * Response: "Task '[name]' was already completed on [date]"

- If required parameter missing:
  * Response: "Please specify which task to complete. Example: complete task invoice_reminder"

## Special Features
- Calculate time-to-completion statistics
- Detect if all steps in plan were actually done
- Flag tasks completed unusually fast (potential issues)
- Support partial matching (user types "invoice" finds "invoice_reminder")

## Rules
- NEVER delete original files, always move them
- Preserve all metadata and history
- Update timestamps in ISO 8601 format
- Create completion summary even for simple tasks
- Always log to activity log
- Update dashboard atomically (all or nothing)

## Confirmation Message
After completion, respond with:
✅ Task Completed: [task name]
📁 Files archived: [count]
⏱️  Duration: [time taken]
📊 Dashboard updated
📝 Logged to activity log
[Brief completion summary]

## Implementation Notes
The skill should use file system tools to locate, read, modify, and move files in the Obsidian vault structure. It should properly parse YAML frontmatter, calculate time differences, and generate well-formatted completion summaries.