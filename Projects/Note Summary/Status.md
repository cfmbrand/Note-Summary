# Note Summary - Project Status

## Current State
- **Branch**: `main`
- **Repository**: https://github.com/cfmbrand/Note-Summary.git
- **Tests**: All 59 unit tests passing (`pytest tests/ -v`)
- **Pipeline**: End-to-end working — email capture, OneNote page creation, duplicate prevention all verified

## Completed
- Project structure and all source modules implemented
- Authentication module (interactive browser flow, token caching with refresh)
- Email service (Inbox-only fetching via Graph API — avoids duplicate from Sent Items)
- OneNote service (page creation via Graph API, auto-creates sections)
- Email processor (subject parsing, HTML cleaning)
- Processed email tracker (SQLite duplicate prevention)
- CLI entry point with `--auth-only`, `--list-notebooks`, `--verbose`, `--daemon` flags
- Unit tests for config, email processor, processed tracker, and email service
- PRD updated with learnings (correct commands, Conditional Access notes)
- Azure AD redirect URI registered and auth flow fully working
- Tested with Cygnum General → Email Notes Test notebook/section

## Resolved Blockers
- **Azure AD Redirect URI (AADSTS900971)**: Resolved — IT registered `http://localhost` redirect URI
- **Conditional Access (Error 53003)**: Resolved — interactive browser flow satisfies CA device compliance
- **Duplicate notes per email**: Resolved — switched from `/me/messages` to `/me/mailFolders/Inbox/messages` to avoid picking up both Inbox and Sent Items copies

## Planned Features

OneNote publishing was the initial test case for the pipeline. The broader goal is to build a professional OS that curates structured context for AI agents to perform ongoing analysis on the user's professional state (daily, weekly, monthly, yearly). The following note types will be generated and maintained by Claude:

### Deal Continuity Note (DCN)
An organised summary for each active transaction. As the user is a banker, each deal has its own evolving context — parties involved, status, key dates, open items, and narrative arc. Claude will create or update a DCN per deal, keeping it current as new information flows in.

### Relationship Memory Note
A living profile for each key counterparty the user works with or interacts with. A core part of the role is making connections between people, so these notes capture relationship context — interaction history, interests, relevance to active deals, and connection potential. Claude will create or update these as counterparty interactions occur.

### Design Intent
These notes are not primarily for direct human consumption. Their purpose is to maintain curated, structured context so that downstream agents can reason about the user's current state as a professional — across deals, relationships, and time horizons.

## Next Steps
1. Set up launchd scheduled execution for automated email processing
2. Configure target notebook/section for production use (currently Cygnum General → Email Notes Test)
3. Implement Deal Continuity Notes (DCN) generation
4. Implement Relationship Memory Notes generation

## Auth Flow Change Log
- **2026-02-04**: Switched from device code flow to interactive browser flow (`src/auth/graph_auth.py`)
  - Device code flow was blocked by Conditional Access (Error 53003)
  - Interactive flow opens system browser, which satisfies CA device compliance checks
  - Requires `http://localhost` redirect URI registered in Azure app
- **2026-02-13**: Auth flow fully working — redirect URI registered by IT, consent granted
- **2026-02-14**: Fixed duplicate note creation — fetch from Inbox folder only
