# Weekly BD Briefing

Generate a business development-focused weekly summary surfacing opportunities, signals, and relationship maintenance needs.

## Usage

Invoke manually, typically end of week or Monday morning:
- `/weekly-bd-briefing`

Or schedule to run automatically.

## Steps

### 1. Gather All RMEs

Search for RMEs:
```
Glob: Work/00. RME*.md
```

For each RME, extract:
- Entity name and type
- Last interaction date (from Interaction Log)
- Current deal involvement (from Current Status)
- Intelligence section content
- Investment criteria

### 2. Categorize Relationships

Sort RMEs into categories:

**Active Deal Relationships:**
- RMEs with deal involvement in active DCNs
- Track last interaction date

**Warm Relationships (BD):**
- RMEs with recent interaction (<8 weeks) but no active deal
- Potential for future deals

**Cold Relationships:**
- RMEs with no interaction in >8 weeks
- Previously engaged but gone quiet

**New This Week:**
- RMEs created in last 7 days

### 3. Scan for New Intelligence

Read Intelligence sections added this week:
- Look for date-prefixed entries from last 7 days
- Or scan recent call notes for intelligence updates

Categorize intelligence by type:
- **Appetite signals**: "Looking for...", "Interested in..."
- **Mandate changes**: "New fund...", "Shifted focus..."
- **Personnel**: "New hire...", "Departure..."
- **Market views**: Opinions on sectors, geographies
- **Fundraise status**: "Fund III closing...", "Deploying..."

### 4. Identify Connection Opportunities

Cross-reference intelligence across RMEs:

**Pattern matching:**
- Investor A "looking for solar in Kenya" + Investor B "has Kenya solar portfolio" = potential intro?
- Investor A "needs co-investor for $100m ticket" + Investor B "targets $30-50m co-investments" = match?
- Client A "seeking debt" + Lender B "expanding Africa exposure" = opportunity?

**Deal sourcing signals:**
- RME mentions considering a sale/raise
- RME mentions portfolio company needing capital
- RME asks about market conditions for a transaction

Flag these as potential BD opportunities.

### 5. Identify Stale Relationships

Flag relationships that need attention:

**Active deal, going cold:**
- RME is counterparty on active DCN
- Last interaction >2 weeks ago
- Critical: May lose deal momentum

**Warm relationship, going cold:**
- Previously engaged (interaction in last 6 months)
- No interaction in >4 weeks
- Risk: Relationship atrophies

**Key relationships to maintain:**
- High-value counterparties (SWFs, major DFIs)
- Strong deal track record
- No interaction in >6 weeks

### 6. Identify Market Themes

Aggregate intelligence to spot patterns:

**What are people talking about?**
- Sectors mentioned frequently
- Geographies of interest
- Concerns (pricing, risk, etc.)
- Structural preferences

**Market sentiment:**
- Bullish/bearish indicators
- Deal flow observations
- Competitive intelligence

### 7. Generate Opportunities List

Compile BD opportunities:

```markdown
## BD Opportunities

### High Priority
1. **CIP mentioned SA platform interest** (Call 2026-02-03)
   - They're actively looking for a platform in South Africa
   - Action: Discuss with [colleague] about relevant opportunities
   - RME: [[00. RME CIP]]

2. **ADIA battery storage appetite** (Call 2026-02-01)
   - Mentioned expanding into battery storage across Africa
   - Potential match with Eranove storage project?
   - RME: [[00. RME ADIA]]

### To Explore
3. **Meridiam new fund**
   - Fund IV launching, larger tickets than before
   - Worth a catch-up call to understand mandate
   - RME: [[00. RME Meridiam]]

### Connections to Consider
4. **Norfund seeking co-investors + Actis deployable capital**
   - Norfund mentioned needing co-investors for larger deals
   - Actis mentioned having capital to deploy
   - Potential intro?
```

### 8. Generate Discussion Questions

