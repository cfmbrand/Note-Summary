# Create RME

Create a new Relationship Memory/Entity (RME) file from template with guided prompts, ensuring consistency.

## Usage

Invoke with entity name:
- `/create-rme Norfund`
- `/create-rme "Abu Dhabi Investment Authority"`

Or invoke without arguments to be prompted for the entity name.

## Steps

### 1. Get Entity Name

If entity name provided as argument, use it.

If not provided, ask:
```
What is the name of the entity/organization?
```

Clean the name:
- Remove common suffixes if duplicative ("Norfund AS" → "Norfund")
- Preserve important legal distinctions ("GreenCo Africa" vs "GreenCo")

### 2. Check for Duplicates

Search existing RMEs:
```
Glob: Work/00. RME*.md
```

For each existing RME:
- Compare entity name (case-insensitive)
- Check for fuzzy matches (common misspellings, abbreviations)
- Check inside file for aliases or alternate names

If potential match found:
```
Found similar RME: [[00. RME Norfund]]

Is this:
1. The same entity (open existing RME)
2. A different entity (create new RME)
```

### 3. Gather Basic Information

Prompt user for core fields (or infer from context if triggered from call notes):

**Entity Type** (required):
```
What type of entity is [Name]?
1. SWF (Sovereign Wealth Fund)
2. DFI (Development Finance Institution)
3. PE (Private Equity)
4. Corporate/Strategic
5. Bank
6. Credit Fund
7. Multiple (specify)
```

**HQ Location** (required):
```
Where is [Name] headquartered?
```

**AUM / Scale** (optional):
```
What is their AUM or scale? (Enter to skip)
```

**Mandate Summary** (required):
```
One-line summary of their investment mandate:
```

### 4. Pre-populate from Context

If triggered from `process-call-notes`:
- Extract attendees from that organization as initial Key Contacts
- Extract any mentioned investment criteria
- Create initial Interaction Log entry linking to the call notes

If triggered from email (Future 365):
- Extract sender as Key Contact (name, title from signature, email)
- Note email date as first interaction

### 5. Optional: Investment Criteria

Ask if user wants to add now or later:
```
Add investment criteria now? (y/N)
```

If yes, prompt for:
- **Sectors**: (e.g., "Renewable energy, infrastructure")
- **Geographies**: (e.g., "Sub-Saharan Africa, excluding South Africa")
- **Ticket Size**: (e.g., "$20-50m equity")
- **Return Expectations**: (e.g., "12-15% USD IRR")
- **Restrictions/Exclusions**: (e.g., "No thermal, no coal adjacency")

### 6. Create the File

Generate filename: `00. RME [Entity Name].md`

Create file in `Work/` folder with populated template:

```markdown
#### Entity Profile
**Type:** [Selected type]
**AUM / Scale:** [If provided, else blank]
**HQ:** [Location]
**Mandate Summary:** [One-liner]

#### Key Contacts
| Name | Title | Email | Notes |
|------|-------|-------|-------|
| [From context if available] | | | |

#### Investment Criteria
**Sectors:** [If provided]
**Geographies:** [If provided]
**Ticket Size:** [If provided]
**Return Expectations:** [If provided]
**Restrictions/Exclusions:** [If provided]

#### Current Status
**Active Conversations:**
**Deal Involvement:**

#### Interaction Log
[YYYY-MM-DD] Created RME. [Context if available, e.g., "Met during CBE Equity process."]

#### Intelligence
[To be populated from future interactions]
```

### 7. Link Back to Source

If triggered from call notes:
- Add RME link to the call notes file (in Attendees or Notes section)

If deal context provided:
- Add entity to relevant DCN Stakeholders section (under Counterparties)

### 8. Confirm Creation

Report to user:
```
Created: [[00. RME Entity Name]]
- Type: DFI
- HQ: Oslo, Norway
- Mandate: Invests in renewable energy in developing markets

Linked to:
- [[Call Notes 2026-02-06]] (source)
- [[0. DCN CBE Equity]] (added to Counterparties)
```

## Entity Type Inference

If context available, suggest type based on signals:

| Signal | Suggested Type |
|--------|----------------|
| "sovereign", "government", "state-owned" | SWF |
| "development", "DFI", "bilateral" | DFI |
| "fund", "GP", "LP", "portfolio company" | PE |
| "corporate", "strategic", "utility", "IPP" | Corporate/Strategic |
| "bank", "commercial bank", "lending" | Bank |
| "credit", "debt fund", "mezzanine" | Credit Fund |

## Future Enhancements (365 Integration)

When MSFT Graph is available:
- Pre-populate Key Contacts from Outlook (name, title, email, phone)
- Infer entity from email domain (e.g., @norfund.no → Norfund)
- Show recent email history with this domain as context
- Suggest related contacts from same organization
- Sync contacts bidirectionally (RME ↔ Outlook)

## Companion Skills

- `update-rme`: Add interaction, update intelligence
- `process-call-notes`: May trigger create-rme for new entities
