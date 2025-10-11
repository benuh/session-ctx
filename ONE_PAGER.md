# Quick Reference

Context persistence for AI coding sessions.

## Problem

AI agents start from zero every session. You waste time re-explaining everything.

## Fix

`.session-ctx.json` file tracks decisions, files, patterns, progress. Agent reads it at start, updates as you work.

## Quick Start

Tell your agent:
```
Use session-ctx. Check for .session-ctx.json - read if exists, create if not. Update throughout session.
```

Next time:
```
Continue from context
```

## What Gets Tracked

- Decisions and reasoning
- File purposes and dependencies
- Coding patterns
- Blockers
- Next steps

Example format:
```json
{
  "sessions": [{
    "goal": "implement_auth",
    "decisions": [{"what": "jwt", "why": "stateless"}],
    "files": {"auth.ts": {"role": "jwt_logic"}},
    "next": ["add_refresh", "tests"]
  }]
}
```

## Impact

```
BEFORE:                      AFTER:
├─ 5 min explaining    →    ├─ 10 sec context load
├─ No history          →    ├─ Full history
├─ Inconsistent        →    ├─ Consistent patterns
└─ Start from scratch  →    └─ Pick up where left off
```

## Git

Commit it for team projects, ignore for personal work.

Archive old sessions if file gets big:
```bash
mv .session-ctx.json .archive-2024.json
```

## Files

- `README.md` - Main guide
- `USAGE.md` - Usage guide
- `prompts/` - AI agent instructions
- `examples/` - Sample files

## Key Points

- Optimized for AI, not humans
- Token-efficient format
- Zero user maintenance
- Updates throughout session
- Works across different AI agents

## When to Use

Good for: Multi-session projects, teams, complex work
Skip for: One-off scripts, single sessions

## Token Savings

Saves ~40% tokens vs standard JSON.

100 context reads: Save $3 (GPT-4), $0.90 (Claude)

See `experimental/` for details.

---

MIT License - use it however you want. Made because re-explaining context every session got old.
