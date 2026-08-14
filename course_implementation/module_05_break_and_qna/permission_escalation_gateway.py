"""
Module 5: Risk-tiered permission gateway with a real approval ledger.

LOW reads a real file. MEDIUM writes a real file. CRITICAL requires an
approval record on disk before a pending-push artifact is written.
Nothing in this module runs `git push` or drops a database.
"""

from __future__ import annotations

import json
from pathlib import Path
import sys
from datetime import datetime, timezone
import uuid


sys.stdout.reconfigure(encoding="utf-8")

MODULE_DIR = Path(__file__).resolve().parent
OUTPUT_DIR = MODULE_DIR / "output"
sys.path.append(str(MODULE_DIR.parent))
from common.llm_client import CourseLLMClient  # noqa: E402


class PermissionEscalationGateway:
    """
    Risk matrix plus durable side effects.

    LOW     — read a file and return its bytes
    MEDIUM  — write a file
    HIGH    — record intent; do not install packages
    CRITICAL — require approvals.json[request_id] before writing
               pending_push.json. Never call git.
    """

    def __init__(self, workspace: Path) -> None:
        self.workspace = workspace
        self.workspace.mkdir(parents=True, exist_ok=True)
        self.audit_path = workspace / "audit.jsonl"
        self.approvals_path = workspace / "approvals.json"
        if not self.approvals_path.exists():
            self.approvals_path.write_text("{}", encoding="utf-8")
        self.risk_matrix = {
            "read_file": "LOW",
            "list_dir": "LOW",
            "grep": "LOW",
            "write_file": "MEDIUM",
            "run_test": "MEDIUM",
            "pip_install": "HIGH",
            "git_push": "CRITICAL",
            "db_drop": "CRITICAL",
        }
        self.llm_client = CourseLLMClient()

    def _log(self, event: dict) -> None:
        event = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            **event,
        }
        with self.audit_path.open("a", encoding="utf-8") as handle:
            handle.write(json.dumps(event) + "\n")

    def _approvals(self) -> dict:
        return json.loads(self.approvals_path.read_text(encoding="utf-8"))

    def grant_approval(self, request_id: str, actor: str) -> None:
        approvals = self._approvals()
        approvals[request_id] = {
            "actor": actor,
            "granted_at": datetime.now(timezone.utc).isoformat(),
        }
        self.approvals_path.write_text(
            json.dumps(approvals, indent=2), encoding="utf-8"
        )
        self._log({"event": "APPROVAL_GRANTED", "request_id": request_id, "actor": actor})

    def evaluate_request(self, tool_name: str, params: dict, request_id: str) -> dict:
        risk = self.risk_matrix.get(tool_name, "HIGH")
        print(
            f"\n[Escalation Gateway] Evaluating Request: Tool='{tool_name}' "
            f"| Risk Level={risk} | request_id={request_id}"
        )

        if risk == "LOW":
            path = self.workspace / params["path"]
            text = path.read_text(encoding="utf-8")
            self._log(
                {
                    "event": "AUTO_APPROVED",
                    "tool": tool_name,
                    "path": str(path),
                    "bytes": len(text),
                }
            )
            print(f"  [PASS] [AUTO-APPROVED] Read {path} ({len(text)} bytes).")
            return {"allowed": True, "content": text}

        if risk == "MEDIUM":
            path = self.workspace / params["path"]
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(params["content"], encoding="utf-8")
            self._log(
                {
                    "event": "LOGGED_AND_APPROVED",
                    "tool": tool_name,
                    "path": str(path),
                    "bytes": path.stat().st_size,
                }
            )
            print(f"  [PASS] [LOGGED & APPROVED] Wrote {path}.")
            return {"allowed": True, "path": str(path)}

        if risk == "HIGH":
            self._log(
                {
                    "event": "HIGH_RISK_LOGGED",
                    "tool": tool_name,
                    "params": params,
                    "installed": False,
                }
            )
            print(
                "  [PASS] [HIGH-RISK ALERT] Intent logged. "
                "No package was installed."
            )
            return {"allowed": True, "installed": False}

        approvals = self._approvals()
        if request_id not in approvals:
            self._log(
                {
                    "event": "ESCALATION_BLOCKED",
                    "tool": tool_name,
                    "request_id": request_id,
                }
            )
            print(
                "  [BLOCKED] [ESCALATION BLOCKED] Critical action requires "
                "an approval record in approvals.json."
            )
            return {"allowed": False, "reason": "missing_approval"}

        pending = {
            "request_id": request_id,
            "tool": tool_name,
            "params": params,
            "approved_by": approvals[request_id],
            "executed": False,
            "note": "git push was not executed; this is a pending-push record.",
        }
        pending_path = self.workspace / "pending_push.json"
        pending_path.write_text(json.dumps(pending, indent=2), encoding="utf-8")
        self._log(
            {
                "event": "CRITICAL_APPROVED_RECORDED",
                "tool": tool_name,
                "request_id": request_id,
                "pending_push": str(pending_path),
            }
        )
        print(
            f"  [PASS] [USER CONFIRMED] Wrote {pending_path}. "
            "git push was not executed."
        )
        return {"allowed": True, "pending_push": str(pending_path)}


