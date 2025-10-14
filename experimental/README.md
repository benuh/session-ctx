# Experimental Format Optimizations

This directory contains advanced token conservation experiments for session-ctx.

## What's Here

### V2 Layered Format (Recommended)
The production-ready V2 format achieves **52% token reduction** through:
- String deduplication table
- Array-based encoding (no key names)
- Layered architecture
- Epoch timestamps
- Numeric enums

**Files:**
- `v2_layered_format.py` - Full encoder/decoder implementation
- `v2_benchmark.py` - Comprehensive benchmark script
- `V2_FORMAT.md` - Complete specification
- `V2_SUMMARY.md` - Overview and usage guide

### V1 Optimizations
Earlier optimization attempts:
- `optimized_json.py` - V1 with single-letter keys (34% reduction)
- `token_conservation_test.py` - Token counting and comparison tools
- `messagepack_impl.py` - Binary format experiment
- `benchmark.py` - Early performance tests

## Quick Start

### Run Benchmark
```bash
# Compare all formats with 5 sessions
python v2_benchmark.py 5

# Results saved to benchmark_samples/
```

### Convert to V2
```bash
# Convert existing .session-ctx.json to V2
python v2_layered_format.py v1-to-v2

# Output: .session-ctx.v2.json
```

### Convert Back to V1
```bash
# Convert V2 back to human-readable V1
python v2_layered_format.py v2-to-v1
```

## Performance Comparison

Based on realistic 3-session test:

| Format | Size | Tokens | Reduction | Cost/1K Reads |
|--------|------|--------|-----------|---------------|
| V1 Standard | 12.1 KB | 2,813 | baseline | $28.13 |
| V1 Minified | 8.0 KB | 1,866 | 34% | $18.66 |
| V1 Optimized | 7.2 KB | 1,859 | 34% | $18.59 |
| **V2 Layered** | **4.8 KB** | **1,354** | **52%** | **$13.54** |

## Format Examples

### V1 Standard (Human-Readable)
```json
{
  "v": "1.0",
  "project": "my-api",
  "sessions": [{
    "id": "s1",
    "goal": "setup_auth",
    "decisions": [{
      "id": "d1",
      "what": "jwt_tokens",
      "why": "stateless_simple",
      "alt": ["sessions", "oauth"]
    }],
    "files": {
      "auth.ts": {
        "action": "created",
        "role": "jwt_logic",
        "deps": ["jsonwebtoken"]
      }
    }
  }]
}
```

### V2 Layered (Agent-Optimized)
```json
{
  "v": "2.0",
  "meta": {"p": "my-api", "c": 1735725600, "u": 1736958600},
  "strings": ["s1", "setup_auth", "d1", "jwt_tokens", "stateless_simple",
              "sessions", "oauth", "auth.ts", "jwt_logic", "jsonwebtoken"],
  "decisions": [[2, 3, 4, [5, 6], [7]]],
  "files": [[7, 0, 8, [9], 0]],
  "sessions": [[0, 1735725600, 1735729200, 1, 1, [0], [0], [], [], [], {}]]
}
```

**Key Differences:**
- V2 stores strings once, uses indices
- Arrays instead of objects (no key names)
- Timestamps are epoch integers
- State/action codes are numbers
- Decisions/files in dedicated arrays, sessions reference by index

## V2 Format Structure

```
strings       - Deduplicated string table (all text)
  └─ ["str1", "str2", ...]

decisions     - All architecture decisions
  └─ [[id_idx, what_idx, why_idx, [alt_indices], [impact_indices]], ...]

files         - All file changes
  └─ [[path_idx, action_code, role_idx, [dep_indices], status_code], ...]

patterns      - All coding patterns
  └─ [[name_idx, desc_idx], ...]

blockers      - All blockers
  └─ [[id_idx, desc_idx, status_code], ...]

sessions      - References to above by index
  └─ [[sid_idx, start, end, goal_idx, state, [dec_indices],
       [file_indices], [pat_indices], [block_indices],
       [next_indices], kv], ...]
```

## Why V2 is Better for Agents

