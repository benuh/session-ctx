#!/usr/bin/env python3
"""
Session Context V2 - Layered, Agent-Optimized Format

This format maximizes token efficiency through:
1. Layered architecture (metadata, decisions, files, flow)
2. Array-based encoding (predictable positions, no key names)
3. String table for deduplication
4. Numeric indices instead of string IDs
5. Compact timestamps (ISO8601 short form or epoch)
6. Bit flags for state combinations

Format Structure:
{
  "v": "2.0",
  "meta": {
    "p": "project_name",
    "c": epoch_created,
    "u": epoch_updated
  },
  "strings": ["common_string1", "common_string2", ...],  // String table
  "sessions": [
    [
      session_id_index,
      epoch_start,
      epoch_end_or_null,
      goal_string_index,
      state_code,
      [decision_indices],
      [file_indices],
      [pattern_indices],
      [blocker_indices],
      [next_step_indices],
      {kv_pairs}  // Only if needed
    ]
  ],
  "decisions": [
    [id, what_index, why_index, [alt_indices], [impact_indices]]
  ],
  "files": [
    [path_index, action_code, role_index, [dep_indices], status_code]
  ],
  "patterns": [
    [name_index, desc_index]
  ],
  "blockers": [
    [id, desc_index, state_code]
  ]
}

Advantages:
- 40-60% fewer tokens than V1
- All data is indexed, no duplicate strings
- Agent can quickly locate layers (decisions, files, etc.)
- Order-based arrays reduce key overhead
- Easier to batch-process similar items
"""

import json
from pathlib import Path
from typing import Dict, Any, List, Optional, Union
from datetime import datetime
from collections import defaultdict


# State codes
STATE = {"in_progress": 0, "completed": 1, "blocked": 2, "cancelled": 3}
STATE_DECODE = {v: k for k, v in STATE.items()}

# Action codes
ACTION = {"created": 0, "modified": 1, "deleted": 2, "renamed": 3}
ACTION_DECODE = {v: k for k, v in ACTION.items()}

# Status codes
STATUS = {"complete": 0, "partial": 1, "blocked": 2, "pending": 3}
STATUS_DECODE = {v: k for k, v in STATUS.items()}


class StringTable:
    """Manages string deduplication via indexed lookup table"""

    def __init__(self):
        self.table: List[str] = []
        self.index_map: Dict[str, int] = {}

    def add(self, s: str) -> int:
        """Add string to table, return index"""
        if s in self.index_map:
            return self.index_map[s]
        idx = len(self.table)
        self.table.append(s)
        self.index_map[s] = idx
        return idx

    def get(self, idx: int) -> str:
        """Get string by index"""
        return self.table[idx] if 0 <= idx < len(self.table) else ""

    def add_list(self, strings: List[str]) -> List[int]:
        """Add list of strings, return indices"""
        return [self.add(s) for s in strings]


