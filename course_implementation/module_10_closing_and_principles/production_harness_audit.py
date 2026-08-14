"""
Module 10: Truthful production-readiness audit for an agent harness.

Each score contribution is backed by a repository inspection performed during
the current run. Audit findings may fail without making the audit process fail.
"""

from __future__ import annotations

import argparse
import ast
import json
from pathlib import Path
import shlex
import subprocess
import sys
from typing import Any


sys.stdout.reconfigure(encoding="utf-8")

DEFAULT_REPOSITORY_ROOT = Path(__file__).resolve().parents[2]
SUBAGENT_FIELDS = {
    "name",
    "description",
    "tools",
    "disallowedTools",
    "model",
    "isolation",
}


def decorator_kind(decorator: ast.expr) -> str | None:
    """Return the final decorator attribute, such as 'tool' or 'resource'."""
    expression = decorator.func if isinstance(decorator, ast.Call) else decorator
    if isinstance(expression, ast.Attribute):
        return expression.attr
    if isinstance(expression, ast.Name):
        return expression.id
    return None


def parse_frontmatter(path: Path) -> dict[str, Any]:
    """Parse the documented scalar and list forms without a YAML dependency."""
    lines = path.read_text(encoding="utf-8").splitlines()
    if not lines or lines[0].strip() != "---":
        raise ValueError("missing opening '---' frontmatter delimiter")
    try:
        closing_index = next(
            index
            for index, line in enumerate(lines[1:], start=1)
            if line.strip() == "---"
        )
    except StopIteration as exc:
        raise ValueError(
            "missing closing '---' frontmatter delimiter"
        ) from exc

    fields: dict[str, Any] = {}
    active_list: str | None = None
    for line_number, raw_line in enumerate(
        lines[1:closing_index], start=2
    ):
        stripped = raw_line.strip()
        if not stripped or stripped.startswith("#"):
            continue
        if stripped.startswith("-"):
            if active_list is None:
                raise ValueError(
                    f"line {line_number}: list item has no field"
                )
            item = stripped.removeprefix("-").strip()
            if not item:
                raise ValueError(f"line {line_number}: empty list item")
            fields[active_list].append(item)
            continue
        if ":" not in raw_line:
            raise ValueError(
                f"line {line_number}: expected 'field: value'"
            )

        key, value = raw_line.split(":", 1)
        key = key.strip()
        value = value.strip()
        if not key:
            raise ValueError(f"line {line_number}: empty field name")
        if key in fields:
            raise ValueError(f"line {line_number}: duplicate field '{key}'")
        if value:
            fields[key] = value.strip("'\"")
            active_list = None
        else:
            fields[key] = []
            active_list = key
    return fields


