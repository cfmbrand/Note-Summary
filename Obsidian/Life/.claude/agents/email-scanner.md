# Email Scanner Agent

Scan inbox for deal updates, relationship signals, and actionable intelligence. Update RMEs and flag items for attention.

## Schedule

- **Primary:** 9:00am, 12:00pm, 4:00pm weekdays
- **Optional:** 8:00pm (evening catch-up)
- **On-demand:** User can invoke manually

## Trigger

```bash
claude --agent email-scanner
```

## Dependency

**Requires:** Microsoft Graph API access (Mail.Read)

**Status:** Blocked until 365 auth resolved

## Purpose

Email is a primary capture source. This agent:
1. Scans new emails since last run
2. Matches senders to RMEs
3. Extracts actionable intelligence
4. Updates RME Interaction Logs
5. Flags high-priority items for Daily Scratchpad

## Processing Steps

### 1. Fetch New Emails

Using MSFT Graph API:
```
GET /me/messages
  ?$filter=receivedDateTime ge {last_scan_time}
  &$select=id,subject,from,receivedDateTime,bodyPreview,importance,flag
  &$top=50
  &$orderby=receivedDateTime desc
```

Track last scan time to avoid reprocessing.

### 2. Filter Emails

**Include:**
- External senders (not @yourcompany.com)
- Flagged/important emails
- Emails from known RME contacts
- Emails with deal keywords in subject

**Exclude:**
- Newsletters/marketing (unsubscribe patterns)
- Auto-replies
- Calendar invites (handled by Calendar Prep)
- Internal admin (IT, HR, facilities)

### 3. Match Senders to RMEs

For each email:
```
1. Extract sender email and domain
2. Search RME Key Contacts for email match
3. If no match, search by domain → org name
4. If no match, flag as potential new contact
```

### 4. Categorize Email Content

Scan subject and body preview for patterns:

| Category | Patterns | Priority |
|----------|----------|----------|
| **Deal response** | "re: teaser", "NBO", "term sheet", deal names | High |
| **Meeting request** | "schedule", "call", "meet", "discuss" | Medium |
| **Document share** | "attached", "model", "memo", links | Medium |
| **Intelligence** | "fund", "raising", "mandate", "strategy" | Medium |
| **Routine** | "thanks", "fyi", "noted" | Low |

### 5. Extract Intelligence

For Medium/High priority emails, extract:

**Deal signals:**
- Interest/pass indicators
- Pricing/terms feedback
- Timeline mentions
- Blocker mentions

**Relationship signals:**
- Personnel changes mentioned
- Fund status updates
- Strategy/mandate changes
- Market views

**Action items:**
- Requests for information
- Meeting requests
- Deadlines mentioned

### 6. Update RMEs

For each matched RME with new email:

**Interaction Log entry:**
```
[YYYY-MM-DD] Email from [Name] re: [Subject summary]. [Key point if any]
```

Only log substantive emails, not routine acknowledgments.

**Intelligence updates:**
If email contains intelligence signals, append to Intelligence section:
```
[YYYY-MM-DD] [Intelligence extracted] (via email)
```

### 7. Update DCNs (if deal-related)

If email relates to active deal:

**Activity Log entry:**
```
[YYYY-MM-DD] Email from [Counterparty] - [summary]. [Key point]
```

**Status updates if warranted:**
- Blocker resolved
- Milestone reached
- Phase progression

### 8. Flag High-Priority Items

Create flags for Daily Intelligence:

```markdown
## Email Flags

### Requires Response
- [[00. RME Norfund]]: Requesting revised model by EOW
- [[00. RME ADIA]]: Asked for call to discuss terms

### Deal Updates
- [[0. DCN CBE Equity]]: Meridiam passed (email from Sarah)
- [[0. DCN Trafigura]]: GreenCo NBO received

### Intelligence Captured
- [[00. RME CIP]]: Mentioned new SA platform mandate
- [[00. RME Actis]]: Fund III final close next month

### New Contacts (no RME)
- john.smith@newcompany.com - emailed about [subject]
```

### 9. Generate Scan Report

```markdown
# Email Scan Report
**Time:** YYYY-MM-DD HH:MM
**Emails scanned:** X
**Since:** [Last scan time]

## Summary
- Deal-related: X emails
- Intelligence captured: Y items
- RMEs updated: Z
- Flags raised: N

## RME Updates Made

| RME | Update Type | Summary |
|-----|-------------|---------|
| [[00. RME Norfund]] | Interaction Log | Email re: pricing |
| [[00. RME CIP]] | Intelligence | SA platform interest |

## High-Priority Flags

[As above]

## New/Unmatched Senders

| Email | Subject | Action |
|-------|---------|--------|
| john@newco.com | Partnership inquiry | Create RME? |

---
*Next scan: [Next scheduled time]*
```

### 10. Persist State

Save scan state:
```
.claude/state/email-scanner-state.json
{
  "last_scan": "2026-02-06T16:00:00Z",
  "emails_processed": ["id1", "id2", ...]
}
```

## Intelligence Extraction Patterns

| Pattern | Intelligence Type | RME Section |
|---------|-------------------|-------------|
| "raising Fund IV", "new fund" | Fundraise status | Intelligence |
| "deploying capital", "dry powder" | Deployment status | Intelligence |
| "[Name] joining/leaving" | Personnel change | Intelligence + Key Contacts |
| "mandate expanded", "new strategy" | Strategy change | Intelligence + Investment Criteria |
| "passed", "not proceeding" | Deal decision | DCN Activity Log |
| "interested", "progressing" | Deal decision | DCN Activity Log |

## Skills Invoked

- May invoke `update-rme` for substantive updates
- May invoke `update-dcn` for deal-related updates
- May invoke `create-rme` for new contacts (with confirmation)
- Flags feed into `daily-intelligence`

## Error Handling

| Issue | Handling |
|-------|----------|
| API rate limit | Back off, retry next scheduled run |
| Token expired | Log error, notify user to re-auth |
| Email parsing fails | Skip email, log for manual review |
| Sender ambiguous | Flag for user confirmation |

## Privacy & Discretion

- Only process emails where user is direct recipient (not CC/BCC initially)
- Don't log sensitive personal emails
- Respect confidentiality markers if present
- Never forward or expose email content externally

## Future Enhancements

- Mail.Send for draft responses
- Thread tracking (follow conversation over time)
- Attachment processing (extract from docs)
- Sentiment analysis on responses
