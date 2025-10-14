# File Structure - V1 vs V2

## Overview

V1 and V2 use **separate files** - they never conflict or overwrite each other.

## File Layout

```
your-repo/
│
├── .session-ctx.json              ← V1 Format (Original)
│   └─ Human-readable JSON
│   └─ Full key names ("what", "why", "alt", etc.)
│   └─ ISO8601 timestamps
│   └─ Pretty printed with indentation
│
├── .session-ctx.v2.json           ← V2 Format (Optimized)
│   └─ Agent-optimized JSON
│   └─ Array-based encoding
│   └─ String deduplication table
│   └─ Minified (no whitespace)
│
└── .session-ctx.v1-from-v2.json   ← Conversion Output (Testing)
    └─ V2 converted back to V1 format
    └─ Used to verify round-trip accuracy
    └─ Safe - doesn't overwrite original
```

## Format Comparison

### V1 Format (`.session-ctx.json`)
```json
{
  "v": "1.0",
  "project": "my-api",
  "created": "2025-01-15T10:00:00Z",
  "updated": "2025-01-15T16:30:00Z",
  "sessions": [
    {
      "id": "s1",
      "start": "2025-01-15T10:00:00Z",
      "end": null,
      "goal": "setup_auth",
      "state": "in_progress",
      "decisions": [
        {
          "id": "d1",
          "what": "jwt_tokens",
          "why": "stateless_simple",
          "alt": ["sessions", "oauth"],
          "impact": ["auth.ts", "middleware.ts"]
        }
      ],
      "files": {
        "auth.ts": {
          "action": "created",
          "role": "jwt_logic",
          "deps": ["jsonwebtoken"],
          "status": "complete"
        }
      },
      "patterns": {},
      "blockers": [],
      "next": ["add_refresh_tokens"],
      "kv": {
        "node_version": "20.x"
      }
    }
  ]
}
```

**Characteristics:**
- ✓ Human readable
- ✓ Self-documenting
- ✗ Verbose (2,813 tokens for 3 sessions)
- ✗ Repeated key names

### V2 Format (`.session-ctx.v2.json`)
```json
{"v":"2.0","meta":{"p":"my-api","c":1736942400,"u":1736965800},"strings":["s1","setup_auth","d1","jwt_tokens","stateless_simple","sessions","oauth","auth.ts","middleware.ts","jwt_logic","jsonwebtoken","add_refresh_tokens","node_version","20.x"],"decisions":[[2,3,4,[5,6],[7,8]]],"files":[[7,0,9,[10],0]],"sessions":[[0,1736942400,null,1,0,[0],[0],[],[],[11],{"12":"13"}]]}
```

**Same data, formatted for inspection:**
```json
{
  "v": "2.0",
  "meta": {
    "p": "my-api",
    "c": 1736942400,
    "u": 1736965800
  },
  "strings": [
    "s1", "setup_auth", "d1", "jwt_tokens", "stateless_simple",
    "sessions", "oauth", "auth.ts", "middleware.ts", "jwt_logic",
    "jsonwebtoken", "add_refresh_tokens", "node_version", "20.x"
  ],
  "decisions": [
    [2, 3, 4, [5, 6], [7, 8]]
  ],
  "files": [
    [7, 0, 9, [10], 0]
  ],
  "sessions": [
    [0, 1736942400, null, 1, 0, [0], [0], [], [], [11], {"12": "13"}]
  ]
}
```

**Characteristics:**
- ✓ Compact (1,354 tokens for 3 sessions)
- ✓ No duplicate strings
- ✓ Fast array-based parsing
- ✗ Not human readable without decoder
- ✗ Requires understanding of positions

## Conversion Flow

```
Original V1                      Conversion                       V2 Format
┌──────────────────┐                                      ┌──────────────────┐
│.session-ctx.json │                                      │.session-ctx.v2   │
│                  │                                      │        .json     │
│  - 12.1 KB       │   v1-to-v2 (SAFE)                   │                  │
│  - 2,813 tokens  │  ───────────────────────────>       │  - 4.8 KB        │
│  - Human format  │  NEVER overwrites source            │  - 1,354 tokens  │
│  - Preserved!    │                                      │  - Agent format  │
│                  │  <───────────────────────────        │                  │
└──────────────────┘   v2-to-v1 (SAFE)                   └──────────────────┘
         ∧               outputs to:
         │             .session-ctx.v1-from-v2.json
         │             (new file, safe testing)
         │
    Never Modified!
```

## Safety Rules

