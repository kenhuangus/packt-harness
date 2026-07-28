"""
Module 2: Core Harness Stack & System Architecture
Demonstrates the 5 pillars of a production AI coding harness:
1. Memory Files (CLAUDE.md / AGENTS.md)
2. Scoped Tools & Path Sandboxing
3. Deterministic Hooks & Policy Engine
4. Context Token Budgeting & Compacting
5. JSONL Tracing & Observability
"""

import os
import json
from datetime import datetime, timezone

class ContextTokenBudgeter:
    """Manages token allocation and compacts long context windows to prevent amnesia."""
    def __init__(self, max_tokens=128000):
        self.max_tokens = max_tokens
        self.allocations = {
            'memory': int(max_tokens * 0.20),
            'spec': int(max_tokens * 0.20),
            'workspace': int(max_tokens * 0.50),
            'output_buffer': int(max_tokens * 0.10)
        }
        
    def estimate_tokens(self, text: str) -> int:
        # Standard token estimation: ~1.33 tokens per word
        words = text.split()
        return int(len(words) * 1.33)
        
    def compact_output(self, raw_output: str, max_lines=20) -> str:
        lines = raw_output.splitlines()
        if len(lines) <= max_lines:
            return raw_output
        header = lines[:5]
        footer = lines[-15:]
        omitted_count = len(lines) - 20
        return "\n".join(header) + f"\n\n... [HARNESS COMPACTION: Omitted {omitted_count} lines of compiler stdout] ...\n\n" + "\n".join(footer)

class CoreHarnessStack:
    def __init__(self, workspace_root: str):
        self.workspace_root = os.path.abspath(workspace_root)
        self.audit_log_path = os.path.join(self.workspace_root, "events.jsonl")
        self.budgeter = ContextTokenBudgeter()

    def log_event(self, event_type: str, details: dict):
        payload = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "event_type": event_type,
            "details": details
        }
        with open(self.audit_log_path, "a", encoding="utf-8") as f:
            f.write(json.dumps(payload) + "\n")

    def validate_tool_permission(self, tool_name: str, target_path: str = None) -> bool:
        allowed_tools = ["read_file", "write_file", "run_test", "list_dir"]
        if tool_name not in allowed_tools:
            self.log_event("PERMISSION_DENIED", {"reason": f"Tool '{tool_name}' not in allowed tool set."})
            return False

        if target_path:
            abs_target = os.path.abspath(target_path)
            if not abs_target.startswith(self.workspace_root):
                self.log_event("PATH_TRAVERSAL_BLOCKED", {"path": target_path, "workspace": self.workspace_root})
                return False

        self.log_event("PERMISSION_GRANTED", {"tool": tool_name, "path": target_path})
        return True

    def run_post_edit_hook(self, file_path: str, code_content: str) -> bool:
        if "sk-proj-" in code_content:
            self.log_event("SECURITY_VIOLATION", {"file": file_path, "issue": "Hardcoded OpenAI secret key detected!"})
            return False

        if not code_content.strip():
            self.log_event("QUALITY_VIOLATION", {"file": file_path, "issue": "Empty code edit proposal."})
            return False

        self.log_event("HOOK_PASS", {"file": file_path, "status": "Post-edit checks passed."})
        return True

if __name__ == "__main__":
    workspace = os.path.abspath(".")
    harness = CoreHarnessStack(workspace)
    print("Core Harness Stack & Context Token Budgeter initialized successfully!")
    print("Allocations:", harness.budgeter.allocations)
