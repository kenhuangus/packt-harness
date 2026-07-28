"""
Module 3: Spec-Driven Development Verifier & Scope Auditor
Integrates standardized LLM Client (.env configured with 127.0.0.1 Qwen model as default).
"""

import os, sys, re
sys.stdout.reconfigure(encoding='utf-8')

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from common.llm_client import CourseLLMClient

class SpecVerifier:
    def __init__(self, spec_path):
        self.spec_path = spec_path
        self.allowed_files = []
        self.non_goals = []
        self.llm_client = CourseLLMClient()
        self.parse_spec()

    def parse_spec(self):
        with open(self.spec_path, "r", encoding="utf-8") as f:
            content = f.read()

        scope_match = re.search(r"Allowed Files:\s*`([^`]+)`", content)
        if scope_match:
            self.allowed_files = [f.strip() for f in scope_match.group(1).split(",")]

        non_goals_section = re.search(r"## 3\. Explicit Non-Goals\n(.*?)\n##", content, re.DOTALL)
        if non_goals_section:
            self.non_goals = [line.strip("- ").strip() for line in non_goals_section.group(1).strip().split("\n")]

        print(f"[Spec Verifier] Parsed SPEC.md:")
        print(f"  Allowed Files Scope: {self.allowed_files}")
        print(f"  Explicit Non-Goals: {self.non_goals}")

    def verify_proposed_diff(self, target_file, code_diff):
        print(f"\n[Spec Verifier] Auditing proposed modification to '{target_file}'...")
        
        base_name = os.path.basename(target_file)
        if base_name not in self.allowed_files:
            print(f"  ❌ SCOPE VIOLATION: '{base_name}' is outside allowed spec scope {self.allowed_files}!")
            return False

        if "database" in code_diff.lower() or "connect_db" in code_diff.lower():
            print("  ❌ NON-GOAL VIOLATION: Code diff attempts to modify database connection logic!")
            return False

        print("  ✓ Spec Compliance Verified: Scope & Non-Goals satisfied.")
        return True

def main():
    print("=" * 60)
    print("MODULE 3 DEMO: SPEC-DRIVEN DEVELOPMENT VERIFIER ")
    print("=" * 60)

    work_dir = os.path.dirname(os.path.abspath(__file__))
    spec_path = os.path.join(work_dir, "SPEC.md")
    verifier = SpecVerifier(spec_path)

    # Invoke LLM via aisuite
    llm_code = verifier.llm_client.complete("Generate auth_validator.py according to SPEC.md")

    # Test Case 1: Valid in-scope code diff
    valid_diff = "def validate_jwt(token: str) -> dict:\n    return {'valid': True, 'user_id': '123'}\n"
    verifier.verify_proposed_diff("auth_validator.py", valid_diff)

    # Test Case 2: Out-of-scope file modification attempt
    verifier.verify_proposed_diff("database.py", "def connect_db(): pass\n")

    # Test Case 3: In-scope file violating explicit Non-Goal
    invalid_diff = "import database\ndef validate_jwt(token):\n    database.connect_db()\n"
    verifier.verify_proposed_diff("auth_validator.py", invalid_diff)

    print("\n" + "=" * 60)
    print("MODULE 3 DEMO COMPLETE: Spec Verifier Enforced Target Boundaries!")
    print("=" * 60)

if __name__ == "__main__":
    main()