### ✅ Safe Operations (Default)
```bash
# V1 → V2 conversion (creates NEW file)
python v2_layered_format.py v1-to-v2
# Result: .session-ctx.json (unchanged) + .session-ctx.v2.json (new)

# V2 → V1 conversion (creates NEW file)
python v2_layered_format.py v2-to-v1
# Result: .session-ctx.json (unchanged) + .session-ctx.v1-from-v2.json (new)

# Compare both formats
python v2_layered_format.py compare
# Result: Both files compared, neither modified
```

### ⚠️ Protected Operations (Require Flag)
```bash
# Overwrite existing V2
python v2_layered_format.py v1-to-v2 --force
# Result: .session-ctx.v2.json overwritten

# Custom output location
python v2_layered_format.py v2-to-v1 custom-file.json
# Result: Output to specified file
```

### 🚫 Prevented Operations (Errors)
```bash
# Try to convert when V2 already exists
python v2_layered_format.py v1-to-v2
# Error: V2 file already exists. Use --force to overwrite.

# Try to convert without source file
python v2_layered_format.py v1-to-v2
# Error: V1 file not found: .session-ctx.json
```

## Testing Workflow

### Step 1: Create V1 Test Data
```bash
# Create or use existing V1 file
cat > .session-ctx.json <<EOF
{
  "v": "1.0",
  "project": "test-project",
  "sessions": [...]
}
EOF
```

### Step 2: Convert to V2
```bash
python v2_layered_format.py v1-to-v2
# ✓ Created V2 format: .session-ctx.v2.json
#   Original V1 file preserved: .session-ctx.json
#   Size reduction: 60.7%
#   Token reduction: 51.9%
```

### Step 3: Verify Both Exist
```bash
ls -lh .session-ctx*.json
# .session-ctx.json       12K  (V1 - original)
# .session-ctx.v2.json    5K   (V2 - optimized)
```

### Step 4: Test V1 Agent
```bash
# Agent reads V1
python your_agent.py --context .session-ctx.json
```

### Step 5: Test V2 Agent
```bash
# Agent reads V2
python your_agent.py --context .session-ctx.v2.json
```

### Step 6: Compare Results
```bash
python v2_layered_format.py compare
# V1 format (.session-ctx.json):
#   Size: 12,392 bytes
#   Tokens: ~2,813
#
# V2 format (.session-ctx.v2.json):
#   Size: 4,866 bytes
#   Tokens: ~1,354
#
# Savings (V2 vs V1):
#   Size: 7,526 bytes (60.7%)
#   Tokens: ~51.9%
```

### Step 7: Verify Round-Trip
```bash
# Convert V2 back to V1 format
python v2_layered_format.py v2-to-v1

# Compare with original
diff .session-ctx.json .session-ctx.v1-from-v2.json
# Should be identical (except timestamp precision)
```

## Which File to Use?

| Scenario | Use File | Why |
|----------|----------|-----|
| Human editing | `.session-ctx.json` (V1) | Readable, self-documenting |
| Agent reading (cost matters) | `.session-ctx.v2.json` (V2) | 52% fewer tokens |
| Debugging | `.session-ctx.json` (V1) | Easy to inspect |
| Production (high volume) | `.session-ctx.v2.json` (V2) | Lower API costs |
| Testing both | Both files | Compare independently |
| Round-trip verification | `.session-ctx.v1-from-v2.json` | Check conversion accuracy |

## File Permissions

Both formats are standard JSON text files:
```bash
-rw-r--r--  .session-ctx.json
-rw-r--r--  .session-ctx.v2.json
-rw-r--r--  .session-ctx.v1-from-v2.json
```

## Git Tracking

### Development Phase (Track Both)
```gitignore
# Don't ignore - commit both for comparison
```

### Production (V1 Only)
```gitignore
.session-ctx.v2.json
.session-ctx.v1-from-v2.json
```

### Production (V2 Only)
```gitignore
.session-ctx.json
.session-ctx.v1-from-v2.json
```

### Local Only (Neither)
```gitignore
.session-ctx*.json
```

## Quick Reference

| Operation | Command | Source | Output | Original |
|-----------|---------|--------|--------|----------|
| V1 → V2 | `v1-to-v2` | `.session-ctx.json` | `.session-ctx.v2.json` | ✅ Preserved |
| V2 → V1 | `v2-to-v1` | `.session-ctx.v2.json` | `.session-ctx.v1-from-v2.json` | ✅ Preserved |
| Compare | `compare` | Both | Terminal output | ✅ Unchanged |
| Force V2 | `v1-to-v2 --force` | `.session-ctx.json` | `.session-ctx.v2.json` (overwrite) | ✅ Preserved |

**Key Point:** `.session-ctx.json` is NEVER modified by conversion tools!
