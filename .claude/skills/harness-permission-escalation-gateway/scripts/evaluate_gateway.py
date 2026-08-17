"""Permission Escalation Gateway Evaluator."""
import json
import sys
import argparse

def evaluate(tool: str, request_id: str, approvals_file: str) -> dict:
    risk_tiers = {
        "read_file": "LOW",
        "list_dir": "LOW",
        "write_file": "MEDIUM",
        "git_push": "CRITICAL"
    }
    risk = risk_tiers.get(tool, "HIGH")
    if risk == "LOW":
        return {"status": "AUTO_APPROVED", "risk": risk}
    if risk == "CRITICAL":
        try:
            with open(approvals_file, "r", encoding="utf-8-sig") as f:
                approvals = json.load(f)
        except FileNotFoundError:
            return {"status": "BLOCKED", "reason": "Approval ledger file not found"}
        except Exception:
            return {"status": "BLOCKED", "reason": "Approval ledger is unreadable or contains invalid JSON"}
        if not isinstance(approvals, dict):
            return {"status": "BLOCKED", "reason": "Approval ledger is unreadable or contains invalid JSON"}
        if request_id in approvals:
            return {"status": "APPROVED_BY_LEDGER", "signed_by": approvals[request_id]}
        return {"status": "BLOCKED", "reason": "Request ID is absent from the approval ledger"}
    return {"status": "LOGGED_AND_APPROVED", "risk": risk}

if __name__ == "__main__":
    print("Permission Escalation Gateway Evaluator active.")
