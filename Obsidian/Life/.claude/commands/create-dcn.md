# Create DCN

Create a new Deal Continuity Notes (DCN) file for tracking a transaction.

## Usage

Invoke with deal name:
- `/create-dcn "CBE Nigeria"`
- `/create-dcn KarmSolar`

Or invoke without arguments to be prompted.

## Steps

### 1. Get Deal Name

If provided as argument, use it.

If not provided:
```
What is the name of this deal/transaction?
```

Naming conventions:
- Use client name or project name
- Prefix with sponsor if helpful (e.g., "CBE Nigeria" not just "Nigeria")
- Keep concise but unambiguous

### 2. Check for Duplicates

Search existing DCNs:
```
Glob: Work/0. DCN*.md
```

If similar name found:
```
Found similar DCN: [[0. DCN CBE Equity]]

Is this:
1. The same deal (open existing)
2. A different deal (create new)
```

### 3. Gather Overview Information

**Client/Counterparty** (required):
```
Who is the client/sponsor for this transaction?
```

Check if RME exists; if not, offer to create one.

**Deal Type** (required):
```
What type of transaction?
1. Equity raise
2. Debt raise
3. M&A / Sale
4. Refinancing
5. Project finance
6. Advisory
7. Other
```

**Our Role** (required):
```
What is our role?
1. Sell-side advisor
2. Buy-side advisor
3. Arranger
4. Placement agent
5. Financial advisor
6. Other
```

**One-liner** (required):
```
One-line description of the deal:
(e.g., "$50m equity raise for 100MW solar portfolio in Nigeria")
```

### 4. Set Initial Status

**Phase** (required):
```
What phase is the deal in?
1. Preparation
2. Teaser and Initial Discussions
3. NBO/Term Sheet
4. Mandate/Binding Offer
5. Legal Execution
```

**Current Milestone** (optional):
```
What is the current milestone? (Enter to skip)
```

**Blockers** (optional):
```
Any current blockers? (Enter to skip)
```

### 5. Investment Thesis (if known)

```
Why does this deal make sense? (2-3 sentences, or Enter to skip)
```

### 6. Key Terms (if known)

```
High-level terms (structure, size, pricing, tenor)? (Enter to skip)
```

### 7. Stakeholders

**Internal team:**
```
Who is on the internal team? (comma-separated, or Enter to skip)
```

**Client contacts:**
```
Key client contacts? (comma-separated, or Enter to skip)
```
- For each, check if RME exists or offer to create

**Counterparties** (if any identified):
```
Known counterparties/investors? (comma-separated, or Enter to skip)
```
- For each, check if RME exists or offer to create
- Will be expanded via Investor Tracking

**Advisors** (if known):
```
Other advisors (legal, technical, etc.)? (Enter to skip)
```

### 8. Key Dates (if known)

```
Any key dates/milestones? (Enter to skip)
Format: Milestone | Date
Example: Teaser launch | 2026-03-01
```

Populate Key Dates table.

### 9. Create the File

Generate filename: `0. DCN [Deal Name].md`

Create file in `Work/` folder:

```markdown
#### Overview
**Client/Counterparty:** [Client name] ([[00. RME Client]] if exists)
**Deal Type:** [Selected type]
**Our Role:** [Selected role]
**One-liner:** [Description]

#### Status
**Phase:** [Selected phase]
**Current Milestone:** [If provided]
**Blockers:** [If provided]

#### Investment Thesis
[If provided, else placeholder]

#### Key Terms
[If provided, else placeholder]

#### Stakeholders
**Internal:** [Team members]
**Client Contacts:** [Names with RME links if exist]
**Counterparties:** [Names with RME links if exist]
**Advisors:** [If provided]

#### Key Dates
| Milestone | Date |
|-----------|------|
| [Entries if provided] |

#### Documents
[Links to SharePoint files - term sheets, models, memos]

#### Activity Log
[YYYY-MM-DD] DCN created. [Initial context if any]
```

### 10. Create Transaction Tag

Note the tag to use for tasks:
- Infer from deal name (e.g., "CBE Nigeria" → #CBE_Nigeria)
- Or ask user to confirm

```
Suggested task tag: #CBE_Nigeria
Use this tag, or enter alternative:
```

Remind user to use this tag for related tasks.

### 11. Offer to Create Investor Tracker

```
Create Investor Tracking file for this deal? (y/N)
```

If yes, invoke `create-investor-tracker` skill.

### 12. Link Back

If client RME exists:
- Add deal to RME Current Status > Deal Involvement

Report summary:
```
Created: [[0. DCN CBE Nigeria]]
- Type: Equity raise
- Role: Sell-side advisor
- Phase: Preparation
- Tag: #CBE_Nigeria

Linked to:
- [[00. RME CrossBoundary Energy]] (client)
```

## Phase Definitions

| Phase | Description |
|-------|-------------|
| Preparation | Internal prep, no market contact yet |
| Teaser and Initial Discussions | Market outreach, initial investor conversations |
| NBO/Term Sheet | Receiving/negotiating non-binding offers |
| Mandate/Binding Offer | Negotiating mandate or binding terms |
| Legal Execution | Documentation, closing |

## Companion Skills

- `update-dcn`: Log activity, update status
- `create-investor-tracker`: Create weekly investor tracking
- `create-rme`: Create RME for client/counterparties

## Future Enhancements (365 Integration)

When MSFT Graph is available:
- Link to SharePoint folder for documents
- Pre-populate team from meeting attendees
- Track email threads related to deal
- Calendar integration for key dates
