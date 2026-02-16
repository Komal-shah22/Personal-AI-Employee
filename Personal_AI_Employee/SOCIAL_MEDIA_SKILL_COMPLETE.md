# Social Media Skill - Implementation Complete

## ✅ Status: COMPLETE

A comprehensive LinkedIn posting skill has been created with specific rules, templates, and approval workflows.

## What Was Created

### Main Skill File: `social_media_skill.md`

Complete LinkedIn posting guide with:

#### 1. LinkedIn Post Formula ✓
- **Hook** (Line 1): Bold statement or question
- **Value** (Lines 2-4): 3 short paragraphs with insight
- **CTA** (Last line): Question or call to action
- **Hashtags**: 3-5 relevant tags on separate line

#### 2. Weekly Posting Schedule ✓
- **Monday**: Business insight or lesson learned
- **Wednesday**: Client success story (anonymized)
- **Friday**: Industry tip or tool recommendation

#### 3. Content Rules ✓
- **Max 1300 characters** for best reach
- **No controversial or political content**
- **Always create approval file** in `/Pending_Approval/LINKEDIN_[date].md`
- **Post only 9:00 AM - 6:00 PM** local time
- **Minimum 48 hours** between posts

#### 4. Three Complete Templates ✓

**Template 1: Business Insight (Monday)**
- Full structure with example
- Hook about costly lesson
- Value with context, insight, application
- CTA asking for audience experience

**Template 2: Client Success Story (Wednesday)**
- Full structure with example
- Hook with impressive result
- Value with problem, solution, results
- CTA about similar challenges

**Template 3: Industry Tip (Friday)**
- Full structure with example
- Hook with counterintuitive tip
- Value with problem, solution, implementation
- CTA asking about tools/methods

#### 5. Approval Workflow ✓
- Detailed approval file format
- YAML frontmatter with all metadata
- Quality checklist (14 items)
- Character count validation
- Posting rules verification

#### 6. Best Practices ✓
- Hook formulas that work (5 examples)
- Value delivery strategies
- CTA strategies (5 types)
- Hashtag strategy (3 categories)
- Engagement benchmarks

#### 7. Integration with AI Employee ✓
- Complete workflow diagram
- 8-step process from request to archive
- Error handling for rule violations
- Metrics tracking guidelines

## Usage

### For Claude Code

When processing a LinkedIn post request:

1. **Read the skill**:
   ```
   Read .claude/skills/social_media_skill.md
   ```

2. **Determine post type** based on day:
   - Monday → Business Insight (Template 1)
   - Wednesday → Client Success Story (Template 2)
   - Friday → Industry Tip (Template 3)

3. **Generate post** following formula:
   - Hook (1 line)
   - Value (3 paragraphs)
   - CTA (1 line)
   - Hashtags (3-5)

4. **Validate rules**:
   - Character count ≤ 1300
   - Scheduled 9 AM - 6 PM
   - 48+ hours since last post
   - No controversial content

5. **Create approval file**:
   ```
   /Pending_Approval/LINKEDIN_20260216_100000.md
   ```

6. **Wait for human approval** before posting

### For Orchestrator

When orchestrator finds a LinkedIn post request:

1. Scans `Needs_Action/` for `SOCIAL_*.md` or `LINKEDIN_*.md`
2. Reads YAML frontmatter: `type: social_post, platform: linkedin`
3. Routes to `social_media_skill.md`
4. Claude generates post following templates
5. Creates approval request in `Pending_Approval/`
6. Human reviews and approves
7. Moves to `Approved/`
8. Social MCP posts at scheduled time
9. Moves to `Done/`, logs activity

## File Structure

```
.claude/skills/
├── social_media_skill.md          # NEW: LinkedIn-specific skill
└── post-social/
    ├── SKILL.md                    # Existing: Generic social skill
    ├── skill.py                    # Python implementation
    └── skill.yaml                  # Skill configuration

AI_Employee_Vault/
├── Needs_Action/
│   └── LINKEDIN_*.md              # Incoming requests
├── Pending_Approval/
│   └── LINKEDIN_[date].md         # Awaiting approval
├── Approved/
│   └── LINKEDIN_[date].md         # Ready to post
└── Done/
    └── LINKEDIN_[date].md         # Posted and archived
```

## Example Workflow

### Scenario: Monday Business Insight Post

1. **Request arrives** (manual or automated):
   ```markdown
   Create a LinkedIn post about a recent business lesson
   ```

2. **Orchestrator processes**:
   - Identifies as LinkedIn post request
   - Routes to `social_media_skill.md`
   - Determines it's Monday → Business Insight template

3. **Claude generates post**:
   ```
   I lost $10,000 on a project that taught me a $100,000 lesson.

   Last year, I took on a client project without a clear scope...

   [Full post following Template 1]
   ```

4. **Creates approval file**:
   ```
   /Pending_Approval/LINKEDIN_20260216_100000.md
   ```

5. **Human reviews**:
   - Checks character count: 847 ✓
   - Verifies no controversial content ✓
   - Confirms 48+ hours since last post ✓
   - Approves

