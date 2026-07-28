"""
Module 1: Harness vs. Un-Harnessed Model Execution Simulator
Demonstrates:
1. Failure Mode 1: Infinite Loop Runaway
2. Failure Mode 2: Unsanitized Dangerous Command Execution
3. Failure Mode 3: Context Decay & Amnesia
4. Harness Interceptor Mitigation
5. standardized LLM Client integration via `.env` (local Qwen on 127.0.0.1 default)
"""

import sys, os, time, re
sys.stdout.reconfigure(encoding='utf-8')

# Import common LLM client with aisuite & .env support
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from common.llm_client import CourseLLMClient

class UnharnessedAgentSimulator:
    """Simulates a raw model execution without system scaffolding."""
    def __init__(self, llm_client):
        self.llm_client = llm_client

    def run_task(self, prompt):
        print("\n--- UN-HARNESSED AGENT SIMULATION ---")
        
        # Invoke aisuite LLM Client
        response = self.llm_client.complete(prompt, system_prompt="You are an un-harnessed coding agent.")
        print(f"[LLM Response Output]: {response[:60]}...")
        
        # Simulate infinite loop failure mode
        print("[LLM Attempt 1] Trying command: pytest tests/auth_test.py")
        print("[System Output] Error: ModuleNotFoundError: No module named 'jwt'")
        
        print("[LLM Attempt 2] Retrying same command: pytest tests/auth_test.py")
        print("[System Output] Error: ModuleNotFoundError: No module named 'jwt'")
        
        print("[LLM Attempt 3] Retrying same command: pytest tests/auth_test.py")
        print("[System Output] Error: ModuleNotFoundError: No module named 'jwt'")
        
        print("[LLM Attempt 4] Trying dangerous cleanup command: rm -rf /var/log/*")
        print("[WARNING] UN-HARNESSED FAILURE: Unsanitized dangerous command executed!")
        return "FAILED_UNSAFE"

class HarnessedAgentRunner:
    """Production Agent Harness enforcing deterministic safety boundaries."""
    def __init__(self, llm_client, max_retries=2):
        self.llm_client = llm_client
        self.max_retries = max_retries
        self.command_history = []
        self.forbidden_patterns = [r"rm\s+-rf", r"sudo", r"chmod\s+777", r"git\s+push\s+--force"]

    def pre_execution_hook(self, command):
        """Sanitizes commands prior to execution."""
        for pattern in self.forbidden_patterns:
            if re.search(pattern, command):
                raise PermissionError(f"BLOCKED BY PRE-HOOK: Dangerous command pattern '{pattern}' detected.")
        return True

    def loop_detector(self, command):
        """Detects repeated failing execution loops."""
        self.command_history.append(command)
        if len(self.command_history) >= self.max_retries:
            recent = self.command_history[-self.max_retries:]
            if len(set(recent)) == 1:
                raise RuntimeError(f"BLOCKED BY HARNESS LOOP DETECTOR: Command '{command}' repeated {self.max_retries} times without progress.")

    def execute_tool_call(self, tool_name, command):
        print(f"\n[Harness Evaluator] Inspecting tool call: {tool_name}('{command}')")
        
        # 1. Pre-execution guardrail check
        try:
            self.pre_execution_hook(command)
            print("  ✓ Pre-action hook passed: Command is safe.")
        except PermissionError as e:
            print(f"  ❌ Security Violation: {e}")
            return {"status": "BLOCKED", "reason": str(e)}

        # 2. Loop detection check
        try:
            self.loop_detector(command)
            print("  ✓ Loop detector passed: No execution trap.")
        except RuntimeError as e:
            print(f"  ❌ Loop Detected: {e}")
            return {"status": "LOOP_HALTED", "reason": str(e)}

        return {"status": "EXECUTED", "output": f"Simulated output of {command}"}

def main():
    print("=" * 60)
    print("MODULE 1 DEMO: WHY HARNESS ENGINEERING IS REQUIRED ")
    print("=" * 60)

    # Initialize aisuite LLM Client (.env configured)
    llm_client = CourseLLMClient()

    # 1. Run un-harnessed agent
    raw_agent = UnharnessedAgentSimulator(llm_client)
    raw_agent.run_task("Fix auth test failures")

    # 2. Run harnessed agent
    harness = HarnessedAgentRunner(llm_client, max_retries=2)
    print("\n--- HARNESSED AGENT SIMULATION ---")
    
    # Test 1: Repeated execution loop detection
    res1 = harness.execute_tool_call("run_shell", "pytest tests/auth_test.py")
    res2 = harness.execute_tool_call("run_shell", "pytest tests/auth_test.py")
    
    # Test 2: Pre-hook interception of dangerous command
    res3 = harness.execute_tool_call("run_shell", "rm -rf /var/log/*")

    print("\n" + "=" * 60)
    print("DEMO SUMMARY: Harness successfully blocked execution loops & dangerous mutations!")
    print("=" * 60)

if __name__ == "__main__":
    main()