def main() -> int:
    print("=" * 60)
    print("MODULE 5 DEMO: RISK-TIERED PERMISSION ESCALATION GATEWAY")
    print("=" * 60)

    OUTPUT_DIR.mkdir(exist_ok=True)
    for leftover in OUTPUT_DIR.iterdir():
        if leftover.is_file():
            leftover.unlink()

    source = OUTPUT_DIR / "src" / "main.py"
    source.parent.mkdir(parents=True, exist_ok=True)
    source.write_text("print('hello from module 5')\n", encoding="utf-8")

    gateway = PermissionEscalationGateway(OUTPUT_DIR)
    gateway.llm_client.complete("Determine risk tier for tool call git_push")

    read = gateway.evaluate_request(
        "read_file", {"path": "src/main.py"}, request_id="req-read"
    )
    write = gateway.evaluate_request(
        "write_file",
        {"path": "src/main.py", "content": "print('edited by gateway')\n"},
        request_id="req-write",
    )
    push_id = f"req-push-{uuid.uuid4().hex[:8]}"
    blocked = gateway.evaluate_request(
        "git_push", {"branch": "main", "remote": "origin"}, request_id=push_id
    )
    gateway.grant_approval(push_id, actor="developer")
    print(f"\n[Operator] Granted approval for {push_id} in {gateway.approvals_path}")
    confirmed = gateway.evaluate_request(
        "git_push", {"branch": "main", "remote": "origin"}, request_id=push_id
    )

    edited = (OUTPUT_DIR / "src" / "main.py").read_text(encoding="utf-8")
    pending_exists = (OUTPUT_DIR / "pending_push.json").is_file()
    audit_lines = gateway.audit_path.read_text(encoding="utf-8").splitlines()

    evidence = {
        "read_bytes": len(read.get("content", "")),
        "write_path": write.get("path"),
        "edited_source": edited,
        "blocked": blocked,
        "confirmed": confirmed,
        "pending_exists": pending_exists,
        "audit_events": len(audit_lines),
        "audit_path": str(gateway.audit_path),
        "approvals_path": str(gateway.approvals_path),
    }
    evidence_path = OUTPUT_DIR / "run_evidence.json"
    evidence_path.write_text(json.dumps(evidence, indent=2), encoding="utf-8")
    print(f"\n[OUTPUT] {evidence_path}")
    print(f"[OUTPUT] {gateway.audit_path}")
    print(f"[OUTPUT] {gateway.approvals_path}")

    ok = (
        read.get("allowed")
        and write.get("allowed")
        and blocked.get("allowed") is False
        and confirmed.get("allowed") is True
        and pending_exists
        and edited == "print('edited by gateway')\n"
        and len(audit_lines) >= 5
    )

    print("\n" + "=" * 60)
    if ok:
        print("MODULE 5 DEMO COMPLETE: Real reads, writes, and an approval ledger.")
        print("=" * 60)
        return 0
    print("MODULE 5 DEMO FAILED: a real side effect did not occur.")
    print("=" * 60)
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
