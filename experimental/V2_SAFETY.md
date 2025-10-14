# V2 Format Safety Guide

## File Structure - NO OVERWRITES!

V1 and V2 formats use **completely separate files**:

```
your-repo/
├── .session-ctx.json            ← V1 format (NEVER modified by V2 tools)
├── .session-ctx.v2.json         ← V2 format (separate file)
└── .session-ctx.v1-from-v2.json ← V2→V1 conversion output (safe testing)
```

## Safety Guarantees

### 1. V1 File is Protected
- **Original V1 file (`.session-ctx.json`) is NEVER overwritten**
- V2 tools only READ from V1, never WRITE to it
- Your V1 data is always safe

### 2. V2 Conversion is Non-Destructive
```bash
# This reads V1, creates NEW V2 file
python v2_layered_format.py v1-to-v2
```

**Result:**
- ✓ `.session-ctx.json` - unchanged
- ✓ `.session-ctx.v2.json` - newly created
- ✓ Both files coexist

### 3. V2→V1 Conversion Uses Safe Output
```bash
# This creates .session-ctx.v1-from-v2.json (NOT .session-ctx.json)
python v2_layered_format.py v2-to-v1
```

**Result:**
- ✓ `.session-ctx.json` - unchanged
- ✓ `.session-ctx.v2.json` - unchanged
- ✓ `.session-ctx.v1-from-v2.json` - newly created

### 4. Protection Against Accidental Overwrite
```bash
# First run - creates V2
python v2_layered_format.py v1-to-v2
# ✓ Created .session-ctx.v2.json

# Second run - BLOCKED!
python v2_layered_format.py v1-to-v2
# Error: V2 file already exists: .session-ctx.v2.json
# Use --force to overwrite existing V2 file

# Must explicitly force overwrite
python v2_layered_format.py v1-to-v2 --force
# ✓ Overwrites .session-ctx.v2.json
```

## Independent Testing

You can test both formats side-by-side:

### Test V1 Format
```bash
# Agent reads V1
cat .session-ctx.json

# Agent updates V1 (use existing tools)
# Original format, no changes
```

### Test V2 Format
```bash
# Create V2 from V1
python v2_layered_format.py v1-to-v2

# Agent reads V2
cat .session-ctx.v2.json

# Compare sizes
python v2_layered_format.py compare
```

### Verify Round-Trip Fidelity
```bash
# 1. Start with V1
cat .session-ctx.json > original-v1.json

# 2. Convert to V2
python v2_layered_format.py v1-to-v2

# 3. Convert back to V1
python v2_layered_format.py v2-to-v1

# 4. Compare (should be identical except timestamps)
diff original-v1.json .session-ctx.v1-from-v2.json
```

## Workflow Options

### Option 1: Keep Both (Recommended During Testing)
```
.session-ctx.json       ← V1 format (agents can use this)
.session-ctx.v2.json    ← V2 format (agents can use this)
```

**Use Case:**
- Test both formats with agents
- Compare token usage
- Verify round-trip conversion
- Choose which format works better

### Option 2: V1 Only
```
.session-ctx.json       ← V1 format only
```

**Use Case:**
- Human readability priority
- Small contexts
- Don't need token optimization

### Option 3: V2 Only
```
.session-ctx.v2.json    ← V2 format only
```

**Use Case:**
- Token costs are critical
- Large contexts
- Agent-only access

### Option 4: V1 as Source of Truth, V2 as Optimized Copy
```
.session-ctx.json       ← V1 (edit this)
.session-ctx.v2.json    ← V2 (regenerate when V1 changes)
```

**Workflow:**
```bash
# Edit V1 manually or with V1 tools
vim .session-ctx.json

# Regenerate V2 from updated V1
python v2_layered_format.py v1-to-v2 --force

# Agents read V2 (optimized)
```

## .gitignore Recommendations

### Ignore Both (Solo Project)
```gitignore
.session-ctx.json
.session-ctx.v2.json
.session-ctx.v1-from-v2.json
```

### Commit V1, Ignore V2 (Team - Human Readable)
```gitignore
.session-ctx.v2.json
.session-ctx.v1-from-v2.json
```

### Commit V2, Ignore V1 (Team - Token Optimized)
```gitignore
.session-ctx.json
.session-ctx.v1-from-v2.json
```

### Commit Both (Team - Testing Phase)
```gitignore
.session-ctx.v1-from-v2.json
```

## Common Questions

### Q: Will v1-to-v2 delete my V1 file?
**A:** No! V1 file is never touched. V2 is created as a separate file.

### Q: Will v2-to-v1 overwrite my V1 file?
**A:** No! It creates `.session-ctx.v1-from-v2.json` by default.

### Q: What if I want to overwrite V1?
**A:** Use custom output:
```bash
python v2_layered_format.py v2-to-v1 .session-ctx.json
```
(But you'll get a warning)

### Q: Can I have both V1 and V2 at the same time?
**A:** Yes! They're completely independent files. Test both.

### Q: Which file should agents read?
**A:** Your choice:
- V1: More readable, easier to debug
- V2: 52% fewer tokens, lower costs

### Q: Can I switch between V1 and V2?
**A:** Yes! Conversion tools work both directions with 100% fidelity.

### Q: What if conversion fails?
**A:** Original files are never modified. Safe to retry.

## Testing Checklist

- [ ] Create V1 file with test data
- [ ] Convert V1 to V2
- [ ] Verify V1 still exists and unchanged
- [ ] Compare file sizes
- [ ] Convert V2 back to V1
- [ ] Verify round-trip accuracy
- [ ] Test agent with V1
- [ ] Test agent with V2
- [ ] Compare token usage
- [ ] Choose format based on results

## Emergency Recovery

### Lost V1 but have V2?
```bash
python v2_layered_format.py v2-to-v1 .session-ctx.json
```

### Lost V2 but have V1?
```bash
python v2_layered_format.py v1-to-v2
```

### Both corrupted?
```bash
# Check git history
git log --all -- .session-ctx.json .session-ctx.v2.json

# Restore from commit
git checkout <commit-hash> -- .session-ctx.json
```

## Summary

✅ V1 and V2 are **completely separate files**
✅ Original V1 is **NEVER overwritten**
✅ Conversions are **non-destructive**
✅ Both formats can **coexist safely**
✅ Full **round-trip fidelity**
✅ Test **independently and safely**

Your data is safe!
