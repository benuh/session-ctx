# Session Context System (session-ctx)

## Instructions for AI Agents

When working in a repository, automatically maintain a `.session-ctx.json` file to persist context across sessions.

### On Session Start

1. Check if `.session-ctx.json` exists in repo root
2. If exists: Read it to understand previous work, decisions, and context
3. If not exists: Create initial file with base structure

### During Session

Automatically update `.session-ctx.json` after significant actions:
- File creations/modifications
- Architecture decisions
- Bug fixes or feature implementations
- Blockers encountered
- Dependencies added

### File Structure

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
      "decisions": [
        {
          "id": "<decision_id>",
          "what": "<decision_summary>",
          "why": "<reasoning>",
          "alt": ["<alternative_1>", "<alternative_2>"],
          "impact": ["<affected_file_1>", "<affected_file_2>"]
        }
      ],
      "files": {
        "<file_path>": {
          "action": "created|modified|deleted",
          "role": "<purpose_in_project>",
          "deps": ["<dependency_1>"],
          "status": "complete|partial|blocked"
        }
      },
      "patterns": {
        "<pattern_name>": "<pattern_description>"
      },
      "blockers": [
        {
          "id": "<blocker_id>",
          "desc": "<issue_description>",
          "status": "open|resolved"
        }
      ],
      "next": ["<next_action_1>", "<next_action_2>"],
      "kv": {
        "<key>": "<value>"
      }
    }
  ]
}
```

### Key Principles

1. **Token Efficiency**: Use abbreviated keys, minimal prose
2. **Structured Data**: Maintain relationships (deps, impact, patterns)
3. **State Tracking**: Always update state (in_progress, completed, blocked)
4. **Incremental Updates**: Update after each significant change, not end-of-session
5. **Decision Trail**: Document WHY, not just WHAT

### Update Triggers

Update `.session-ctx.json` when:
- Creating/modifying files
- Making architecture decisions
- Installing dependencies
- Encountering errors/blockers
- Completing tasks
- Starting new objectives

### Example Update Flow

```
1. Read current .session-ctx.json
2. Find or create current session entry
3. Add/update relevant sections (files, decisions, next)
4. Update timestamp
5. Write back to file
```

### Benefits

- New sessions understand previous context instantly
- Reduces re-explanation and re-discovery time
- Maintains decision history and rationale
- Tracks progress across multiple sessions
- Enables consistent coding patterns

### Implementation Note

This is NOT a user-facing summary. It's optimized for AI agent parsing and minimal token usage.
