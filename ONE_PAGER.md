# session-ctx: One Page Reference

## What It Is
Token-efficient context persistence for AI coding agents across sessions.

## The Problem
❌ AI agents forget context between sessions
❌ You re-explain decisions every time
❌ Inconsistent patterns across sessions
❌ Wasted time re-discovering code

## The Solution
✅ Auto-maintained `.session-ctx.json` in repo root
✅ Agent reads on start, updates throughout
✅ Zero user maintenance
✅ Seamless continuity

## Quick Start

### Give Agent This Prompt (Once):
```
Use session-ctx system. Check for .session-ctx.json in repo root.
If exists: read to understand context. If not: create it.
Update throughout session after file changes, decisions, blockers.
Use token-efficient format with abbreviated keys.
```

### Next Session:
```
Continue from .session-ctx.json
```

Done! Agent handles everything.

## File Format (Agent Manages)
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
    "patterns": {"auth_flow": "jwt->cookie->verify"},
    "next": ["add_refresh_token", "write_tests"]
  }]
}
```

## What Gets Tracked
- **Decisions**: What you chose & why
- **Files**: Purpose, dependencies, status
- **Patterns**: Coding conventions
- **Blockers**: Issues encountered
- **Next steps**: What's pending
- **State**: What's done/in-progress

## Benefits
| Before | After |
|--------|-------|
| Re-explain context (5 min) | Instant load (10 sec) |
| No decision history | Full rationale logged |
| Inconsistent patterns | Enforced conventions |
| "What were we doing?" | "Continuing step 3..." |

## Git Usage
```bash
# Option 1: Commit it (team projects)
git add .session-ctx.json

# Option 2: Ignore it (personal)
echo ".session-ctx.json" >> .gitignore

# Option 3: Archive periodically
mv .session-ctx.json .archive-2025-10.json
```

## Examples
📁 `examples/01_initial_session.json` - First session
📁 `examples/02_multi_session.json` - Continued work
📁 `examples/03_bugfix_session.json` - Bug fix

## Full Docs
📖 `README.md` - Complete guide
📖 `USAGE.md` - User workflow
📖 `OVERVIEW.md` - Visual explanation
📖 `prompts/AGENT_PROMPT.md` - Full agent instructions
📖 `prompts/QUICK_START.md` - Agent quick reference

## Helper Script (Optional)
```bash
python session_ctx_manager.py init "feature_goal"
python session_ctx_manager.py summary
python session_ctx_manager.py end
```

## Key Principles
1. **Agent-first**: Optimized for LLM parsing
2. **Token-efficient**: Abbreviated keys, no prose
3. **Zero maintenance**: Agent handles everything
4. **Incremental**: Updates as you work
5. **Stateful**: Preserves context across sessions

## Use Cases
✅ Multi-session projects
✅ Team development
✅ Agent switching
✅ Complex refactoring

❌ Single-session tasks
❌ Human documentation (use ADRs)

## The Magic
```
Session 1: Agent creates context while working
         ↓
    .session-ctx.json (persists)
         ↓
Session 2: Agent reads & continues seamlessly
```

**Result**: Stateful AI collaboration 🎉

---
**MIT License** • Adapt freely • Built for efficiency
