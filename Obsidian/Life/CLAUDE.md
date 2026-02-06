# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Vault Overview

This is an Obsidian vault for investment/business development work focused on relationship tracking, deal management, and daily task organization.

## Role Overview

The notes contained in this vault are for a Managing Director at a niche investment bank specialised in frontier markets renewable energy transactions. 

This MD has a team that typically does a lot of the underlying analytical and production (teasers, term sheets, IMs) work for me. The goal is to direct that work effectively and to understand all of the particular nuances without getting bogged down. 

A big part of the job is business development. It is critical that this vault is used to save down key information which may lead to new business; which may also come through new connections between counterparties that I am tracking. 

## Information Management Approach

Primary information is inserted into the vault mainly through Call or Interaction Notes. The intent is to manage 

## Structure

```
Life/
├── 0. Templates/           # Templater templates
├── Personal/               # Personal notes
└── Work/
    ├── Scratchpad/         # Daily scratchpads
    ├── Weekly Reviews/     # Weekly review summaries
    ├── 0. DCN *.md         # Deal/Company research files
    ├── 00. RME *.md        # Relationship/Investor research files
    ├── 01. Investor Tracking *.md  # Weekly investor tracking per deal
    └── [Meeting notes]     # Call/meeting documentation
```

**Naming conventions (MUST be followed when creating files):**
- `0. DCN [Name].md` = Deal Continuity Notes - deal/project context for agents
- `00. RME [Name].md` = Relationship Memory/Entity - investor/counterparty dossiers
- `01. Investor Tracking [Deal Name].md` = Weekly investor status tracker per transaction
- `Daily Scratchpad YYYY-MM-DD.md` in Work/Scratchpad/

## Task Format

Uses Obsidian Tasks plugin with this syntax:
```
- [ ] Task description #Tag 📅 YYYY-MM-DD
- [x] Completed task ✅ YYYY-MM-DD
- [/] In progress task
- [-] Cancelled task
```

**Priority markers:** ⏫ (high), 🔼 (medium), 🔽 (low)

**Common tags:**
- `#CBE_Equity`, `#CBE_Kamoa` - Crossboundary Energy projects that are in progress
- `#Trafigura`, `#Gridworks`, `#Eranove`, `#GreenCo` - Other projects that are in progress
- `#BD` - Business development
- `#Other` - Miscellaneous

## Templates

Templates live in `0. Templates/`. Use these as the structure when creating new notes.

| Template | Purpose | Filename Pattern |
|----------|---------|------------------|
| **DCN.md** | Deal context for agents - thesis, status, terms, stakeholders, activity log | `0. DCN [Deal Name].md` |
| **RME.md** | Investor/counterparty dossier - profile, contacts, criteria, intelligence | `00. RME [Entity Name].md` |
| **Investor Tracking.md** | Week-over-week investor status per transaction - positioning, next actions | `01. Investor Tracking [Deal Name].md` |
| **Daily Notes.md** | Daily scratchpad with task queries and notes (uses Templater) | `Daily Scratchpad YYYY-MM-DD.md` |
| **Weekly Review.md** | Weekly summary pulling from daily scratchpads, by project (uses Templater) | `Weekly Review YYYY-MM-DD.md` |
| **Call or Interaction Notes.md** | Meeting documentation (uses Templater) | `Call Notes YYYY-MM-DD.md` |

**DCN Phases:** Preparation → Teaser and Initial Discussions → NBO/Term Sheet → Mandate/Binding Offer → Legal Execution

**RME Entity Types:** SWF, DFI, PE, Corporate/Strategic, Bank, Credit Fund (can have multiple)

## Information Flow

**Source data:** Daily Scratchpads, Call Notes, and other imported notes

**Derived documents:** RMEs, DCNs, Investor Tracking - populated from source data

**Feedback loop:** RMEs and DCNs provide critical context for interpreting new daily scratchpads and notes

When processing new notes:
- Update relevant RME Interaction Logs and DCN Activity Logs with summary narratives
- Cross-reference intelligence across RMEs (e.g., if ADIA mentions their view on CIP, note it in both RMEs)
- Detail lives in the source notes; summaries in RMEs/DCNs
- Investor Tracking aggregates weekly status and links to both DCN and relevant RMEs

**DCNs are primarily context for agents** - write them to be scannable and provide enough background that an agent can get up to speed quickly without ambiguity.

**RME Intelligence sections** should capture: org dynamics, decision-making process, what matters to them, recent promotions, strategy shifts, fundraise status, fund lifecycle position.

## Linking Conventions

- Use wikilinks: `[[Note Title]]`
- Meeting notes should link to relevant RME/DCN files at the top
- Example: `[[00. RME Investor Name]]` and `[[0. DCN Deal Name]]`
- Investor Tracking tables should wikilink to each RME in the Investor column

## Headers

- `####` (H4) for main sections
- `#####` (H5) for subsections
