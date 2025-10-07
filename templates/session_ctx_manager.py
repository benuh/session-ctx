#!/usr/bin/env python3
"""
Session Context Manager - Helper script for AI agents to manage .session-ctx.json

This script provides utilities for reading, updating, and managing session context files.
AI agents can use this to maintain context across sessions with minimal overhead.
"""

import json
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Any
import sys


class SessionContextManager:
    def __init__(self, repo_root: str = "."):
        self.ctx_file = Path(repo_root) / ".session-ctx.json"
        self.data: Dict[str, Any] = self._load_or_create()

    def _load_or_create(self) -> Dict[str, Any]:
        """Load existing context or create new one"""
        if self.ctx_file.exists():
            with open(self.ctx_file, 'r') as f:
                return json.load(f)
        else:
            return {
                "v": "1.0",
                "project": Path.cwd().name,
                "created": datetime.utcnow().isoformat() + "Z",
                "updated": datetime.utcnow().isoformat() + "Z",
                "sessions": []
            }

    def save(self):
        """Save context to file"""
        self.data["updated"] = datetime.utcnow().isoformat() + "Z"
        with open(self.ctx_file, 'w') as f:
            json.dump(self.data, f, indent=2)

    def start_session(self, goal: str, session_id: Optional[str] = None) -> str:
        """Start a new session"""
        if not session_id:
            session_id = f"s{len(self.data['sessions']) + 1}"

        session = {
            "id": session_id,
            "start": datetime.utcnow().isoformat() + "Z",
            "end": None,
            "goal": goal,
            "state": "in_progress",
            "decisions": [],
            "files": {},
            "patterns": {},
            "blockers": [],
            "next": [],
            "kv": {}
        }
        self.data["sessions"].append(session)
        self.save()
        return session_id

    def get_current_session(self) -> Optional[Dict]:
        """Get the most recent in-progress session"""
        for session in reversed(self.data["sessions"]):
            if session["state"] == "in_progress":
                return session
        return None

    def add_decision(self, what: str, why: str, alternatives: List[str], impact: List[str]):
        """Add an architecture decision to current session"""
        session = self.get_current_session()
        if not session:
            raise ValueError("No active session. Start a session first.")

        decision_id = f"d{len(session['decisions']) + 1}"
        session["decisions"].append({
            "id": decision_id,
            "what": what,
            "why": why,
            "alt": alternatives,
            "impact": impact
        })
        self.save()

    def update_file(self, file_path: str, action: str, role: str,
                   deps: List[str], status: str = "complete"):
        """Update file information in current session"""
        session = self.get_current_session()
        if not session:
            raise ValueError("No active session. Start a session first.")

        session["files"][file_path] = {
            "action": action,
            "role": role,
            "deps": deps,
            "status": status
        }
        self.save()

    def add_pattern(self, name: str, description: str):
        """Add a coding pattern to current session"""
        session = self.get_current_session()
        if not session:
            raise ValueError("No active session. Start a session first.")

        session["patterns"][name] = description
        self.save()

    def add_blocker(self, description: str, status: str = "open") -> str:
        """Add a blocker to current session"""
        session = self.get_current_session()
        if not session:
            raise ValueError("No active session. Start a session first.")

        blocker_id = f"b{len(session['blockers']) + 1}"
        session["blockers"].append({
            "id": blocker_id,
            "desc": description,
            "status": status
        })
        self.save()
        return blocker_id

    def update_next_steps(self, steps: List[str]):
        """Update next steps for current session"""
        session = self.get_current_session()
        if not session:
            raise ValueError("No active session. Start a session first.")

        session["next"] = steps
        self.save()

    def set_kv(self, key: str, value: str):
        """Set a key-value pair in current session"""
        session = self.get_current_session()
        if not session:
            raise ValueError("No active session. Start a session first.")

        session["kv"][key] = value
        self.save()

    def end_session(self, state: str = "completed"):
        """End the current session"""
        session = self.get_current_session()
        if not session:
            raise ValueError("No active session to end.")

        session["end"] = datetime.utcnow().isoformat() + "Z"
        session["state"] = state
        self.save()

    def get_context_summary(self) -> str:
        """Get a human-readable summary of the context"""
        summary = [f"Project: {self.data['project']}"]
        summary.append(f"Sessions: {len(self.data['sessions'])}")

        current = self.get_current_session()
        if current:
            summary.append(f"\nCurrent Session ({current['id']}):")
            summary.append(f"  Goal: {current['goal']}")
            summary.append(f"  State: {current['state']}")
            summary.append(f"  Decisions: {len(current['decisions'])}")
            summary.append(f"  Files: {len(current['files'])}")
            if current['next']:
                summary.append(f"  Next: {', '.join(current['next'])}")

        return "\n".join(summary)


def main():
    """CLI for manual context management"""
    if len(sys.argv) < 2:
        print("Usage: session_ctx_manager.py <command> [args...]")
        print("\nCommands:")
        print("  init <goal>              - Start a new session")
        print("  summary                  - Show context summary")
        print("  decision <what> <why>    - Add a decision")
        print("  file <path> <action> <role> - Update file info")
        print("  next <step1> [step2...]  - Set next steps")
        print("  end [state]              - End current session")
        sys.exit(1)

    manager = SessionContextManager()
    command = sys.argv[1]

    if command == "init":
        goal = sys.argv[2] if len(sys.argv) > 2 else "general_work"
        session_id = manager.start_session(goal)
        print(f"Started session {session_id} with goal: {goal}")

    elif command == "summary":
        print(manager.get_context_summary())

    elif command == "decision":
        what = sys.argv[2]
        why = sys.argv[3]
        manager.add_decision(what, why, [], [])
        print(f"Added decision: {what}")

    elif command == "file":
        file_path = sys.argv[2]
        action = sys.argv[3]
        role = sys.argv[4]
        manager.update_file(file_path, action, role, [])
        print(f"Updated file: {file_path}")

    elif command == "next":
        steps = sys.argv[2:]
        manager.update_next_steps(steps)
        print(f"Set next steps: {', '.join(steps)}")

    elif command == "end":
        state = sys.argv[2] if len(sys.argv) > 2 else "completed"
        manager.end_session(state)
        print(f"Ended session with state: {state}")

    else:
        print(f"Unknown command: {command}")
        sys.exit(1)


if __name__ == "__main__":
    main()
