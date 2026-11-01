# 📜 Project History & Architecture Log: AI Code Reviewer CLI

> **Author / Maintainer:** 0abhishhek-hub (Sourav Kumar)  
> **Initial Release:** 02 November 2026  
> **Host Architecture:** Realme Phone (Android ARM64) -> Termux -> PRoot Ubuntu Linux Container  
> **GitHub Repository:** [0abhishhek-hub/ai-code-reviewer](https://github.com/0abhishhek-hub/ai-code-reviewer)  

---

## 1. 🎯 Problem Statement & Goal
Junior developers frequently encounter harsh PR review cycles due to security pitfalls (SQL injection, leaked credentials, unhandled exceptions) or poor architectural conventions.
* **The Goal:** Build an instant CLI tool that acts like an in-house **Principal Staff Software Architect**, providing strict, educational, and constructive code reviews directly from the terminal before submitting code to senior peers.

---

## 2. 🏗️ Review Engine Architecture
- **Diff Ingestion Engine:**
  - Priority 1: Unstaged changes (`git diff`)
  - Priority 2: Staged changes (`git diff --staged`)
  - Priority 3: Last commit inspection (`git diff HEAD~1`)
  - Priority 4: Built-in self-diagnostic sample (if invoked outside a git repository)
- **Review Rubric:**
  1. 🛡️ Security & Vulnerabilities (SQLi, XSS, Secret Leaks, Auth flaws)
  2. 🐛 Edge Cases & Logical Bugs (Null safety, race conditions, memory leaks)
  3. ⚡ Performance & Efficiency (Algorithmic complexity, DB connection pools)
  4. 🎨 Clean Code & Architecture (DRY, SOLID, modular design)
  5. 💡 Production-Ready Refactor (Exact code replacement diff)

---

## 3. 🔬 Iteration & Engineering Log

### Phase 1: Context Size & Diff Truncation
- Large diffs can exceed token limits or increase latency.
- Implemented intelligent slice windowing (`diff[:15000]`) to ensure reviews process within 3-5 seconds while capturing the most critical code changes.

### Phase 2: Global Alias Installation
- Installed global shell alias in `~/.bashrc`:
  ```bash
  alias ai-review="python3 /root/projects/ai-code-reviewer/reviewer.py"
  ```
- Any developer can type `ai-review` from ANY git project folder on the system to trigger immediate inspection.

### Phase 3: Push Protection & Secrets Compliance
- Stripped all hardcoded API tokens.
- Bound API client to `GEMINI_API_KEY` system environment variable.
- Re-initialized pristine git commit history with `.gitignore`.

---

## 4. 🚀 Quickstart for Developers

### Setup
```bash
git clone git@github.com:0abhishhek-hub/ai-code-reviewer.git
cd ai-code-reviewer
pip install google-genai
```

### Configure Key
```bash
export GEMINI_API_KEY="your_gemini_api_key"
```

### Usage
```bash
# Review unstaged changes in current git repo
python3 reviewer.py

# Review staged changes
python3 reviewer.py --staged
```
