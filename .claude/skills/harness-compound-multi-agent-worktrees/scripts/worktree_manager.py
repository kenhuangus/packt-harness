"""Git Worktree Isolation Manager."""
import subprocess
import os

def create_worktree(repo_root: str, branch_name: str, target_path: str):
    subprocess.run(["git", "worktree", "add", "-b", branch_name, target_path, "HEAD"], cwd=repo_root, check=True)

def remove_worktree(repo_root: str, branch_name: str, target_path: str):
    subprocess.run(["git", "worktree", "remove", "--force", target_path], cwd=repo_root)
    subprocess.run(["git", "branch", "-D", branch_name], cwd=repo_root)

if __name__ == "__main__":
    print("Worktree manager ready.")