### 1. Predictable Structure
Arrays have fixed positions - no key lookups needed:
```python
decision = decisions[0]
what = strings[decision[1]]  # Position 1 is always "what"
why = strings[decision[2]]   # Position 2 is always "why"
```

### 2. Batch Processing
Process all similar items at once:
```python
# Analyze all decisions
for dec in data["decisions"]:
    analyze_decision(dec)

# Update all files
for file in data["files"]:
    update_file_status(file)
```

### 3. No Duplicate Strings
"fastapi" appears 50 times? Stored once, referenced 50 times:
```
V1: "fastapi" × 50 = 400 chars
V2: "fastapi" once + index (1-2 digits) × 50 = ~100 chars
```

### 4. Reduced Noise
No repeated key names cluttering the context:
```
V1: "what": ... "why": ... "alt": ... (repeated 50 times)
V2: [idx1, idx2, idx3, ...] (clean arrays)
```

## When to Use Each Format

### Use V2 Layered If:
- Token costs matter (high-volume usage)
- Large contexts (>5 sessions, >10 decisions each)
- Working with AI agents exclusively
- Production environment with frequent reads

### Use V1 Optimized If:
- Need some human readability
- Moderate size contexts
- Balance between tokens and readability

### Use V1 Standard If:
- Human debugging is frequent
- Small contexts (1-2 sessions)
- Development/learning phase
- Manual inspection required

## Implementation Details

### String Table Algorithm
1. Collect all strings during encoding
2. Build deduplicated table with index map
3. Replace strings with indices
4. Single table for entire context

### Conversion Fidelity
- 100% round-trip accuracy (V1 → V2 → V1)
- All data preserved
- Timestamps converted but accurate
- No information loss

### Performance
- Encoding: O(n) where n = total items
- Decoding: O(n) with O(1) lookups
- Memory: 40-60% reduction vs V1

## Real-World Savings

### Scenario 1: Solo Developer
- 10 sessions, 30 decisions, 50 files
- 200 context reads over 6 months
- GPT-4 usage

**Savings:** $2.92 (52%)

### Scenario 2: Active Project
- 30 sessions, 100 decisions, 200 files
- 1,000 context reads over 1 year
- GPT-4 usage

**Savings:** $14.59 (52%)

### Scenario 3: Team Project
- 100 sessions, 300 decisions, 500 files
- 10,000 context reads (multiple agents, daily)
- GPT-4 usage

**Savings:** $145.90 (52%)

## Tools Provided

### Command Line
```bash
# Convert formats
python v2_layered_format.py v1-to-v2
python v2_layered_format.py v2-to-v1
python v2_layered_format.py compare

# Run benchmarks
python v2_benchmark.py [num_sessions]
python token_conservation_test.py [num_sessions]
```

### Python API
```python
from v2_layered_format import V2LayeredEncoder, V2LayeredDecoder, V2ContextManager

# Quick conversion
manager = V2ContextManager()
manager.convert_v1_to_v2()

# Manual encoding
encoder = V2LayeredEncoder()
v2_data = encoder.encode(v1_data)

# Manual decoding
decoder = V2LayeredDecoder()
v1_data = decoder.decode(v2_data)
```

## Documentation

- `V2_FORMAT.md` - Complete technical specification
- `V2_SUMMARY.md` - Overview and use cases
- `../prompts/V2_AGENT_PROMPT.md` - Instructions for AI agents

## Benchmark Samples

After running benchmarks, check `benchmark_samples/`:
- `v1_standard.json` - Original format
- `v1_minified.json` - V1 without whitespace
- `v1_optimized.json` - V1 with abbreviated keys
- `v2_layered.json` - V2 minified (production)
- `v2_layered_pretty.json` - V2 with indentation (inspection)

## Future Work

Potential V3 optimizations:
- Delta encoding (store only changes)
- Bit packing (multiple flags in single int)
- Huffman coding (variable-length indices)
- Binary formats (MessagePack, Protocol Buffers)
- Compression (gzip on top of V2)

Expected gains: **70-80% reduction** vs V1 Standard

## Contributing

Experiments welcome! Ideas to explore:
- Better string deduplication algorithms
- More compact timestamp formats
- Alternative encoding schemes
- Binary format implementations
- Compression strategies

## License

MIT - Same as parent project
