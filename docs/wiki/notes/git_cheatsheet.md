# Git Commands Cheatsheet

### 🚀 Getting Started
* `git init`: Initialize a new local repository.
* `git clone <url>`: Download a project and its entire version history from a remote URL.

### 📝 Working with Changes
* `git status`: List which files are staged, unstaged, and untracked.
* `git add <file>`: Add a specific file to the staging area.
* `git add .`: Add all changed files to the staging area.
* `git commit -m "message"`: Record file snapshots permanently in version history.
* `git diff`: Show changes between your working directory and the staging area.
* `git diff --staged`: Show changes between the staged area and the last commit.

### 🌿 Branching & Merging
* `git branch`: List all local branches in the current repository.
* `git branch <branch-name>`: Create a new branch.
* `git checkout <branch-name>`: Switch to a specific branch.
* `git checkout -b <branch-name>`: Create a new branch and switch to it immediately.
* `git merge <branch-name>`: Combine the specified branch’s history into the current one.
* `git branch -d <branch-name>`: Delete the specified branch.

### 🌍 Remote Repositories
* `git remote add <name> <url>`: Connect your local repo to a remote server.
* `git push <remote> <branch>`: Upload local branch commits to the remote repository.
* `git pull`: Fetch and merge changes from the remote server to your local directory.
* `git fetch`: Download objects and refs from another repository without merging.

### ⏳ Undo & History
* `git log`: List the commit history for the current branch.
* `git reset <file>`: Unstage a file while retaining its contents.
* `git reset --hard <commit>`: Discard all local changes and reset to a specific commit.
* `git revert <commit>`: Create a new commit that undoes the changes of a previous one.

