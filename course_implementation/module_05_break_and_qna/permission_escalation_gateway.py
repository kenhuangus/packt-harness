"""
Module 5: Risk-Tiered Permission Escalation Gateway
Integrates standardized LLM Client (.env configured with 127.0.0.1 Qwen model as default).
"""

import sys, os
sys.stdout.reconfigure(encoding='utf-8')

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from common.llm_client import CourseLLMClient

class PermissionEscalationGateway:
    """
    Risk-tiered approval gate for tool calls.

    LOW    — read-only tools, auto-approve
    MEDIUM — non-destructive writes/tests, log then approve
    HIGH   — package installs, extra logging, still allowed here
    CRITICAL — git_push / db_drop: blocked unless the caller supplies
               an explicit user confirmation (user_auto_approve=True)

    The demo never opens a real confirmation UI. The boolean stands in
    for a modal click so the two CRITICAL outcomes can be shown in one run.
    """

    def __init__(self):
        self.risk_matrix = {
            "read_file": "LOW",
            "list_dir": "LOW",
            "grep": "LOW",
            "write_file": "MEDIUM",
            "run_test": "MEDIUM",
            "pip_install": "HIGH",
            "git_push": "CRITICAL",
            "db_drop": "CRITICAL"
        }
        self.llm_client = CourseLLMClient()

    def evaluate_request(self, tool_name, params, user_auto_approve=False):
        """Return True when the request may proceed under the risk matrix."""
        # Unknown tools default to HIGH so they are never silently treated as LOW.
        risk = self.risk_matrix.get(tool_name, "HIGH")
        print(f"\n[Escalation Gateway] Evaluating Request: Tool='{tool_name}' | Risk Level={risk}")

        if risk == "LOW":
            print("  ✓ [AUTO-APPROVED] Low-risk tool call permitted instantly.")
            return True
        elif risk == "MEDIUM":
            print("  ✓ [LOGGED & APPROVED] Medium-risk tool call executed and logged to audit trace.")
            return True
        elif risk == "HIGH":
            print("  ⚠️ [HIGH-RISK ALERT] Tool requires heightened logging.")
            return True
        elif risk == "CRITICAL":
            if user_auto_approve:
                print("  ✓ [USER CONFIRMED] Critical action approved by developer modal prompt.")
                return True
            else:
                print("  ❌ [ESCALATION BLOCKED] Critical action requires explicit developer click approval!")
                return False

def main():
    print("=" * 60)
    print("MODULE 5 DEMO: RISK-TIERED PERMISSION ESCALATION GATEWAY ")
    print("=" * 60)

    gateway = PermissionEscalationGateway()

    # Optional LLM call. The matrix below is deterministic and does not
    # take the model's answer as an approval signal.
    llm_req = gateway.llm_client.complete("Determine risk tier for tool call git_push")

    # 1. LOW: read_file is auto-approved.
    gateway.evaluate_request("read_file", {"path": "src/main.py"})

    # 2. MEDIUM: write_file is logged and approved.
    gateway.evaluate_request("write_file", {"path": "src/main.py"})

    # 3. CRITICAL without a confirmation click: blocked.
    gateway.evaluate_request("git_push", {"branch": "main"}, user_auto_approve=False)

    # 4. Same CRITICAL action after the developer confirms: allowed.
    gateway.evaluate_request("git_push", {"branch": "main"}, user_auto_approve=True)

    print("\n" + "=" * 60)
    print("MODULE 5 DEMO COMPLETE: Escalation Gateway Risk Matrix Active!")
    print("=" * 60)

if __name__ == "__main__":
    main()
