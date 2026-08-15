"""TDA Pytest Subprocess Runner."""
import subprocess
import sys

def run_pytest(test_file: str) -> tuple[bool, str]:
    res = subprocess.run(
        [sys.executable, "-m", "pytest", test_file, "-q", "--tb=short", "-p", "no:cacheprovider"],
        capture_output=True, text=True
    )
    return res.returncode == 0, res.stdout + res.stderr

if __name__ == "__main__":
    print("TDA Subprocess runner ready.")
