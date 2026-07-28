import os
import subprocess
import sys

base_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'course_implementation')
modules = sorted([d for d in os.listdir(base_dir) if os.path.isdir(os.path.join(base_dir, d)) and d.startswith('module_')])
passed = 0
failures = []

for m in modules:
    m_path = os.path.join(base_dir, m)
    py_files = [f for f in os.listdir(m_path) if f.endswith('.py') and not f.startswith('fix_') and not f.startswith('update_') and not f.startswith('run_')]
    for py in py_files:
        full_py = os.path.join(m_path, py)
        res = subprocess.run([sys.executable, full_py], capture_output=True, text=True, cwd=m_path, encoding='utf-8', errors='ignore')
        if res.returncode == 0:
            passed += 1
            print(f"PASS {m}/{py}")
        else:
            failures.append((m, py, res.returncode))
            print(f"FAIL {m}/{py} (exit {res.returncode})")

print(f"\nSummary: {passed} passed, {len(failures)} failed")
sys.exit(1 if failures else 0)
