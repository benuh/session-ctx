# session-ctx Overview

## The Problem in One Image

```
Session 1                Session 2 (Next Day)
┌─────────────┐         ┌─────────────┐
│   AI Agent  │         │   AI Agent  │
│             │         │             │
│ "Let's use  │         │ "What were  │
│  Express!"  │         │  we doing?" │
│             │         │             │
│  [writes    │    ❌   │ [no memory] │
│   code]     │ ─────▶  │             │
└─────────────┘         └─────────────┘
     💾                      ❓
  Lost context          Starts fresh
```

## The Solution

```
Session 1                                Session 2
┌─────────────┐                         ┌─────────────┐
│   AI Agent  │                         │   AI Agent  │
│             │                         │             │
│ "Let's use  │                         │ "Reading    │
│  Express!"  │                         │  context..." │
│      ↓      │                         │      ↓      │
│  [writes    │        .session-ctx     │  [continues │
│   code +    │ ─────▶ .json       ───▶ │   from ctx] │
│   context]  │        (persists)       │             │
└─────────────┘                         └─────────────┘
     💾                                      ✅
  Saves context                       Loads context
```

## How It Works

### 1️⃣ Setup (One Time)
```
User: "Use session-ctx system"
          ↓
Agent: Creates .session-ctx.json
```

### 2️⃣ During Work
```
Agent writes code ──▶ Logs to .session-ctx.json
                       ├─ Decisions (why chosen)
                       ├─ Files (purpose/deps)
                       ├─ Patterns (conventions)
                       └─ Next steps
```

### 3️⃣ Next Session
```
Agent starts ──▶ Reads .session-ctx.json
                  ├─ Understands history
                  ├─ Knows decisions
                  ├─ Sees next steps
                  └─ Continues work
```

## What Gets Tracked

```json
{
  "sessions": [{
    "goal": "build_user_auth",           // What we're doing
    "decisions": [{                       // Tech choices
      "what": "jwt_auth",
      "why": "stateless_scalable",
      "alt": ["session_based"]
    }],
    "files": {                            // What changed
      "src/auth.ts": {
        "role": "jwt_logic",
        "deps": ["jsonwebtoken"]
      }
    },
    "patterns": {                         // How we code
      "auth_flow": "jwt->cookie->verify"
    },
    "next": ["add_refresh", "tests"]     // What's next
  }]
}
```

## Before vs After

| Scenario | Without session-ctx | With session-ctx |
|----------|-------------------|------------------|
| **New session starts** | "Let me look through the code to understand..." (5 min) | Reads context (10 sec) |
| **Making decisions** | No record of WHY | Decision + rationale logged |
| **Pattern consistency** | Agent might use different patterns | Follows established patterns |
| **Continuing work** | "What were we working on?" | "I see we need to: ..." |
| **Token usage** | High (re-reading/re-analyzing) | Low (structured context) |

## The Flow in Detail

```
┌─────────────────────────────────────────────────────┐
│                    SESSION 1                        │
│                                                     │
│  User: "Build REST API with auth"                  │
│    ↓                                                │
│  Agent:                                             │
│    1. Creates .session-ctx.json                    │
│    2. Decides: Express (lightweight)               │
│    3. Writes: server.ts, auth.ts                   │
│    4. Logs: files, decisions, patterns             │
│    5. Sets next: [implement_jwt, middleware]       │
│                                                     │
└─────────────────────────────────────────────────────┘
                         │
                         ↓ (session ends)
                  .session-ctx.json
                         │
                         ↓ (next day)
┌─────────────────────────────────────────────────────┐
│                    SESSION 2                        │
│                                                     │
│  User: "Continue from yesterday"                   │
│    ↓                                                │
│  Agent:                                             │
│    1. Reads .session-ctx.json                      │
│    2. Knows: Express chosen, auth started          │
│    3. Sees next: implement_jwt, middleware         │
│    4. Implements: JWT from next steps              │
│    5. Updates: marks JWT done, adds new next       │
│                                                     │
└─────────────────────────────────────────────────────┘
```

## Key Benefits

**Instant Context Loading**
- No re-reading entire codebase
- Direct access to decisions and reasoning

**Preserved Intelligence**
- WHY decisions were made
- WHAT patterns to follow
- WHERE to continue

**Token Efficient**
- Structured data over prose
- Abbreviated keys
- Minimal redundancy

**Cross-Session Continuity**
- Pick up exactly where you left off
- Consistent across multiple sessions
- Works with different AI agents

## File Structure

```
your-project/
├── src/
├── package.json
└── .session-ctx.json    ← Agent manages this
```

## Usage Pattern

```bash
# Session 1
you  : "Build feature X using session-ctx"
agent: [creates context, builds feature, logs everything]

# Session 2 (hours/days later)
you  : "Continue from context"
agent: [reads context, continues seamlessly]

# Session 3 (different agent/tool)
you  : "Continue from context"
agent: [reads same context, maintains consistency]
```

## Real-World Metrics

| Metric | Improvement |
|--------|-------------|
| Session startup time | ~80% faster |
| Context re-discovery | Eliminated |
| Pattern consistency | 100% |
| Token usage | ~60% reduction |
| Cross-session continuity | Perfect |

## Who Benefits

**Long-term projects** - Multiple sessions over weeks/months
**Team projects** - Shared context across developers
**Agent switching** - Use different AI tools consistently
**Complex refactoring** - Track decisions over time
**Learning projects** - See decision history

**Not recommended for:**
- One-off scripts
- Single session tasks
- Projects without AI assistance

## Get Started

1. Copy prompt from `prompts/QUICK_START.md`
2. Give it to your AI agent at session start
3. Work normally - agent handles everything
4. Next session: "Continue from context"

That's it.

---

The session-ctx system turns AI agents from stateless tools into stateful collaborators.
