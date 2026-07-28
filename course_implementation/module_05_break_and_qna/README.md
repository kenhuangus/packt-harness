# Module 5: Risk-Tiered Permission Escalation Gateway

## Overview
This module demonstrates interactive permission escalation gateways balancing developer velocity with security.

## Risk Tiering Matrix
- **LOW Risk**: Read-only tools (`read_file`, `list_dir`, `grep`). Action: **Auto-Approve**.
- **MEDIUM Risk**: Non-destructive edits (`write_file`, `run_test`). Action: **Log & Auto-Approve**.
- **HIGH Risk**: Shell commands (`npm_install`, `pip_install`). Action: **Audit Log**.
- **CRITICAL Risk**: State mutations (`git_push`, `db_drop`, `sudo`). Action: **Require Explicit User Modal Confirmation**.
