# How to Actually Use This

## First Time

Copy this and paste it when you start working with an AI coding assistant:

```
I'm using the session-ctx system to maintain context across sessions.

Check if .session-ctx.json exists in this repo root. If yes, read it to
understand previous work and decisions. If no, create it.

Throughout our session, update .session-ctx.json after file changes,
architecture decisions, or when hitting blockers. Use token-efficient
format with abbreviated keys.
```

Then just work normally. The AI will handle the rest.

## Next Time You Code

Just say:
```
Continue from where we left off using .session-ctx.json
```

That's it. The agent reads the context and knows what you were doing.

## What Happens Behind the Scenes

```
FIRST TIME
────────────────────────────────────────
1. AI creates .session-ctx.json
2. Starts tracking your work

DURING WORK
────────────────────────────────────────
Create/edit files      →  Logged to context
Make tech choices      →  Recorded with reasoning
Hit a blocker          →  Documented
Finish a task          →  Status updated

NEW SESSION
────────────────────────────────────────
1. AI reads .session-ctx.json
2. Understands previous work
3. Picks up where you left off
```

## Real Example

```
DAY 1
────────────────────────────────────────
You: "Build a REST API with user auth"
AI:  Creates context file
     Decides on Express + JWT
     Builds auth system
     Logs everything to .session-ctx.json

DAY 2
────────────────────────────────────────
You: "Continue from yesterday"
AI:  Reads context
     Sees Express + JWT decision
     Knows auth is done
     Moves on to next steps

WEEK LATER - Different AI
────────────────────────────────────────
You: "Fix the auth bug"
AI:  Reads same context
     Understands JWT flow
     Fixes bug without explanation
```

## The File You Never Touch

You don't manually edit `.session-ctx.json`. Ever. The AI maintains it.

But if you're curious what it looks like:

```bash
cat .session-ctx.json
```

Or use the helper script:
```bash
python templates/session_ctx_manager.py summary
```

## Git: To Commit or Not

I commit it on team projects because then everyone's AI agents can see the full context. Makes onboarding faster.

For personal stuff, I usually `.gitignore` it unless I want the history.

```bash
# To ignore it
echo ".session-ctx.json" >> .gitignore

# To commit it
git add .session-ctx.json
git commit -m "Update session context"
```

If the file gets big, you can archive old sessions:
```bash
mv .session-ctx.json .session-ctx-archive-2024.json
# AI will create a fresh one next session
```

## What If Something Breaks

**AI not updating the file?**
Just remind it: "Update .session-ctx.json with that decision"

**File too big?**
Delete old sessions or start fresh. Context from the last few sessions is usually enough.

**Want to reset everything?**
```bash
rm .session-ctx.json
# AI creates new one next time
```

**Multiple projects?**
Each repo gets its own `.session-ctx.json` in the root.

## Advanced: Custom Tracking

You can tell the AI to track specific things:

```
Also track performance considerations and security decisions
in .session-ctx.json
```

The AI will adapt the format to include whatever you need.

## The Difference It Makes

```
WITHOUT session-ctx                    WITH session-ctx
──────────────────────────────────     ──────────────────────────────────
0 min   You explain project            0 sec   "Continue from context"
2 min   Still explaining...            10 sec  AI reads context file
5 min   AI re-reads all code           10 sec  Ready to code
8 min   AI re-discovers patterns
10 min  Finally ready to code
──────────────────────────────────     ──────────────────────────────────
Total: 10 minutes                      Total: 10 seconds

                    Save 9 min 50 sec per session
```

Worth it just for the time saved.

## One More Thing

The context file is optimized for token efficiency (abbreviated keys, minified format). That means it looks kinda ugly if you open it. That's intentional - saves ~40% on API costs.

If you want to see what different formats look like, check `experimental/` for comparisons.
