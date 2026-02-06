	# BankerOS - Product Requirements Document

## Vision

BankerOS is an agent-augmented operating system for an investment banking MD focused on frontier markets renewable energy. It captures, organizes, connects, and surfaces information to:

1. **Never lose signal** - intelligence from calls and interactions is durably stored and retrievable
2. **Surface connections** - pattern match across relationships and deals to identify BD opportunities
3. **Enable weekly rhythm** - structured briefings that feed collaborative voice sessions with an agent

The goal is to direct team work effectively, maintain nuanced understanding of all active deals, and systematically develop new business through long-term intelligence accumulation.

---

## Information Flow

```
┌─────────────────────────────────────────────────────────────────────┐
│                      AUTOMATED CAPTURE                               │
│   Email (MSFT Graph) │ Teams Transcripts │ Calendar (meeting prep)  │
└─────────────────────────────────┬───────────────────────────────────┘
                                  │
                                  ▼
┌─────────────────────────────────────────────────────────────────────┐
│                       MANUAL CAPTURE                                 │
│         Call Notes, Daily Scratchpad, ad-hoc imports                │
└─────────────────────────────────┬───────────────────────────────────┘
                                  │
                                  ▼
┌─────────────────────────────────────────────────────────────────────┐
│                           ORGANIZE                                   │
│              RME (relationships) ←→ DCN (deals)                     │
│                     Investor Tracking (weekly status)                │
└─────────────────────────────────┬───────────────────────────────────┘
                                  │
                                  ▼
┌─────────────────────────────────────────────────────────────────────┐
│                      DAILY INTELLIGENCE                              │
│   Smart task prioritization │ Stale items │ Implied urgency flags   │
│              ↓                                                       │
│         Injected into Daily Scratchpad each morning                 │
└─────────────────────────────────┬───────────────────────────────────┘
                                  │
                                  ▼
┌─────────────────────────────────────────────────────────────────────┐
│                      WEEKLY SYNTHESIS                                │
│         Weekly Review (deals) │ BD Weekly Briefing (opportunities)  │
│                    ↓                        ↓                        │
│              Questions for collaborative voice session               │
└─────────────────────────────────────────────────────────────────────┘
```

**Key principle:** Detail lives in source notes (Call Notes, Scratchpad). RMEs/DCNs contain structured summaries. Weekly outputs surface what matters and prompt discussion.

---

## Architecture

### Skills vs Agents

| | Skills | Agents |
|---|--------|--------|
| **Invocation** | User runs explicitly (`/process-call-notes`) | Triggered automatically by events |
| **Interaction** | Interactive prompts, confirmations | Runs in background, minimal interaction |
| **Scope** | Single task, immediate result | May orchestrate multiple skills |
| **Location** | `.claude/commands/*.md` | `.claude/agents/*.md` (to be created) |
| **Examples** | `/create-rme`, `/update-dcn` | Email Scanner, Calendar Prep |

### How Agents Use Skills

Agents invoke skills as part of their workflow:

```
┌─────────────────────────────────────────────────────────┐
│  TRANSCRIPT INGESTER (Agent)                            │
│                                                         │
│  Trigger: Post-meeting (scheduled poll)                 │
│                                                         │
│  1. Detect new transcript available                     │
│  2. Download and format as Call Notes                   │
│  3. Save to Work/Call Notes YYYY-MM-DD.md               │
│  4. ──► Invoke `process-call-notes` skill ◄──           │
│  5. Log completion                                      │
└─────────────────────────────────────────────────────────┘
```

Some components can work as both skill (user-invoked) and agent (scheduled):

```
┌─────────────────────────────────────────────────────────┐
│  DAILY INTELLIGENCE                                     │
│                                                         │
│  As Skill: User runs `/daily-intelligence`              │
│  As Agent: Scheduled to run at 6:30am automatically     │
│                                                         │
│  Same logic, different trigger.                         │
└─────────────────────────────────────────────────────────┘
```

### Trigger Mechanism

Claude Code doesn't have a built-in scheduler. Agents are triggered via **external scheduler** (macOS launchd or cron):

