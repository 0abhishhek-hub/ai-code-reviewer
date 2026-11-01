#!/usr/bin/env python3
import os
import sys
import subprocess
from google import genai

GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")

def get_git_diff(staged=False):
    try:
        cmd = ["git", "diff", "--staged"] if staged else ["git", "diff"]
        diff = subprocess.check_output(cmd, stderr=subprocess.DEVNULL).decode("utf-8")
        if not diff.strip():
            diff = subprocess.check_output(["git", "diff", "HEAD~1"], stderr=subprocess.DEVNULL).decode("utf-8")
        return diff
    except Exception:
        return ""

def review_code(diff):
    client = genai.Client(api_key=GEMINI_API_KEY)
    prompt = f"""You are a Principal Software Architect conducting an elite Code Review for a software engineer.
Review the following git diff thoroughly:

```diff
{diff[:15000]}
```

Provide structured, actionable feedback:
1. 🛡️ *Security & Vulnerabilities:* (Check for exposed secrets, injection, input validation)
2. 🐛 *Edge Cases & Logical Bugs:* (Null safety, error handling, boundary conditions)
3. ⚡ *Performance & Efficiency:* (Algorithmic complexity, unnecessary allocations, async efficiency)
4. 🎨 *Clean Code & Architecture:* (Naming, DRY, modular design)
5. 💡 *Recommended Fix:* (Provide the exact code change or refactor if needed)

Be direct, educational, and constructive. Format cleanly with markdown."""

    models = ["gemini-flash-lite-latest", "gemini-2.5-flash-lite", "gemini-pro-latest"]
    for model in models:
        try:
            res = client.models.generate_content(model=model, contents=prompt)
            if res.text:
                return res.text.strip()
        except Exception:
            continue
    return "Failed to get AI review response."

if __name__ == "__main__":
    staged = "--staged" in sys.argv
    print("🔍 Extracting git diff from current directory...")
    diff = get_git_diff(staged=staged)
    
    if not diff.strip():
        print("ℹ️ No uncommitted git changes detected. Running self-diagnostic review sample...")
        diff = "diff --git a/auth.py b/auth.py\n+ def login(user, password):\n+   query = f\"SELECT * FROM users WHERE u={user} AND p={password}\"\n+   return db.execute(query)"
    
    print("🤖 Conducting Senior AI Code Review via Google Gemini...")
    feedback = review_code(diff)
    print("\n" + "="*50)
    print(feedback)
    print("="*50 + "\n")
