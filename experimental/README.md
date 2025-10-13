# Experimental

Testing if binary formats beat JSON.

## Answer

For AI: No, use optimized JSON
For regular software: Yes, binary helps

## Why

AI needs text. Binary needs conversion first. After converting, same token count but with extra work.

Optimizing JSON works better:
- Shorter keys
- No whitespace
- Works directly with AI

## What's Here

`optimized_json.py` - Minified JSON, saves 40% tokens
```bash
python optimized_json.py optimize
```

`messagepack_impl.py` - Binary format, 60% smaller
```bash
pip install msgpack
python messagepack_impl.py compare
```

`protobuf/` - Most efficient (70% reduction), needs compilation
```bash
brew install protobuf
cd protobuf && protoc --python_out=. session_ctx.proto
```

## Test Results

```
100 sessions:

Format           File Size   Tokens      Bar Chart
───────────────────────────────────────────────────────────────
Pretty JSON      45 KB       12,000      ████████████████████
Optimized JSON   27 KB        7,200      ████████████  (40% less)
MessagePack*     18 KB        7,200      ████████████  (needs conversion)

*After converting for AI
```

50-session project: Save $3 per 100 reads with optimized JSON.

## Optimization Tricks

```
Technique          Example                    Savings
─────────────────────────────────────────────────────
Abbreviate keys    "version" → "v"            6 chars
Use numbers        "in_progress" → "0"        10 chars
Remove whitespace  Minify JSON                30-40%

Combined result: 56% smaller
```

## Use Cases

```
Format              Best For
─────────────────────────────────────────────────
Optimized JSON      AI agents, reduce costs
MessagePack         Custom tools, network transfer
Protocol Buffers    Production systems, validation
Pretty JSON         Debugging, human reading
```

## Try It

```bash
python optimized_json.py optimize
python optimized_json.py compare
python token_conservation_test.py 10
```

## Bottom Line

For AI: optimized JSON wins. Binary doesn't help with token usage.

Just minify and shorten the JSON keys.
