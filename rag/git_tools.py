# rag/git_tools.py
import subprocess

def git(cmd: list[str]) -> str:
    return subprocess.check_output(
        ["git"] + cmd,
        text=True,
        stderr=subprocess.STDOUT
    ).strip()

def last_commit_message() -> str:
    return git(["log", "-1", "--pretty=%B"])

def last_commit_summary() -> str:
    return git(["log", "-1", "--pretty=oneline"])

def last_commit_diff() -> str:
    return git(["show", "--name-status", "--pretty="])