3-5 questions for voice discussion:

**Question types:**

| Trigger | Example Question |
|---------|------------------|
| Appetite signal | "CIP is looking for SA platform - anything in our pipeline or network?" |
| Connection opportunity | "Should we introduce Norfund to Actis for co-investment?" |
| Stale relationship | "Haven't spoken to [key RME] in 6 weeks - worth a check-in?" |
| Market theme | "Multiple investors mentioned battery storage - do we have a view on this space?" |
| New intelligence | "[RME] is raising Fund IV - should we get a meeting?" |

### 9. Compile Briefing

Structure the full briefing:

```markdown
# Weekly BD Briefing
**Week of:** [Date]
**Generated:** [Timestamp]

## Summary

- **New intelligence this week:** X items captured
- **Stale relationships:** Y need attention
- **Opportunities identified:** Z

## Relationship Health

| Category | Count | Action Needed |
|----------|-------|---------------|
| Active deal relationships | 12 | 2 going cold |
| Warm relationships | 8 | 3 need touch |
| Cold relationships | 15 | Review for reactivation |
| New this week | 2 | - |

### Relationships Needing Attention

| RME | Last Contact | Context | Suggested Action |
|-----|--------------|---------|------------------|
| [[00. RME Actis]] | 6 weeks | Previously warm | Schedule catch-up |
| [[00. RME GreenCo]] | 3 weeks | Active on Kamoa | Check in on DD status |

## New Intelligence This Week

### Appetite Signals
- **[[00. RME CIP]]**: Looking for SA platform
- **[[00. RME ADIA]]**: Battery storage interest

### Mandate/Strategy Changes
- **[[00. RME Meridiam]]**: Fund IV launching, larger tickets

### Personnel
- **[[00. RME Norfund]]**: New Principal joining renewables team

### Market Views
- Several investors cautious on Nigeria FX
- Battery storage emerging as theme

## BD Opportunities

[As above]

## Market Themes

- Battery storage: Mentioned by 3 investors this month
- South Africa: Renewed interest after policy clarity
- Nigeria caution: FX concerns cited by 2 investors

## Questions for Discussion

1. CIP mentioned SA platform interest - worth a call with [colleague] about options?
2. ADIA expanding into battery storage - do we have any relevant deals?
3. Actis hasn't been in touch in 6 weeks - should we schedule a catch-up?
4. Seeing battery storage interest from multiple parties - should we proactively source?
5. Fund IV at Meridiam - worth getting a meeting to understand new mandate?

---
*Generated by weekly-bd-briefing*
```

### 10. Save Briefing

Save to:
```
Work/Weekly Reviews/BD Briefing YYYY-MM-DD.md
```

Or inject into Weekly Review as BD section.

### 11. Report Summary

```
Generated Weekly BD Briefing:
- 35 relationships analyzed
- 5 stale relationships flagged
- 3 BD opportunities identified
- 2 potential connections to explore
- 5 discussion questions generated

Saved to: [[BD Briefing 2026-02-07]]
```

## Intelligence Categories

| Category | What to capture |
|----------|-----------------|
| **Appetite signals** | What they want to invest in |
| **Mandate changes** | New funds, strategy shifts |
| **Personnel** | Key hires, departures, promotions |
| **Market views** | Their take on sectors/geographies |
| **Fund status** | Fundraising, deployment, lifecycle |
| **Competitive intel** | What they're seeing from others |

## Companion Skills

- `weekly-deals-briefing`: Companion briefing for active deals
- `daily-intelligence`: Daily version with task focus
- `create-rme`: Capture new relationships
- `update-rme`: Update intelligence and interactions

## Future Enhancements (365 Integration)

When MSFT Graph is available:
- Scan emails for intelligence signals
- Track email frequency per relationship
- Identify contacts we've emailed but no RME exists
- Suggest contacts for reactivation based on email history
- Calendar integration for scheduling suggested catch-ups
