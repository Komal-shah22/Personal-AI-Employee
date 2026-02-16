# Email Reply Skill

## Purpose
Analyze incoming emails and generate professional replies following company guidelines.

## Step-by-Step Instructions

### Step 1: Analyze Email Tone
Read the email and classify it as:
- **URGENT**: Contains words like "urgent", "asap", "immediately", "critical", deadline within 24 hours
- **COMPLAINT**: Contains negative sentiment, words like "disappointed", "frustrated", "issue", "problem"
- **NORMAL**: Standard business communication

### Step 2: Security Check
Before proceeding, verify:
- ❌ **STOP if unknown sender**: If sender is not in your contacts/previous emails, create approval request instead of reply
- ❌ **STOP if mentions money**: If email mentions amounts over PKR 10,000, flag for approval
- ✅ **Proceed**: If sender is known and no high-value amounts mentioned

### Step 3: Generate Reply

#### For URGENT emails:
- Acknowledge urgency in first line
- Provide immediate next steps or timeline
- Offer alternative contact method if needed

#### For COMPLAINT emails:
- Start with empathy and acknowledgment
- Take responsibility where appropriate
- Provide concrete solution or timeline
- Offer direct contact (phone/meeting)

#### For NORMAL emails:
- Professional but friendly tone
- Clear and concise response
- Answer all questions asked
- Provide next steps if applicable

### Step 4: Apply Template

```
[Greeting],

[Body - 2-4 paragraphs maximum]

[Closing line]

Best regards,
[Your Name]
[Your Title]
[Company Name]
[Contact Information]
```

### Step 5: Save Draft
Save to: `/AI_Employee_Vault/Needs_Action/REPLY_[YYYYMMDD]_[HHMMSS]_[Subject].md`

## Input Specification
- Email content (subject, sender, body)
- Sender history (known/unknown)
- Context from previous conversations if available

## Output Specification

```markdown
---
type: email_reply
original_subject: [subject]
sender: [email]
tone_detected: [URGENT/COMPLAINT/NORMAL]
requires_approval: [yes/no]
reason: [if approval required]
created: [timestamp]
---

# Email Reply Draft

## Original Email
[Quote relevant parts]

## Proposed Reply

[Full reply text with signature]

## Notes
- [Any special considerations]
- [Follow-up actions needed]
```

## Example Format

```markdown
---
type: email_reply
original_subject: Invoice Payment Delay
sender: client@example.com
tone_detected: COMPLAINT
requires_approval: no
created: 2026-02-16T10:30:00
---

# Email Reply Draft

## Original Email
> We haven't received the invoice yet and payment is due tomorrow.
> This is causing issues with our accounting department.

## Proposed Reply

Hi [Client Name],

I sincerely apologize for the delay in sending your invoice. I understand this is causing inconvenience for your accounting team.

I'm generating your invoice right now and will send it within the next hour. To help expedite your payment process, I'll also include our bank details for direct transfer.

If you need any adjustments or have questions about the invoice, please let me know immediately and I'll prioritize it.

Best regards,
[Your Name]
[Your Title]
[Company Name]
[Contact Information]

## Notes
- Generate invoice immediately after sending this reply
- Follow up in 2 hours to confirm receipt
```

## Error Handling Rules

### Unknown Sender
```markdown
---
type: approval_request
reason: unknown_sender
---

# Approval Required: Unknown Sender

**From**: [email]
**Subject**: [subject]
**Content**: [email body]

**Action**: Reply to this email?
**Risk Level**: Medium - Unknown sender

**Proposed Reply**: [draft]

**Approve?** [YES/NO]
```

### High-Value Amount Mentioned
```markdown
---
type: approval_request
reason: high_value_amount
amount_mentioned: PKR [amount]
---

# Approval Required: High-Value Discussion

**From**: [email]
**Subject**: [subject]
**Amount Mentioned**: PKR [amount]

**Proposed Reply**: [draft]

**Approve?** [YES/NO]
```

### Missing Information
If you cannot generate a proper reply due to missing information:
1. List what information is needed
2. Suggest where to find it
3. Create a task to gather the information
4. Do NOT send a vague or incomplete reply

## Quality Checklist
Before saving the draft, verify:
- [ ] All questions in original email are addressed
- [ ] Tone matches the situation (urgent/complaint/normal)
- [ ] No spelling or grammar errors
- [ ] Signature is complete
- [ ] No promises that can't be kept
- [ ] No sensitive information exposed
- [ ] Professional but human tone

---
*Last updated: 2026-02-16*
