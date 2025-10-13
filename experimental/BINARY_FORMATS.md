# Binary Formats

Testing if binary formats are better than JSON for AI context.

## Comparison

```
Format              Size   Speed      Readable   AI Ready   Tools
──────────────────────────────────────────────────────────────────
JSON                100%   Baseline   Yes        Yes        Universal
MessagePack         ~60%   2-3x       No         Convert    Good
Protocol Buffers    ~40%   3-5x       No         Convert    Excellent
CBOR                ~55%   2x         No         Convert    Limited
Custom Binary       ~30%   Fastest    No         Complex    None
```

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
Standard JSON        1,507 bytes   ████████████████████  100%
Minified JSON          892 bytes   ████████████           59%
MessagePack            600 bytes   ████████               40%
Protocol Buffers       450 bytes   █████                  30%
```

But for AI, minified JSON is best since binary needs conversion anyway.

## What's Here

- `messagepack_impl.py` - MessagePack format
- `protobuf/` - Protocol Buffers schema
- `optimized_json.py` - Compressed JSON

## Results

```
100 sessions test:

Format           Tokens    Savings
─────────────────────────────────
JSON             12,000    -
Minified JSON     7,200    40%
Binary*           7,200    40%*

*After converting to text for AI
```

## Bottom Line

For AI: Use minified JSON
For regular software: Use Protocol Buffers or MessagePack
