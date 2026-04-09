# About Git Hooks (Important Reminder)
.git/hooks/* does NOT get pushed to GitHub

## Keep Hooks in:
```
scripts/git-hooks/post-commit
```
## Add:
```
scripts/install-hooks.sh
```
##  After cloning the repo elsewhere:
```
git clone https://github.com/mla133/wiki.git
cd wiki
./scripts/install-hooks.sh
```
This will copy the current git hooks to the .git/hooks directory

## System Requirements for this project

This project expects a local Ollama server to be running.

- Install Ollama:  https://ollama.com
- Start the server:
    ollama serve

The CLI communicates with Ollama over HTTP at:
    http://localhost:11434
