# llama.cpp Ollama-like local registry (Windows 11 + PowerShell)

This document describes a **deterministic, Ollama‑like workflow built on top of `llama.cpp` using `-m`**.  
The goal is to achieve Ollama’s convenience **without** hidden caches, background daemons, or implicit behavior.

---

## 1. Environment

- **OS**: Windows 11
- **Terminal**: Windows Terminal → PowerShell
- **Installation**: `winget install llama.cpp`
- **Primary CLI binary**: `llama-cli` (not `main`)

Binaries available on PATH:
- `llama-cli` → interactive / batch inference
- `llama-server` → OpenAI‑compatible HTTP API

---

## 2. Core Design Principles

1. **No hidden cache at runtime**  
   Hugging Face is used only as a *download source*, not a runtime dependency.
2. **Explicit model paths**  
   All inference uses `-m <path-to-gguf>`.
3. **Deterministic configuration**  
   Chat templates, context size, and GPU offload are declared explicitly.
4. **Human‑readable registry**  
   Models are registered by name in a JSON file.

This mirrors Ollama’s UX but keeps behavior transparent and reproducible.

---

## 3. Directory Layout

```text
C:\Users\<you>\llama-registry\
├── models\          # GGUF files you explicitly run
│   ├── llama-3-8b-instruct.Q4_K_M.gguf
│   └── gemma-3-1b-it.Q4_K_M.gguf
├── registry.json     # Model name → config mapping
└── llama.ps1         # Ollama-like CLI wrapper
```

## 4. Hugging Face (-hf) Is Download‑Only
Using:
Markdownllama-cli -hf ggml-org/gemma-3-1b-it-GGUFShow more lines

Downloads GGUF files into:
Plain Text%USERPROFILE%\.cache\huggingface\hubShow more lines

Loads the model from that cache path

Important
Once you later run:
PowerShellllama-cli -m C:\path\to\model.ggufShow more lines
➡️ The HF cache is no longer used or consulted at all.
The model is memory-mapped directly from the specified file path.

## 5. Promoting GGUFs Into the Registry
Recommended approach (copy, not move):
PowerShellcopy `  $HOME\.cache\huggingface\hub\models--ggml-org--gemma-3-1b-it-GGUF\snapshots\*\*.gguf `  $HOME\llama-registry\models\Show more lines
After this step, inference should always use -m.

## 6. Chat Templates (Critical Concept)
What --chat-template Does
--chat-template defines how a structured conversation is serialized into raw text
for the model.
Without the correct template, instruct/chat models will:

ignore system instructions
confuse roles
echo tags
degrade in output quality

Ollama applies templates automatically.
llama.cpp requires you to specify them explicitly.

## 7. Exact llama-3 Chat Template
For LLaMA‑3 Instruct models, llama.cpp internally produces exactly:
Plain Text<|begin_of_text|><|system|>You are a helpful assistant.<|user|>Explain gravity simply.<|assistant|>Show more lines
The model begins generating tokens after <|assistant|>.
This structure is mandatory for LLaMA‑3‑Instruct models.

## 8. Determining the Chat Template for an Unknown Model
Use evidence, in this order:
### 1 Model Type

Contains instruct, chat, it → requires a template
Contains base, pretrain → no chat template


### 2 GGUF Metadata (Authoritative)
PowerShellllama-cli -m model.gguf --infoShow more lines
If tokenizer.chat_template or chat_template exists, use it.

### 3 Base Model Lineage (Most Common Case)
Base Model FamilyChat TemplateLLaMA‑3 Instructllama-3LLaMA‑2 Chatllama-2Mistral / MixtralmistralGemma‑ITgemmaQwen / Yi / Phi / DeepSeekchatml

### 4 Prompt Examples in Model Card
Prompt format shown in documentation is almost always the correct template.

### 5 Empirical Test (Last Resort)
PowerShellllama-cli -m model.gguf --chat-template llama-3 -p "Say OK" -n 5llama-cli -m model.gguf --chat-template chatml  -p "Say OK" -n 5llama-cli -m model.gguf --chat-template mistral -p "Say OK" -n 5Show more lines
Correct template produces short, clean output with no role leakage.

## 9. Ollama‑Like Registry (registry.json)
Example:
JSON{  "models": {    "llama3": {      "file": "llama-3-8b-instruct.Q4_K_M.gguf",      "template": "llama-3",      "ctx": 8192,      "ngl": 999,      "description": "LLaMA 3 8B Instruct"    },    "gemma3": {      "file": "gemma-3-1b-it.Q4_K_M.gguf",      "template": "gemma",      "ctx": 8192,      "ngl": 999,      "description": "Gemma 3 1B IT"    }  }}Show more lines

## 10. Ollama‑Like llama Wrapper CLI
Supported commands:

llama list
llama run <name>
llama register <name> <file> <template> <ctx> <description>
llama rm <name>

Each run expands internally to:
JSONllama-cli -m <explicit-gguf-path> `  --chat-template <template> `  --ctx-size <n> `  -ngl <n>Show more lines
No hidden cache.
No daemon.
No implicit behavior.

## 11. Key Takeaways

-hf is a package manager, not a runtime mode
-m is direct binary execution
Chat templates are non‑optional for instruct models
Determinism requires explicit paths and explicit templates
Ollama’s UX can be recreated entirely in userland


This setup provides maximum transparency, reproducibility, and control
while preserving an Ollama‑like developer experience.
