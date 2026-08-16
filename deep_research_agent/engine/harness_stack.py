"""
Module 1 & 2 Integration: Core Harness Stack for Deep Research Agent.
Provides LoopDetector (deque-10 hashing), ContextTokenBudgeter (20/20/50/10 split),
PathSanitizer (Path.resolve().is_relative_to), and EventLogger (append-only JSONL).
"""

from __future__ import annotations

import collections
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
from typing import Any


class LoopDetector:
    """Detects and intercepts recursive execution loops and repeated queries."""

    def __init__(self, threshold: int = 2, maxlen: int = 10):
        self.threshold = threshold
        self.maxlen = maxlen
        self.call_history: collections.deque[str] = collections.deque(maxlen=maxlen)
        self.signature_counts: collections.defaultdict[str, int] = collections.defaultdict(int)

    def record_call(self, tool_name: str, **kwargs: Any) -> tuple[bool, str]:
        """Returns (action_allowed, signature_hash)."""
        payload = json.dumps({"tool": tool_name, "args": kwargs}, sort_keys=True)
        sig = hashlib.sha256(payload.encode("utf-8")).hexdigest()[:16]

        self.call_history.append(sig)
        self.signature_counts[sig] += 1

        if self.signature_counts[sig] >= self.threshold:
            return False, sig
        return True, sig

    def reset(self) -> None:
        self.call_history.clear()
        self.signature_counts.clear()


class ContextTokenBudgeter:
    """Manages token budgets: 20% system/spec, 20% tools, 50% documents/evidence, 10% response."""

    def __init__(self, max_tokens: int = 8000):
        self.max_tokens = max_tokens
        self.allocations = {
            "system_spec": int(max_tokens * 0.20),
            "tool_defs": int(max_tokens * 0.20),
            "evidence_docs": int(max_tokens * 0.50),
            "response": int(max_tokens * 0.10),
        }

    def compact_evidence(self, text: str, max_chars: int = 2500) -> str:
        """Compact long research evidence keeping head and tail."""
        if len(text) <= max_chars:
            return text
        head_len = int(max_chars * 0.6)
        tail_len = int(max_chars * 0.4)
        omitted = len(text) - (head_len + tail_len)
        return (
            text[:head_len]
            + f"\n\n[... OMITTED {omitted} CHARACTERS OF EVIDENCE FOR TOKEN BUDGET ...]\n\n"
            + text[-tail_len:]
        )


class PathSanitizer:
    """Enforces strict filesystem sandboxing."""

    def __init__(self, workspace_root: Path):
        self.workspace_root = workspace_root.resolve()
        self.workspace_root.mkdir(parents=True, exist_ok=True)

    def validate_path(self, target_path: str | Path) -> Path:
        resolved = (self.workspace_root / target_path).resolve()
        if not resolved.is_relative_to(self.workspace_root):
            raise PermissionError(
                f"Path traversal blocked: '{target_path}' is outside sandbox '{self.workspace_root}'"
            )
        return resolved


class EventLogger:
    """Appends structured audit records to events.jsonl."""

    def __init__(self, log_path: Path):
        self.log_path = log_path
        self.log_path.parent.mkdir(parents=True, exist_ok=True)

    def log(self, event_type: str, details: dict[str, Any]) -> dict[str, Any]:
        record = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "event_type": event_type,
            "details": details,
        }
        with open(self.log_path, "a", encoding="utf-8") as f:
            f.write(json.dumps(record, ensure_ascii=False) + "\n")
        return record
