# Lab 5: Identified Issues and Fix Documentation

**Student Name:** Shakthi Raja G P  
**SRN:** PES1UG25CS843  
**Section:** L (Semester 5)  
**Assigned Script:** `attendance_tracker.py`  

---

## Static Code Analysis Issue Tracking Table

| Issue / Error Code | Tool | Type / Severity | Line(s) | Description | Fix Approach |
|:---|:---|:---|:---:|:---|:---|
| **B501: `verify=False`** | Bandit | Security / **High** | 60 | `requests.post` called with `verify=False`, disabling SSL certificate validation and exposing HTTP requests to Man-in-the-Middle (MITM) attacks. | Removed `verify=False` to enforce default strict TLS/SSL certificate validation. |
| **B609 & B602: Wildcard Injection & `shell=True`** | Bandit | Security / **High & Low** | 64 | `subprocess.Popen("tar -czf reports_backup.tgz *.csv", shell=True)` invoked shell interpretation with wildcard expansion, creating command injection and privilege escalation vectors. | Replaced `subprocess.Popen` with Python's built-in `tarfile` and `glob` modules (`tarfile.open(..., "w:gz")`), eliminating process execution risks. |
| **B113: Request Without Timeout** | Bandit / Pylint (`W3101`) | Security / **Medium** | 60 | Network request executed without a timeout, which can cause the process to hang indefinitely if the remote ERP server is unresponsive. | Added explicit `timeout=10` parameter to `requests.post`. |
| **B503: Insecure SSL/TLS Defaults** | Bandit | Security / **Medium** | 66 | `legacyChannel` defaulted to deprecated, insecure protocol `ssl.PROTOCOL_TLSv1`. | Updated protocol parameter default to modern `ssl.PROTOCOL_TLS_CLIENT`. |
| **B604: Function with `shell=True`** | Bandit | Security / **Medium** | 73 | `scheduleReminders()` passed `shell=True` to `runJob()`, leaving subcommands vulnerable to shell execution exploits. | Set `shell=False` in `scheduleReminders()` invocation. |
| **W0102: Mutable Default Argument** | Pylint | Bug / **High** | 18 | `register={}` defined as default argument in `markAttendance()`. Because default dictionaries are evaluated once at function definition, state persisted across all function calls, polluting dates across students. | Changed default argument to `register=None` and initialized `target_register = DAILY_REGISTER if register is None else register` inside function body. |
| **R1719 & Logic Bug: Eligibility Check** | Pylint | Bug / **Medium** | 29–30 | `return True if percentage > MIN_ATTENDANCE else False` redundantly used ternary logic and incorrectly excluded students meeting exact 75% threshold (`> 75` instead of `>= 75`). | Replaced with direct boolean comparison: `return percentage >= MIN_ATTENDANCE`. |
| **C0103: Naming Style** | Pylint | Style / Quality | Multiple | Function names (`addStudent`, `markAttendance`, etc.) used camelCase instead of PEP 8 snake_case. | Refactored all function identifiers and internal calls to standard snake_case (`add_student`, `mark_attendance`, etc.). |
| **C0114 & C0116: Missing Docstrings** | Pylint | Documentation | 1, 15+ | Missing module-level and function-level docstrings across all functions. | Added clear, PEP 257-compliant docstrings documenting parameters, return values, and module purpose. |
| **W1514 & R1732: File Resource Handling** | Pylint | Quality / Reliability | 50 | File opened with raw `open(path, "w")` without context manager or explicit encoding, risking resource leaks and encoding mismatches. | Refactored to `with open(path, "w", newline="", encoding="utf-8") as f:`. |
| **R1721 & R1729: Redundant Comprehensions** | Pylint | Performance / Quality | 43, 46 | Unnecessary nested list comprehensions and passing list comprehension into `any([...])`. | Simplified list extraction and used memory-efficient generator expressions inside `any(...)`. |
| **W0611 & F401: Unused Imports** | Pylint / Flake8 | Quality / Cleanliness | 1, 4, 6 | Unused modules (`os`, `json`, `datetime`) imported at module level. | Removed unused imports and organized standard library imports cleanly. |
| **E302 & E305: Blank Line Spacing** | Flake8 | Style / PEP 8 | Multiple | Only 1 blank line found between top-level functions and classes instead of required 2 blank lines. | Added 2 standard blank lines separating all top-level definitions. |
| **E501: Line Length Exceeded** | Flake8 | Style / PEP 8 | 43, 54, 60, etc. | Several statements and comments exceeded standard 79-character PEP 8 maximum line length. | Reformatted, broke arguments, and wrapped lines cleanly within 79 characters. |
| **E712: Boolean Comparison to False** | Flake8 | Style / PEP 8 | 35 | Non-idiomatic comparison `isEligible(...) == False`. | Replaced with pythonic falsiness test: `if not is_eligible(...)`. |

