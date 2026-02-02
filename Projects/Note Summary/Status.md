# Note Summary - Project Status

## Current State
- **Branch**: `main` (up to date with `origin/main`)
- **Repository**: https://github.com/cfmbrand/Note-Summary.git
- **Tests**: All 49 unit tests passing (`pytest tests/ -v`)

## Completed
- Project structure and all source modules implemented
- Authentication module (MSAL device code flow)
- Email service (Outlook fetching via Graph API)
- OneNote service (page creation via Graph API)
- Email processor (subject parsing, HTML cleaning)
- Processed email tracker (SQLite duplicate prevention)
- CLI entry point with `--auth-only`, `--list-notebooks`, `--verbose`, `--daemon` flags
- Unit tests for config, email processor, and processed tracker
- PRD updated with learnings (correct commands, Conditional Access notes)

## Blocked
- **Azure AD Conditional Access (Error 53003)**: Corporate policy requires device registration or compliance. User's Mac is not registered with Azure AD/Intune.
- **Action needed**: IT must either exempt the app from device compliance requirements or register the device.

## Planned Features

OneNote publishing was the initial test case for the pipeline. The broader goal is to build a professional OS that curates structured context for AI agents to perform ongoing analysis on the user's professional state (daily, weekly, monthly, yearly). The following note types will be generated and maintained by Claude:

### Deal Continuity Note (DCN)
An organised summary for each active transaction. As the user is a banker, each deal has its own evolving context — parties involved, status, key dates, open items, and narrative arc. Claude will create or update a DCN per deal, keeping it current as new information flows in.

### Relationship Memory Note
A living profile for each key counterparty the user works with or interacts with. A core part of the role is making connections between people, so these notes capture relationship context — interaction history, interests, relevance to active deals, and connection potential. Claude will create or update these as counterparty interactions occur.

### Design Intent
These notes are not primarily for direct human consumption. Their purpose is to maintain curated, structured context so that downstream agents can reason about the user's current state as a professional — across deals, relationships, and time horizons.

## Next Steps (once unblocked)
1. Run `python -m src.main --auth-only` to authenticate via device code flow
2. Run `python -m src.main --list-notebooks` to verify OneNote access
3. Send a test email with subject `[Note] Test note` and run the script
4. Verify OneNote page creation and duplicate prevention
5. Set up launchd scheduled execution
