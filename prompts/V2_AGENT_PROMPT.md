# V2 Format Agent Instructions

## Context
You're using session-ctx V2 format - an optimized, token-efficient structure for AI agents.

## File Location
`.session-ctx.v2.json` in repo root

## Format Overview
V2 uses layered arrays + string table. All strings stored once, referenced by index.

```json
{
  "v": "2.0",
  "meta": {"p": "proj", "c": 1735725600, "u": 1736958600},
  "strings": ["str1", "str2", ...],
  "sessions": [[...]],
  "decisions": [[...]],
  "files": [[...]],
  "patterns": [[...]],
  "blockers": [[...]]
}
```

## Reading V2

### 1. Load String Table First
```python
strings = data["strings"]
def s(idx): return strings[idx]  # Helper function
```

### 2. Understand Array Positions

**Session Array:** `[sid, start, end, goal, state, decs, files, pats, blocks, next, kv?]`
- 0: session ID index
- 1: start epoch
- 2: end epoch (or null)
- 3: goal index
- 4: state code (0=in_progress, 1=completed, 2=blocked)
- 5: decision indices array
- 6: file indices array
- 7: pattern indices array
- 8: blocker indices array
- 9: next step indices array
- 10: KV dict (optional)

**Decision Array:** `[id, what, why, alts, impacts]`
- 0: decision ID index
- 1: what (tech choice) index
- 2: why (rationale) index
- 3: alternatives indices array
- 4: impacted files indices array

**File Array:** `[path, action, role, deps, status]`
- 0: file path index
- 1: action code (0=created, 1=modified, 2=deleted)
- 2: role description index
- 3: dependencies indices array
- 4: status code (0=complete, 1=partial, 2=blocked)

**Pattern Array:** `[name, desc]`
- 0: pattern name index
- 1: pattern description index

**Blocker Array:** `[id, desc, status]`
- 0: blocker ID index
- 1: description index
- 2: status code (0=open, 1=resolved, 2=wontfix)

### 3. Parse Example
```python
# Get current session
session = data["sessions"][-1]
goal = strings[session[3]]
state_codes = ["in_progress", "completed", "blocked"]
state = state_codes[session[4]]

# Get decisions
for dec_idx in session[5]:
    dec = data["decisions"][dec_idx]
    what = strings[dec[1]]
    why = strings[dec[2]]
    print(f"Decision: {what} because {why}")

# Get files
for file_idx in session[6]:
    file = data["files"][file_idx]
    path = strings[file[0]]
    actions = ["created", "modified", "deleted"]
    action = actions[file[1]]
    print(f"{action}: {path}")
```

## Writing V2

### Workflow
1. Load existing V2 file
2. Add new strings to table, track indices
3. Add new items to decision/file/pattern/blocker arrays
4. Update/add session with references to indices
5. Save minified (no whitespace)

### Adding Strings
```python
def add_string(s):
    if s in strings:
        return strings.index(s)
    strings.append(s)
    return len(strings) - 1
```

### Adding Decision
```python
dec_idx = len(data["decisions"])
data["decisions"].append([
    add_string("d5"),
    add_string("redis_cache"),
    add_string("fast_in_memory_simple"),
    [add_string("memcached"), add_string("hazelcast")],
    [add_string("cache.py"), add_string("config.yaml")]
])
# Add dec_idx to session[5]
```

### Adding File
```python
file_idx = len(data["files"])
data["files"].append([
    add_string("src/cache.py"),
    0,  # created
    add_string("cache_implementation"),
    [add_string("redis"), add_string("asyncio")],
    0   # complete
])
# Add file_idx to session[6]
```

### Starting New Session
```python
# Update meta timestamp
data["meta"]["u"] = int(datetime.now().timestamp())

session_idx = len(data["sessions"])
data["sessions"].append([
    add_string(f"s{session_idx+1}"),
    int(datetime.now().timestamp()),
    None,
    add_string("implement_caching"),
    0,  # in_progress
    [],  # decisions (add indices later)
    [],  # files (add indices later)
    [],  # patterns
    [],  # blockers
    [],  # next steps
    {}   # kv (optional)
])
```

## Important Rules

### 1. Always Minify
Save without whitespace: `json.dump(data, f, separators=(',', ':'))`