class ProductionHarnessAuditor:
    """
    Five evidence-backed readiness checks against a real directory.

    Each check returns (passed, reason). A failed check lowers the
    score; the process still exits 0 so a partial project can be
    audited. The reason string is the evidence, not a slogan.
    """

    def __init__(self, target_dir: Path) -> None:
        self.target_dir = target_dir.resolve()

    def check_memory_files(self) -> tuple[bool, str]:
        """Check 1: CLAUDE.md and/or AGENTS.md exist as regular files."""
        found = [
            name
            for name in ("CLAUDE.md", "AGENTS.md")
            if (self.target_dir / name).is_file()
        ]
        if found:
            return True, f"found regular file(s): {', '.join(found)}"
        return False, "neither CLAUDE.md nor AGENTS.md is a regular file"

    def _existing_hook_file(self, command: str) -> Path | None:
        expanded = command.replace(
            "${CLAUDE_PROJECT_DIR}", str(self.target_dir)
        ).replace("$CLAUDE_PROJECT_DIR", str(self.target_dir))
        try:
            tokens = shlex.split(expanded, posix=False)
        except ValueError:
            return None
        for token in tokens:
            candidate_text = token.strip("'\"")
            if not candidate_text:
                continue
            candidate = Path(candidate_text)
            if not candidate.is_absolute():
                candidate = self.target_dir / candidate
            if candidate.is_file():
                return candidate.resolve()
        return None

    def check_pre_execution_hooks(self) -> tuple[bool, str]:
        """
        Check 2: .claude/settings.json registers a PreToolUse command hook
        whose command string points at a file that actually exists.
        """
        settings_path = self.target_dir / ".claude" / "settings.json"
        if not settings_path.is_file():
            return False, f"missing settings file: {settings_path}"
        try:
            settings = json.loads(settings_path.read_text(encoding="utf-8"))
        except (OSError, UnicodeError, json.JSONDecodeError) as exc:
            return False, f"could not parse {settings_path}: {exc}"

        hooks = settings.get("hooks")
        if not isinstance(hooks, dict):
            return False, "settings.json has no object-valued 'hooks'"
        registrations = hooks.get("PreToolUse")
        if not isinstance(registrations, list) or not registrations:
            return False, "no exact PascalCase PreToolUse registration found"

        reasons: list[str] = []
        for registration in registrations:
            if not isinstance(registration, dict):
                reasons.append("registration is not an object")
                continue
            matcher = registration.get("matcher")
            if not isinstance(matcher, str) or not matcher.strip():
                reasons.append("registration has no nonempty matcher")
                continue
            commands = registration.get("hooks")
            if not isinstance(commands, list) or not commands:
                reasons.append("registration has no hook implementations")
                continue
            for hook in commands:
                if not isinstance(hook, dict):
                    continue
                command = hook.get("command")
                if (
                    hook.get("type") == "command"
                    and isinstance(command, str)
                    and command.strip()
                ):
                    hook_file = self._existing_hook_file(command)
                    if hook_file is not None:
                        return (
                            True,
                            f"PreToolUse matcher '{matcher}' runs existing "
                            f"hook file {hook_file}",
                        )
            reasons.append(
                f"matcher '{matcher}' has no command hook referencing "
                "an existing file"
            )
        return False, "; ".join(reasons)

    def check_test_runner(self) -> tuple[bool, str]:
        """Check 3: run_all_modules.py parses as Python and pytest --version works."""
        runner = self.target_dir / "run_all_modules.py"
        if not runner.is_file():
            return False, f"missing automated runner: {runner}"
        try:
            ast.parse(
                runner.read_text(encoding="utf-8"), filename=str(runner)
            )
        except (OSError, UnicodeError, SyntaxError) as exc:
            return False, f"test runner is not readable Python: {exc}"

        try:
            completed = subprocess.run(
                [sys.executable, "-m", "pytest", "--version"],
                cwd=self.target_dir,
                capture_output=True,
                text=True,
                encoding="utf-8",
                errors="replace",
                timeout=15,
                check=False,
            )
        except (OSError, subprocess.TimeoutExpired) as exc:
            return False, f"pytest availability check could not run: {exc}"
        output = (completed.stdout or completed.stderr).strip()
        if completed.returncode != 0:
            return (
                False,
                f"pytest availability check returned "
                f"{completed.returncode}: {output}",
            )
        if not output:
            return False, "pytest availability check returned no version"
        return True, f"{runner.name} is valid Python; {output}"

    def check_mcp_scoped_tools(self) -> tuple[bool, str]:
        """Check 4: module 7 Python files declare at least one @tool and one @resource."""
        module_dir = (
            self.target_dir
            / "course_implementation"
            / "module_07_skills_plugins_mcp"
        )
        if not module_dir.is_dir():
            return False, f"missing module 7 directory: {module_dir}"

        tools: list[str] = []
        resources: list[str] = []
        python_files = sorted(module_dir.rglob("*.py"))
        if not python_files:
            return False, "module 7 contains no Python source files"
        for source_path in python_files:
            try:
                tree = ast.parse(
                    source_path.read_text(encoding="utf-8"),
                    filename=str(source_path),
                )
            except (OSError, UnicodeError, SyntaxError) as exc:
                return False, f"could not AST-inspect {source_path}: {exc}"
            for node in ast.walk(tree):
                if not isinstance(
                    node, (ast.FunctionDef, ast.AsyncFunctionDef)
                ):
                    continue
                kinds = {
                    decorator_kind(decorator)
                    for decorator in node.decorator_list
                }
                if "tool" in kinds:
                    tools.append(node.name)
                if "resource" in kinds:
                    resources.append(node.name)
        if not tools or not resources:
            return (
                False,
                f"AST declarations found: {len(tools)} tool(s), "
                f"{len(resources)} resource(s)",
            )
        return (
            True,
            f"AST declarations found: tools={tools}; resources={resources}",
        )

    def check_multi_agent_roles(self) -> tuple[bool, str]:
        """Check 5: .claude/agents/*.md have documented frontmatter (name, description, ...)."""
        agents_dir = self.target_dir / ".claude" / "agents"
        if not agents_dir.is_dir():
            return False, f"missing subagent directory: {agents_dir}"
        agent_files = sorted(agents_dir.glob("*.md"))
        if not agent_files:
            return False, f"no .md subagent definitions in {agents_dir}"

        errors: list[str] = []
        for agent_file in agent_files:
            try:
                fields = parse_frontmatter(agent_file)
            except (OSError, UnicodeError, ValueError) as exc:
                errors.append(f"{agent_file.name}: {exc}")
                continue

            unknown = sorted(set(fields) - SUBAGENT_FIELDS)
            if unknown:
                errors.append(
                    f"{agent_file.name}: undocumented field(s) "
                    f"{', '.join(unknown)}"
                )
            for required in ("name", "description"):
                value = fields.get(required)
                if not isinstance(value, str) or not value.strip():
                    errors.append(
                        f"{agent_file.name}: missing nonempty '{required}'"
                    )
            for tool_field in ("tools", "disallowedTools"):
                if tool_field not in fields:
                    continue
                value = fields[tool_field]
                if isinstance(value, str):
                    populated = any(
                        item.strip() for item in value.split(",")
                    )
                else:
                    populated = isinstance(value, list) and bool(value)
                if not populated:
                    errors.append(
                        f"{agent_file.name}: '{tool_field}' is empty"
                    )
            isolation = fields.get("isolation")
            if isolation is not None and isolation != "worktree":
                errors.append(
                    f"{agent_file.name}: isolation must be 'worktree', "
                    f"not '{isolation}'"
                )
            model = fields.get("model")
            if model is not None and (
                not isinstance(model, str) or not model.strip()
            ):
                errors.append(f"{agent_file.name}: 'model' is empty")

        if errors:
            return False, "; ".join(errors)
        return (
            True,
            f"validated {len(agent_files)} subagent definition(s): "
            + ", ".join(path.name for path in agent_files),
        )

    def run_audit(self) -> tuple[int, int]:
        print("=" * 60)
        print("MODULE 10 DEMO: PRODUCTION HARNESS READINESS AUDIT")
        print("=" * 60)
        print(f"Target Project Path: {self.target_dir}\n")

        checks = [
            ("Memory files", self.check_memory_files),
            ("Pre-execution hooks", self.check_pre_execution_hooks),
            ("Automated test runner", self.check_test_runner),
            ("MCP scoped tools/resources", self.check_mcp_scoped_tools),
            ("Multi-agent role definitions", self.check_multi_agent_roles),
        ]
        results: list[bool] = []
        for number, (label, check) in enumerate(checks, start=1):
            try:
                passed, reason = check()
            except Exception as exc:
                passed, reason = False, f"unexpected inspection error: {exc}"
            results.append(passed)
            status = "PASS" if passed else "FAIL"
            print(f"  [{status}] Check {number}: {label} -> {reason}")

        score = sum(results)
        total = len(results)
        percentage = score / total * 100
        print("\n" + "=" * 60)
        print(
            f"AUDIT SUMMARY: {score}/{total} Checks Passed "
            f"({percentage:.0f}% Production Readiness Score)"
        )
        if score == total:
            print("STATUS: ALL AUDITED READINESS CHECKS PASSED.")
        else:
            print(
                "STATUS: READINESS GAPS FOUND; "
                "THE TARGET IS NOT FULLY READY."
            )
        print("=" * 60)
        return score, total


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Audit an agent-harness project using repository evidence."
    )
    parser.add_argument(
        "target",
        nargs="?",
        type=Path,
        default=DEFAULT_REPOSITORY_ROOT,
        help="project directory to audit (default: this repository root)",
    )
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    target = args.target.expanduser()
    if not target.is_dir():
        print(f"[FAIL] Target project directory does not exist: {target}")
        return 2
    auditor = ProductionHarnessAuditor(target)
    auditor.run_audit()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