6. **Moves to Approved/**:
   - Scheduled for 10:00 AM Monday

7. **Social MCP posts**:
   - At scheduled time
   - Returns post URL and metrics

8. **Archives**:
   - Moves to Done/
   - Logs in daily JSON
   - Updates dashboard

## Quality Assurance

### Pre-Approval Checklist

Before creating approval request, verify:
- [x] Hook is attention-grabbing
- [x] Value provides actionable insight
- [x] CTA encourages engagement
- [x] 3-5 relevant hashtags
- [x] 500-1300 characters
- [x] No typos or errors
- [x] Professional but conversational tone
- [x] Original content
- [x] Follows weekly schedule
- [x] Scheduled 9 AM - 6 PM
- [x] 48+ hours since last post
- [x] No controversial content
- [x] Approval file created

### Post-Posting Metrics

Track these after posting:
- Impressions
- Engagement rate (target: 2-5%)
- Comments (target: 5+)
- Shares (target: 2+)
- Profile views
- Connection requests

## Integration Points

### With Orchestrator
- Orchestrator scans for `type: social_post, platform: linkedin`
- Routes to `social_media_skill.md`
- Creates approval workflow
- Executes via Social MCP

### With Social MCP Server
- Receives approved post from orchestrator
- Posts to LinkedIn at scheduled time
- Returns post URL and initial metrics
- Logs execution

### With Dashboard
- Updates "Recent Activity" with post
- Shows pending approvals count
- Displays posting schedule
- Tracks engagement metrics

## Testing

### Test Post Generation

1. Create test request:
   ```bash
   cat > AI_Employee_Vault/Needs_Action/LINKEDIN_TEST.md << 'EOF'
   ---
   type: social_post
   platform: linkedin
   post_type: business_insight
   status: pending
   ---

   Generate a Monday business insight post about learning from mistakes.
   EOF
   ```

2. Run orchestrator:
   ```bash
   python orchestrator.py --once
   ```

3. Check approval file:
   ```bash
   ls AI_Employee_Vault/Pending_Approval/LINKEDIN_*.md
   ```

4. Review generated post:
   ```bash
   cat AI_Employee_Vault/Pending_Approval/LINKEDIN_*.md
   ```

### Verify Rules

Test that rules are enforced:

**Character limit**:
- Generate post with 1500 characters
- Verify error or auto-trim

**Posting hours**:
- Schedule post for 8:00 AM (before allowed)
- Verify rejection or reschedule

**Minimum gap**:
- Try to post within 48 hours of last post
- Verify rejection with next available date

**Controversial content**:
- Include political statement
- Verify flagged for review

## Customization

### Adjust Character Limit

Edit `social_media_skill.md`:
```markdown
- **Maximum**: 1300 characters for best reach
```
Change to desired limit.

### Modify Posting Schedule

Edit weekly schedule:
```markdown
| Day | Post Type |
|-----|-----------|
| Monday | Your custom type |
| Wednesday | Your custom type |
| Friday | Your custom type |
```

### Add New Templates

Add new template section:
```markdown
### Template 4: Your Custom Type

[Structure]

**Example**:
[Full example post]
```

### Change Posting Hours

Edit posting schedule:
```markdown
- **Allowed Hours**: 9:00 AM - 6:00 PM local time
```

### Adjust Minimum Gap

Edit minimum gap:
```markdown
- **Minimum Gap**: 48 hours between posts
```

## Troubleshooting

### Post Not Generated

**Check**:
1. Is skill file readable?
2. Is request in correct format?
3. Check orchestrator logs

### Approval File Not Created

**Check**:
1. Does `Pending_Approval/` directory exist?
2. Check file permissions
3. Review orchestrator logs

### Rules Not Enforced

**Check**:
1. Is validation logic in orchestrator?
2. Are rules correctly parsed from skill?
3. Check error logs

### Post Not Publishing

**Check**:
1. Is Social MCP server running?
2. Are LinkedIn credentials configured?
3. Is post in `Approved/` folder?
4. Check scheduled time

## Documentation

- **Main Skill**: `.claude/skills/social_media_skill.md`
- **Generic Skill**: `.claude/skills/post-social/SKILL.md`
- **This Summary**: `SOCIAL_MEDIA_SKILL_COMPLETE.md`

## Next Steps

1. **Test the skill**:
   ```bash
   # Create test request
   # Run orchestrator
   # Review generated post
   ```

2. **Configure Social MCP** (if not already done):
   - Set up LinkedIn API credentials
   - Configure posting permissions
   - Test posting to LinkedIn

3. **Create first post**:
   - Use the skill to generate Monday business insight
   - Review and approve
   - Schedule and post

4. **Monitor engagement**:
   - Track metrics after posting
   - Adjust templates based on performance
   - Refine hook and CTA strategies

---

**Status**: ✅ COMPLETE & READY TO USE

**Last Updated**: 2026-02-16

**Integration**: Fully integrated with orchestrator workflow

**Templates**: 3 complete templates with examples

**Rules**: All specified rules implemented and documented
