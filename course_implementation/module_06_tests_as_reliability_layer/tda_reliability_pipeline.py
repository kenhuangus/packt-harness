"""
Module 6: Test-Driven Agent (TDA) & Anti-Regression Pipeline
Integrates standardized LLM Client (.env configured with 127.0.0.1 Qwen model as default).
"""

import sys, os
sys.stdout.reconfigure(encoding='utf-8')

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from common.llm_client import CourseLLMClient

class TDAReliabilityPipeline:
    def __init__(self):
        self.regression_suite = []
        self.llm_client = CourseLLMClient()

    def run_test_suite(self, code_under_test):
        print("\n[TDA Pipeline] Running automated test suite against proposed code...")
        
        if "ZeroDivisionError" in code_under_test or " / 0" in code_under_test:
            traceback = (
                "Traceback (most recent call last):\n"
                "  File 'calculator.py', line 4, in divide\n"
                "    return a / b\n"
                "ZeroDivisionError: division by zero\n"
                "FAILED tests/test_calc.py::test_divide_by_zero"
            )
            print("  ❌ Test Run Failed! Traceback captured automatically.")
            return {"passed": False, "traceback": traceback}
        else:
            print("  ✓ All unit tests PASSED (100% coverage).")
            return {"passed": True, "traceback": None}

    def format_fix_prompt(self, traceback_str):
        print("\n[TDA Pipeline] Formatting captured traceback into agent repair prompt:")
        prompt = f"System Instruction: Fix the following test failure traceback:\n```\n{traceback_str}\n```"
        print("--- REPAIR PROMPT GENERATED ---")
        print(prompt)
        
        # Pass traceback repair prompt to aisuite LLM
        fix_response = self.llm_client.complete(prompt, system_prompt="You are a TDA repair agent.")
        return prompt

    def register_anti_regression_test(self, bug_name, test_code):
        self.regression_suite.append({"name": bug_name, "code": test_code})
        print(f"\n[Anti-Regression Pipeline] Registered new regression safeguard: '{bug_name}' (Total Safeguards: {len(self.regression_suite)})")

def main():
    print("=" * 60)
    print("MODULE 6 DEMO: TEST-DRIVEN AGENT (TDA) & ANTI-REGRESSION PIPELINE ")
    print("=" * 60)

    tda = TDAReliabilityPipeline()

    # 1. Simulate failing code run
    failing_code = "def divide(a, b):\n    return a / b  # Bug: ZeroDivisionError"
    res = tda.run_test_suite(failing_code)

    # 2. Extract traceback & format repair prompt
    if not res["passed"]:
        repair_prompt = tda.format_fix_prompt(res["traceback"])

    # 3. Simulate repaired code run
    fixed_code = "def divide(a, b):\n    if b == 0: return 0\n    return a / b"
    res_fixed = tda.run_test_suite(fixed_code)

    # 4. Register anti-regression safeguard
    if res_fixed["passed"]:
        tda.register_anti_regression_test("test_divide_zero_guard", "def test_divide_zero_guard(): assert divide(10, 0) == 0")

    print("\n" + "=" * 60)
    print("MODULE 6 DEMO COMPLETE: TDA Automated Feedback Loop Active!")
    print("=" * 60)

if __name__ == "__main__":
    main()
