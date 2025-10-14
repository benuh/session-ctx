# Session Context V2 Format Specification

## Overview

V2 is an agent-optimized, layered format that achieves **50-60% token reduction** compared to standard JSON, while maintaining full information fidelity and machine readability.

## Key Innovations

### 1. String Deduplication Table
All repeated strings are stored once in a central table and referenced by numeric index.

```json
{
  "strings": [
    "fastapi",
    "sqlalchemy",
    "pydantic",
    "redis"
  ]
}
```

Reference: `0` = "fastapi", `1` = "sqlalchemy", etc.

### 2. Array-Based Encoding
Instead of objects with key names, data uses positional arrays:

**V1 (object-based):**
```json
{
  "id": "d1",
  "what": "postgresql",
  "why": "relational_acid",
  "alt": ["mongodb", "mysql"],
  "impact": ["schema.sql", "db.py"]
}
```

**V2 (array-based):**
```json
[0, 12, 45, [23, 24], [67, 68]]
```
Position meanings: `[id_idx, what_idx, why_idx, [alt_indices], [impact_indices]]`

### 3. Layered Architecture
Data is organized into semantic layers that agents can process independently:

- `meta`: Project metadata
- `strings`: Deduplicated string table
- `decisions`: All architectural decisions
- `files`: All file changes
- `patterns`: All coding patterns
- `blockers`: All blockers
- `sessions`: References to above layers by index

### 4. Epoch Timestamps
ISO8601 timestamps converted to Unix epoch (integers):
- `"2025-01-15T16:30:00Z"` → `1736958600`
- Saves ~20 chars per timestamp

### 5. Numeric Enums
Common values encoded as numbers:
- States: `0=in_progress, 1=completed, 2=blocked, 3=cancelled`
- Actions: `0=created, 1=modified, 2=deleted, 3=renamed`
- Status: `0=complete, 1=partial, 2=blocked, 3=pending`

## Complete Format Structure

```json
{
  "v": "2.0",
  "meta": {
    "p": "project_name",
    "c": 1735725600,
    "u": 1736958600
  },
  "strings": ["str1", "str2", ...],
  "sessions": [
    [
      sid_idx,           // 0: session ID index
      start_epoch,       // 1: start timestamp (epoch)
      end_epoch,         // 2: end timestamp (epoch or null)
      goal_idx,          // 3: goal string index
      state_code,        // 4: state enum (0-3)
      [dec_indices],     // 5: decision indices
      [file_indices],    // 6: file indices
      [pat_indices],     // 7: pattern indices
      [block_indices],   // 8: blocker indices
      [next_indices],    // 9: next step indices
      {...}              // 10: key-value pairs (optional)
    ]
  ],
  "decisions": [
    [id_idx, what_idx, why_idx, [alt_indices], [impact_indices]]
  ],
  "files": [
    [path_idx, action_code, role_idx, [dep_indices], status_code]
  ],
  "patterns": [
    [name_idx, desc_idx]
  ],
  "blockers": [
    [id_idx, desc_idx, state_code]
  ]
}
```

## Token Efficiency Comparison

Based on benchmark with 3 realistic sessions:

| Format | Size | Tokens | Savings |
|--------|------|--------|---------|
| V1 Standard (pretty) | 12.1 KB | 2,813 | baseline |
| V1 Minified | 8.0 KB | 1,866 | 33.7% |
| V1 Optimized (abbrev) | 7.2 KB | 1,859 | 33.9% |
| **V2 Layered** | **4.8 KB** | **1,354** | **51.9%** |

### Cost Savings (per 1,000 reads)

**GPT-4:**
- V1 Standard: $28.13
- V2 Layered: $13.54
- **Savings: $14.59** (51.9%)

**GPT-3.5:**
- V1 Standard: $1.41
- V2 Layered: $0.68
- **Savings: $0.73** (51.9%)

## Why V2 is Agent-Friendly

### 1. Predictable Structure
Arrays have fixed positions. Agents can parse without key lookups:
```python
decision = decisions[idx]
what = strings[decision[1]]  # Position 1 is always "what"
why = strings[decision[2]]   # Position 2 is always "why"
```

### 2. Efficient Batch Processing
All similar items in one array:
```python
# Process all decisions at once
for dec in data["decisions"]:
    analyze_decision(dec)

# Process all files at once
for file in data["files"]:
    analyze_file(file)
```