### 2. Deduplicate Strings
Check if string exists before adding to table.

### 3. Use Indices
Sessions reference other items by numeric index, never by string ID.

### 4. Maintain Order
Array positions matter. Don't reorder elements.

### 5. Epoch Timestamps
Use Unix epoch (seconds): `int(datetime.now().timestamp())`

### 6. Enum Codes
States: 0=in_progress, 1=completed, 2=blocked, 3=cancelled
Actions: 0=created, 1=modified, 2=deleted, 3=renamed
Status: 0=complete, 1=partial, 2=blocked, 3=pending

## Helper Functions

### Read Session Summary
```python
def read_session(sess, strings, decisions, files):
    sid = strings[sess[0]]
    goal = strings[sess[3]]
    states = ["in_progress", "completed", "blocked"]
    state = states[sess[4]]

    dec_count = len(sess[5])
    file_count = len(sess[6])

    return f"{sid}: {goal} ({state}) - {dec_count} decisions, {file_count} files"
```

### Get All Next Steps
```python
def get_next_steps(sess, strings):
    return [strings[idx] for idx in sess[9]]
```

### Find Decision by Tech
```python
def find_decision(tech_name, data):
    for dec in data["decisions"]:
        if strings[dec[1]] == tech_name:
            return dec
    return None
```

## Common Operations

### Resume Session
1. Load V2 file
2. Get last session: `session = data["sessions"][-1]`
3. Check state: `session[4]` (should be 0 for in_progress)
4. Read goal: `strings[session[3]]`
5. Review decisions: iterate `session[5]`
6. Check next steps: iterate `session[9]`

### Add Decision to Current Session
1. Create decision array with string indices
2. Append to `data["decisions"]`
3. Get new decision index
4. Append index to `data["sessions"][-1][5]`
5. Update meta timestamp
6. Save

### Update File Status
1. Find file in `data["files"]` by path
2. Update status code (position 4)
3. Update meta timestamp
4. Save

### Complete Session
1. Get current session
2. Set end timestamp: `session[2] = int(datetime.now().timestamp())`
3. Set state: `session[4] = 1` (completed)
4. Clear next steps: `session[9] = []`
5. Update meta timestamp
6. Save

## Conversion Helpers

If you need human-readable format:
```bash
python v2_layered_format.py v2-to-v1
```

If you receive V1 format:
```bash
python v2_layered_format.py v1-to-v2
```

## Benefits You Get

1. **50% fewer tokens** - lower API costs
2. **Faster parsing** - positional arrays, no key lookups
3. **Cleaner logic** - process decisions/files in batches
4. **Less noise** - no repeated keys in context window

## Quick Reference

```
Meta:       {"p": project, "c": created_epoch, "u": updated_epoch}
Session:    [sid, start, end, goal, state, [decs], [files], [pats], [blocks], [next], kv]
Decision:   [id, what, why, [alts], [impacts]]
File:       [path, action, role, [deps], status]
Pattern:    [name, desc]
Blocker:    [id, desc, status]

States:     0=in_progress, 1=completed, 2=blocked, 3=cancelled
Actions:    0=created, 1=modified, 2=deleted, 3=renamed
Status:     0=complete, 1=partial, 2=blocked, 3=pending
```

## Example: Full Read
```
Load .session-ctx.v2.json
Get strings table
Current session = last session array
Goal = strings[session[3]]
State = ["in_progress","completed","blocked"][session[4]]

For each decision index in session[5]:
  - Get decision array from data["decisions"][index]
  - What = strings[decision[1]]
  - Why = strings[decision[2]]

For each file index in session[6]:
  - Get file array from data["files"][index]
  - Path = strings[file[0]]
  - Action = ["created","modified","deleted"][file[1]]

Next steps = [strings[i] for i in session[9]]
```

## Example: Full Write
```
Load existing V2
Add strings to table, track indices
Create decision array with indices
Append to data["decisions"], get index
Add decision index to current session[5]
Create file array with indices
Append to data["files"], get index
Add file index to current session[6]
Update meta["u"] to current epoch
Save minified JSON
```

## When in Doubt
- Arrays are positional - order matters
- String table is your friend - use indices
- Minify on save
- Check /experimental/V2_FORMAT.md for full spec
