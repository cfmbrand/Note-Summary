# Process Call Notes

Parse call/meeting notes and propagate extracted information to relevant RMEs and DCNs.

## Usage

Invoke after creating or editing call notes. Optionally provide the path to the call notes file.

## Steps

### 1. Identify the Call Notes File

If no path provided, look for:
- Most recently modified file matching `Work/Call Notes*.md`
- Or ask user which call notes to process

Read the call notes file.

### 2. Parse Call Notes

Extract from the file:
- **Attendees**: Listed under `#### Attendees`, organized by organization
- **Discussion points**: Content under `#### Notes`
- **Tasks**: Content under `#### Take-Aways and Next Steps`
- **Date**: From filename (`Call Notes YYYY-MM-DD`)

### 3. Identify Linked Entities

For each organization/attendee mentioned:

1. Search for existing RME: `Glob` for `Work/00. RME*.md`, then `Grep` for organization name
2. Use fuzzy matching if exact match fails
3. Flag any unrecognized entities for user confirmation

For deal/transaction mentions:

1. Search for existing DCN: `Glob` for `Work/0. DCN*.md`
2. Match based on deal names, project names, or company names mentioned
3. Also check task tags (#CBE_Equity, #CBE_Kamoa, etc.) to infer deals

### 4. Prepare RME Updates

For each matched RME, prepare updates:

**Interaction Log** (always update):
```
[YYYY-MM-DD] Call with [attendees from that org] - [1-line summary of discussion relevant to them]. See [[Call Notes YYYY-MM-DD]]
```

**Intelligence** (update if any of these mentioned):
- Strategy or mandate changes
- Personnel changes ("X is leaving", "Y just joined")
- Fund status (fundraising, deployment pace, fund lifecycle)
- Preferences or concerns expressed
- Market views or appetite signals

**Key Contacts** (update if new people introduced):
- Add new contacts to the table with available info

**Current Status** (update if deal involvement discussed):
- Update Active Conversations or Deal Involvement

### 5. Prepare DCN Updates

For each matched DCN, prepare updates:

**Activity Log** (always update):
```
[YYYY-MM-DD] Call with [counterparties] - [summary of deal-relevant discussion]. See [[Call Notes YYYY-MM-DD]]
```

**Status/Phase** (update if milestone discussed):
- Update Current Milestone
- Update Phase if progressing

**Blockers** (update if new blockers identified or resolved):
- Add new blockers
- Mark resolved blockers

**Key Dates** (update if dates mentioned):
- Add to Key Dates table

### 6. Validate Tasks

Review tasks in Take-Aways section:
- Ensure each has appropriate transaction tag (#CBE_Equity, #Trafigura, etc.)
- Ensure each has a due date where timing was implied
- Flag any commitments in Notes section not captured as tasks:
  - "I will...", "I'll...", "We'll send...", "Let me..."
  - "Let's schedule...", "We should..."

### 7. Confirm with User

Present summary of proposed changes:

```
## Proposed Updates

### RMEs to Update:
- [[00. RME Norfund]]: Interaction Log + Intelligence (mentioned fund deployment pace)
- [[00. RME ADIA]]: Interaction Log only

### DCNs to Update:
- [[0. DCN CBE Equity]]: Activity Log + Key Dates (targeting Q2 close)

### New Entities (create RME?):
- "Meridiam" - mentioned as potential co-investor

### Task Validation:
- Missing tag: "Send teaser to Norfund" → suggest #CBE_Equity
- Untracked commitment: "I'll send the updated model" (from Notes section)

Proceed with updates? [Y/n]
```

### 8. Apply Changes

After user confirmation:
- Use `Edit` tool to update each RME file
- Use `Edit` tool to update each DCN file
- If user confirms new entity, invoke `create-rme` skill
- Report summary of changes made

## Future Enhancements (365 Integration)

When MSFT Graph is available:
- Auto-trigger when Transcript Ingester saves new call notes
- Pre-populate attendee matches from Outlook contacts / meeting invite
- Cross-reference with recent email threads for additional context
- Create calendar follow-ups directly

## Entity Matching Logic

Priority order for matching attendees to RMEs:
1. Exact match on organization name in RME filename
2. Exact match on organization name in RME Entity Profile
3. Fuzzy match on organization name (Levenshtein distance)
4. Match on contact name in RME Key Contacts table
5. Future (365): Match on email domain

If no match found with reasonable confidence, flag for user.

## Intelligence Extraction Patterns

| Pattern in Notes | Update Location |
|------------------|-----------------|
| "They're raising...", "new fund", "Fund IV" | RME Intelligence (fundraise status) |
| "[Name] is leaving", "[Name] just joined", "promoted" | RME Intelligence + Key Contacts |
| "can't do X due to mandate", "excluded sectors" | RME Investment Criteria |
| "targeting close by", "expecting to sign" | DCN Key Dates |
| "waiting on", "need approval from", "blocker" | DCN Blockers |
| "interested in [sector/geo]", "looking at" | RME Intelligence (appetite signals) |
