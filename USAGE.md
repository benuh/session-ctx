# How to Use session-ctx

## For Users (You)

### First Time Setup

1. **Copy the agent prompt** from `prompts/QUICK_START.md`
2. **Start your AI coding session** with this instruction:

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

Use token-efficient format with abbreviated keys and structured data.
```

3. **Work normally** - The agent will handle everything automatically

### Subsequent Sessions

Just start with:
```
Continue from where we left off using .session-ctx.json
```

The agent will:
- Read the context file
- Understand previous decisions
- Continue with the next steps
- Keep updating the context

### That's It!

You never touch `.session-ctx.json` manually. The agent manages it completely.

## What the Agent Does

### On First Use
1. Creates `.session-ctx.json` in your repo root
2. Initializes with project info
3. Starts tracking the first session

### Throughout the Session
Automatically updates the file when:
- You create/modify files → Logs file changes
- Make tech choices → Records decisions with rationale
- Install packages → Tracks dependencies
- Hit blockers → Documents issues
- Complete tasks → Updates state

### On New Session
1. Reads `.session-ctx.json`
2. Reviews previous sessions
3. Understands context instantly
4. Continues work seamlessly

## Real-World Example

### Session 1: Initial Development
```
You: "Build a REST API with user authentication"

Agent:
- Creates .session-ctx.json
- Logs decision: "express_framework" (why: lightweight)
- Creates files: server.ts, auth.ts
- Updates context with file purposes
- Sets next steps: [implement_jwt, add_middleware]
```

### Session 2: Continue Next Day
```
You: "Continue from yesterday"

Agent:
- Reads .session-ctx.json
- Sees: "Next: implement_jwt, add_middleware"
- Understands: Express chosen for lightweight API
- Continues: Implements JWT from next steps
- Updates: Marks JWT done, adds new next steps
```

### Session 3: Bug Fix
```
You: "Fix the auth bug"

Agent:
- Reads context
- Knows: JWT implementation in auth.ts
- Understands: Auth flow pattern from context
- Fixes: Bug in JWT verification
- Logs: Decision and fix in context
```

## Benefits You'll Notice

1. **No Re-explaining**
   - ❌ Before: "Remember we're using Express with JWT..."
   - ✅ After: "Continue where we left off"

2. **Consistent Decisions**
   - Context remembers WHY choices were made
   - Future work follows established patterns

3. **Better Continuity**
   - Agent knows what's done, in-progress, blocked
   - Picks up exactly where you left off

4. **Cross-Agent Compatibility**
   - Switch between different AI tools
   - All read the same context file

## Optional: Review Context

If you want to see what's been tracked:

```bash
# View the file
cat .session-ctx.json

# Or use the helper script
python session_ctx_manager.py summary
```

But you typically never need to look at it!

## Git Considerations

### Option 1: Commit It (Recommended for teams)
```bash
git add .session-ctx.json
git commit -m "Update session context"
```

**Pros:**
- Team members' agents can see project history
- Shared understanding across developers
- Context survives repo clones

**Cons:**
- File can grow large over time
- Contains detailed implementation notes

### Option 2: Ignore It (For personal projects)
```bash
echo ".session-ctx.json" >> .gitignore
```

**Pros:**
- Keeps repo cleaner
- Private work history

**Cons:**
- Lose context on new clones
- No shared context with team

### Option 3: Periodic Cleanup
```bash
# Archive old sessions
mv .session-ctx.json .session-ctx-archive-2025-10.json

# Agent creates fresh file
# But you can still reference the archive if needed
```

## Troubleshooting

**Q: Agent isn't updating the context**
A: Remind it: "Update .session-ctx.json with this decision"

**Q: File is getting too large**
A: Archive old sessions or start fresh periodically

**Q: Want to reset context**
A: Delete `.session-ctx.json` - agent will create a new one

**Q: Multiple projects**
A: Each repo has its own `.session-ctx.json` in its root

## Advanced: Custom Instructions

You can customize what gets tracked:

```
Also track these in .session-ctx.json:
- Performance metrics for optimization decisions
- Security considerations for auth choices
- API endpoint versioning strategy
```

The agent will adapt the context format to include your needs.

## Summary

**What you do:** Give the initial prompt once
**What the agent does:** Everything else automatically
**What you get:** Seamless context across sessions

Start your next AI coding session with session-ctx and experience the difference!