```
┌──────────────┐     ┌─────────────────┐     ┌──────────────┐
│  launchd     │────►│  Claude Code    │────►│  Vault       │
│  (schedule)  │     │  runs agent     │     │  updated     │
└──────────────┘     └─────────────────┘     └──────────────┘
```

**Schedule configuration:**
- Defined in `~/Library/LaunchAgents/` (macOS) or crontab
- Each agent has a plist file specifying when to run
- Invokes Claude Code CLI with the agent command

### Agent Schedule (Planned)

| Agent | Schedule | Depends on |
|-------|----------|------------|
| **Daily Intelligence** | 6:30am daily | - |
| **Calendar Prep** | 6:30am daily (with Daily Intelligence) | 365 |
| **Email Scanner** | 9am, 12pm, 4pm daily | 365 |
| **Transcript Ingester** | Every 30min during work hours | 365 / Meeting Bot |
| **BD Scanner** | Sunday 6pm weekly | - |
| **Weekly Deals Briefing** | Friday 5pm weekly | - |
| **Weekly BD Briefing** | Friday 5pm weekly | - |

---

## Product Suite

### Documents (Data Layer)

| Document | Purpose | Template |
|----------|---------|----------|
| **RME** | Relationship Memory/Entity - investor/counterparty dossier with intelligence | `00. RME [Name].md` |
| **DCN** | Deal Continuity Notes - deal context, status, stakeholders, activity log | `0. DCN [Deal].md` |
| **Investor Tracking** | Weekly status grid per transaction | `01. Investor Tracking [Deal].md` |
| **Call Notes** | Meeting/interaction documentation | Via Templater |
| **Daily Scratchpad** | Daily task and note capture | Via Templater |
| **Weekly Review** | Aggregated weekly summary by project | Via Templater |

### Skills (Automation Layer)

| Skill | Purpose | Status |
|-------|---------|--------|
| `process-call-notes` | Parse call notes → update relevant RMEs and DCNs | Specced |
| `create-rme` | Initialize new RME from template with guided prompts | Specced |
| `update-rme` | Add interaction log entry, refresh intelligence section | Specced |
| `create-dcn` | Initialize new DCN with deal details | Specced |
| `update-dcn` | Log activity, update phase/status | Specced |
| `create-investor-tracker` | New weekly tracker for a deal | Specced |
| `daily-intelligence` | Generate smart daily briefing with prioritized attention items | Specced |
| `weekly-deals-briefing` | Generate deals-focused weekly summary with questions | Specced |
| `weekly-bd-briefing` | Generate BD-focused weekly summary with questions (= BD Scanner) | Specced |

### Agents (Intelligence Layer)

