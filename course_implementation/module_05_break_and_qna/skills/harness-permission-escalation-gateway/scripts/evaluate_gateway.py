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
            with open(approvals_file, "r") as f:
                approvals = json.load(f)
            if request_id in approvals:
                return {"status": "APPROVED_BY_LEDGER", "signed_by": approvals[request_id]}
        except Exception:
            pass
        return {"status": "BLOCKED", "reason": "Requires human approval token in approvals.json"}
    return {"status": "LOGGED_AND_APPROVED", "risk": risk}

if __name__ == "__main__":
    print("Permission Escalation Gateway Evaluator active.")
