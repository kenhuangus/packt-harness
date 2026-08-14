"""
Module 1: Harness vs. Un-Harnessed Model Execution Simulator

Teaching goal: a capable model is not a reliable agent. Reliability comes
from the deterministic scaffolding around the model.

This demo shows three un-harnessed failure modes, then the same actions
under a harness that blocks them:

1. Infinite loop runaway — the model retries the same failing command.
2. Unsanitized dangerous command — `rm -rf` is executed with no policy.
3. Context decay / amnesia — the model never inspects why the test failed.
4. Harness interceptor mitigation — pre-hooks + loop detection stop both.

LLM calls go through `common.llm_client.CourseLLMClient`. If the configured
OpenAI-compatible endpoint is unreachable, the client returns simulated text
so the harness checks still run.
"""

import sys, os, time, re
sys.stdout.reconfigure(encoding='utf-8')

# Import the shared course LLM client from course_implementation/common.
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from common.llm_client import CourseLLMClient


class UnharnessedAgentSimulator:
    """
    Simulate a raw model runner with no policy, no sandbox, and no loop stop.

    Everything after the LLM call is scripted so the failure modes are
    reproducible. The point is not that a particular model always does this;
    it is that nothing in this runner would stop it if it did.
    """

    def __init__(self, llm_client):
        # Keep a client handle so the demo still exercises the .env LLM path.
        self.llm_client = llm_client

    def run_task(self, prompt):
        print("\n--- UN-HARNESSED AGENT SIMULATION ---")

        # Call the model. The return value is printed but never inspected
        # for command safety, so a dangerous suggestion would still run.
        response = self.llm_client.complete(prompt, system_prompt="You are an un-harnessed coding agent.")
        print(f"[LLM Response Output]: {response[:60]}...")

        # Failure mode 1: the same pytest command is retried three times
        # against the same ModuleNotFoundError. No loop detector exists.
        print("[LLM Attempt 1] Trying command: pytest tests/auth_test.py")
        print("[System Output] Error: ModuleNotFoundError: No module named 'jwt'")

        print("[LLM Attempt 2] Retrying same command: pytest tests/auth_test.py")
        print("[System Output] Error: ModuleNotFoundError: No module named 'jwt'")

        print("[LLM Attempt 3] Retrying same command: pytest tests/auth_test.py")
        print("[System Output] Error: ModuleNotFoundError: No module named 'jwt'")

        # Failure mode 2: a destructive cleanup command is executed as typed.
        print("[LLM Attempt 4] Trying dangerous cleanup command: rm -rf /var/log/*")
        print("[WARNING] UN-HARNESSED FAILURE: Unsanitized dangerous command executed!")
        return "FAILED_UNSAFE"


class HarnessedAgentRunner:
    """
    Production-shaped harness: every tool call is inspected before it runs.

    Two deterministic gates sit in front of execution:
    - pre_execution_hook: regex deny-list for destructive shell patterns
    - loop_detector: halt when the same command repeats without progress
    """

    def __init__(self, llm_client, max_retries=2):
        self.llm_client = llm_client
        # After this many identical commands, the loop detector raises.
        self.max_retries = max_retries
        # Ordered history of proposed commands used by loop_detector.
        self.command_history = []
        # Patterns that must never reach a shell, even if the model asks.
        self.forbidden_patterns = [r"rm\s+-rf", r"sudo", r"chmod\s+777", r"git\s+push\s+--force"]

    def pre_execution_hook(self, command):
        """Reject a command that matches a known-destructive regex."""
        for pattern in self.forbidden_patterns:
            if re.search(pattern, command):
                raise PermissionError(f"BLOCKED BY PRE-HOOK: Dangerous command pattern '{pattern}' detected.")
        return True

    def loop_detector(self, command):
        """
        Record the command and halt if the last N entries are identical.

        This is a teaching stand-in for "no progress": the demo never
        inspects stdout, so repetition itself is treated as a stall.
        """
        self.command_history.append(command)
        if len(self.command_history) >= self.max_retries:
            recent = self.command_history[-self.max_retries:]
            if len(set(recent)) == 1:
                raise RuntimeError(f"BLOCKED BY HARNESS LOOP DETECTOR: Command '{command}' repeated {self.max_retries} times without progress.")

    def execute_tool_call(self, tool_name, command):
        """
        Evaluate one proposed tool call.

        Order matters: security first, then loop detection, then execute.
        Either gate can return a BLOCKED / LOOP_HALTED status without
        running the command.
        """
        print(f"\n[Harness Evaluator] Inspecting tool call: {tool_name}('{command}')")

        # Gate 1: deny-list check before anything is recorded as executed.
        try:
            self.pre_execution_hook(command)
            print("  ✓ Pre-action hook passed: Command is safe.")
        except PermissionError as e:
            print(f"  ❌ Security Violation: {e}")
            return {"status": "BLOCKED", "reason": str(e)}

        # Gate 2: identical-retry detector. The first pytest call passes;
        # the second identical call is halted when max_retries == 2.
        try:
            self.loop_detector(command)
            print("  ✓ Loop detector passed: No execution trap.")
        except RuntimeError as e:
            print(f"  ❌ Loop Detected: {e}")
            return {"status": "LOOP_HALTED", "reason": str(e)}

        # Teaching simulation: a command that survives both gates is
        # treated as executed. No real shell is opened here.
        return {"status": "EXECUTED", "output": f"Simulated output of {command}"}


def main():
    print("=" * 60)
    print("MODULE 1 DEMO: WHY HARNESS ENGINEERING IS REQUIRED ")
    print("=" * 60)

    # Shared client. Prints its endpoint; falls back to simulated text
    # when http://127.0.0.1:8000/v1 is not serving a model.
    llm_client = CourseLLMClient()

    # Side-by-side contrast: un-harnessed first, then the same intents
    # under the harness.
    raw_agent = UnharnessedAgentSimulator(llm_client)
    raw_agent.run_task("Fix auth test failures")

    harness = HarnessedAgentRunner(llm_client, max_retries=2)
    print("\n--- HARNESSED AGENT SIMULATION ---")

    # Same failing pytest twice: first allowed, second stopped as a loop.
    res1 = harness.execute_tool_call("run_shell", "pytest tests/auth_test.py")
    res2 = harness.execute_tool_call("run_shell", "pytest tests/auth_test.py")

    # Same destructive command the un-harnessed runner executed: blocked.
    res3 = harness.execute_tool_call("run_shell", "rm -rf /var/log/*")

    print("\n" + "=" * 60)
    print("DEMO SUMMARY: Harness successfully blocked execution loops & dangerous mutations!")
    print("=" * 60)


if __name__ == "__main__":
    main()
