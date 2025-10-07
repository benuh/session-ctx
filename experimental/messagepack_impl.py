#!/usr/bin/env python3
"""
MessagePack Implementation for session-ctx

MessagePack is a binary serialization format that's more compact than JSON.
This implementation converts session-ctx to/from MessagePack format.

Install: pip install msgpack
"""

import msgpack
import json
from pathlib import Path
from datetime import datetime
from typing import Dict, Any


class MessagePackSessionContext:
    """Manage session context in MessagePack format"""

    def __init__(self, repo_root: str = "."):
        self.repo_root = Path(repo_root)
        self.json_file = self.repo_root / ".session-ctx.json"
        self.msgpack_file = self.repo_root / ".session-ctx.msgpack"

    def json_to_msgpack(self) -> bytes:
        """Convert JSON context to MessagePack"""
        if not self.json_file.exists():
            raise FileNotFoundError(f"{self.json_file} not found")

        with open(self.json_file, 'r') as f:
            data = json.load(f)

        # Pack to MessagePack
        packed = msgpack.packb(data, use_bin_type=True)

        # Save to file
        with open(self.msgpack_file, 'wb') as f:
            f.write(packed)

        return packed

    def msgpack_to_json(self) -> Dict[str, Any]:
        """Convert MessagePack context to JSON"""
        if not self.msgpack_file.exists():
            raise FileNotFoundError(f"{self.msgpack_file} not found")

        with open(self.msgpack_file, 'rb') as f:
            packed = f.read()

        # Unpack from MessagePack
        data = msgpack.unpackb(packed, raw=False)

        # Save to JSON
        with open(self.json_file, 'w') as f:
            json.dump(data, f, indent=2)

        return data

    def load_context(self) -> Dict[str, Any]:
        """
        Load context, preferring MessagePack if available and newer
        Falls back to JSON if MessagePack doesn't exist
        """
        json_exists = self.json_file.exists()
        msgpack_exists = self.msgpack_file.exists()

        if msgpack_exists and json_exists:
            # Check which is newer
            json_mtime = self.json_file.stat().st_mtime
            msgpack_mtime = self.msgpack_file.stat().st_mtime

            if msgpack_mtime >= json_mtime:
                # MessagePack is newer, use it
                with open(self.msgpack_file, 'rb') as f:
                    return msgpack.unpackb(f.read(), raw=False)

        # Fall back to JSON
        if json_exists:
            with open(self.json_file, 'r') as f:
                return json.load(f)

        raise FileNotFoundError("No context file found")

    def save_context(self, data: Dict[str, Any], format: str = "both"):
        """
        Save context in specified format(s)

        Args:
            data: Context data
            format: "json", "msgpack", or "both"
        """
        if format in ["json", "both"]:
            with open(self.json_file, 'w') as f:
                json.dump(data, f, indent=2)

        if format in ["msgpack", "both"]:
            packed = msgpack.packb(data, use_bin_type=True)
            with open(self.msgpack_file, 'wb') as f:
                f.write(packed)

    def get_size_comparison(self) -> Dict[str, int]:
        """Compare file sizes"""
        sizes = {}

        if self.json_file.exists():
            sizes['json'] = self.json_file.stat().st_size

        if self.msgpack_file.exists():
            sizes['msgpack'] = self.msgpack_file.stat().st_size

        if 'json' in sizes and 'msgpack' in sizes:
            sizes['reduction_percent'] = round(
                (1 - sizes['msgpack'] / sizes['json']) * 100, 2
            )

        return sizes


def main():
    """CLI for MessagePack conversion"""
    import sys

    if len(sys.argv) < 2:
        print("Usage:")
        print("  python messagepack_impl.py to-msgpack    # Convert JSON to MessagePack")
        print("  python messagepack_impl.py to-json       # Convert MessagePack to JSON")
        print("  python messagepack_impl.py compare       # Compare sizes")
        print("  python messagepack_impl.py load          # Load context (auto-detect format)")
        sys.exit(1)

    manager = MessagePackSessionContext()
    command = sys.argv[1]

    if command == "to-msgpack":
        packed = manager.json_to_msgpack()
        print(f"✓ Converted to MessagePack: {len(packed)} bytes")
        sizes = manager.get_size_comparison()
        if 'reduction_percent' in sizes:
            print(f"  Size reduction: {sizes['reduction_percent']}%")

    elif command == "to-json":
        data = manager.msgpack_to_json()
        print(f"✓ Converted to JSON")
        print(f"  Project: {data.get('project', 'unknown')}")
        print(f"  Sessions: {len(data.get('sessions', []))}")

    elif command == "compare":
        sizes = manager.get_size_comparison()
        if 'json' in sizes:
            print(f"JSON size:       {sizes['json']:,} bytes")
        if 'msgpack' in sizes:
            print(f"MessagePack size: {sizes['msgpack']:,} bytes")
        if 'reduction_percent' in sizes:
            print(f"Reduction:        {sizes['reduction_percent']}%")

    elif command == "load":
        data = manager.load_context()
        print(f"✓ Loaded context")
        print(f"  Project: {data.get('project', 'unknown')}")
        print(f"  Sessions: {len(data.get('sessions', []))}")
        print(f"  Updated: {data.get('updated', 'unknown')}")

    else:
        print(f"Unknown command: {command}")
        sys.exit(1)


if __name__ == "__main__":
    main()
