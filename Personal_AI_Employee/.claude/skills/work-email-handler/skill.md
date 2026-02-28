# Work Email Handler Skill

## Purpose
This skill specializes in detecting, processing, and responding to work/employment-related emails with an approval workflow for job opportunities. It automatically identifies job-related communications and creates appropriate responses for user approval.

## Functionality

### 1. Work Email Detection
- Monitors incoming emails in the `AI_Employee_Vault/Needs_Action` folder
- Scans for keywords related to job opportunities, employment, contracts, and work inquiries
- Identifies job-specific details like company name, position, salary, and requirements

### 2. Job Detail Extraction
The skill extracts key information from job-related emails:
- Company name
- Job title/position
- Salary range
- Location
- Application deadline
- Requirements

### 3. Response Generation
- Creates professional responses for work opportunities
- Follows standard business communication format
- Tailors response based on extracted job details

### 4. Approval Workflow
- Creates approval requests for all work-related email responses
- Stores approval requests in `AI_Employee_Vault/Pending_Approval`
- Requires human approval before sending any job-related responses

## Input Specification
- Email files in `AI_Employee_Vault/Needs_Action/EMAIL_*.md` format
- Must contain YAML frontmatter with email metadata
- Supports common email fields: subject, from, body, etc.

## Output Specification
- Approval requests in `AI_Employee_Vault/Pending_Approval/APPROVAL_work_email_*.md`
- Updates to the main dashboard with work email statistics
- Activity logs in `AI_Employee_Vault/Logs`

## Work Keywords Detected
- job, work, employment, opportunity
- hire, contract, freelance, position
- role, application, candidate, recruit
- hiring, vacancy, opening, interview
- company, project, engagement
- consultant, contractor, offer
- Specific company names like "linden"

## Security & Approval Requirements
- All work-related responses require approval
- No automated responses to job opportunities
- Maintains professional standards for job correspondence

## Dashboard Integration
- Updates work opportunity email statistics
- Tracks processed job-related communications
- Shows important job details in dashboard summary

## Example Use Case
When an email arrives about a "Software Engineer position at Linden Corp", this skill will:
1. Detect it as work-related
2. Extract job details (position, company, etc.)
3. Generate a professional response
4. Create an approval request for user review
5. Update dashboard with job opportunity information

---
*Last updated: 2026-02-24*