# session-ctx: Quick Reference

## What is it?

Context persistence for AI coding sessions. Stops agents from forgetting everything between chats.

## The Problem

Every new AI session starts from zero. You waste time re-explaining decisions, patterns, what you were working on. The code persists but the context doesn't.

## The Fix

Auto-maintained `.session-ctx.json` file that tracks decisions, file purposes, patterns, and progress. AI reads it on start, updates it as you work.

## Quick Start

Tell your AI agent:
```
Use session-ctx system. Check for .session-ctx.json in repo root.
If exists: read to understand context. If not: create it.
Update throughout session. Use token-efficient format.
```

Next session:
```
Continue from .session-ctx.json
```

Done.

## File Format (AI manages this)
```json
{
  "sessions": [{
    "goal": "implement_auth",
    "state": "in_progress",
    "decisions": [
      {"what": "jwt", "why": "stateless", "alt": ["session"], "impact": ["auth.ts"]}
    ],
    "files": {
      "auth.ts": {"action": "created", "role": "jwt_logic", "deps": ["jsonwebtoken"]}
    },
    "next": ["add_refresh", "tests"]
  }]
}
```

## What Gets Tracked

- Decisions: What you chose and why
- Files: Purpose, deps, status
- Patterns: Coding conventions
- Blockers: Issues hit
- Next steps: TODOs
- State: Done/in-progress/blocked

## Before vs After

| Before | After |
|--------|-------|
| "Let me explain the architecture..." (5 min) | Reads context (10 sec) |
| No decision history | Full rationale logged |
| Inconsistent patterns | Follows established conventions |
| "What were we doing?" | "Continuing step 3..." |

## Git

```bash
# Commit it (team projects)
git add .session-ctx.json

# Ignore it (personal)
echo ".session-ctx.json" >> .gitignore

# Archive when big
mv .session-ctx.json .archive-jan2024.json
```

## Examples

In `examples/`:
- 01_initial_session.json - First session
- 02_multi_session.json - Continued work
- 03_bugfix_session.json - Bug fix

## Docs

- README.md - Full guide
- USAGE.md - How to use
- OVERVIEW.md - Visual explanation
- prompts/AGENT_PROMPT.md - Complete AI instructions
- prompts/QUICK_START.md - Quick AI reference

## Helper Script (optional)

```bash
python session_ctx_manager.py init "feature_goal"
python session_ctx_manager.py summary
python session_ctx_manager.py end
```

## Key Ideas

1. Optimized for AI parsing, not humans
2. Token-efficient (abbreviated keys, no whitespace)
3. Zero user maintenance
4. Updates as you work, not end-of-session
5. Preserves context across sessions

## When to Use

Good for:
- Multi-session projects
- Team development
- Switching between different AI tools
- Complex refactoring

Not for:
- Single-session tasks
- Human documentation (use ADRs instead)

## How It Works

```
Session 1: Agent creates context while working
         ↓
    .session-ctx.json
         ↓
Session 2: Agent reads and continues seamlessly
```

Result: AI that remembers what you were doing.

## Token Savings

Optimized format saves ~40% tokens vs pretty JSON.

For 100 context reads:
- GPT-4: Save $3
- Claude: Save $0.90

See `experimental/` for benchmarks.

---

MIT License - use it however you want. Made because re-explaining context every session got old.
