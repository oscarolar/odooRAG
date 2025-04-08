import subprocess
import os
import json

def clone_repo(repo_url, branch, path):
    subprocess.run(["git", "clone", "-b", branch, repo_url, path], check=True)

def get_commit_list(path, old_branch, new_branch):
    result = subprocess.run(["git", "log", f"{old_branch}..{new_branch}", "--pretty=format:%H||%s"], capture_output=True, text=True, cwd=path)
    commits = [line.split('||') for line in result.stdout.splitlines()]
    return commits

def main():
    clone_repo("git@github.com:odoo/odoo.git", "14.0", "odoo_14")
    clone_repo("git@github.com:odoo/odoo.git", "15.0", "odoo_15")
    commits = get_commit_list("odoo_15", "14.0", "15.0")
    with open("commit_changes.json", "w", encoding="utf-8") as f:
        json.dump(commits, f, indent=2)

if __name__ == "__main__":
    main()
