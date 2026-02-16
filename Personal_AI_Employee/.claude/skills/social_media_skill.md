# Social Media Skill - LinkedIn Post Generation

## Purpose
Generate professional LinkedIn posts that follow best practices for engagement and reach. All posts require human approval before publishing.

## LinkedIn Post Formula

### Structure (4 Components)

1. **Hook (Line 1)**: Bold statement or question that grabs attention
   - Use strong verbs
   - Create curiosity or controversy (within professional bounds)
   - Make it personal or relatable

2. **Value (Lines 2-4)**: Key insight, tip, or story in 3 short paragraphs
   - Paragraph 1: Context or problem
   - Paragraph 2: Solution or insight
   - Paragraph 3: Result or lesson learned
   - Keep paragraphs 2-3 sentences each

3. **CTA (Last Line)**: Call to action
   - Ask a question to encourage comments
   - Direct to action (share, save, follow)
   - Make it conversational

4. **Hashtags**: 3-5 relevant hashtags on separate line
   - Mix popular and niche hashtags
   - Industry-specific tags
   - No more than 5 hashtags

## Weekly Posting Schedule

Follow this rotation for consistent, varied content:

| Day | Post Type | Focus |
|-----|-----------|-------|
| **Monday** | Business Insight or Lesson Learned | Share a recent learning, mistake, or business principle |
| **Wednesday** | Client Success Story (Anonymized) | Showcase results, transformations, or case studies |
| **Friday** | Industry Tip or Tool Recommendation | Practical advice, tools, or resources |

## Content Rules

### Character Limits
- **Maximum**: 1300 characters for best reach
- **Optimal**: 1000-1200 characters
- **Minimum**: 500 characters (too short = low engagement)

### Content Guidelines
- ✅ **DO**: Share personal experiences, lessons learned, practical tips
- ✅ **DO**: Use storytelling, be authentic, show vulnerability
- ✅ **DO**: Include data or specific examples when possible
- ❌ **DON'T**: Post controversial or political content
- ❌ **DON'T**: Use clickbait or misleading hooks
- ❌ **DON'T**: Over-promote products/services (80/20 rule: 80% value, 20% promotion)

### Approval Workflow
- **ALWAYS** create `/Pending_Approval/LINKEDIN_[date].md` before posting
- Include full post text, hashtags, and scheduled time
- Wait for human approval before publishing
- Never auto-post without approval

### Posting Schedule
- **Allowed Hours**: 9:00 AM - 6:00 PM local time
- **Optimal Times**:
  - Tuesday-Thursday: 10:00 AM - 12:00 PM
  - Tuesday-Thursday: 5:00 PM - 6:00 PM
- **Minimum Gap**: 48 hours between posts
- **Maximum Frequency**: 3 posts per week

## Post Templates

### Template 1: Business Insight (Monday)

```
[HOOK: Bold statement about business lesson]

[PARAGRAPH 1: Context - What situation led to this insight?]

[PARAGRAPH 2: The insight or lesson - What did you learn?]

[PARAGRAPH 3: Application - How can others apply this?]

[CTA: Question to audience about their experience]

#BusinessGrowth #Entrepreneurship #Leadership #BusinessTips #ProfessionalDevelopment
```

**Example**:
```
I lost $10,000 on a project that taught me a $100,000 lesson.

Last year, I took on a client project without a clear scope. No contract, no milestones, just a handshake and good intentions. Three months later, the project had ballooned to 3x the original estimate.

The lesson? Trust isn't a substitute for clarity. Now, every project starts with a detailed scope, clear deliverables, and signed agreement. It's not about trust—it's about setting everyone up for success.

Since implementing this, we've had zero scope creep issues and client satisfaction is at an all-time high.

What's a costly mistake that taught you an invaluable lesson?

#BusinessLessons #Entrepreneurship #ClientManagement #SmallBusiness #LessonsLearned
```

### Template 2: Client Success Story (Wednesday)

