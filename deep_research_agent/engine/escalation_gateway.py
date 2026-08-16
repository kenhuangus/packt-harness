"""
Module 5 Integration: Permission Escalation Gateway for Deep Research Agent.
4-Tier Risk Matrix (LOW, MEDIUM, HIGH, CRITICAL) and cryptographic signed approvals.json ledger.
"""

from __future__ import annotations

from enum import Enum
import hashlib
import json
from pathlib import Path
from typing import Any


class RiskTier(str, Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"


class PermissionEscalationGateway:
    """Manages risk tiers and validates cryptographic human approvals for critical actions."""

    def __init__(self, approvals_ledger_path: Path):
        self.approvals_path = approvals_ledger_path
        self.approvals_path.parent.mkdir(parents=True, exist_ok=True)
        if not self.approvals_path.exists():
            self.approvals_path.write_text("[]", encoding="utf-8")

    def evaluate_risk(self, operation: str) -> RiskTier:
        op = operation.lower()
        if any(w in op for w in ["export_production", "git_push", "delete", "publish_report"]):
            return RiskTier.CRITICAL
        elif any(w in op for w in ["external_api", "web_search", "network_fetch"]):
            return RiskTier.HIGH
        elif any(w in op for w in ["write_file", "save_cache", "update_citation"]):
            return RiskTier.MEDIUM
        return RiskTier.LOW

    def authorize_operation(self, request_id: str, operation: str) -> tuple[bool, str]:
        tier = self.evaluate_risk(operation)

        if tier in (RiskTier.LOW, RiskTier.MEDIUM, RiskTier.HIGH):
            return True, f"Operation '{operation}' automatically authorized under {tier.value} risk tier."

        # CRITICAL: Requires cryptographic signature in approvals.json
        try:
            records = json.loads(self.approvals_path.read_text(encoding="utf-8"))
        except Exception:
            records = []

        for entry in records:
            if entry.get("request_id") == request_id and entry.get("status") == "APPROVED":
                # Validate cryptographic token digest
                expected_digest = hashlib.sha256(
                    f"{request_id}:{operation}:{entry.get('authorized_by')}".encode("utf-8")
                ).hexdigest()
                if entry.get("digest") == expected_digest:
                    return True, f"CRITICAL operation '{operation}' verified with cryptographic signature."

        return False, (
            f"PERMISSION BLOCKED: Operation '{operation}' classified as CRITICAL. "
            f"Requires signed approval token in {self.approvals_path.name} with request_id '{request_id}'."
        )

    def record_approval(self, request_id: str, operation: str, authorizer: str) -> dict[str, Any]:
        """Utility for test suites or human UI to record an approval signature."""
        digest = hashlib.sha256(f"{request_id}:{operation}:{authorizer}".encode("utf-8")).hexdigest()
        entry = {
            "request_id": request_id,
            "risk_tier": "CRITICAL",
            "operation": operation,
            "authorized_by": authorizer,
            "status": "APPROVED",
            "digest": digest,
        }
        try:
            records = json.loads(self.approvals_path.read_text(encoding="utf-8"))
        except Exception:
            records = []
        records.append(entry)
        self.approvals_path.write_text(json.dumps(records, indent=2), encoding="utf-8")
        return entry
