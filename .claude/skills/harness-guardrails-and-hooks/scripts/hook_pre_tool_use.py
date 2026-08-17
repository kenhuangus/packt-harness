"""Claude Code PascalCase PreToolUse Hook Interceptor."""
import json
import sys

def main():
    try:
        payload = json.load(sys.stdin)
        tool_name = payload.get("tool_name", "")
        tool_input = payload.get("tool_input", {})
        command = tool_input.get("command", "")
        
        if tool_name == "Bash":
            for flag in ["--dangerously-skip-permissions", "-y", "--force-all"]:
                if flag in command:
                    out = {
                        "hookSpecificOutput": {
                            "hookEventName": "PreToolUse",
                            "permissionDecision": "deny",
                            "permissionDecisionReason": f"Prohibited CLI flag '{flag}'."
                        }
                    }
                    print(json.dumps(out))
                    sys.exit(0)
                    
        out = {
            "hookSpecificOutput": {
                "hookEventName": "PreToolUse",
                "permissionDecision": "allow"
            }
        }
        print(json.dumps(out))
    except Exception as e:
        print(json.dumps({
            "hookSpecificOutput": {
                "hookEventName": "PreToolUse",
                "permissionDecision": "deny",
                "permissionDecisionReason": f"PreToolUse parse failure: {str(e)}"
            }
        }))

if __name__ == "__main__":
    main()