```
[HOOK: Impressive result or transformation]

[PARAGRAPH 1: Client's initial situation/problem]

[PARAGRAPH 2: What you did to help (process, not pitch)]

[PARAGRAPH 3: Results and impact]

[CTA: Question about similar challenges]

#ClientSuccess #CaseStudy #BusinessResults #[Industry] #[Service]
```

**Example**:
```
A client went from 50 to 500 qualified leads per month in 90 days.

They came to us frustrated. Their website was getting traffic, but visitors weren't converting. The bounce rate was 78%, and they were spending $5,000/month on ads with minimal ROI.

We rebuilt their landing page with a clear value proposition, simplified the form from 12 fields to 3, and added social proof above the fold. Then we A/B tested everything—headlines, CTAs, images.

Result: Conversion rate jumped from 2% to 12%. Same traffic, 10x more leads. They've since scaled their ad spend to $15,000/month because the ROI finally makes sense.

What's the biggest conversion challenge you're facing right now?

#ConversionOptimization #DigitalMarketing #LeadGeneration #MarketingStrategy #GrowthHacking
```

### Template 3: Industry Tip (Friday)

```
[HOOK: Counterintuitive tip or tool recommendation]

[PARAGRAPH 1: Common problem or inefficiency]

[PARAGRAPH 2: The solution/tool/tip]

[PARAGRAPH 3: How to implement or get started]

[CTA: Ask if they've tried it or want more tips]

#ProductivityTips #[Industry]Tools #WorkSmarter #BusinessTips #[Specific Tool/Method]
```

**Example**:
```
Stop using spreadsheets for project management. Here's what to use instead.

I see so many teams drowning in Excel files—version conflicts, lost updates, zero visibility into who's doing what. It works until it doesn't, and then it's chaos.

Switch to a proper project management tool. We use ClickUp (free tier is generous), but Asana, Monday, or Trello work great too. The key features: task assignments, due dates, progress tracking, and comments all in one place.

Start simple: Create one board, add your current projects as tasks, assign owners, set deadlines. Don't overcomplicate it. You can always add complexity later.

What project management tool has transformed your workflow?

#ProjectManagement #ProductivityTools #TeamCollaboration #WorkflowOptimization #ClickUp
```

## Approval File Format

When creating a LinkedIn post for approval, use this format:

**Filename**: `/Pending_Approval/LINKEDIN_[YYYYMMDD]_[HHMMSS].md`

**Content**:
```markdown
---
type: social_post
platform: linkedin
scheduled_date: 2026-02-16
scheduled_time: 10:00 AM
post_type: business_insight
character_count: 847
status: pending_approval
created: 2026-02-16T09:30:00
---

# LinkedIn Post for Approval

## Post Type
Business Insight (Monday)

## Scheduled Time
Monday, February 16, 2026 at 10:00 AM

## Post Content

[Full post text here, exactly as it will appear]

## Hashtags
#BusinessGrowth #Entrepreneurship #Leadership #BusinessTips #ProfessionalDevelopment

## Character Count
847 characters (within 1300 limit ✓)

## Posting Rules Checklist
- [x] Character count under 1300
- [x] Scheduled between 9 AM - 6 PM
- [x] 48+ hours since last post
- [x] No controversial content
- [x] Follows weekly schedule (Monday = Business Insight)
- [x] Includes CTA question
- [x] 3-5 hashtags included

## Approval
- [ ] Approve and schedule
- [ ] Request changes
- [ ] Reject

## Notes
[Any additional context or considerations]
```

## Quality Checklist

Before creating approval request, verify:

- [ ] Hook is attention-grabbing and relevant
- [ ] Value section provides actionable insight
- [ ] CTA encourages engagement (question or action)
- [ ] 3-5 relevant hashtags included
- [ ] Character count: 500-1300 characters
- [ ] No typos or grammatical errors
- [ ] Tone is professional but conversational
- [ ] Content is original (not copied)
- [ ] Follows weekly schedule (Monday/Wednesday/Friday)
- [ ] Scheduled between 9 AM - 6 PM
- [ ] At least 48 hours since last post
- [ ] No controversial or political content
- [ ] Approval file created in Pending_Approval/

