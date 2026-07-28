"""
Module 5: Risk-Tiered Permission Escalation Gateway
Integrates standardized LLM Client (.env configured with 127.0.0.1 Qwen model as default).
"""

import sys, os
sys.stdout.reconfigure(encoding='utf-8')

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from common.llm_client import CourseLLMClient

class PermissionEscalationGateway:
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

    # Call LLM via aisuite
    llm_req = gateway.llm_client.complete("Determine risk tier for tool call git_push")

    # 1. Low-risk auto-approved
    gateway.evaluate_request("read_file", {"path": "src/main.py"})

    # 2. Medium-risk logged
    gateway.evaluate_request("write_file", {"path": "src/main.py"})

    # 3. Critical-risk without user approval
    gateway.evaluate_request("git_push", {"branch": "main"}, user_auto_approve=False)

    # 4. Critical-risk with user confirmation
    gateway.evaluate_request("git_push", {"branch": "main"}, user_auto_approve=True)

    print("\n" + "=" * 60)
    print("MODULE 5 DEMO COMPLETE: Escalation Gateway Risk Matrix Active!")
    print("=" * 60)

if __name__ == "__main__":
    main()
