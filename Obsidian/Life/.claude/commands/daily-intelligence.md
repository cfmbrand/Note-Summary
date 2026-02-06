# Daily Intelligence

Generate smart daily briefing structured by transaction, surfacing items that need attention. Inject into Daily Scratchpad.

## Usage

Run each morning, or invoke manually at any time.

## Steps

### 1. Ensure Daily Scratchpad Exists

Check for today's scratchpad: `Work/Scratchpad/Daily Scratchpad YYYY-MM-DD.md`

If it doesn't exist:
- This skill focuses on intelligence generation
- Inform user to create scratchpad first (via Templater) or create a basic one

### 2. Gather All Incomplete Tasks

Search across the vault for tasks:

```
Grep for:
- "- [ ]" (incomplete)
- "- [/]" (in progress)
```

For each task found:
- Extract task text
- Extract due date (📅 YYYY-MM-DD)
- Extract tags (#CBE_Equity, #CBE_Kamoa, #Trafigura, #Gridworks, #KarmSolar, #GreenCo, #BD, #Other)
- Note which file it's in
- Note if in-progress, when it was marked as such (from git or file modified date)

Categorize:
- **Overdue**: Due date < today, not completed
- **Stale**: In-progress (`[/]`) for >3 days
- **Upcoming**: Due today or tomorrow

### 3. Scan Recent Notes for Commitments

Read call notes and scratchpads from last 7 days:

```
Glob: Work/Call Notes*.md (last 7 days by modified date)
Glob: Work/Scratchpad/Daily Scratchpad*.md (last 7 days)
```

Search for commitment patterns:
- "I will...", "I'll..."
- "We'll send...", "We should..."
- "Let me...", "Let's..."
- "Need to follow up on..."

For each commitment found:
- Check if corresponding task exists
- If no task: flag as "Untracked commitment"

Search for urgency patterns:
- "urgent", "ASAP", "EOD", "EOW", "by Friday", "by end of week"
- "need to revert", "they're waiting"

### 4. Check Relationship Health

For each RME file (`Work/00. RME*.md`):

1. Read the Interaction Log section
2. Parse the most recent entry date
3. Check Current Status for active deal links

Categorize:
- **Active deal relationship**: RME linked to a DCN in progress
  - Flag if last interaction >2 weeks ago
- **BD/warm relationship**: Not on active deal but previously engaged
  - Flag if last interaction >4 weeks ago

### 5. Check Deal Momentum

For each DCN file (`Work/0. DCN*.md`):

1. Read the Activity Log section
2. Parse the most recent entry date
3. Read Status section (Phase, Blockers)

Flag:
- **Stale deal**: No activity logged in >1 week
- **Unresolved blocker**: Blocker listed for >1 week
- **Milestone risk**: Key Date approaching with no recent activity

### 6. Gather Calendar (Future - 365)

When Calendar integration available:
- Get today's meetings
- For each meeting, identify attendee RMEs and relevant DCNs
- Note last interaction with each attendee
- Flag meetings needing prep

For now: Skip this section or note "Calendar integration pending"

### 7. Gather Email Flags (Future - 365)

When Email integration available:
- Get high-priority flagged emails not yet processed
- Match sender to RMEs

For now: Skip this section

### 8. Structure Output by Transaction

Group all findings by transaction:

```markdown
#### Daily Intelligence

##### CBE Equity [[0. DCN CBE Equity]]
- [ ] Overdue: [task description] (X days overdue)
- [ ] Stale: [task description] (in progress since [date])
- [ ] Commitment: [untracked commitment] (from [[Call Notes YYYY-MM-DD]])
- Relationship: No contact with [[00. RME Name]] in X weeks
- [HH:MM] Meeting with [[00. RME Name]] - last spoke [date]

##### CBE Kamoa [[0. DCN CBE Kamoa]]
[same structure]

##### Gridworks [[0. DCN Gridworks]]
[same structure]

##### Trafigura [[0. DCN Trafigura]]
[same structure]

##### KarmSolar [[0. DCN KarmSolar]]
[same structure]

##### Africa GreenCo [[0. DCN Africa GreenCo]]
[same structure]

##### BD / Pipeline
- Email from [[00. RME Name]] re: [subject] - not yet logged
- [[00. RME Name]] mentioned [opportunity] ([[Call Notes YYYY-MM-DD]]) - follow up?
- Stale relationship: [[00. RME Name]] - no contact in X weeks

##### Other
- [Items not matching any transaction]
```

**Rules:**
- Only show transaction sections that have items to flag
- For sections with nothing to flag, either omit or show "Nothing to flag today"
- Prefix actionable items with `- [ ]` so they can become tasks
- Include wikilinks to source notes and RMEs/DCNs

### 9. Inject into Daily Scratchpad

Open the Daily Scratchpad file.

Find the `#### Daily Intelligence` section (should be near the top).

Replace everything between `#### Daily Intelligence` and the next `---` or `####` with the generated content.

Preserve all other sections of the scratchpad.

### 10. Report Summary

Tell the user:
- Number of overdue tasks
- Number of stale items
- Number of untracked commitments
- Number of stale relationships
- Any deals with blockers or momentum concerns

## Configurable Thresholds

| Item | Default | Description |
|------|---------|-------------|
| Task stale threshold | 3 days | In-progress task with no update |
| Relationship stale (active deal) | 2 weeks | Investor on live deal, no contact |
| Relationship stale (BD) | 4 weeks | Warm relationship, no contact |
| Deal activity threshold | 1 week | No DCN activity log entry |
| Blocker age threshold | 1 week | Blocker unresolved |
| Recent notes window | 7 days | How far back to scan for commitments |

## Future Enhancements (365 Integration)

When MSFT Graph is available:
- Calendar Prep output feeds directly into this skill
- Today's meetings shown with RME/DCN context
- Email flags for unprocessed high-priority items
- Smarter attendee matching via Outlook contacts
- Auto-create follow-up calendar blocks from flagged items

## Transaction Tag Mapping

| Tag | DCN |
|-----|-----|
| #CBE_Equity | [[0. DCN CBE Equity]] |
| #CBE_Kamoa | [[0. DCN CBE Kamoa]] |
| #Trafigura | [[0. DCN Trafigura]] |
| #Gridworks | [[0. DCN Gridworks]] |
| #KarmSolar | [[0. DCN KarmSolar]] |
| #GreenCo | [[0. DCN Africa GreenCo]] |
| #BD | BD / Pipeline section |
| #Other | Other section |
