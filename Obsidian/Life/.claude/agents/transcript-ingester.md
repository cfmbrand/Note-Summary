# Transcript Ingester Agent

Automatically ingest Teams call transcripts, save as Call Notes, and trigger processing.

## Schedule

- **Primary:** Every 30 minutes during work hours (9am-7pm)
- **On-demand:** User can invoke after specific meeting

## Trigger

```bash
claude --agent transcript-ingester
```

## Dependency

**Requires:** One of the following:
1. Microsoft Graph API (OnlineMeetings.Read) - native Teams transcripts
2. Meeting Bot integration - third-party transcription service
3. Manual upload with auto-detection

**Status:** Blocked until 365 auth resolved or Meeting Bot configured

## Purpose

Convert meeting transcripts into structured Call Notes and trigger the processing pipeline:
1. Detect new transcripts available
2. Format as Call Notes template
3. Save to vault
4. Invoke `process-call-notes` skill
5. Log completion

## Processing Steps

### 1. Check for New Transcripts

**Option A: MSFT Graph (if transcription enabled)**
```
GET /me/onlineMeetings
  ?$filter=endDateTime ge {last_check}
  &$expand=transcripts
```

**Option B: Meeting Bot webhook**
- Receive POST notification when transcript ready
- Download from bot's API

**Option C: Watch folder**
- Monitor designated folder for new transcript files
- Process any new .vtt, .txt, or .docx files

### 2. Match Transcript to Meeting

For each new transcript:
- Extract meeting subject/title
- Extract attendees (from transcript or calendar)
- Extract meeting date/time
- Match to calendar event if possible

### 3. Parse Transcript Content

**Input formats supported:**
- VTT (WebVTT subtitle format)
- SRT (SubRip subtitle format)
- Plain text with speaker labels
- DOCX with speaker identification

**Extract:**
- Speaker-attributed text
- Timestamps (if available)
- Duration

### 4. Identify Speakers

Map transcript speaker labels to actual people:

```
For each unique speaker in transcript:
  1. If "You" or user's name → mark as self
  2. Match speaker name to calendar attendees
  3. Match to RME Key Contacts if possible
  4. Flag unidentified speakers
```

Create speaker key:
```
Speaker Key:
- Speaker 1: You
- Speaker 2: Lars Hansen ([[00. RME Norfund]])
- Speaker 3: Siri Olsen ([[00. RME Norfund]])
- Speaker 4: [Unidentified - internal?]
```

### 5. Generate Call Notes Structure

Transform transcript into Call Notes template:

```markdown
#### Attendees
*List attendees organised by organisation*

**Norfund** ([[00. RME Norfund]])
- Lars Hansen (Investment Director)
- Siri Olsen (Analyst)

**[Your Company]**
- [Your name]
- [Colleague if present]

#### Notes

[Cleaned transcript with speaker attribution]

**Key Discussion Points:**
1. [Extracted point 1]
2. [Extracted point 2]
3. [Extracted point 3]

**Verbatim Highlights:**
> "[Important quote]" - Lars Hansen

#### Take-Aways and Next Steps
*Tasks plugin list here*

- [ ] [Identified action item 1]
- [ ] [Identified action item 2]

---
*Transcript source: [Teams/Bot name]*
*Meeting duration: X minutes*
```

### 6. Extract Key Points (AI Processing)

Use AI to:
- Summarize main discussion topics
- Identify decisions made
- Extract action items and commitments
- Flag important quotes
- Detect intelligence signals (fund status, strategy, etc.)

### 7. Save Call Notes

Generate filename:
```
Call Notes YYYY-MM-DD [Subject].md
```

If multiple calls same day:
```
Call Notes YYYY-MM-DD [Subject] (2).md
```

Save to `Work/` folder.

### 8. Invoke Processing Skill

Automatically invoke `process-call-notes` skill:
```bash
claude /process-call-notes "Work/Call Notes YYYY-MM-DD [Subject].md"
```

This will:
- Update relevant RMEs
- Update relevant DCNs
- Validate/create tasks

### 9. Log Completion

```markdown
# Transcript Ingestion Log

## YYYY-MM-DD HH:MM

**Meeting:** Call with Norfund re: CBE Equity
**Duration:** 45 minutes
**Attendees:** 4 (2 external, 2 internal)

**Output:** [[Call Notes 2026-02-06 Norfund CBE Equity]]

**Processing:**
- RMEs updated: [[00. RME Norfund]]
- DCNs updated: [[0. DCN CBE Equity]]
- Action items extracted: 3

**Status:** Complete
```

Save log to:
```
.claude/logs/transcript-ingestion.md
```

## Transcript Cleaning

Before processing, clean transcript:
- Remove filler words (um, uh, like)
- Fix obvious transcription errors
- Consolidate speaker turns (don't split every sentence)
- Remove system messages ("X joined the meeting")
- Redact if sensitive markers present

## Quality Thresholds

| Issue | Handling |
|-------|----------|
| Short transcript (<5 min) | Skip or flag for review |
| Low confidence (many [inaudible]) | Flag for manual cleanup |
| No external attendees | Skip (internal meeting) |
| Duplicate detected | Skip, note in log |

## Skills Invoked

- `process-call-notes` - always invoked after ingestion
- `create-rme` - if new attendees detected
- `update-rme` - via process-call-notes
- `update-dcn` - via process-call-notes

## Error Handling

| Issue | Handling |
|-------|----------|
| Transcript not available | Retry next cycle (up to 4 hours post-meeting) |
| Speaker identification fails | Save with generic labels, flag for review |
| Processing fails | Save raw Call Notes, skip auto-processing |
| Duplicate meeting | Skip ingestion |

## Meeting Bot Integration

If using external meeting bot (Otter, Fireflies, Fathom):

**Webhook setup:**
- Configure bot to POST to webhook when transcript ready
- Include meeting metadata and transcript URL

**API integration:**
- Authenticate with bot service
- Download transcript via API
- Map bot's speaker IDs to attendees

## State Persistence

Track processed meetings:
```
.claude/state/transcript-ingester-state.json
{
  "last_check": "2026-02-06T16:30:00Z",
  "processed_meetings": [
    {"id": "xxx", "date": "2026-02-06", "subject": "Norfund call"}
  ]
}
```

## Future Enhancements

- Real-time transcription during call
- Automatic meeting scheduling for follow-ups
- Sentiment analysis on counterparty tone
- Key quote extraction and tagging
- Multi-language support
