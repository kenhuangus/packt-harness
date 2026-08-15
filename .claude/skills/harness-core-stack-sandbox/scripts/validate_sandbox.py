"""Sandbox & Path Containment Validator."""
from pathlib import Path
import sys
import argparse

def validate_path(workspace_root: str, target_path: str) -> bool:
    workspace = Path(workspace_root).resolve()
    target = Path(target_path).resolve()
    return target.is_relative_to(workspace)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Check path containment")
    parser.add_argument("--workspace", default=".", help="Workspace root")
    parser.add_argument("--path", required=True, help="Target path to check")
    args = parser.parse_args()
    valid = validate_path(args.workspace, args.path)
    print(f"Path containment: {'VALID' if valid else 'VIOLATION'}")
    sys.exit(0 if valid else 1)
