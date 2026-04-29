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

### Utilizing llama.cpp GGUF models

This project can run llama.cpp models starting the server using:
```
llama-server -m "/path/to/models/model.gguf" --jinja --ctx-size 24576 --temp 0.2 --top-p 0.95 -ngl 10 --threads 20 --port 8123

llama-server -m "C:\Users\allenma\models\qwen2.5-coder-14b-instruct-q5_k_m.gguf" --jinja --ctx-size 24576 --temp 0.2 --top-p 0.95 -ngl 10 --threads 20 --port 8123
```
NOTE: *qwen2.5-coder-14b-instruct-q5_k_m.gguf* is currently being used with a larger context size (24576)
