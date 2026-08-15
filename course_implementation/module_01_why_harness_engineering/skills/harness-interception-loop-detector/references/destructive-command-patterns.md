# Destructive Command Patterns & Policy

The following shell command patterns are strictly prohibited in autonomous agent execution:

| Pattern | Risk | Rationale |
| :--- | :--- | :--- |
| `rm -rf <path>` | CRITICAL | Permanent recursive deletion without recycle bin protection. |
| `sudo <command>` | CRITICAL | Privilege escalation outside container boundary. |
| `chmod 777 <path>` | HIGH | Global read/write/execute permission breach. |
| `DROP DATABASE` | CRITICAL | Irreversible data store destruction. |
