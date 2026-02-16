# Invoice Generation Skill

## Purpose
Generate professional invoices for clients based on rates and work completed.

## Step-by-Step Instructions

### Step 1: Read Client Rates
1. Open `/AI_Employee_Vault/Accounting/Rates.md`
2. Find the client's current rate
3. Verify rate is still valid (check effective date)
4. If rate not found, STOP and request rate information

### Step 2: Calculate Amount
1. Determine billing period (monthly/project/hourly)
2. Calculate total amount based on:
   - Monthly retainer: Use fixed rate
   - Hourly: Hours worked × hourly rate
   - Project: Agreed project fee
3. Add any additional charges (if applicable)
4. Calculate subtotal
5. Apply tax if required (check Company_Handbook.md for tax rules)
6. Calculate total

### Step 3: Generate Invoice Number
Format: `INV-[YYYY]-[MM]-[###]`
- YYYY: Current year
- MM: Current month
- ###: Sequential number (check last invoice in /Invoices/)

Example: `INV-2026-02-001`

### Step 4: Create Invoice Document

Use this exact format:

```markdown
---
invoice_number: INV-[YYYY]-[MM]-[###]
client_name: [Client Name]
client_email: [Email]
issue_date: [YYYY-MM-DD]
due_date: [YYYY-MM-DD] (30 days from issue)
amount: PKR [total]
status: draft
---

# INVOICE

**Invoice Number**: INV-[YYYY]-[MM]-[###]
**Date**: [DD Month YYYY]
**Due Date**: [DD Month YYYY]

---

## Bill To
**[Client Name]**
[Client Company]
[Client Address]
[Client Email]

## Bill From
**[Your Name]**
[Your Company]
[Your Address]
[Your Email]
[Your Phone]

---

## Invoice Details

| Description | Quantity | Rate | Amount |
|-------------|----------|------|--------|
| [Service Description] | [qty] | PKR [rate] | PKR [amount] |
| [Additional Item] | [qty] | PKR [rate] | PKR [amount] |

**Subtotal**: PKR [subtotal]
**Tax ([%])**: PKR [tax]
**Total**: PKR [total]

---

## Payment Details

**Bank Name**: [Your Bank]
**Account Title**: [Account Name]
**Account Number**: [Account Number]
**IBAN**: [IBAN if applicable]

**Payment Methods Accepted**:
- Bank Transfer
- [Other methods]

---

## Terms & Conditions

- Payment is due within 30 days of invoice date
- Late payments may incur [X]% monthly interest
- Please include invoice number in payment reference

---

## Notes
[Any additional notes or thank you message]

---

*Thank you for your business!*
```

### Step 5: Create Approval Request
**CRITICAL**: NEVER send invoice without approval

Create approval file: `/AI_Employee_Vault/Pending_Approval/APPROVAL_invoice_[YYYYMMDD]_[HHMMSS]_[ClientName].md`

```markdown
---
type: approval_request
action: send_invoice
client: [Client Name]
amount: PKR [total]
invoice_number: INV-[YYYY]-[MM]-[###]
created: [timestamp]
priority: normal
---

# Invoice Approval Required

## Client Information
- **Name**: [Client Name]
- **Email**: [Client Email]
- **Last Invoice**: [Date of last invoice]

## Invoice Details
- **Invoice Number**: INV-[YYYY]-[MM]-[###]
- **Amount**: PKR [total]
- **Period**: [Billing period]
- **Due Date**: [Date]

## Line Items
| Description | Amount |
|-------------|--------|
| [Item 1] | PKR [amount] |
| [Item 2] | PKR [amount] |
| **Total** | **PKR [total]** |

## Invoice Preview
[Link to invoice file in /Invoices/]

## Action Required
- [ ] Review invoice details
- [ ] Verify amount is correct
- [ ] Approve to send to client

**Approve?** [YES/NO]

## Notes
[Any special considerations]
```

### Step 6: Save Invoice
Save to: `/AI_Employee_Vault/Invoices/[YYYY-MM]_[ClientName]_INV-[###].md`

## Input Specification
Required inputs:
- Client name
- Billing period or project description
- Hours worked (if hourly) OR fixed amount
- Any additional charges
- Client email address

## Output Specification
Two files created:
1. Invoice document in `/Invoices/`
2. Approval request in `/Pending_Approval/`

## Example Format

### Example Invoice
```markdown
---
invoice_number: INV-2026-02-001
client_name: Acme Corporation
client_email: billing@acme.com
issue_date: 2026-02-16
due_date: 2026-03-18
amount: PKR 150000
status: draft
---

# INVOICE

**Invoice Number**: INV-2026-02-001
**Date**: 16 February 2026
**Due Date**: 18 March 2026

---

## Bill To
**Acme Corporation**
123 Business Street
Karachi, Pakistan
billing@acme.com

## Bill From
**[Your Name]**
[Your Company]
[Your Address]
[Your Email]
[Your Phone]

---

## Invoice Details

| Description | Quantity | Rate | Amount |
|-------------|----------|------|--------|
| Monthly Retainer - February 2026 | 1 | PKR 150,000 | PKR 150,000 |

**Subtotal**: PKR 150,000
**Tax (0%)**: PKR 0
**Total**: PKR 150,000

---

## Payment Details

**Bank Name**: [Your Bank]
**Account Title**: [Account Name]
**Account Number**: [Account Number]

**Payment Methods Accepted**:
- Bank Transfer
- Online Payment

---

## Terms & Conditions

- Payment is due within 30 days of invoice date
- Late payments may incur 2% monthly interest
- Please include invoice number in payment reference

---

## Notes
Thank you for your continued partnership. Looking forward to another productive month!

---

*Thank you for your business!*
```

## Error Handling Rules

### Missing Rate Information
```markdown
# ERROR: Cannot Generate Invoice

**Reason**: No rate found for client [Client Name]

**Action Required**:
1. Add client rate to /Accounting/Rates.md
2. Retry invoice generation

**Template for Rates.md**:
```
## [Client Name]
- Rate: PKR [amount] per [month/hour/project]
- Effective Date: [YYYY-MM-DD]
- Payment Terms: Net 30
- Notes: [any special terms]
```
```

### Duplicate Invoice Number
If invoice number already exists:
1. Check last invoice number in /Invoices/
2. Increment by 1
3. Retry with new number

### Missing Client Information
If client email or details missing:
1. Search previous invoices for this client
2. If not found, create task to gather information
3. Do NOT generate incomplete invoice

## Quality Checklist
Before creating approval request:
- [ ] Invoice number is unique
- [ ] All amounts calculated correctly
- [ ] Client information is complete
- [ ] Bank details are included
- [ ] Due date is 30 days from issue date
- [ ] No spelling errors in client name
- [ ] Invoice saved to correct folder
- [ ] Approval request created

## Post-Approval Actions
After invoice is approved:
1. Update invoice status from "draft" to "sent"
2. Send invoice to client via email
3. Create follow-up task for due date
4. Update /Accounting/Current_Month.md with expected revenue
5. Move approval file to /Approved/

---
*Last updated: 2026-02-16*
