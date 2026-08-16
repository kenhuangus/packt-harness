"""
packt-harness CLI: Production-Grade AI Agent Harness Engineering

Command-line tool to run interactive course modules, verify readiness audits,
test harness implementations, and launch the presentation slide deck.
"""

from __future__ import annotations

import argparse
from pathlib import Path
import subprocess
import sys
import webbrowser

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

MODULES = {
    1: {
        "title": "Why Harness Engineering",
        "folder": "module_01_why_harness_engineering",
        "script": "harness_vs_model_demo.py",
        "summary": "Interception hooks, loop detection & unharnessed failure modes.",
    },
    2: {
        "title": "Core Harness Stack",
        "folder": "module_02_core_harness_stack",
        "script": "core_harness_stack.py",
        "summary": "The 5 golden pillars, token budgeting & sandbox enforcement.",
    },
    3: {
        "title": "Spec-Driven Development",
        "folder": "module_03_spec_driven_development",
        "script": "spec_driven_verifier.py",
        "summary": "SPEC.md machine contracts, allowed file scope & acceptance tests.",
    },
    4: {
        "title": "Guardrails & Hooks Engine",
        "folder": "module_04_guardrails_and_hooks",
        "script": "guardrails_engine.py",
        "summary": "Claude Code PreToolUse/PostToolUse hooks, AST & secret scanning.",
    },
    5: {
        "title": "Permission Escalation Gateway",
        "folder": "module_05_break_and_qna",
        "script": "permission_escalation_gateway.py",
        "summary": "Risk-tiered approval matrix & human-in-the-loop signing ledger.",
    },
    6: {
        "title": "Tests as Reliability Layer",
        "folder": "module_06_tests_as_reliability_layer",
        "script": "tda_reliability_pipeline.py",
        "summary": "Test-Driven Agent (TDA) repair loop & regression test persistence.",
    },
    7: {
        "title": "Model Context Protocol (MCP)",
        "folder": "module_07_skills_plugins_mcp",
        "script": "mcp_client_runner.py",
        "summary": "MCP 2.x Python SDK client-server stdio session & LLM synthesis.",
    },
    8: {
        "title": "Compound Engineering",
        "folder": "module_08_compound_engineering",
        "script": "multi_agent_team_simulator.py",
        "summary": "Multi-agent role separation & git worktree sandbox isolation.",
    },
    9: {
        "title": "5-Step SOP Practical Workflow",
        "folder": "module_09_practical_workflow_pattern",
        "script": "five_step_sop_pipeline.py",
        "summary": "Spec -> Constraint -> Guardrails -> Pytest -> Diff review pipeline.",
    },
    10: {
        "title": "Production Harness Audit",
        "folder": "module_10_closing_and_principles",
        "script": "production_harness_audit.py",
        "summary": "5-Gate enterprise readiness audit & compliance score.",
    },
}


def get_repo_root() -> Path:
    """Resolve repository root directory containing course_implementation."""
    pkg_dir = Path(__file__).resolve().parent
    candidates = [
        pkg_dir.parent,
        Path.cwd(),
        Path.cwd().parent,
    ]
    for c in candidates:
        if (c / "course_implementation").is_dir():
            return c
    return pkg_dir.parent


def cmd_list(args: argparse.Namespace) -> int:
    """List all available modules with titles and summaries."""
    print("=" * 70)
    print("PACKT HARNESS ENGINEERING: 10-MODULE CURRICULUM")
    print("=" * 70)
    for num, mod in MODULES.items():
        print(f"\n[{num:02d}] {mod['title']}")
        print(f"     Script:  course_implementation/{mod['folder']}/{mod['script']}")
        print(f"     Summary: {mod['summary']}")
    print("\n" + "=" * 70)
    print("Run any module using: packt-harness run <1-10>")
    print("=" * 70)
    return 0


