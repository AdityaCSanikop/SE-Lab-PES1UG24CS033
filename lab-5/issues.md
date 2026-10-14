# Lab 5: Static Code Analysis — Issue Table

**Name:** Aditya C Sanikop  **SRN:** PES1UG24CS033  **Section:** 5A
**Assigned repo:** [L5_32_expense_tracker](https://github.com/SETAPESU26/L5_32_expense_tracker) — `expense_tracker.py`

## Results summary

| Tool   | Before                         | After            |
|--------|--------------------------------|------------------|
| Pylint | 5.27/10 (26 messages)          | **10.00/10**     |
| Bandit | 4 issues (1 High, 2 Med, 1 Low)| **0 issues**     |
| Flake8 | 4 issues                       | **0 issues**     |

Program output is identical before and after the fixes.
Raw reports are in `reports/before/` and `reports/after/`.

## Issues found and fixed (high and medium severity first)

| # | Issue | Tool / Code | Type | Line(s) | Description | Fix Approach |
|---|-------|-------------|------|---------|-------------|--------------|
| 1 | Shell injection | Bandit B605 (**High**) | Security | 61 | `os.system("xdg-open " + path)` passes user-controlled `path` through a shell; a path like `x; rm -rf ~` would run arbitrary commands | Replaced with `webbrowser.open(Path(path).resolve().as_uri())` — no shell is involved, and it works on any OS |
| 2 | Insecure temp file | Bandit B306 (Medium) | Security | 55 | `tempfile.mktemp()` only returns a name; another process can create that file before we do (race condition, CWE-377) | Used `tempfile.mkstemp()`, which atomically creates the file, then closed the returned descriptor |
| 3 | Hardcoded `/tmp` directory | Bandit B108 (Medium) | Security | 8 | `REPORT_DIR = "/tmp/expense_reports"` is predictable, shared and Linux-only; the directory was also never created | Built the path from `tempfile.gettempdir()` and create it with `os.makedirs(..., exist_ok=True)` before use |
| 4 | Hardcoded password | Bandit B105 (Low) | Security | 5, 50 | Bank-sync password stored in source code; `==` comparison is also open to timing attacks | Read from the `BANK_SYNC_PASSWORD` environment variable; compare with `hmac.compare_digest`; reject everything if no password is configured |
| 5 | Overly broad exception | Pylint W0718 | Bug | 41 | `except Exception` around `max()` hides any error, not just the empty-list case | Check `if not expenses: return None` explicitly and removed the `try/except` |
| 6 | Global statement | Pylint W0603 | Design | 29 | `setBudget` mutated a module global via `global monthly_budget` | Stored the budget in a module-level `budget_state` dict that is updated in place |
| 7 | range(len()) loop | Pylint C0200 | Style | 45 | `for i in range(len(expenses))` indexes the list manually | `for number, expense in enumerate(expenses, start=1)` |
| 8 | Non-snake_case names | Pylint C0103 | Convention | 7, 11–59 | camelCase functions/args/variables (`addExpense`, `newBudget`, `reportPath`, …) | Renamed to snake_case (`add_expense`, `new_budget`, `report_path`, …) |
| 9 | Missing docstrings | Pylint C0114 / C0116 | Documentation | 1, all functions | No module or function docstrings | Added a module docstring and one-line docstrings for every function |
| 10 | Script runs on import | Code review | Design | 80 | `main()` was called at module level, so importing the file ran the demo | Wrapped in `if __name__ == "__main__":` |
| 11 | Whitespace before `:` | Flake8 E203 | Style | 15 | `{"amount" : amount` | Removed the extra space |
| 12 | Missing blank lines | Flake8 E302 | Style | 44 | Only one blank line before `def printLedger` | Added a second blank line |
| 13 | Inline comment spacing | Flake8 E261 | Style | 74 | One space before `#` | Two spaces before the inline comment |
| 14 | Line too long | Flake8 E501 | Style | 77 | 93 characters (limit 79) | Wrapped the `print` call across lines |

## Commits

1. `Fix Bandit issues` — issues 1–4
2. `Fix Flake8 style issues` — issues 11–14
3. `Fix Pylint issues` — issues 5–10