class V2LayeredEncoder:
    """Encode V1 format to V2 layered format"""

    def __init__(self):
        self.strings = StringTable()
        self.decisions: List[List] = []
        self.decision_map: Dict[str, int] = {}
        self.files: List[List] = []
        self.file_map: Dict[str, int] = {}
        self.patterns: List[List] = []
        self.pattern_map: Dict[str, int] = {}
        self.blockers: List[List] = []
        self.blocker_map: Dict[str, int] = {}
        self.next_steps: Dict[str, int] = {}

    def _timestamp_to_epoch(self, ts: Optional[str]) -> Optional[int]:
        """Convert ISO8601 timestamp to epoch seconds"""
        if not ts:
            return None
        try:
            dt = datetime.fromisoformat(ts.replace('Z', '+00:00'))
            return int(dt.timestamp())
        except:
            return None

    def _encode_decision(self, decision: Dict[str, Any]) -> int:
        """Encode decision and return its index"""
        dec_id = decision.get("id", "")

        if dec_id in self.decision_map:
            return self.decision_map[dec_id]

        idx = len(self.decisions)
        self.decisions.append([
            self.strings.add(dec_id),
            self.strings.add(decision.get("what", "")),
            self.strings.add(decision.get("why", "")),
            self.strings.add_list(decision.get("alt", [])),
            self.strings.add_list(decision.get("impact", []))
        ])
        self.decision_map[dec_id] = idx
        return idx

    def _encode_file(self, path: str, file_info: Dict[str, Any]) -> int:
        """Encode file and return its index"""
        if path in self.file_map:
            return self.file_map[path]

        idx = len(self.files)
        self.files.append([
            self.strings.add(path),
            ACTION.get(file_info.get("action", "modified"), 1),
            self.strings.add(file_info.get("role", "")),
            self.strings.add_list(file_info.get("deps", [])),
            STATUS.get(file_info.get("status", "complete"), 0)
        ])
        self.file_map[path] = idx
        return idx

    def _encode_pattern(self, name: str, desc: str) -> int:
        """Encode pattern and return its index"""
        if name in self.pattern_map:
            return self.pattern_map[name]

        idx = len(self.patterns)
        self.patterns.append([
            self.strings.add(name),
            self.strings.add(desc)
        ])
        self.pattern_map[name] = idx
        return idx

    def _encode_blocker(self, blocker: Dict[str, Any]) -> int:
        """Encode blocker and return its index"""
        block_id = blocker.get("id", "")

        if block_id in self.blocker_map:
            return self.blocker_map[block_id]

        idx = len(self.blockers)
        # Convert status to code (open=0, resolved=1, wontfix=2)
        status_map = {"open": 0, "resolved": 1, "wontfix": 2}
        status_str = blocker.get("status", "open")
        self.blockers.append([
            self.strings.add(block_id),
            self.strings.add(blocker.get("desc", "")),
            status_map.get(status_str, 0)
        ])
        self.blocker_map[block_id] = idx
        return idx

    def _encode_next_step(self, step: str) -> int:
        """Add next step to string table and return index"""
        return self.strings.add(step)

    def encode(self, v1_data: Dict[str, Any]) -> Dict[str, Any]:
        """Convert V1 format to V2 layered format"""

        v2 = {
            "v": "2.0",
            "meta": {
                "p": v1_data.get("project", ""),
                "c": self._timestamp_to_epoch(v1_data.get("created", "")),
                "u": self._timestamp_to_epoch(v1_data.get("updated", ""))
            },
            "strings": [],
            "sessions": [],
            "decisions": [],
            "files": [],
            "patterns": [],
            "blockers": []
        }

        # Process all sessions
        for session in v1_data.get("sessions", []):
            # First, encode all referenced entities
            decision_indices = [
                self._encode_decision(d)
                for d in session.get("decisions", [])
            ]

            file_indices = [
                self._encode_file(path, info)
                for path, info in session.get("files", {}).items()
            ]

            pattern_indices = [
                self._encode_pattern(name, desc)
                for name, desc in session.get("patterns", {}).items()
            ]

            blocker_indices = [
                self._encode_blocker(b)
                for b in session.get("blockers", [])
            ]

            next_indices = [
                self._encode_next_step(step)
                for step in session.get("next", [])
            ]

            # Encode session as array
            session_array = [
                self.strings.add(session.get("id", "")),
                self._timestamp_to_epoch(session.get("start", "")),
                self._timestamp_to_epoch(session.get("end")),
                self.strings.add(session.get("goal", "")),
                STATE.get(session.get("state", "in_progress"), 0),
                decision_indices,
                file_indices,
                pattern_indices,
                blocker_indices,
                next_indices
            ]

            # Add KV if present and non-empty
            kv = session.get("kv", {})
            if kv:
                session_array.append(kv)

            v2["sessions"].append(session_array)

        # Populate the deduplicated tables
        v2["strings"] = self.strings.table
        v2["decisions"] = self.decisions
        v2["files"] = self.files
        v2["patterns"] = self.patterns
        v2["blockers"] = self.blockers

        return v2


