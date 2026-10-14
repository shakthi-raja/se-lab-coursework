# Lab 5: Static Code Analysis — Student Attendance Tracker

- **Student Name:** `Shakthi Raja G P`
- **SRN:** `PES1UG25CS843`
- **Section:** `L`
- **Semester:** `5`
- **Assigned Repository:** [`https://github.com/SETAPESU26/L5_61_attendance-tracker`](https://github.com/SETAPESU26/L5_61_attendance-tracker)

---

## Executive Summary & Results

In this lab, static analysis was performed on `attendance_tracker.py` using **Bandit** (security), **Pylint** (code quality & logic), and **Flake8** (PEP 8 style). All identified issues were systematically resolved in three targeted commits, achieving a **10.00/10 Pylint score**, **0 Bandit vulnerabilities**, and **0 Flake8 style violations**.

### Before vs. After Metrics

| Static Analysis Tool | Baseline (Before) | Final State (After) | Status |
|:---|:---:|:---:|:---:|
| **Bandit** (Security Auditor) | 8 issues (2 High, 3 Med, 3 Low) | **0 issues identified** | **PASSED** |
| **Pylint** (Code Quality & Logic) | `4.55 / 10` | **`10.00 / 10` (Target > 9.5)** | **PASSED** |
| **Flake8** (Style & PEP 8) | 25 style violations | **0 errors / violations** | **PASSED** |

---

## Deliverables

1. **Cleaned Source Code:**
   - [`attendance_tracker.py`](./attendance_tracker.py) — fully refactored, secure, PEP 8 compliant, and verified.
2. **Issue Tracking Table:**
   - [`issues.md`](./issues.md) — complete documentation of all 15 detected issues, severities, lines, and fix approaches.
3. **Formal Lab Report:**
   - [`01-static-code-analysis-report.docx`](./01-static-code-analysis-report.docx) | [`01-static-code-analysis-report.pdf`](./01-static-code-analysis-report.pdf)
4. **Static Analysis Reports (Before & After):**
   - **Bandit:** [`bandit_report_before.txt`](./bandit_report_before.txt) → [`bandit_report_after.txt`](./bandit_report_after.txt)
   - **Pylint:** [`pylint_report_before.txt`](./pylint_report_before.txt) → [`pylint_report_after.txt`](./pylint_report_after.txt)
   - **Flake8:** [`flake8_report_before.txt`](./flake8_report_before.txt) → [`flake8_report_after.txt`](./flake8_report_after.txt)

---

## Commit History for Tool Fixes

1. `feat(lab-05): add initial attendance tracker starter code and baseline reports` (`57486ce`)
2. `fix(lab-05): resolve bandit security issues with ssl, subprocess, and requests` (`a623798`)
3. `refactor(lab-05): fix pylint code quality issues, mutable default args, and add docstrings` (`32ef468`)
4. `style(lab-05): resolve flake8 formatting, line lengths, and pep 8 style issues` (`c3f75e5`)
