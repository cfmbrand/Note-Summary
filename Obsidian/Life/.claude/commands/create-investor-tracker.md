# Create Investor Tracker

Create a new Investor Tracking file to track week-over-week investor status for a transaction.

## Usage

Invoke with deal name:
- `/create-investor-tracker "CBE Equity"`
- `/create-investor-tracker Trafigura`

Or invoke without arguments to select from existing DCNs.

## Steps

### 1. Identify the Deal

If deal name provided:
- Search `Work/0. DCN*.md` for matching DCN
- Confirm this is the correct deal

If not provided:
- List existing DCNs (filter to active deals in Teaser phase or later)
- Ask user to select one

Check for existing tracker:
```
Glob: Work/01. Investor Tracking*.md
```

If tracker already exists for this deal:
```
Investor Tracking already exists: [[01. Investor Tracking CBE Equity]]
Open existing file? Or create new week's tracker?
```

### 2. Set Week Commencing Date

```
Week commencing date? (YYYY-MM-DD, or Enter for this Monday)
```

Default to the Monday of the current week.

### 3. Gather Initial Investor List

Pull from DCN Stakeholders > Counterparties if available.

Then prompt:
```
Initial investors to track (comma-separated):
(These will be added to the tracker with RME links)
```

For each investor:
- Check if RME exists: `Work/00. RME [Name].md`
- If not, offer to create RME

### 4. Set Initial Positioning

For each investor, prompt:
```
[Investor Name] - Initial positioning:
1. Not yet contacted
2. Teaser sent
3. Initial call scheduled
4. Initial call completed - interested
5. Initial call completed - passed
6. NDA signed
7. IM sent
8. In DD
9. NBO received
10. Custom (enter text)
```

### 5. Set Next Week Actions

For each investor showing interest (not "passed"):
```
[Investor Name] - Next week action:
(e.g., "Schedule follow-up call", "Send IM", "Await NBO")
```

### 6. Create the File

Generate filename: `01. Investor Tracking [Deal Name].md`

Create file in `Work/` folder:

```markdown
#### Deal
**Transaction:** [[0. DCN Deal Name]]
**Week commencing:** YYYY-MM-DD

#### Investor Tracker

| Investor | Positioning | Next Week Actions |
|----------|-------------|-------------------|
| [[00. RME Investor1]] | [Status] | [Action] |
| [[00. RME Investor2]] | [Status] | [Action] |
| [[00. RME Investor3]] | [Status] | [Action] |

#### Weekly Notes

[Week commencing YYYY-MM-DD]
- Tracker created with X investors
```

### 7. Link to DCN

Update the DCN to reference the tracker:
- Add note in Documents section: "Investor Tracking: [[01. Investor Tracking Deal Name]]"

### 8. Report Summary

```
Created: [[01. Investor Tracking CBE Equity]]
- Week commencing: 2026-02-03
- Tracking 5 investors:
  - [[00. RME Norfund]] - Teaser sent
  - [[00. RME ADIA]] - Initial call scheduled
  - [[00. RME Meridiam]] - Not yet contacted
  ...

Linked to [[0. DCN CBE Equity]]
```

## Rolling Forward

When a new week starts, the tracker should be updated rather than creating a new file.
Use `update-investor-tracker` skill (or manually):

1. Update "Week commencing" date
2. Add column for previous week or archive to Weekly Notes
3. Update positioning based on progress
4. Set new Next Week Actions

**Weekly Notes format:**
```
[Week commencing YYYY-MM-DD]
- Norfund: Completed IC, awaiting NBO
- ADIA: Passed after DD concerns
- Meridiam: Strong interest, requesting model
```

## Positioning Stages

Typical progression:
```
Not yet contacted
    → Teaser sent
    → Initial call scheduled
    → Initial call completed
        → Interested (continue below)
        → Passed (end)
    → NDA signed
    → IM sent
    → In DD
    → NBO received
    → Selected / Shortlisted
    → Binding offer
    → Closed
```

## Companion Skills

- `create-dcn`: Creates deal that tracker links to
- `create-rme`: Creates RME for new investors
- `weekly-deals-briefing`: Pulls from tracker for weekly summary

## Future Enhancements (365 Integration)

When MSFT Graph is available:
- Auto-suggest investors based on recent email/calendar activity
- Track last contact date from email/calendar
- Flag investors with no recent communication
- Sync with team calendar for scheduled calls
