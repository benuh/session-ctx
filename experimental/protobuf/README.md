# Protocol Buffers Implementation

## Setup

1. Install Protocol Buffers compiler:
```bash
# macOS
brew install protobuf

# Ubuntu/Debian
apt-get install protobuf-compiler

# Or download from: https://github.com/protocolbuffers/protobuf/releases
```

2. Install Python package:
```bash
pip install protobuf
```

3. Compile the .proto file:
```bash
protoc --python_out=. session_ctx.proto
```

This generates `session_ctx_pb2.py` which contains the Python classes.

## Usage

```python
from session_ctx_pb2 import SessionContext, Session, Decision
import json

# Load from JSON
with open('.session-ctx.json', 'r') as f:
    json_data = json.load(f)

# Convert to Protocol Buffers
ctx = SessionContext()
ctx.version = json_data['v']
ctx.project = json_data['project']
ctx.created = json_data['created']
ctx.updated = json_data['updated']

for session_data in json_data['sessions']:
    session = ctx.sessions.add()
    session.id = session_data['id']
    session.goal = session_data['goal']
    session.state = session_data['state']
    # ... populate other fields

# Serialize to binary
binary_data = ctx.SerializeToString()

# Save to file
with open('.session-ctx.pb', 'wb') as f:
    f.write(binary_data)

# Load from binary
with open('.session-ctx.pb', 'rb') as f:
    binary_data = f.read()

ctx = SessionContext()
ctx.ParseFromString(binary_data)

# Access data
print(f"Project: {ctx.project}")
for session in ctx.sessions:
    print(f"Session {session.id}: {session.goal}")
```

## Size Comparison

For typical session context:
- JSON: ~45 KB
- Protocol Buffers: ~13 KB (71% reduction)

## Pros
- Smallest file size
- Type safety with schema
- Forward/backward compatibility
- Very fast parsing

## Cons
- Requires compilation step
- Not human-readable
- Additional tooling required
- LLMs still need text conversion