| Agent | Purpose | Trigger | Status |
|-------|---------|---------|--------|
| **BD Scanner** | Scan intelligence for connections → outputs Weekly BD Briefing | Friday 5pm / on-demand | Specced |
| **Voice Session Prep** | Pre-flight briefing for voice chat (key questions, context) | Before voice session | Specced |
| **Calendar Prep** | Pre-meeting briefing from RME + DCN → feeds into Daily Intelligence | Morning (for day's meetings) | Specced (needs 365) |
| **Email Scanner** | Scan inbox for deal/relationship updates → update RMEs/DCNs | Multiple times daily | Specced (needs 365) |
| **Transcript Ingester** | Save Teams call transcripts as Call Notes, trigger processing | Post-meeting | Specced (needs 365) |
| **Meeting Bot** | Dial into Teams calls as participant, record and transcribe | Joins scheduled calls | Specced (needs 365/service) |

---

## Integrations

### Microsoft Graph API

**Status:** Pending - awaiting auth/permissions from corporate IT

**Purpose:** Email and Teams are primary communication channels. Integrating via Graph API enables automated capture without manual copy-paste.

**Capabilities (once auth is resolved):**

| Capability | Use Case | Agent |
|------------|----------|-------|
| **Mail.Read** | Scan inbox for deal updates, investor responses, market intel | Email Scanner |
| **Mail.Send** | Send drafted emails after approval | Email Drafter (future) |
| **Calendars.Read** | Trigger pre-meeting prep based on upcoming calls | Calendar Prep |
| **Calendars.ReadWrite** | Create follow-up meetings, block focus time | Calendar Manager (future) |
| **OnlineMeetings.Read** | Access Teams meeting metadata (may not include transcripts) | Transcript Ingester |

**Email Scanning Logic:**
- Run multiple times daily (e.g., 9am, 12pm, 4pm)
- Identify emails involving known RME contacts
- Extract actionable intel, update relevant RME Interaction Log
- Flag high-priority items for Daily Scratchpad
- Ignore routine/administrative emails

**Transcript Ingestion Logic:**
- Trigger post-meeting when transcript becomes available
- Save as Call Notes in `Work/` with standard template
- Auto-link to relevant RMEs based on participants
- Queue for `process-call-notes` skill

**Auth Considerations:**
- Delegated permissions (user-consented) vs. application permissions
- Token refresh handling for background agents
- Corporate IT may require admin consent for certain scopes
- Consider read-only scopes initially to minimize risk

### Meeting Transcription Strategy

**Problem:** OnlineMeetings.Read may not reliably provide transcripts, especially for:
- External calls (guests outside org)
- Calls where transcription wasn't enabled
- Calls on other platforms (Zoom, Google Meet)

**Solution: Meeting Bot**

A bot that joins calls as a participant (like Otter.ai, Fireflies, Fathom):

| Approach | Pros | Cons |
|----------|------|------|
| **OnlineMeetings.Read** | Native, no extra participant | May not have transcripts, Teams-only |
| **Meeting Bot (dial-in)** | Reliable transcripts, platform-agnostic | Visible as participant, may need consent |

**Meeting Bot Flow:**
1. Calendar Prep agent identifies upcoming calls
2. Meeting Bot auto-joins at scheduled time (or on-demand invite)
3. Records audio, generates transcript
4. Saves as Call Notes in vault with RME links
5. Queues for `process-call-notes` skill

**Implementation options:**
- Build custom bot (Azure Bot Service + Speech-to-Text)
- Use existing service (Otter, Fireflies, Fathom) + API integration
- Hybrid: Use Teams transcription where available, bot as fallback

**Open:** Does corporate IT allow bots joining calls? Compliance/recording consent requirements?

---

## Daily Intelligence

### Daily Scratchpad (Auto-Created)
- Created automatically each morning from template (via Templater or automation)
- Contains standard task queries from Obsidian Tasks plugin
- Serves as the working document for the day

### Daily Intelligence (Injected)
The `daily-intelligence` skill runs each morning and injects a smart briefing section into the Daily Scratchpad. This goes beyond simple task listing.

**Inputs:**
- Task status across vault (overdue, stale, in-progress)
- Recent call notes and scratchpad entries (commitments, implied urgency)
- RME interaction history (stale relationships)
- **Calendar Prep output** (today's meetings with RME/DCN context)
- Email flags from Email Scanner (unprocessed high-priority items)

**Structured by transaction, then BD** - mirrors how you think about the day.

**Signal types detected:**

| Signal Type | Detection Logic | Example |
|-------------|-----------------|---------|
| **Stale tasks** | In-progress (`[/]`) for >3 days | "Follow up with ADIA" started Monday, still open |
| **Overdue tasks** | Past due date | Task with 📅 2026-02-04 not completed |
| **Implied urgency** | "Urgent", "ASAP", "by EOW" in recent notes | Call note says "need to revert by Friday" |
| **Unactioned commitments** | "I will..." or "Let's..." in call notes, no task created | "I'll send the teaser" mentioned Tuesday, no task |
| **Stale relationships** | No RME interaction in X weeks + active deal connection | Haven't spoken to key investor on live deal |
| **Today's meetings** | Calendar prep needed | "Call with Gridworks at 2pm - see [[00. RME Gridworks]]" |
| **Email flags** | High-priority emails not yet processed | Email from CIP re: term sheet, no vault update |

**Output format:**
```markdown
#### Daily Intelligence

##### CBE Equity [[0. DCN CBE Equity]]
- [ ] Overdue: Follow up with ADIA on term sheet (3 days stale)
- [ ] Commitment: Send revised model to team (mentioned in Monday call)
- 10:00 Call with [[00. RME Norfund]] - prep: last spoke 2 weeks ago re: pricing

##### CBE Kamoa [[0. DCN CBE Kamoa]]
- [ ] Stale: No contact with [[00. RME GreenCo]] in 2 weeks
- [ ] Implied urgent: "Need Gridworks response by EOW" (Call 2026-02-03)

##### Gridworks [[0. DCN Gridworks]]
- 14:00 Call with [[00. RME Gridworks]] - prep: awaiting their response on structure
- No overdue items

##### Trafigura [[0. DCN Trafigura]]
- [ ] Commitment: You said you'd send the teaser (Call 2026-02-03)
- No meetings today

##### KarmSolar [[0. DCN KarmSolar]]
- Nothing to flag today

##### Africa GreenCo [[0. DCN Africa GreenCo]]
- Nothing to flag today

##### BD / Pipeline
- Email from [[00. RME CIP]] yesterday re: SA platform interest - not yet logged
- [[00. RME ADIA]] mentioned battery storage appetite (Call 2026-02-01) - connect to Eranove?
- Stale relationship: [[00. RME Actis]] - no contact in 4 weeks

##### Other
- No transaction-specific items today
```

### Morning Flow
1. Daily Scratchpad auto-created
2. `daily-intelligence` runs and injects briefing
3. Review on commute / with coffee
4. Triage: convert items to tasks, delegate, or dismiss

---

## Weekly Rhythm

### Weekly Deals Briefing
- Status of each active deal (phase, blockers, next steps)
- Key activities from the week (from DCN activity logs)
- Investor Tracking highlights (who moved, who stalled)
- **3-5 questions for voice discussion** (e.g., "Gridworks has missed two milestones - escalate?")

### Weekly BD Briefing
- New signals captured this week (from RME Intelligence sections)
- Stale relationships (no interaction in X weeks)
- Potential connections surfaced by BD Scanner
- Market/sector themes emerging across conversations
- **3-5 questions for voice discussion** (e.g., "CIP mentioned SA platform interest - worth a call with [colleague]?")

### Voice Session (Walk to Work)
- Agent has read both briefings
- Opens with top 2-3 items to discuss
- Collaborative back-and-forth, agent takes notes
- Outputs: action items added to Daily Scratchpad, flags for team

---

## BD Philosophy

BD is **intelligence accumulation over time**. Deals don't appear fully formed - they emerge from:

1. **Signal capture** - noting what counterparties mention they need, even if not immediately actionable
2. **Pattern recognition** - connecting dots across RMEs (Investor A needs X + Company B has X)
3. **Relationship maintenance** - not letting warm relationships go cold
4. **Proactive surfacing** - agent periodically prompts "have you considered...?"

The RME Intelligence section is the container for loose signals. The BD Scanner makes that intelligence queryable and actionable.

---

## Skill Specifications

Detailed skill specs are in `.claude/commands/`. Summary below.

| Skill | File | Purpose |
|-------|------|---------|
| `process-call-notes` | `.claude/commands/process-call-notes.md` | Parse call notes → update RMEs/DCNs |
| `daily-intelligence` | `.claude/commands/daily-intelligence.md` | Generate daily briefing by transaction |
| `create-rme` | `.claude/commands/create-rme.md` | Create new RME with guided prompts |
| `update-rme` | `.claude/commands/update-rme.md` | Add interaction, update intelligence/contacts |
| `create-dcn` | `.claude/commands/create-dcn.md` | Create new deal file with guided prompts |
| `update-dcn` | `.claude/commands/update-dcn.md` | Log activity, update phase/status |
| `create-investor-tracker` | `.claude/commands/create-investor-tracker.md` | Create weekly investor tracking for deal |
| `weekly-deals-briefing` | `.claude/commands/weekly-deals-briefing.md` | Weekly deals summary with questions |
| `weekly-bd-briefing` | `.claude/commands/weekly-bd-briefing.md` | Weekly BD summary with opportunities |

### Summary: `process-call-notes`

**Trigger:** Manual after creating call notes; Future: auto on transcript ingestion

**Flow:**
1. Parse attendees, notes, tasks from call notes
2. Match entities → existing RMEs/DCNs
3. Update RME Interaction Log + Intelligence
4. Update DCN Activity Log + Status
5. Validate tasks, flag untracked commitments
6. Confirm with user → apply changes

**365-ready:** Entity matching via Outlook contacts, auto-trigger from transcripts

---

### Summary: `daily-intelligence`

**Trigger:** Morning schedule or manual

**Scans:**
- Tasks (overdue, stale >3 days)
- Recent notes (commitments, urgency)
- RME Interaction Logs (stale relationships)
- DCN Activity Logs (deal momentum)
- Future: Calendar, email flags

**Output:** Structured by transaction, injected into Daily Scratchpad

**365-ready:** Calendar integration, email flags

---

### Summary: `create-rme`

**Trigger:** Manual, or prompted by process-call-notes for new entities

**Flow:**
1. Check for duplicates
2. Gather basic info (type, HQ, mandate)
3. Pre-populate from context if available
4. Create file, link back to source

**365-ready:** Pre-populate from Outlook contacts, infer from email domain

---

### Summary: `update-rme`

**Trigger:** Manual with entity name

**Capabilities:**
- Add interaction log entry (call/meeting/email)
- Update intelligence section
- Update contacts (add/update/remove)
- Update investment criteria
- Update deal involvement

**365-ready:** Pre-populate from calendar events, Outlook contacts

---

### Summary: `create-dcn`

**Trigger:** Manual with deal name

**Flow:**
1. Check for duplicates
2. Gather overview (client, type, role, one-liner)
3. Set initial phase and status
4. Add stakeholders (with RME links)
5. Create file, suggest task tag
6. Offer to create Investor Tracker

**365-ready:** Link to SharePoint, team from calendar

---

### Summary: `update-dcn`

**Trigger:** Manual with deal name

**Capabilities:**
- Log activity (calls, documents, milestones)
- Update status (phase, milestone, blockers)
- Update key dates
- Update stakeholders
- Cascade updates to related RMEs

**365-ready:** Suggest activities from calendar, email tracking

---

### Summary: `create-investor-tracker`

**Trigger:** Manual, or offered when creating DCN

**Flow:**
1. Link to existing DCN
2. Set week commencing date
3. Add initial investor list (with RME links)
4. Set positioning and next actions
5. Create file, link to DCN

**365-ready:** Auto-suggest investors from email/calendar activity

---

### Summary: `weekly-deals-briefing`

**Trigger:** Weekly (Friday/Monday) or manual

**Generates:**
- Status summary per active deal
- Investor tracking highlights
- Concerns (stale, blocked, slipping)
- 3-5 discussion questions

**365-ready:** Calendar integration, email activity tracking

---

### Summary: `weekly-bd-briefing`

**Note:** This is the same as BD Scanner agent - can be invoked as skill or scheduled as agent.

**Trigger:** Friday 5pm (scheduled) or manual (`/weekly-bd-briefing`)

**Generates:**
- Connections to explore (from cross-referencing intelligence)
- Follow-ups from last week
- Stale relationships needing attention
- Market themes emerging
- Questions for discussion

**365-ready:** Email scanning for signals, contact activity tracking

---

## Agent Specifications

Detailed agent specs are in `.claude/agents/`. Summary below.

| Agent | File | Schedule | 365 Required |
|-------|------|----------|--------------|
| `bd-scanner` | `.claude/agents/bd-scanner.md` | Sunday 6pm, Wed 12pm | No |
| `voice-session-prep` | `.claude/agents/voice-session-prep.md` | 7am weekdays | No |
| `calendar-prep` | `.claude/agents/calendar-prep.md` | 6:30am weekdays | Yes |
| `email-scanner` | `.claude/agents/email-scanner.md` | 9am, 12pm, 4pm | Yes |
| `transcript-ingester` | `.claude/agents/transcript-ingester.md` | Every 30min work hours | Yes |
| `meeting-bot` | `.claude/agents/meeting-bot.md` | Joins scheduled calls | Yes |

### Summary: `bd-scanner`

**Schedule:** Friday 5pm (weekly), optionally mid-week

**Scans:**
- RME Intelligence sections (appetite, mandates, needs)
- Recent call notes (opportunities, interests, intro requests)
- Previous BD Briefings (follow-up on open items)

**Finds:**
- Connections (Investor A needs X + Investor B has X)
- Stale relationships to reactivate
- Market themes emerging across conversations

**Output:** Weekly BD Briefing (no separate report)

**Note:** BD Scanner IS the `weekly-bd-briefing` - same thing.

**Can run now:** Yes

---

### Summary: `voice-session-prep`

**Schedule:** 7am weekdays (before commute)

**What it does:**
- Loads Daily Intelligence (already has prioritized items)
- Loads Weekly Briefings if recent
- Loads relevant RMEs/DCNs for context
- Signals ready for voice conversation

**Outputs:** No separate document. Outcomes captured directly into Daily Scratchpad during/after voice session.

**Can run now:** Yes

---

### Summary: `calendar-prep`

**Schedule:** 6:30am weekdays (with Daily Intelligence)

**For each meeting:**
- Match attendees to RMEs
- Pull last interaction and intelligence
- Identify relevant DCNs
- Surface open items and talking points

**Feeds into:** Daily Intelligence

**Can run now:** No (needs Calendars.Read)

---

### Summary: `email-scanner`

**Schedule:** 9am, 12pm, 4pm weekdays

**Processing:**
- Scan new emails since last run
- Match senders to RMEs
- Extract intelligence and deal signals
- Update RME Interaction Logs
- Flag high-priority items

**Skills invoked:** `update-rme`, `update-dcn`

**Can run now:** No (needs Mail.Read)

---

### Summary: `transcript-ingester`

**Schedule:** Every 30 min during work hours

**Processing:**
- Detect new transcripts (Graph API, Meeting Bot, or folder watch)
- Parse and format as Call Notes
- Identify speakers and match to RMEs
- Save to vault
- Invoke `process-call-notes`

**Can run now:** No (needs OnlineMeetings.Read or Meeting Bot)

---

### Summary: `meeting-bot`

**Trigger:** Joins qualifying scheduled meetings

**Options:**
- Third-party service (Fireflies, Otter) - recommended to start
- Custom Azure Bot - future

**Meeting selection:**
- External attendees required
- Exclude internal-only, 1:1s, confidential
- Minimum duration threshold

**Consent:** Must announce recording or note in calendar invite

**Can run now:** No (needs service setup)

---

## Backlog / Future Ideas

- [ ] Sector/geography views (e.g., "all Zambia power intel across RMEs")
- [ ] Team handoff notes (brief a colleague on a relationship/deal)
- [ ] CRM-style pipeline view generated from DCNs
- [ ] Email draft suggestions based on stale relationships
- [ ] Outlook/Teams send capability (draft → review → send with approval)
- [ ] Contact sync (RME contacts ↔ Outlook contacts)
- [ ] Shared inbox monitoring (team deal inbox)

---

## Open Questions

1. **Trigger for voice session prep** - calendar-based? Manual? Time of day?
2. **BD Scanner frequency** - weekly? Or also triggered by new call notes?
3. **Question generation** - how opinionated should the agent be? Neutral prompts vs. recommendations?
4. **Team visibility** - should any outputs be shareable with team, or purely personal?
5. **MSFT Graph auth model** - delegated (requires user session) vs. application (runs in background)?
6. **Email filtering** - which folders to scan? How to handle high-volume threads?
7. **Transcript attribution** - how to identify speakers in Teams transcripts reliably?
8. **Daily intelligence timing** - what time should it run? Before you wake up? On-demand?
9. **Staleness thresholds** - how many days before a task is "stale"? Relationship "cold"?
10. **Commitment detection** - how aggressive should parsing be for "I will..." statements?
11. **Meeting bot visibility** - is a visible bot participant acceptable? Compliance requirements?
12. **Transcript service** - build custom vs. use existing (Otter/Fireflies/Fathom)?

---

## Changelog

- 2026-02-06: Added all 6 agent specs to .claude/agents/
- 2026-02-06: Added Architecture section (skills vs agents, trigger mechanism)
- 2026-02-06: Added all 9 skill specs to .claude/commands/
- 2026-02-06: Added Meeting Bot strategy, Mail.Send, Calendar.ReadWrite; Calendar Prep feeds into Daily Intelligence
- 2026-02-06: Restructured Daily Intelligence by transaction + BD section
- 2026-02-06: Added MSFT Graph API integration section (email, Teams transcripts, calendar)
- 2026-02-06: Initial draft from brainstorm session
