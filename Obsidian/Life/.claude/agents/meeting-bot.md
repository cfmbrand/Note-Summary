# Meeting Bot Agent

A bot that joins calls as a participant to record and transcribe meetings reliably.

## Schedule

- **Trigger:** Joins scheduled meetings automatically
- **Timing:** Joins 1-2 minutes after meeting start
- **Duration:** Stays until meeting ends or host removes

## Trigger

Bot joins based on calendar events:
```bash
# Checks calendar, joins qualifying meetings
claude --agent meeting-bot --mode monitor
```

## Dependency

**Requires:** One of:
1. Custom Azure Bot Service + Speech-to-Text (build)
2. Third-party service integration (Otter.ai, Fireflies.ai, Fathom) (buy)
3. Teams native transcription (if available and reliable)

**Status:** Architecture decision needed

## Purpose

Solves the transcript reliability problem:
- Native Teams transcription may not be enabled
- External calls (non-Teams) need coverage
- Consistent format across all calls
- No reliance on meeting organizer settings

## Architecture Options

### Option A: Third-Party Service (Recommended to Start)

Use existing service like Otter, Fireflies, or Fathom:

**Flow:**
```
┌──────────────┐     ┌─────────────────┐     ┌──────────────┐
│  Calendar    │────►│  Bot Service    │────►│  Transcript  │
│  (Graph API) │     │  (Otter/etc)    │     │  Ingester    │
└──────────────┘     └─────────────────┘     └──────────────┘
```

**Pros:**
- Quick to deploy
- Proven transcription quality
- Speaker identification built-in
- Existing integrations

**Cons:**
- Monthly cost
- Data goes through third party
- Less customization

**Integration:**
1. Connect service to calendar
2. Configure which meetings to join
3. Set up webhook to notify when transcript ready
4. Transcript Ingester pulls and processes

### Option B: Custom Azure Bot (Future)

Build custom bot using Azure services:

**Components:**
- Azure Bot Service (Teams integration)
- Azure Communication Services (joining calls)
- Azure Speech-to-Text (transcription)
- Custom logic for speaker identification

**Pros:**
- Full control
- Data stays in your tenant
- Customizable behavior

**Cons:**
- Significant development effort
- Ongoing maintenance
- Higher complexity

## Meeting Selection Logic

Not all meetings should have the bot:

**Include:**
- External attendees present (investor calls, client calls)
- Subject contains deal names or "call with [RME name]"
- Explicitly flagged meetings
- Recurring deal review meetings

**Exclude:**
- Internal-only meetings (optional)
- 1:1s with direct reports
- Sensitive/confidential meetings
- Short meetings (<15 min)
- Social/informal meetings

**Configuration:**
```yaml
meeting_bot:
  include_patterns:
    - "*investor*"
    - "*call with*"
    - "CBE*"
    - "Trafigura*"
  exclude_patterns:
    - "*1:1*"
    - "*internal*"
    - "*confidential*"
  min_duration_minutes: 15
  external_attendees_required: true
```

## Bot Behavior

### Joining

- Join 1-2 minutes after scheduled start (not at exact time)
- Identify as "Meeting Notes Bot" or similar
- Request permission if Teams requires it
- Announce presence (or stay silent based on config)

### During Meeting

- Record audio stream
- Real-time transcription (if supported)
- Track speakers
- Note meeting duration

### Leaving

- Leave when meeting ends
- Or leave after X minutes of silence
- Or when host removes bot

### Post-Meeting

- Process final transcript
- Identify speakers with calendar attendee list
- Send to Transcript Ingester pipeline
- Notify that transcript is ready

## Consent & Compliance

**Important considerations:**

1. **Recording consent:** Many jurisdictions require consent to record
   - Bot should announce it's recording
   - Or meeting invite should note recording

2. **Data handling:**
   - Where is audio/transcript stored?
   - Retention period
   - Access controls

3. **Corporate policy:**
   - Check with IT/Legal about recording policies
   - External parties may have restrictions

**Consent patterns:**
- Bot name clearly indicates recording ("Notes Bot")
- Announcement on join: "This meeting is being recorded for notes"
- Calendar invite includes recording notice

## Integration with Pipeline

```
Meeting Bot
    │
    ▼
┌─────────────────────────────┐
│  Transcript available        │
│  (webhook or polling)        │
└─────────────┬───────────────┘
              │
              ▼
┌─────────────────────────────┐
│  Transcript Ingester Agent  │
│  - Download transcript       │
│  - Format as Call Notes      │
│  - Save to vault            │
└─────────────┬───────────────┘
              │
              ▼
┌─────────────────────────────┐
│  process-call-notes Skill   │
│  - Update RMEs              │
│  - Update DCNs              │
│  - Extract action items     │
└─────────────────────────────┘
```

## Configuration

Store in `.claude/config/meeting-bot.yaml`:

```yaml
meeting_bot:
  enabled: true
  service: "fireflies"  # or "otter", "fathom", "custom"

  # Service-specific settings
  fireflies:
    api_key: "${FIREFLIES_API_KEY}"
    webhook_url: "https://..."

  # Meeting selection
  selection:
    external_required: true
    min_duration: 15
    include_patterns:
      - "*CBE*"
      - "*investor*"
    exclude_patterns:
      - "*internal*"
      - "*1:1*"

  # Behavior
  behavior:
    join_delay_seconds: 90
    announce_on_join: true
    leave_on_silence_minutes: 5

  # Consent
  consent:
    add_calendar_notice: true
    announce_recording: true
```

## Third-Party Service Comparison

| Service | Pricing | Quality | Integration |
|---------|---------|---------|-------------|
| **Otter.ai** | $20/mo | Good | Calendar, Zoom, Teams |
| **Fireflies.ai** | $19/mo | Good | Calendar, most platforms |
| **Fathom** | Free tier | Good | Zoom focus, Teams beta |
| **Grain** | $19/mo | Good | Video focus |

Recommendation: Start with **Fireflies** for broad platform support and good API.

## Implementation Steps

1. **Choose service** and sign up
2. **Connect calendar** for auto-join
3. **Configure meeting selection** rules
4. **Set up webhook** for transcript notifications
5. **Test with internal meeting** first
6. **Configure Transcript Ingester** to receive from service
7. **Roll out gradually** to external meetings

## Future Enhancements

- Custom bot with full control
- Real-time note-taking during call
- Live action item detection
- Automatic meeting summary email
- Integration with meeting follow-up scheduling
