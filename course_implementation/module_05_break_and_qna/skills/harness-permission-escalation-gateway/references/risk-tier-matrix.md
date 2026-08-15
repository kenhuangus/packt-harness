# 4-Tier Risk Matrix

| Tier | Operations | Policy |
| :--- | :--- | :--- |
| **LOW** | `read_file`, `list_dir`, `grep` | Auto-approved immediately. |
| **MEDIUM** | `write_file`, `run_test` | Logged and executed in sandbox. |
| **HIGH** | `pip_install` | Intent logged with warning alert. |
| **CRITICAL** | `git_push`, `drop_db` | Strictly gated by `approvals.json` signed token. |
