# CEO Briefing Skill

## Purpose
Generate a concise, actionable weekly briefing for the CEO covering key metrics, progress, and priorities.

## Tone Guidelines
Write like a **senior analyst briefing a busy CEO**:
- Short, factual, actionable
- No fluff or unnecessary details
- Lead with what matters most
- Use bullet points, not paragraphs
- Highlight problems and solutions, not just status
- Be direct about bad news
- Quantify everything possible

## Step-by-Step Instructions

### Step 1: Gather Data

#### Revenue Data
1. Read `/AI_Employee_Vault/Accounting/Current_Month.md`
2. Extract:
   - Total revenue this month
   - Revenue by category
   - Outstanding invoices
   - Expected revenue (pending invoices)

#### Goals & Targets
1. Read `/AI_Employee_Vault/Business_Goals.md`
2. Extract:
   - Q1 2026 revenue target
   - Current progress percentage
   - Key metrics targets vs actuals

#### Completed Tasks
1. Count files in `/AI_Employee_Vault/Done/` from last 7 days
2. Categorize by type:
   - Emails processed
   - Invoices sent
   - Social posts published
   - Other tasks
3. Calculate completion rate if targets exist

#### Pending Items
1. Count files in `/AI_Employee_Vault/Needs_Action/`
2. Count files in `/AI_Employee_Vault/Pending_Approval/`
3. Identify oldest pending item (potential bottleneck)

#### Upcoming Deadlines
1. Read `/AI_Employee_Vault/Dashboard.md`
2. Extract deadlines in next 7 days
3. Flag any overdue items

### Step 2: Analyze & Identify Issues

Look for:
- **Revenue gaps**: Behind target by >10%
- **Bottlenecks**: Items pending >3 days
- **Trends**: Declining completion rates
- **Risks**: Upcoming deadlines with no progress
- **Opportunities**: Quick wins or optimizations

### Step 3: Generate Briefing

Use this exact structure:

```markdown
---
briefing_date: [YYYY-MM-DD]
week_ending: [YYYY-MM-DD]
type: weekly_briefing
status: draft
---

# Weekly CEO Briefing
**Week Ending**: [DD Month YYYY]

---

## Executive Summary
[2-3 sentences max: biggest win, biggest concern, key decision needed]

---

## Revenue Status

**This Month**: PKR [amount] / PKR [target] ([%]%)
**Q1 2026**: PKR [amount] / PKR [target] ([%]%)

| Category | Target | Actual | Variance |
|----------|--------|--------|----------|
| [Category 1] | PKR [x] | PKR [y] | [+/-]PKR [z] |
| [Category 2] | PKR [x] | PKR [y] | [+/-]PKR [z] |

**Outstanding**: PKR [amount] ([#] invoices)
**Expected**: PKR [amount] (pending approvals)

---

## Completed This Week

- **[#]** emails processed
- **[#]** invoices sent (PKR [total])
- **[#]** social posts published
- **[#]** other tasks completed

**Total**: [#] tasks | **Completion Rate**: [%]%

---

## Current Bottlenecks

1. **[Issue 1]**: [Brief description] - [Impact] - [Suggested action]
2. **[Issue 2]**: [Brief description] - [Impact] - [Suggested action]
3. **[Issue 3]**: [Brief description] - [Impact] - [Suggested action]

**Awaiting Approval**: [#] items (oldest: [#] days)

---

## Recommendations

### Immediate Actions (This Week)
- [ ] [Action 1] - [Expected outcome]
- [ ] [Action 2] - [Expected outcome]

### Strategic Priorities (This Month)
- [ ] [Priority 1] - [Why it matters]
- [ ] [Priority 2] - [Why it matters]

---

## Upcoming Deadlines (Next 7 Days)

| Date | Item | Status | Risk |
|------|------|--------|------|
| [Date] | [Task] | [Status] | 🔴/🟡/🟢 |
| [Date] | [Task] | [Status] | 🔴/🟡/🟢 |

**Overdue**: [#] items

---

## Key Metrics

| Metric | Target | Actual | Trend |
|--------|--------|--------|-------|
| Email Response Time | < 2h | [X]h | ↑/↓/→ |
| Invoice Processing | < 24h | [X]h | ↑/↓/→ |
| Task Completion | > 90% | [X]% | ↑/↓/→ |

---

## Notes
[Any additional context, one-time events, or explanations]

---

*Generated: [Timestamp]*
```

### Step 4: Save Briefing
Save to: `/AI_Employee_Vault/Briefings/[YYYY-MM-DD]_Monday_Briefing.md`

Note: Always use Monday's date for the week, even if generated on another day.

