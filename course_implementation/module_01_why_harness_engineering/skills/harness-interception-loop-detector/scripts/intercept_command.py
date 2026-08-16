"""Command Interception & Loop Detection Helper Script."""
import re
import sys
import json
import argparse
from collections import deque
from pathlib import Path

FORBIDDEN_PATTERNS = [
    r"\brm\s+-[rR][fF]\b",
    r"\bsudo\b",
    r"\bchmod\s+777\b",
    r"\bdrop\s+database\b",
]

def _load_pattern_rules() -> list[dict[str, str]]:
    asset_path = Path(__file__).resolve().parent.parent / "assets" / "forbidden_patterns.json"
    try:
        payload = json.loads(asset_path.read_text(encoding="utf-8"))
        raw_patterns = payload["patterns"]
        if not isinstance(raw_patterns, list):
            raise ValueError("patterns must be a list")
        pattern_rules = []
        for item in raw_patterns:
            if not isinstance(item, dict):
                raise ValueError("pattern entry must be an object")
            regex = item["regex"]
            severity = item["severity"]
            action = item.get("action", "BLOCK")
            if not isinstance(regex, str) or not isinstance(severity, str) or not isinstance(action, str):
                raise ValueError("pattern fields must be strings")
            pattern_rules.append({
                "regex": regex,
                "severity": severity.upper(),
                "action": action.upper(),
            })
        if not pattern_rules:
            raise ValueError("patterns cannot be empty")
        return pattern_rules
    except (OSError, json.JSONDecodeError, KeyError, TypeError, ValueError):
        fallback_severities = {
            r"\brm\s+-[rR][fF]\b": "CRITICAL",
            r"\bsudo\b": "CRITICAL",
            r"\bchmod\s+777\b": "HIGH",
            r"\bdrop\s+database\b": "CRITICAL",
        }
        return [
            {"regex": pattern, "severity": fallback_severities[pattern], "action": "BLOCK"}
            for pattern in FORBIDDEN_PATTERNS
        ]

def _get_pattern_match(command: str, pattern_rules: list[dict[str, str]]) -> dict[str, str] | None:
    for item in pattern_rules:
        pattern = item["regex"]
        if re.search(pattern, command):
            return item
    return None

def _is_loop_detected(command: str, history: list[str] | None, max_retries: int) -> bool:
    if max_retries < 1:
        return False
    normalized_command = command.strip()
    command_history = deque((entry.strip() for entry in (history or [])), maxlen=max_retries)
    if len(command_history) < max_retries:
        return False
    return all(entry == normalized_command for entry in command_history)

def evaluate(command: str, history: list[str] | None = None, max_retries: int = 2) -> dict[str, object]:
    pattern_rules = _load_pattern_rules()
    matched_pattern = _get_pattern_match(command, pattern_rules)
    loop_detected = _is_loop_detected(command, history, max_retries)

    if matched_pattern is not None:
        pattern = matched_pattern["regex"]
        return {
            "verdict": "BLOCK",
            "risk_level": matched_pattern["severity"],
            "reason": f"BLOCKED: Destructive pattern '{pattern}' detected.",
            "loop_detected": loop_detected,
        }
    if loop_detected:
        return {
            "verdict": "BLOCK",
            "risk_level": "HIGH",
            "reason": (
                f"BLOCKED: Detected {max_retries} identical recent retries of '{command.strip()}'. "
                "Change strategy instead of retrying the same command."
            ),
            "loop_detected": True,
        }
    return {
        "verdict": "ALLOW",
        "risk_level": "LOW",
        "reason": "ALLOWED: Command passed pattern and loop checks.",
        "loop_detected": False,
    }

def check_command(command: str) -> tuple[bool, str]:
    matched_pattern = _get_pattern_match(command, _load_pattern_rules())
    if matched_pattern is not None:
        pattern = matched_pattern["regex"]
        return False, f"BLOCKED: Destructive pattern '{pattern}' detected."
    return True, "ALLOWED"

def _run_selftest() -> None:
    clean_allow = evaluate("pytest -q")
    assert clean_allow == {
        "verdict": "ALLOW",
        "risk_level": "LOW",
        "reason": "ALLOWED: Command passed pattern and loop checks.",
        "loop_detected": False,
    }

    pattern_block = evaluate("rm -rf /tmp/data")
    assert pattern_block["verdict"] == "BLOCK"
    assert pattern_block["risk_level"] == "CRITICAL"
    assert pattern_block["loop_detected"] is False
    pattern_and_loop_block = evaluate(
        "rm -rf /tmp/data",
        history=["rm -rf /tmp/data", "rm -rf /tmp/data"],
        max_retries=2,
    )
    assert pattern_and_loop_block["verdict"] == "BLOCK"
    assert pattern_and_loop_block["risk_level"] == "CRITICAL"
    assert pattern_and_loop_block["loop_detected"] is True

    loop_block = evaluate("pytest -q", history=["pytest -q", "pytest -q"], max_retries=2)
    assert loop_block["verdict"] == "BLOCK"
    assert loop_block["risk_level"] == "HIGH"
    assert loop_block["loop_detected"] is True

    partial_window = evaluate("pytest -q", history=["pytest -q"], max_retries=2)
    assert partial_window["verdict"] == "ALLOW"
    assert partial_window["loop_detected"] is False

    verdict, reason = check_command("rm -rf /tmp/data")
    assert verdict is False
    assert reason == "BLOCKED: Destructive pattern '\\brm\\s+-[rR][fF]\\b' detected."

    print("ALL CHECKS PASSED")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Audit shell command safety")
    parser.add_argument("--command", help="Shell command to evaluate")
    parser.add_argument("--history", action="append", default=[], help="Prior commands (oldest first)")
    parser.add_argument("--max-retries", type=int, default=2, help="Loop detection window size")
    parser.add_argument("--json", action="store_true", help="Print machine-readable verdict JSON")
    parser.add_argument("--selftest", action="store_true", help="Run built-in assertions and exit")
    args = parser.parse_args()

    if args.selftest:
        _run_selftest()
        sys.exit(0)

    if not args.command:
        parser.error("--command is required unless --selftest is set")
    if args.max_retries < 1:
        parser.error("--max-retries must be >= 1")

    verdict = evaluate(args.command, history=args.history, max_retries=args.max_retries)
    allowed = verdict["verdict"] == "ALLOW"

    if args.json:
        print(json.dumps(verdict, indent=2))
    else:
        print(f"[{'PASS' if allowed else 'FAIL'}] {verdict['reason']}")

    sys.exit(0 if allowed else 1)