## Engagement Best Practices

### Hook Formulas That Work
- "I [did something unexpected] and here's what happened..."
- "Most people think [common belief]. Here's why they're wrong..."
- "The [number] [thing] that [result]..."
- "[Surprising statistic or fact]"
- "Stop [common practice]. Do this instead..."

### Value Delivery
- Use specific numbers and data
- Tell stories with clear beginning, middle, end
- Show vulnerability (mistakes, failures, lessons)
- Provide actionable takeaways
- Use line breaks for readability

### CTA Strategies
- Ask for opinions: "What's your experience with...?"
- Request shares: "Know someone who needs to hear this?"
- Encourage saves: "Save this for later when..."
- Invite discussion: "Agree or disagree?"
- Ask for examples: "What's your go-to...?"

## Hashtag Strategy

### Categories to Mix

1. **Broad Industry** (100k+ followers)
   - #Entrepreneurship
   - #BusinessGrowth
   - #Leadership
   - #Marketing
   - #Sales

2. **Niche Specific** (10k-50k followers)
   - #SmallBusinessTips
   - #FreelanceLife
   - #StartupAdvice
   - #B2BMarketing
   - #SaaS

3. **Trending/Timely** (varies)
   - Check LinkedIn trending hashtags
   - Industry-specific events
   - Seasonal topics

### Hashtag Rules
- Use 3-5 hashtags (optimal for reach)
- Place on separate line at end
- Mix broad and niche
- Avoid banned or spammy hashtags
- Keep relevant to post content

## Error Handling

### If Post Violates Rules

**Character count over 1300**:
- Trim value section
- Shorten examples
- Remove redundant phrases
- Keep hook and CTA intact

**Scheduled outside posting hours**:
- Suggest next available slot (9 AM - 6 PM)
- Provide 3 alternative times
- Note optimal engagement times

**Less than 48 hours since last post**:
- Calculate next available date
- Suggest rescheduling
- Explain importance of spacing

**Controversial content detected**:
- Flag for human review
- Suggest alternative angle
- Explain potential risks

## Integration with AI Employee

### Workflow

1. **Content Request**: User or system triggers LinkedIn post creation
2. **Generate Post**: Use appropriate template based on day/type
3. **Create Approval**: Save to `/Pending_Approval/LINKEDIN_[date].md`
4. **Human Review**: User approves, requests changes, or rejects
5. **Schedule**: If approved, move to `/Approved/` with scheduled time
6. **Execute**: Social MCP server posts at scheduled time
7. **Archive**: Move to `/Done/` after posting
8. **Log**: Record in daily log with engagement metrics

### Example Flow

```
Monday 9:00 AM: System suggests business insight post
    ↓
Generate post using Template 1
    ↓
Create LINKEDIN_20260216_090000.md in Pending_Approval/
    ↓
User reviews and approves
    ↓
Move to Approved/ with scheduled time: 10:00 AM
    ↓
Social MCP posts at 10:00 AM
    ↓
Move to Done/, log activity
```

## Metrics to Track

After posting, track these metrics (manual or via API):

- **Impressions**: How many people saw the post
- **Engagement Rate**: (Likes + Comments + Shares) / Impressions
- **Comments**: Number and quality of comments
- **Shares**: How many times shared
- **Profile Views**: Increase after post
- **Connection Requests**: New connections from post

**Target Benchmarks**:
- Engagement Rate: 2-5% (good), 5%+ (excellent)
- Comments: 5+ per post
- Shares: 2+ per post

---

## Quick Reference

**Post Formula**: Hook → Value (3 paragraphs) → CTA → Hashtags

**Schedule**: Monday (Insight), Wednesday (Success), Friday (Tip)

**Rules**: Max 1300 chars, 9 AM - 6 PM, 48hr gap, approval required

**Hashtags**: 3-5 relevant, mix broad + niche

**Approval**: Always create Pending_Approval/LINKEDIN_[date].md first

---

*Last Updated: 2026-02-16*
