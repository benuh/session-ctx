# session-ctx

> **Agent-optimized context persistence across coding sessions**

## Problem

When working with AI coding agents, each new session starts fresh:
- Conversation history is lost
- Previous decisions and reasoning aren't available
- Agents must re-interpret code without context
- Time wasted re-explaining goals and patterns

## Solution

**session-ctx** is a lightweight, token-efficient context system that persists:
- ✅ Architecture decisions and rationale
- ✅ File purposes and relationships
- ✅ Project patterns and conventions
- ✅ Progress state and next steps
- ✅ Blockers and resolutions

## Key Features

### For AI Agents
- **Token-efficient format**: Abbreviated keys, minimal prose
- **Structured relationships**: Dependencies, impact tracking, state machines
- **Fast parsing**: JSON format optimized for LLM consumption
- **Incremental updates**: Update after each significant change

### For Developers
- **Zero maintenance**: Agents handle all updates
- **Cross-session continuity**: New sessions pick up where you left off
- **Decision history**: Understand WHY choices were made
- **Progress tracking**: See what's done, in-progress, or blocked

## Quick Start

### 1. Add the Agent Prompt

When starting an AI coding session, provide this instruction:

```
Use the session-ctx system to maintain context. Read prompts/AGENT_PROMPT.md
for full instructions. Create/update .session-ctx.json in the repo root
throughout our session.
```

### 2. Agent Auto-Creates Context

The agent will:
- Check for existing `.session-ctx.json`
- Read it to understand previous work (if exists)
- Create one if it doesn't exist
- Update it automatically as work progresses

### 3. Continuous Updates

The agent updates `.session-ctx.json` when:
- Creating/modifying files
- Making architecture decisions
- Installing dependencies
- Encountering blockers
- Completing objectives

## File Format

```json
{
  "v": "1.0",
  "project": "<project_name>",
  "created": "<ISO_timestamp>",
  "updated": "<ISO_timestamp>",
  "sessions": [
    {
      "id": "<session_id>",
      "start": "<ISO_timestamp>",
      "end": "<ISO_timestamp>",
      "goal": "<primary_objective>",
      "state": "completed|in_progress|blocked",
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

See [examples/](./examples) for real-world scenarios.

## Examples

### Initial Session
```json
{
  "goal": "setup_project_structure",
  "state": "in_progress",
  "decisions": [
    {
      "what": "express_framework",
      "why": "lightweight_flexible",
      "alt": ["fastify", "koa"],
      "impact": ["src/server.ts"]
    }
  ],
  "next": ["setup_database", "create_routes"]
}
```

### Continuation Session
Agent reads previous context:
- Understands Express was chosen for flexibility
- Knows database setup is next
- Follows established patterns

## Directory Structure

```
session-ctx/
├── README.md                          # This file
├── prompts/
│   └── AGENT_PROMPT.md               # Full agent instructions
├── examples/
│   ├── 01_initial_session.json       # First session example
│   ├── 02_multi_session.json         # Multi-session example
│   └── 03_bugfix_session.json        # Bug fix example
└── templates/
    └── .session-ctx.json              # Base template
```

## Benefits

| Without session-ctx | With session-ctx |
|---------------------|------------------|
| Re-explain context each session | Agent reads previous context |
| Re-discover architecture decisions | Decision history with rationale |
| Inconsistent patterns | Documented conventions |
| Lost progress tracking | Clear state and next steps |
| High token usage on re-interpretation | Efficient context loading |

## Design Principles

1. **Agent-first**: Optimized for LLM parsing, not human readability
2. **Token-efficient**: Abbreviated keys, structured data
3. **Minimal friction**: Zero developer maintenance
4. **Incremental**: Update as you go, not end-of-session
5. **Stateful**: Track progress across sessions

## Use Cases

- ✅ Long-term projects with multiple sessions
- ✅ Onboarding new AI agents to existing projects
- ✅ Maintaining consistency across different agents
- ✅ Complex refactoring with decision tracking
- ✅ Team projects with AI assistance

## Not Suitable For

- ❌ Single-session tasks
- ❌ Projects requiring human-readable documentation (use ADRs instead)
- ❌ Version-controlled decision logs (complement with ADRs)

## FAQ

**Q: Should I commit `.session-ctx.json` to git?**
A: Optional. It's useful for team context but can grow large. Consider `.gitignore` or periodic cleanup.

**Q: How is this different from ADRs (Architecture Decision Records)?**
A: ADRs are human-readable documentation. session-ctx is agent-optimized for minimal token usage and fast parsing.

**Q: Can I use this with multiple AI agents?**
A: Yes! That's a key use case. Different agents can share context through the same file.

**Q: What if the file gets too large?**
A: Archive old sessions to `.session-ctx-archive.json` and keep recent sessions in the main file.

## Contributing

This is a reference implementation. Adapt the format and prompts to your needs!

## License

MIT

---

**Built for efficient AI collaboration across sessions**
