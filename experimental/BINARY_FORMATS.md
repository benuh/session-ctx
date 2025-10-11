# Binary Formats

Testing if binary formats are better than JSON for AI context.

## Comparison

| Format | Size | How Fast | Human Readable | Works with AI | Tools Available |
|--------|------|----------|----------------|---------------|-----------------|
| **JSON** | 100% | Baseline | Yes | Native | Universal |
| **MessagePack** | ~60% | 2-3x faster | No | Needs conversion | Good |
| **Protocol Buffers** | ~40% | 3-5x faster | No | Needs conversion | Excellent |
| **CBOR** | ~55% | 2x faster | No | Needs conversion | Limited |
| **Custom Binary** | ~30% | Fastest | No | Complex | None |

## The Issue

Binary formats are smaller and faster to read. But AI needs text, not binary. So you have to convert them first, which removes the benefit.

## Better Approach

Optimize JSON instead:
- Abbreviate keys
- Remove whitespace
- Use numeric codes
- Minify everything

## Size Comparison

```
Standard JSON:        1507 bytes
████████████████████████████████████████  100%

Minified JSON:        892 bytes
███████████████████████                    59%

MessagePack:          600 bytes
████████████████                           40%

Protocol Buffers:     450 bytes
███████████                                30%
```

But for AI, minified JSON is best since binary needs conversion anyway.

## What's Here

- `messagepack_impl.py` - MessagePack format
- `protobuf/` - Protocol Buffers schema
- `optimized_json.py` - Compressed JSON

## Results

100 sessions test:
- JSON: 12,000 tokens
- Minified JSON: 7,200 tokens (40% savings)
- Binary: Same 7,200 tokens after converting + extra work

## Bottom Line

For AI: Use minified JSON
For regular software: Use Protocol Buffers or MessagePack
