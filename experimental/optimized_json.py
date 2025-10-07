#!/usr/bin/env python3
"""
Optimized JSON Implementation for session-ctx

This implementation creates a minified, token-efficient JSON format
that's still readable by LLMs but uses fewer tokens.

Strategies:
1. Minification (no whitespace)
2. Aggressive abbreviation
3. Numeric codes for common values
4. Array-based structure instead of objects where possible
"""

import json
from pathlib import Path
from typing import Dict, Any, List


# Value code mappings
STATE_CODES = {
    "in_progress": 0,
    "completed": 1,
    "blocked": 2
}

STATE_DECODE = {v: k for k, v in STATE_CODES.items()}

ACTION_CODES = {
    "created": 0,
    "modified": 1,
    "deleted": 2
}

ACTION_DECODE = {v: k for k, v in ACTION_CODES.items()}

STATUS_CODES = {
    "complete": 0,
    "partial": 1,
    "blocked": 2
}

STATUS_DECODE = {v: k for k, v in STATUS_CODES.items()}


class OptimizedJSONContext:
    """Manage optimized JSON session context"""

    def __init__(self, repo_root: str = "."):
        self.repo_root = Path(repo_root)
        self.normal_file = self.repo_root / ".session-ctx.json"
        self.optimized_file = self.repo_root / ".session-ctx.min.json"

    def optimize(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Convert normal format to optimized format"""
        optimized = {
            "v": data.get("v", "1.0"),
            "p": data.get("project", ""),
            "c": data.get("created", ""),
            "u": data.get("updated", ""),
            "s": []
        }

        for session in data.get("sessions", []):
            opt_session = {
                "i": session.get("id", ""),
                "st": session.get("start", ""),
                "e": session.get("end"),
                "g": session.get("goal", ""),
                "state": STATE_CODES.get(session.get("state", "in_progress"), 0),
                "d": [],
                "f": {},
                "p": session.get("patterns", {}),
                "b": [],
                "n": session.get("next", []),
                "k": session.get("kv", {})
            }

            # Optimize decisions
            for decision in session.get("decisions", []):
                opt_session["d"].append({
                    "i": decision.get("id", ""),
                    "w": decision.get("what", ""),
                    "y": decision.get("why", ""),
                    "a": decision.get("alt", []),
                    "imp": decision.get("impact", [])
                })

            # Optimize files
            for file_path, file_info in session.get("files", {}).items():
                opt_session["f"][file_path] = {
                    "a": ACTION_CODES.get(file_info.get("action", "modified"), 1),
                    "r": file_info.get("role", ""),
                    "d": file_info.get("deps", []),
                    "s": STATUS_CODES.get(file_info.get("status", "complete"), 0)
                }

            # Optimize blockers
            for blocker in session.get("blockers", []):
                opt_session["b"].append({
                    "i": blocker.get("id", ""),
                    "d": blocker.get("desc", ""),
                    "s": blocker.get("status", "open")
                })

            optimized["s"].append(opt_session)

        return optimized

    def normalize(self, optimized: Dict[str, Any]) -> Dict[str, Any]:
        """Convert optimized format back to normal format"""
        normal = {
            "v": optimized.get("v", "1.0"),
            "project": optimized.get("p", ""),
            "created": optimized.get("c", ""),
            "updated": optimized.get("u", ""),
            "sessions": []
        }

        for opt_session in optimized.get("s", []):
            session = {
                "id": opt_session.get("i", ""),
                "start": opt_session.get("st", ""),
                "end": opt_session.get("e"),
                "goal": opt_session.get("g", ""),
                "state": STATE_DECODE.get(opt_session.get("state", 0), "in_progress"),
                "decisions": [],
                "files": {},
                "patterns": opt_session.get("p", {}),
                "blockers": [],
                "next": opt_session.get("n", []),
                "kv": opt_session.get("k", {})
            }

            # Normalize decisions
            for opt_decision in opt_session.get("d", []):
                session["decisions"].append({
                    "id": opt_decision.get("i", ""),
                    "what": opt_decision.get("w", ""),
                    "why": opt_decision.get("y", ""),
                    "alt": opt_decision.get("a", []),
                    "impact": opt_decision.get("imp", [])
                })

            # Normalize files
            for file_path, opt_file in opt_session.get("f", {}).items():
                session["files"][file_path] = {
                    "action": ACTION_DECODE.get(opt_file.get("a", 1), "modified"),
                    "role": opt_file.get("r", ""),
                    "deps": opt_file.get("d", []),
                    "status": STATUS_DECODE.get(opt_file.get("s", 0), "complete")
                }

            # Normalize blockers
            for opt_blocker in opt_session.get("b", []):
                session["blockers"].append({
                    "id": opt_blocker.get("i", ""),
                    "desc": opt_blocker.get("d", ""),
                    "status": opt_blocker.get("s", "open")
                })

            normal["sessions"].append(session)

        return normal

    def save_optimized(self, data: Dict[str, Any]):
        """Save in optimized format (minified)"""
        optimized = self.optimize(data)
        # Save without whitespace
        with open(self.optimized_file, 'w') as f:
            json.dump(optimized, f, separators=(',', ':'))

    def load_optimized(self) -> Dict[str, Any]:
        """Load optimized format and convert to normal"""
        with open(self.optimized_file, 'r') as f:
            optimized = json.load(f)
        return self.normalize(optimized)

    def convert_to_optimized(self):
        """Convert existing .session-ctx.json to optimized format"""
        with open(self.normal_file, 'r') as f:
            data = json.load(f)
        self.save_optimized(data)

    def get_size_comparison(self) -> Dict[str, Any]:
        """Compare file sizes and token counts"""
        sizes = {}

        if self.normal_file.exists():
            normal_size = self.normal_file.stat().st_size
            with open(self.normal_file, 'r') as f:
                normal_content = f.read()
            normal_tokens = len(normal_content) // 4  # Rough token estimate

            sizes['normal'] = {
                'bytes': normal_size,
                'tokens_estimate': normal_tokens
            }

        if self.optimized_file.exists():
            opt_size = self.optimized_file.stat().st_size
            with open(self.optimized_file, 'r') as f:
                opt_content = f.read()
            opt_tokens = len(opt_content) // 4  # Rough token estimate

            sizes['optimized'] = {
                'bytes': opt_size,
                'tokens_estimate': opt_tokens
            }

        if 'normal' in sizes and 'optimized' in sizes:
            sizes['reduction'] = {
                'bytes_percent': round((1 - opt_size / normal_size) * 100, 2),
                'tokens_percent': round((1 - opt_tokens / normal_tokens) * 100, 2)
            }

        return sizes


def main():
    """CLI for optimized JSON conversion"""
    import sys

    if len(sys.argv) < 2:
        print("Usage:")
        print("  python optimized_json.py optimize    # Convert to optimized format")
        print("  python optimized_json.py normalize   # Convert back to normal format")
        print("  python optimized_json.py compare     # Compare sizes")
        sys.exit(1)

    manager = OptimizedJSONContext()
    command = sys.argv[1]

    if command == "optimize":
        manager.convert_to_optimized()
        print("✓ Converted to optimized format")
        sizes = manager.get_size_comparison()
        if 'reduction' in sizes:
            print(f"  Size reduction: {sizes['reduction']['bytes_percent']}%")
            print(f"  Token reduction: {sizes['reduction']['tokens_percent']}%")

    elif command == "normalize":
        data = manager.load_optimized()
        with open(manager.normal_file, 'w') as f:
            json.dump(data, f, indent=2)
        print("✓ Converted to normal format")

    elif command == "compare":
        sizes = manager.get_size_comparison()
        if 'normal' in sizes:
            print(f"Normal format:")
            print(f"  Size: {sizes['normal']['bytes']:,} bytes")
            print(f"  Tokens: ~{sizes['normal']['tokens_estimate']:,}")
        if 'optimized' in sizes:
            print(f"\nOptimized format:")
            print(f"  Size: {sizes['optimized']['bytes']:,} bytes")
            print(f"  Tokens: ~{sizes['optimized']['tokens_estimate']:,}")
        if 'reduction' in sizes:
            print(f"\nReduction:")
            print(f"  Size: {sizes['reduction']['bytes_percent']}%")
            print(f"  Tokens: {sizes['reduction']['tokens_percent']}%")

    else:
        print(f"Unknown command: {command}")
        sys.exit(1)


if __name__ == "__main__":
    main()