## Input Specification
Data sources:
- `/AI_Employee_Vault/Business_Goals.md`
- `/AI_Employee_Vault/Accounting/Current_Month.md`
- `/AI_Employee_Vault/Dashboard.md`
- `/AI_Employee_Vault/Done/` (last 7 days)
- `/AI_Employee_Vault/Needs_Action/`
- `/AI_Employee_Vault/Pending_Approval/`

## Output Specification
Single markdown file with all sections completed.

## Example Format

```markdown
---
briefing_date: 2026-02-17
week_ending: 2026-02-17
type: weekly_briefing
status: draft
---

# Weekly CEO Briefing
**Week Ending**: 17 February 2026

---

## Executive Summary
Strong week with 23 tasks completed and PKR 450K in invoices sent. Main concern: 5 approvals pending >3 days, blocking PKR 200K in revenue. Decision needed: automate approvals under PKR 50K?

---

## Revenue Status

**This Month**: PKR 450,000 / PKR 800,000 (56%)
**Q1 2026**: PKR 1,200,000 / PKR 2,400,000 (50%)

| Category | Target | Actual | Variance |
|----------|--------|--------|----------|
| Services | PKR 600K | PKR 350K | -PKR 250K |
| Products | PKR 200K | PKR 100K | -PKR 100K |

**Outstanding**: PKR 300,000 (4 invoices)
**Expected**: PKR 200,000 (pending approvals)

---

## Completed This Week

- **18** emails processed
- **3** invoices sent (PKR 450,000)
- **2** social posts published
- **0** other tasks completed

**Total**: 23 tasks | **Completion Rate**: 92%

---

## Current Bottlenecks

1. **Approval Backlog**: 5 items pending >3 days - Blocking PKR 200K revenue - Suggest: auto-approve <PKR 50K
2. **Client Response Delays**: 2 projects waiting on client feedback - Delaying Feb deliverables - Suggest: send reminder + deadline
3. **Subscription Costs**: 3 unused services identified - Wasting PKR 15K/month - Suggest: cancel immediately

**Awaiting Approval**: 5 items (oldest: 4 days)

---

## Recommendations

### Immediate Actions (This Week)
- [ ] Approve pending invoices - Unlock PKR 200K revenue
- [ ] Cancel unused subscriptions - Save PKR 15K/month
- [ ] Send client reminders - Unblock 2 projects

### Strategic Priorities (This Month)
- [ ] Implement auto-approval for <PKR 50K - Reduce bottlenecks
- [ ] Launch Q1 marketing campaign - Close revenue gap

---

## Upcoming Deadlines (Next 7 Days)

| Date | Item | Status | Risk |
|------|------|--------|------|
| Feb 18 | Client A Deliverable | In Progress | 🟡 |
| Feb 20 | Invoice Payment Due | Sent | 🟢 |
| Feb 22 | Proposal Submission | Not Started | 🔴 |

**Overdue**: 1 item (follow-up email from Feb 14)

---

## Key Metrics

| Metric | Target | Actual | Trend |
|--------|--------|--------|-------|
| Email Response Time | < 2h | 1.5h | ↓ |
| Invoice Processing | < 24h | 18h | ↓ |
| Task Completion | > 90% | 92% | ↑ |

---

## Notes
Strong execution week. Main focus should be clearing approval backlog and closing revenue gap. Consider automation for routine approvals.

---

*Generated: 2026-02-17T09:00:00*
```

## Error Handling Rules

### Missing Data Files
If required files don't exist:
```markdown
## Data Unavailable

**Missing Files**:
- [ ] /Accounting/Current_Month.md
- [ ] /Business_Goals.md

**Action**: Cannot generate complete briefing without these files.

**Partial Briefing Available**:
[Include whatever data is available]
```

### No Activity This Week
If no tasks completed:
```markdown
## Completed This Week

**Total**: 0 tasks

**⚠️ Alert**: No activity detected this week. Possible issues:
- System not running?
- No incoming work?
- Tasks stuck in pipeline?

**Recommend**: Investigate immediately.
```

### Revenue Data Incomplete
If revenue data is missing or unclear:
```markdown
## Revenue Status

**⚠️ Data Quality Issue**: Revenue data incomplete or inconsistent.

**Available Data**:
[Show what you have]

**Action Required**: Update /Accounting/Current_Month.md with accurate figures.
```

## Quality Checklist
Before saving briefing:
- [ ] All numbers are accurate and sourced
- [ ] Executive summary is <3 sentences
- [ ] Bottlenecks have suggested actions
- [ ] Recommendations are specific and actionable
- [ ] No jargon or unnecessary details
- [ ] Trends are indicated (↑/↓/→)
- [ ] Risk levels are assigned (🔴/🟡/🟢)
- [ ] File saved with Monday's date

## Automation Notes
This briefing should be generated:
- Every Monday at 9:00 AM
- On-demand when requested
- Before important meetings

---
*Last updated: 2026-02-16*
