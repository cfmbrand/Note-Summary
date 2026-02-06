# Update RME

Add interaction log entry and/or update intelligence section for an existing RME.

## Usage

Invoke with RME name:
- `/update-rme Norfund`
- `/update-rme "Abu Dhabi Investment Authority"`

Or invoke without arguments to select from existing RMEs.

## Steps

### 1. Identify the RME

If entity name provided:
- Search `Work/00. RME*.md` for matching file
- Fuzzy match if exact match not found

If not provided:
- List existing RMEs
- Ask user to select one

Read the current RME file.

### 2. Determine Update Type

Ask user:
```
What would you like to update?
1. Add interaction (log a call/meeting/email)
2. Update intelligence (new info about the org)
3. Update contacts (new person / changed role)
4. Update investment criteria
5. Update deal involvement
6. Multiple of the above
```

### 3. Add Interaction (if selected)

Prompt for interaction details:

**Date** (default today):
```
When was this interaction? (YYYY-MM-DD, or Enter for today)
```

**Type**:
```
What type of interaction?
1. Call
2. Meeting (in-person)
3. Email
4. Conference/event
5. Other
```

**Attendees** (from their side):
```
Who attended from [Entity]? (comma-separated names)
```

**Summary**:
```
One-line summary of the interaction:
```

**Link to notes** (optional):
```
Link to call notes? (Enter filename or skip)
```

Construct entry:
```
[YYYY-MM-DD] [Type] with [attendees] - [summary]. See [[Call Notes YYYY-MM-DD]]
```

Append to Interaction Log section.

### 4. Update Intelligence (if selected)

Show current Intelligence section.

Prompt:
```
What intelligence to add? (Enter multi-line, blank line to finish)

Categories to consider:
- Org dynamics / politics
- Decision-making process
- Strategy shifts
- Personnel changes
- Fundraise / fund status
- Deployment pace
- Preferences / concerns
- Market views
```

Append new intelligence with date prefix:
```
[YYYY-MM-DD] [New intelligence text]
```

### 5. Update Contacts (if selected)

Show current Key Contacts table.

Options:
```
1. Add new contact
2. Update existing contact
3. Remove contact (left org)
```

**Add new contact:**
```
Name:
Title:
Email:
Notes (optional):
```

Add row to Key Contacts table.

**Update existing:**
- Select contact to update
- Show current values, prompt for changes

**Remove:**
- Select contact
- Move to Intelligence section: "[Date] [Name] left the organization"

### 6. Update Investment Criteria (if selected)

Show current Investment Criteria section.

For each field, show current value and prompt for update:
```
Current Sectors: Renewable energy, infrastructure
New value (Enter to keep):
```

Fields:
- Sectors
- Geographies
- Ticket Size
- Return Expectations
- Restrictions/Exclusions

### 7. Update Deal Involvement (if selected)

Show current Current Status section.

**Active Conversations:**
```
Current: CBE Equity (in DD)
Add/update? (Enter to keep):
```

**Deal Involvement:**
```
Current: Invested in Project X (2023)
Add/update? (Enter to keep):
```

Also prompt to update relevant DCN Stakeholders section if deal is in vault.

### 8. Apply Changes

Use `Edit` tool to update the RME file with all changes.

Report summary:
```
Updated [[00. RME Norfund]]:
- Added interaction: 2026-02-06 Call with Lars, Siri
- Added intelligence: Fund III 80% deployed, looking at larger tickets
- Added contact: Erik Johansen (new Principal)
```

## Companion Skills

- `create-rme`: Create new RME from scratch
- `process-call-notes`: Auto-updates RMEs from call notes

## Future Enhancements (365 Integration)

When MSFT Graph is available:
- Pre-populate interaction details from calendar event
- Pull contact info from Outlook
- Cross-reference recent emails for context
- Suggest contacts who emailed recently but aren't in Key Contacts
