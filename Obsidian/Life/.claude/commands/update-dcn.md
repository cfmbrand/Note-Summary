# Update DCN

Log activity, update phase/status, or modify deal details for an existing DCN.

## Usage

Invoke with deal name:
- `/update-dcn "CBE Equity"`
- `/update-dcn Trafigura`

Or invoke without arguments to select from existing DCNs.

## Steps

### 1. Identify the DCN

If deal name provided:
- Search `Work/0. DCN*.md` for matching file
- Fuzzy match if exact match not found

If not provided:
- List existing DCNs with current phase
- Ask user to select one

Read the current DCN file.

### 2. Determine Update Type

Ask user:
```
What would you like to update?
1. Log activity (add to Activity Log)
2. Update status (phase, milestone, blockers)
3. Update key dates
4. Update stakeholders
5. Update terms / thesis
6. Multiple of the above
```

### 3. Log Activity (if selected)

Prompt for activity details:

**Date** (default today):
```
When did this occur? (YYYY-MM-DD, or Enter for today)
```

**Activity type**:
```
What type of activity?
1. Call/meeting
2. Document sent (teaser, IM, etc.)
3. Document received (NBO, term sheet)
4. Internal milestone
5. Investor update
6. Other
```

**Summary**:
```
One-line summary:
```

**Link to notes** (optional):
```
Link to call notes? (Enter filename or skip)
```

**Counterparties involved** (optional):
```
Which counterparties involved? (comma-separated, or skip)
```
- For each, also update their RME Interaction Log

Construct entry:
```
[YYYY-MM-DD] [Activity type] - [summary]. See [[Call Notes YYYY-MM-DD]]
```

Append to Activity Log section.

### 4. Update Status (if selected)

Show current Status section.

**Phase progression:**
```
Current Phase: Teaser and Initial Discussions

Update phase?
1. Keep current
2. Preparation
3. Teaser and Initial Discussions
4. NBO/Term Sheet
5. Mandate/Binding Offer
6. Legal Execution
7. Closed / Completed
8. On Hold
9. Dead
```

**Current Milestone:**
```
Current: Awaiting feedback on teaser
Update milestone (Enter to keep):
```

**Blockers:**
```
Current: None
Update blockers (Enter to keep, 'clear' to remove all):
```

### 5. Update Key Dates (if selected)

Show current Key Dates table.

Options:
```
1. Add new date
2. Update existing date
3. Mark date as completed
4. Remove date
```

**Add new:**
```
Milestone name:
Target date (YYYY-MM-DD):
```

**Update existing:**
- Select from list
- Enter new date or mark completed

### 6. Update Stakeholders (if selected)

Show current Stakeholders section.

For each category, offer to add/update:

**Internal team:**
```
Current: John, Sarah
Add/update (Enter to keep):
```

**Client Contacts:**
```
Current: CEO Name
Add/update (Enter to keep):
```

**Counterparties:**
```
Current: Norfund, ADIA
Add/update (Enter to keep):
```
- For new counterparties, check if RME exists
- Offer to update Investor Tracking if exists

**Advisors:**
```
Current: Clifford Chance (legal)
Add/update (Enter to keep):
```

### 7. Update Terms / Thesis (if selected)

**Investment Thesis:**
```
Current thesis:
[Current text]

Update? (Enter new text, or Enter to keep):
```

**Key Terms:**
```
Current terms:
[Current text]

Update? (Enter new text, or Enter to keep):
```

### 8. Apply Changes

Use `Edit` tool to update the DCN file with all changes.

### 9. Cascade Updates

If activity involved counterparties:
- Prompt to update relevant RME Interaction Logs
- Show proposed entries, confirm before applying

If phase changed significantly:
- Prompt to update Investor Tracking status if exists
- Suggest adding milestone to Key Dates

### 10. Report Summary

```
Updated [[0. DCN CBE Equity]]:
- Logged: 2026-02-06 Call with Norfund - discussed pricing expectations
- Phase: Teaser and Initial Discussions → NBO/Term Sheet
- Added milestone: NBOs due | 2026-03-15

Also updated:
- [[00. RME Norfund]]: Added interaction log entry
```

## Status Transitions

Typical progression:
```
Preparation → Teaser and Initial Discussions → NBO/Term Sheet → Mandate/Binding Offer → Legal Execution → Closed
```

Off-ramps:
- **On Hold**: Paused but may resume
- **Dead**: Not proceeding

When marking Closed:
- Prompt for outcome summary
- Update client RME with deal outcome
- Archive or move file (optional)

## Companion Skills

- `create-dcn`: Create new DCN
- `process-call-notes`: Auto-updates DCNs from call notes
- `update-rme`: Update counterparty RMEs

## Future Enhancements (365 Integration)

When MSFT Graph is available:
- Suggest activities from recent calendar events
- Link to SharePoint documents
- Track email threads for activity
- Auto-update stakeholders from meeting attendees