class V2LayeredDecoder:
    """Decode V2 layered format back to V1 format"""

    def __init__(self):
        self.strings: List[str] = []

    def _epoch_to_timestamp(self, epoch: Optional[int]) -> Optional[str]:
        """Convert epoch seconds to ISO8601 timestamp"""
        if epoch is None:
            return None
        try:
            dt = datetime.fromtimestamp(epoch)
            return dt.strftime("%Y-%m-%dT%H:%M:%SZ")
        except:
            return None

    def _get_string(self, idx: int) -> str:
        """Get string from table by index"""
        return self.strings[idx] if 0 <= idx < len(self.strings) else ""

    def _decode_decision(self, dec_array: List, decisions: List[List]) -> Dict[str, Any]:
        """Decode decision array to V1 format"""
        return {
            "id": self._get_string(dec_array[0]),
            "what": self._get_string(dec_array[1]),
            "why": self._get_string(dec_array[2]),
            "alt": [self._get_string(i) for i in dec_array[3]],
            "impact": [self._get_string(i) for i in dec_array[4]]
        }

    def _decode_file(self, file_array: List) -> tuple[str, Dict[str, Any]]:
        """Decode file array to V1 format"""
        path = self._get_string(file_array[0])
        info = {
            "action": ACTION_DECODE.get(file_array[1], "modified"),
            "role": self._get_string(file_array[2]),
            "deps": [self._get_string(i) for i in file_array[3]],
            "status": STATUS_DECODE.get(file_array[4], "complete")
        }
        return path, info

    def _decode_pattern(self, pattern_array: List) -> tuple[str, str]:
        """Decode pattern array to V1 format"""
        return (
            self._get_string(pattern_array[0]),
            self._get_string(pattern_array[1])
        )

    def _decode_blocker(self, blocker_array: List) -> Dict[str, Any]:
        """Decode blocker array to V1 format"""
        status_map = {0: "open", 1: "resolved", 2: "wontfix"}
        return {
            "id": self._get_string(blocker_array[0]),
            "desc": self._get_string(blocker_array[1]),
            "status": status_map.get(blocker_array[2], "open")
        }

    def decode(self, v2_data: Dict[str, Any]) -> Dict[str, Any]:
        """Convert V2 layered format to V1 format"""

        self.strings = v2_data.get("strings", [])

        v1 = {
            "v": "1.0",  # Output as V1 for compatibility
            "project": v2_data.get("meta", {}).get("p", ""),
            "created": self._epoch_to_timestamp(v2_data.get("meta", {}).get("c")),
            "updated": self._epoch_to_timestamp(v2_data.get("meta", {}).get("u")),
            "sessions": []
        }

        # Get lookup tables
        decisions = v2_data.get("decisions", [])
        files = v2_data.get("files", [])
        patterns = v2_data.get("patterns", [])
        blockers = v2_data.get("blockers", [])

        # Decode sessions
        for sess_array in v2_data.get("sessions", []):
            session = {
                "id": self._get_string(sess_array[0]),
                "start": self._epoch_to_timestamp(sess_array[1]),
                "end": self._epoch_to_timestamp(sess_array[2]),
                "goal": self._get_string(sess_array[3]),
                "state": STATE_DECODE.get(sess_array[4], "in_progress"),
                "decisions": [],
                "files": {},
                "patterns": {},
                "blockers": [],
                "next": [],
                "kv": {}
            }

            # Decode decisions by index
            for dec_idx in sess_array[5]:
                if 0 <= dec_idx < len(decisions):
                    session["decisions"].append(
                        self._decode_decision(decisions[dec_idx], decisions)
                    )

            # Decode files by index
            for file_idx in sess_array[6]:
                if 0 <= file_idx < len(files):
                    path, info = self._decode_file(files[file_idx])
                    session["files"][path] = info

            # Decode patterns by index
            for pat_idx in sess_array[7]:
                if 0 <= pat_idx < len(patterns):
                    name, desc = self._decode_pattern(patterns[pat_idx])
                    session["patterns"][name] = desc

            # Decode blockers by index
            for block_idx in sess_array[8]:
                if 0 <= block_idx < len(blockers):
                    session["blockers"].append(
                        self._decode_blocker(blockers[block_idx])
                    )

            # Decode next steps
            session["next"] = [
                self._get_string(idx) for idx in sess_array[9]
            ]

            # Add KV if present (position 10)
            if len(sess_array) > 10:
                session["kv"] = sess_array[10]

            v1["sessions"].append(session)

        return v1