### 3. Reduced Noise
No repeated keys like `"what":`, `"why":`, `"alt":` in every decision.
Agents parse raw data without distraction.

### 4. Fast Lookups
String table enables O(1) lookups:
```python
strings = data["strings"]
# Instant access
tech_name = strings[decision[1]]
```

### 5. Space-Efficient References
Sessions reference decisions/files by small integers instead of string IDs:
- V1: `"decisions": [{"id": "d1", ...}, {"id": "d2", ...}]`
- V2: `[0, 1]` (references to decision array)

## Usage

### Encoding (V1 → V2)
```python
from v2_layered_format import V2LayeredEncoder
import json

# Load V1 format
with open('.session-ctx.json') as f:
    v1_data = json.load(f)

# Encode to V2
encoder = V2LayeredEncoder()
v2_data = encoder.encode(v1_data)

# Save V2 format (minified)
with open('.session-ctx.v2.json', 'w') as f:
    json.dump(v2_data, f, separators=(',', ':'))
```

### Decoding (V2 → V1)
```python
from v2_layered_format import V2LayeredDecoder
import json

# Load V2 format
with open('.session-ctx.v2.json') as f:
    v2_data = json.load(f)

# Decode to V1
decoder = V2LayeredDecoder()
v1_data = decoder.decode(v2_data)

# Use as normal V1 format
for session in v1_data['sessions']:
    print(session['goal'])
```

### CLI Tools
```bash
# Convert V1 to V2
python v2_layered_format.py v1-to-v2

# Convert V2 back to V1
python v2_layered_format.py v2-to-v1

# Compare sizes
python v2_layered_format.py compare

# Run benchmark
python v2_benchmark.py 5  # 5 sessions
```

## Agent Prompts

### Reading V2 Format
```
Load the V2 session context from .session-ctx.v2.json. The format uses:
- String table for deduplication (all strings indexed)
- Array-based encoding (no key names, positional)
- Layered architecture (decisions, files, patterns, blockers)

Parse structure:
1. Load "strings" array for lookups
2. Read "decisions", "files", etc. arrays
3. Sessions reference these by index
4. Use position to determine meaning (e.g., decisions[i][1] is "what")
```

### Writing V2 Format
```
Update the V2 session context efficiently:
1. Add new strings to "strings" array, get index
2. Add new decisions/files/patterns to respective arrays
3. Reference them by index in session array
4. Use epoch timestamps and numeric codes
5. Keep format minified (no whitespace)
```

## When to Use V2

**Use V2 if:**
- Token conservation is critical (high-volume usage)
- Working with agents that support structured formats
- Need to minimize API costs
- Sessions are large (>5 sessions, >10 decisions each)

**Use V1 if:**
- Human readability is priority
- Simple, infrequent usage
- Debugging/development
- Small sessions (1-2 sessions)

## Implementation Notes

### String Table Management
- Automatically deduplicates on encoding
- No manual string table management needed
- Common strings (like dependency names) only stored once

### Backward Compatibility
- V2 decoder outputs standard V1 format
- Existing tools can consume decoded output
- Transparent conversion both directions

### Data Integrity
- Full round-trip fidelity (V1 → V2 → V1)
- No data loss in conversion
- All semantic information preserved

## Performance Characteristics

### Encoding Speed
- O(n) where n = total items (decisions + files + patterns + blockers)
- String table built in single pass
- Typical: ~1ms for 10 sessions

### Decoding Speed
- O(n) where n = total items
- Array lookups are O(1)
- Typical: ~0.5ms for 10 sessions

### Memory Overhead
- String table: ~20-30% of original string data
- Index arrays: negligible (small integers)
- Overall: 40-60% reduction vs V1

## Advanced Optimizations

### Future Enhancements
1. **Delta encoding**: Store only changes between sessions
2. **Bit packing**: Pack multiple enums into single integers
3. **Huffman coding**: Variable-length encoding for indices
4. **Dictionary compression**: zlib on top of V2 format

### Experimental Features
See `/experimental` for:
- MessagePack binary format
- Protocol Buffer schemas
- Compression benchmarks

## Examples

See `/experimental/benchmark_samples/` for real examples:
- `v1_standard.json` - Original format
- `v2_layered.json` - V2 minified
- `v2_layered_pretty.json` - V2 with indentation (for inspection)

## Specification Version

Current: `v2.0` (2025-01-15)

Changes from v1.0:
- Layered architecture
- String deduplication
- Array-based encoding
- Epoch timestamps
- Numeric enums
