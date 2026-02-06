# Voice Session Prep Agent

Load context for collaborative voice session (walk to work briefing).

## Schedule

- **Primary:** 7:00am weekdays (before commute)
- **On-demand:** User can invoke before any voice session

## Trigger

```bash
claude --agent voice-session-prep
```

## Purpose

Ensure the agent has read all relevant context before the voice conversation begins. The Daily Intelligence already contains prioritized items - this agent simply loads that context and is ready to discuss.

## Prerequisites

Before this agent runs, these should exist:
- Today's Daily Scratchpad with Daily Intelligence section
- Weekly Deals Briefing (if Monday or recent)
- Weekly BD Briefing (if Monday or recent)

If missing, agent will note gaps.

## Processing Steps

### 1. Load Daily Intelligence

Read today's Daily Scratchpad:
```
Work/Scratchpad/Daily Scratchpad YYYY-MM-DD.md
```

Ingest the Daily Intelligence section - this contains:
- Items flagged by transaction
- BD / Pipeline items
- Meetings scheduled for today

### 2. Load Weekly Briefings (if available)

Check for recent briefings:
```
Work/Weekly Reviews/Deals Briefing YYYY-MM-DD.md
Work/Weekly Reviews/BD Briefing YYYY-MM-DD.md
```

If exist and recent (within last 7 days), read and ingest:
- Discussion questions
- Key concerns
- Opportunities identified

### 3. Load Relevant RMEs and DCNs

Based on items in Daily Intelligence:
- Read linked DCN files for deal context
- Read linked RME files for relationship context

This ensures agent can speak knowledgeably about any item that comes up.

### 4. Signal Ready

Output to console:
```
Voice Session Ready

Context loaded:
- Daily Intelligence: 12 items across 5 deals
- Weekly Deals Briefing: loaded (5 questions)
- Weekly BD Briefing: loaded (4 opportunities)
- DCNs loaded: 5
- RMEs loaded: 8

Ready when you are.
```

## Voice Session Flow

1. **User starts voice conversation**
2. **Agent has full context** from Daily Intelligence and Weekly Briefings
3. **Natural discussion** - work through items, make decisions, note action items
4. **Agent captures outcomes** in real-time

## Capturing Outcomes

During/after the voice session, agent writes directly to Daily Scratchpad:

**New tasks:**
```markdown
- [ ] Follow up with Norfund on pricing #CBE_Equity 📅 2026-02-08
- [ ] Schedule call with Actis to reactivate #BD
```

**Notes:**
```markdown
#### Voice Session Notes - 2026-02-06

- Decided to hold firm on CBE Equity pricing - strong interest from others
- Will introduce ADIA to Actis for co-investment discussion
- Trafigura: give it another week before pushing
```

**Updates to flag:**
- If decision affects DCN status, note for later `update-dcn`
- If intelligence emerges, note for later `update-rme`

## Output

**No separate prep document.** All outcomes go into Daily Scratchpad.

## Skills Invoked

- Reads output from `daily-intelligence`
- Reads output from `weekly-deals-briefing` and `weekly-bd-briefing`
- May invoke `update-dcn` or `update-rme` post-session based on notes

## Future Enhancements (365 Integration)

When MSFT Graph available:
- Pull today's calendar for meeting context
- Check email for overnight updates
- Auto-send action items to team after session
- Create calendar events for follow-ups