def cmd_run(args: argparse.Namespace) -> int:
    """Run a specific module (1-10) or all modules."""
    target = str(args.module).strip().lower()
    repo_root = get_repo_root()

    if target in ("all", "0"):
        print(">>> Executing All Course Modules Sequentially <<<\n")
        runner = repo_root / "run_all_modules.py"
        res = subprocess.run([sys.executable, str(runner)], cwd=repo_root)
        return res.returncode

    try:
        mod_num = int(target)
    except ValueError:
        for num, data in MODULES.items():
            if target in data["folder"].lower() or target in data["title"].lower():
                mod_num = num
                break
        else:
            print(f"Error: Unknown module '{target}'. Choose 1..10 or 'all'. Run 'packt-harness list' to view modules.")
            return 1

    if mod_num not in MODULES:
        print(f"Error: Module number {mod_num} out of range (1-10).")
        return 1

    mod = MODULES[mod_num]
    mod_dir = repo_root / "course_implementation" / mod["folder"]
    script_path = mod_dir / mod["script"]

    if not script_path.is_file():
        print(f"Error: Script file '{script_path}' not found.")
        return 1

    print("=" * 70)
    print(f"RUNNING MODULE {mod_num:02d}: {mod['title'].upper()}")
    print(f"Path: {script_path}")
    print("=" * 70 + "\n")

    res = subprocess.run([sys.executable, str(script_path)], cwd=mod_dir)
    return res.returncode


def cmd_audit(args: argparse.Namespace) -> int:
    """Run the 5-Gate production readiness audit."""
    repo_root = get_repo_root()
    target_path = Path(args.target).resolve() if args.target else repo_root
    audit_script = repo_root / "course_implementation" / "module_10_closing_and_principles" / "production_harness_audit.py"
    
    res = subprocess.run([sys.executable, str(audit_script), str(target_path)], cwd=audit_script.parent)
    return res.returncode


def cmd_test(args: argparse.Namespace) -> int:
    """Run the complete test suite."""
    repo_root = get_repo_root()
    runner = repo_root / "run_all_modules.py"
    res = subprocess.run([sys.executable, str(runner)], cwd=repo_root)
    return res.returncode


def cmd_slides(args: argparse.Namespace) -> int:
    """Launch local presentation slides server and open in browser."""
    repo_root = get_repo_root()
    docs_dir = repo_root / "docs"
    serve_dir = docs_dir if docs_dir.is_dir() else repo_root
    port = args.port

    url = f"http://localhost:{port}/slides.html"
    print(f"[*] Starting local slides server at {url} (serving: {serve_dir})")
    print("[*] Press Ctrl+C to stop the server.\n")

    if not args.no_browser:
        webbrowser.open(url)

    try:
        subprocess.run(
            [sys.executable, "-m", "http.server", str(port), "--directory", str(serve_dir)],
            cwd=repo_root
        )
    except KeyboardInterrupt:
        print("\n[*] Slides server stopped.")
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="packt-harness",
        description="Production-Grade AI Agent Harness Engineering CLI",
    )
    parser.add_argument(
        "-v", "--version",
        action="version",
        version="packt-harness 1.0.0 (Ken Huang)",
    )

    subparsers = parser.add_subparsers(dest="command", help="Available subcommands")

    # list
    subparsers.add_parser("list", help="List all 10 course modules and summaries")

    # run
    p_run = subparsers.add_parser("run", help="Run a specific course module demo (1-10 or 'all')")
    p_run.add_argument("module", help="Module number (1-10) or 'all'")

    # audit
    p_audit = subparsers.add_parser("audit", help="Run Module 10 5-Gate production readiness audit")
    p_audit.add_argument("target", nargs="?", default=".", help="Target project root directory to audit (default: .)")

    # test
    subparsers.add_parser("test", help="Run the unified multi-module test runner")

    # slides
    p_slides = subparsers.add_parser("slides", help="Serve and open interactive HTML presentation slides")
    p_slides.add_argument("-p", "--port", type=int, default=8080, help="HTTP port to serve on (default: 8080)")
    p_slides.add_argument("--no-browser", action="store_true", help="Do not automatically open the browser")

    args = parser.parse_args(argv)

    if not args.command:
        parser.print_help()
        return 0

    command_handlers = {
        "list": cmd_list,
        "run": cmd_run,
        "audit": cmd_audit,
        "test": cmd_test,
        "slides": cmd_slides,
    }

    handler = command_handlers.get(args.command)
    if handler:
        return handler(args)

    parser.print_help()
    return 0


if __name__ == "__main__":
    sys.exit(main())
