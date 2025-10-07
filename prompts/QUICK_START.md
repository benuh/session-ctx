# Quick Start for AI Agents

## Copy This Prompt

```
I'm using the session-ctx system to maintain context across sessions.

1. Check if .session-ctx.json exists in this repo root
2. If yes: Read it to understand previous work, decisions, and next steps
3. If no: Create it using the base template

Throughout our session, update .session-ctx.json after:
- File creates/edits
- Architecture decisions
- Installing dependencies
- Encountering blockers
- Completing tasks

Use this format: https://github.com/[username]/session-ctx/blob/main/prompts/AGENT_PROMPT.md

Keep updates token-efficient with abbreviated keys and structured data.
```

## Implementation Steps

### Step 1: Session Start
```python
# Check for existing context
if ".session-ctx.json" exists:
    context = read_json(".session-ctx.json")
    current_session = context["sessions"][-1]  # Get latest
    understand_previous_work(current_session)
else:
    create_initial_context()
```

### Step 2: Create Initial Context
```json
{
  "v": "1.0",
  "project": "<detect from cwd>",
  "created": "<now>",
  "updated": "<now>",
  "sessions": [
    {
      "id": "s1",
      "start": "<now>",
      "end": null,
      "goal": "<user's stated goal>",
      "state": "in_progress",
      "decisions": [],
      "files": {},
      "patterns": {},
      "blockers": [],
      "next": [],
      "kv": {}
    }
  ]
}
```

### Step 3: Update Throughout Session

**After making a decision:**
```json
{
  "decisions": [{
    "id": "d1",
    "what": "use_redis_cache",
    "why": "fast_in_memory_simple_api",
    "alt": ["memcached", "in_process"],
    "impact": ["src/cache.ts", "docker-compose.yml"]
  }]
}
```

**After modifying a file:**
```json
{
  "files": {
    "src/cache.ts": {
      "action": "created",
      "role": "redis_cache_wrapper",
      "deps": ["redis"],
      "status": "complete"
    }
  }
}
```

**When blocked:**
```json
{
  "blockers": [{
    "id": "b1",
    "desc": "redis_connection_timeout",
    "status": "open"
  }]
}
```

**Setting next steps:**
```json
{
  "next": ["fix_redis_timeout", "add_cache_tests", "update_docs"]
}
```

### Step 4: Session End
```json
{
  "end": "<now>",
  "state": "completed"  // or "blocked", "in_progress"
}
```

## Token Efficiency Tips

1. **Use abbreviations**: `desc` not `description`, `alt` not `alternatives`
2. **Avoid prose**: `"why": "fast_reliable"` not `"why": "We chose this because it's fast and reliable"`
3. **Structured over freeform**: Use arrays and objects, not paragraphs
4. **Minimal redundancy**: Don't repeat info available in code/git

## Example Update Flow

```
User: "Add authentication using JWT"

Agent Internal Process:
1. Read current .session-ctx.json
2. Find or create current session
3. Add decision:
   - what: jwt_auth
   - why: stateless_scalable
   - alt: [session_based]
   - impact: [src/auth.ts, src/middleware/auth.ts]
4. Create src/auth.ts
5. Update files section:
   - src/auth.ts: {action: created, role: jwt_logic, ...}
6. Set next steps: [add_refresh_tokens, write_tests]
7. Save .session-ctx.json
```

## Usage with Helper Script

Optionally use `session_ctx_manager.py`:

```bash
# Start session
python session_ctx_manager.py init "implement_auth"

# Add decision
python session_ctx_manager.py decision "jwt_auth" "stateless"

# Update file
python session_ctx_manager.py file "src/auth.ts" "created" "jwt_logic"

# Set next steps
python session_ctx_manager.py next "add_refresh" "write_tests"

# End session
python session_ctx_manager.py end "completed"
```

## Remember

- Update incrementally, not just at session end
- Keep one session "in_progress" at a time
- New sessions read context to continue work seamlessly
- This is for agent parsing - optimize for tokens, not human reading