class V2ContextManager:
    """Manage V2 layered context files"""

    def __init__(self, repo_root: str = "."):
        self.repo_root = Path(repo_root)
        self.v1_file = self.repo_root / ".session-ctx.json"
        self.v2_file = self.repo_root / ".session-ctx.v2.json"

    def convert_v1_to_v2(self, overwrite: bool = False) -> Dict[str, Any]:
        """Convert V1 file to V2 format

        Args:
            overwrite: If True, overwrites existing V2 file. Default False raises error if exists.
        """
        if not self.v1_file.exists():
            raise FileNotFoundError(f"V1 file not found: {self.v1_file}")

        if self.v2_file.exists() and not overwrite:
            raise FileExistsError(
                f"V2 file already exists: {self.v2_file}\n"
                f"Use overwrite=True to replace it, or delete it first."
            )

        with open(self.v1_file, 'r') as f:
            v1_data = json.load(f)

        encoder = V2LayeredEncoder()
        v2_data = encoder.encode(v1_data)

        with open(self.v2_file, 'w') as f:
            json.dump(v2_data, f, separators=(',', ':'))

        print(f"✓ Created V2 format: {self.v2_file}")
        print(f"  Original V1 file preserved: {self.v1_file}")
        return v2_data

    def convert_v2_to_v1(self, output_file: Optional[str] = None) -> Dict[str, Any]:
        """Convert V2 file to V1 format

        Args:
            output_file: Custom output filename. If None, uses '.session-ctx.v1-from-v2.json'
                        to avoid overwriting original V1 file.

        IMPORTANT: This does NOT overwrite .session-ctx.json by default!
        """
        if not self.v2_file.exists():
            raise FileNotFoundError(f"V2 file not found: {self.v2_file}")

        with open(self.v2_file, 'r') as f:
            v2_data = json.load(f)

        decoder = V2LayeredDecoder()
        v1_data = decoder.decode(v2_data)

        # Use safe output filename by default
        if output_file is None:
            output_path = self.repo_root / ".session-ctx.v1-from-v2.json"
        else:
            output_path = Path(output_file)

        with open(output_path, 'w') as f:
            json.dump(v1_data, f, indent=2)

        print(f"✓ Converted V2 to V1 format: {output_path}")
        if output_file is None:
            print(f"  Original V1 file NOT modified: {self.v1_file}")
        return v1_data

    def compare_sizes(self) -> Dict[str, Any]:
        """Compare V1 and V2 file sizes"""
        result = {}

        if self.v1_file.exists():
            v1_size = self.v1_file.stat().st_size
            with open(self.v1_file, 'r') as f:
                v1_content = f.read()
            result['v1'] = {
                'bytes': v1_size,
                'tokens_estimate': len(v1_content) // 4
            }

        if self.v2_file.exists():
            v2_size = self.v2_file.stat().st_size
            with open(self.v2_file, 'r') as f:
                v2_content = f.read()
            result['v2'] = {
                'bytes': v2_size,
                'tokens_estimate': len(v2_content) // 4
            }

        if 'v1' in result and 'v2' in result:
            result['savings'] = {
                'bytes': result['v1']['bytes'] - result['v2']['bytes'],
                'bytes_percent': round((1 - result['v2']['bytes'] / result['v1']['bytes']) * 100, 2),
                'tokens_percent': round((1 - result['v2']['tokens_estimate'] / result['v1']['tokens_estimate']) * 100, 2)
            }

        return result


def main():
    """CLI for V2 conversion"""
    import sys

    if len(sys.argv) < 2:
        print("Session Context V2 - Layered Format")
        print("\nUsage:")
        print("  python v2_layered_format.py v1-to-v2              # Convert V1 to V2 (safe)")
        print("  python v2_layered_format.py v1-to-v2 --force      # Overwrite existing V2")
        print("  python v2_layered_format.py v2-to-v1              # Convert V2 to V1 (safe)")
        print("  python v2_layered_format.py v2-to-v1 <file>       # Convert V2 to custom file")
        print("  python v2_layered_format.py compare               # Compare sizes")
        print("\nFile Structure:")
        print("  .session-ctx.json          - Original V1 format (NEVER overwritten)")
        print("  .session-ctx.v2.json       - V2 format")
        print("  .session-ctx.v1-from-v2.json - V2→V1 conversion output (safe)")
        sys.exit(1)

    manager = V2ContextManager()
    command = sys.argv[1]

    if command == "v1-to-v2":
        overwrite = "--force" in sys.argv or "-f" in sys.argv
        try:
            manager.convert_v1_to_v2(overwrite=overwrite)
            sizes = manager.compare_sizes()
            if 'savings' in sizes:
                print(f"  Size reduction: {sizes['savings']['bytes_percent']}%")
                print(f"  Token reduction: {sizes['savings']['tokens_percent']}%")
        except FileExistsError as e:
            print(f"Error: {e}")
            print("\nUse --force to overwrite existing V2 file")
            sys.exit(1)
        except Exception as e:
            print(f"Error: {e}")
            sys.exit(1)

    elif command == "v2-to-v1":
        output_file = sys.argv[2] if len(sys.argv) > 2 else None
        try:
            manager.convert_v2_to_v1(output_file=output_file)
        except Exception as e:
            print(f"Error: {e}")
            sys.exit(1)

    elif command == "compare":
        sizes = manager.compare_sizes()
        if 'v1' in sizes:
            print(f"V1 format (.session-ctx.json):")
            print(f"  Size: {sizes['v1']['bytes']:,} bytes")
            print(f"  Tokens: ~{sizes['v1']['tokens_estimate']:,}")
        if 'v2' in sizes:
            print(f"\nV2 format (.session-ctx.v2.json):")
            print(f"  Size: {sizes['v2']['bytes']:,} bytes")
            print(f"  Tokens: ~{sizes['v2']['tokens_estimate']:,}")
        if 'savings' in sizes:
            print(f"\nSavings (V2 vs V1):")
            print(f"  Size: {sizes['savings']['bytes']:,} bytes ({sizes['savings']['bytes_percent']}%)")
            print(f"  Tokens: ~{sizes['savings']['tokens_percent']}%")

    else:
        print(f"Unknown command: {command}")
        sys.exit(1)


if __name__ == "__main__":
    main()
