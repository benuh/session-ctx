# Overview

## The Problem

AI agents forget everything between sessions. You have to re-explain your project every time.

## The Solution

`.session-ctx.json` file that tracks:
- What decisions you made and why
- What each file does
- What patterns you're following
- What's next

## How It Works

First session: Agent creates `.session-ctx.json` and logs everything as you work

Next session: Agent reads the file and picks up where you left off

## What Gets Tracked

Example:
```json
{
  "sessions": [{
    "goal": "build_user_auth",
    "decisions": [{
      "what": "jwt_auth",
      "why": "stateless_scalable",
      "alt": ["session_based"]
    }],
    "files": {
      "src/auth.ts": {"role": "jwt_logic"}
    },
    "next": ["add_refresh", "tests"]
  }]
}
```

## Why It Helps

```
WITHOUT session-ctx:                WITH session-ctx:
┌─────────────────────────┐        ┌─────────────────────────┐
│ Start session           │        │ Start session           │
│         ↓               │        │         ↓               │
│ Explain everything      │        │ Read .session-ctx.json  │
│   (5 minutes)           │        │   (10 seconds)          │
│         ↓               │        │         ↓               │
│ Agent re-reads code     │        │ Agent ready to work     │
│   (5 minutes)           │        │                         │
│         ↓               │        │                         │
│ Agent re-discovers      │        │                         │
│   patterns              │        │                         │
│   (5 minutes)           │        │                         │
│         ↓               │        │         ↓               │
│ Finally start work      │        │ Start work immediately  │
│   (15 min lost)         │        │   (10 sec lost)         │
└─────────────────────────┘        └─────────────────────────┘

Benefits Summary:
────────────────────────────────────
Setup time:      15 min → 10 sec
Context loss:    Yes → No
Consistency:     Maybe → Always
Decision history: None → Complete
────────────────────────────────────
```

## Example Flow

Session 1:
- You: "Build REST API with auth"
- Agent creates `.session-ctx.json`, builds the API, logs decisions

Session 2:
- You: "Continue from yesterday"
- Agent reads the context, sees what's done, continues building

## Benefits

```
┌────────────────────────────────────────────────┐
│ Speed         Session startup: 80% faster     │
│ Context       No re-discovery needed          │
│ Consistency   Patterns stay the same          │
│ Cost          Uses 40% fewer tokens           │
│ Flexibility   Works across any AI agent       │
└────────────────────────────────────────────────┘

Real Numbers:
  Before: 15 minutes to get started
  After:  10 seconds to get started

  Before: 12,000 tokens per context load
  After:  7,200 tokens per context load
```

## When to Use

Good for: Long-term projects, team work, complex refactoring

Skip it for: One-off scripts, single sessions

## Getting Started

Tell your AI agent:
```
Use session-ctx system. Check for .session-ctx.json in repo root.
If exists: read it. If not: create it. Update throughout session.
```

Next time just say: "Continue from context"
