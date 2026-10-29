# Lab 6: Code and Branch Coverage Analysis

- **Student Name:** `Shakthi Raja G P`
- **SRN:** `PES1UG25CS843`
- **Section:** `L`
- **Semester:** `5`
- **Assigned Repository:** `SETAPESU26/L6_L7_60_marathon_registration` (Problem #60)
- **Module Under Test:** [`marathon_registration.py`](file:///home/sr/Downloads/se-lab/se-lab-coursework/lab-06/marathon_registration.py)

---

## 1. Executive Summary

This lab focuses on the implementation, evaluation, and comparative analysis of **Line/Statement Coverage** and **Branch Coverage** using the Python `coverage` framework on a marathon registration management system (`marathon_registration.py`). 

The application implements three primary business logic functions:
1. `calculate_entry_fee(race, age, early_bird)`: Calculates race fees based on distance (`5k`, `10k`, `half`, `full`), age thresholds (junior under 18 discount, senior 60+ discount), early-bird discounts (20% off), and eligibility validation (minors barred from half/full marathons).
2. `assign_wave(race, qualifying_time_minutes, bib_number)`: Allocates runners to starting waves (Wave A elite, Wave B fast, Wave C open, Wave D walking/charity) based on qualifying pace thresholds and bib assignment fallback rules.
3. `determine_finisher_status(chip_time_seconds, dnf, dq)`: Evaluates competition outcomes into categorical states (`Disqualified`, `Did Not Finish`, `Finisher`, or `Time Limit Exceeded` at 6 hours).

Across the experiment:
- The initial baseline suite achieved only **37% statement coverage** and **32% branch coverage**.
- An enhanced statement coverage suite ([`CodeCoverageTest_marathon_registration.py`](file:///home/sr/Downloads/se-lab/se-lab-coursework/lab-06/CodeCoverageTest_marathon_registration.py)) was constructed, reaching **100% statement coverage** (38/38 statements) but revealing hidden logical vulnerabilities due to missing branch decisions (achieving 75% branch coverage).
- A rigorous branch coverage test suite ([`BranchCoverageTest_marathon_registration.py`](file:///home/sr/Downloads/se-lab/se-lab-coursework/lab-06/BranchCoverageTest_marathon_registration.py)) was developed to achieve **100% branch coverage** (28/28 branches) and **100% statement coverage** (38/38 statements), validating all compound predicate combinations and boundary edges.

---

## 2. Coverage Progression Summary

| Test Phase | Test Suite File | Stmts | Exec | Stmt Cov | Branch Total | Branch Partial | Branch Cov | Handout Target |
|:---|:---|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| **Baseline** | `test_marathon_registration.py` | 38 | 14 | **37%** | 28 | 7 | **32%** | N/A |
| **Phase 1: Code Coverage** | `CodeCoverageTest_marathon_registration.py` | 38 | 38 | **100%** | 28 | 7 | **75%** | $\ge 90\%$ (Exceeded) |
| **Phase 2: Branch Coverage** | `BranchCoverageTest_marathon_registration.py` | 38 | 38 | **100%** | 28 | 0 | **100%** | $\ge 90\%$ (Exceeded) |

---

## 3. Comparative Gap Analysis: Statement vs. Branch Coverage

A core objective of this lab is analyzing why **100% statement coverage is insufficient for software reliability**:

1. **Short-Circuit Evaluation in Compound Conditions:**
   - In `calculate_entry_fee`:
     ```python
     if race in ("half", "full") and age < 18:
         raise ValueError("Runners under 18 cannot enter half or full marathons")
     ```
   - When reaching 100% statement coverage, executing a test with `race="half", age=16` executes the body `raise ValueError(...)`.
   - However, the branch where `race in ("half", "full")` is `True` while `age < 18` is `False` (adult running half/full marathon) is an independent decision path. Similarly, `race="5k"` with `age < 18` evaluates the first clause to `False` immediately.
   - Statement coverage cannot guarantee that both outcomes of compound predicates are exercised.

2. **Hidden Fallthrough Branches in Multi-Branch Predicates:**
   - In `assign_wave`:
     ```python
     if race == "full":
         if qualifying_time_minutes is not None:
             if qualifying_time_minutes < 180:
                 return "Wave A"
             elif qualifying_time_minutes < 240:
                 return "Wave B"
             else:
                 return "Wave C"
         else:
             if bib_number is not None and bib_number < 1000:
                 return "Wave A"
             elif bib_number is not None and bib_number < 5000:
                 return "Wave B"
             return "Wave C"
     ```
   - To achieve statement coverage, one only needs tests reaching each individual `return` statement.
   - However, in `bib_number is not None and bib_number < 1000`, the branch where `bib_number is None` at the second check is evaluated differently from `bib_number >= 5000`. Full branch coverage forces the construction of explicit vectors for `bib_number=None`, `bib_number=800`, `bib_number=3500`, and `bib_number=7500`, ensuring all 28 execution branches are exercised.

---

## 4. Test Suite Architecture

### 4.1. Statement Coverage Suite (`CodeCoverageTest_marathon_registration.py`)
Consists of 15 targeted test cases exercising all functional paths:
- `test_entry_fee_5k_standard`: Standard 5k registration.
- `test_entry_fee_10k_senior_discount`: 10k senior discount calculation.
- `test_entry_fee_half_early_bird_discount`: Half marathon early-bird discount calculation.
- `test_entry_fee_full_junior_rejected`: Age boundary validation rejecting minors from full marathon.
- `test_entry_fee_full_standard`: Standard full marathon calculation.
- `test_entry_fee_invalid_race`: Input validation raising `ValueError` on unknown distance.
- `test_entry_fee_invalid_age_negative`: Input validation raising `ValueError` on negative age.
- `test_assign_wave_full_qualifying_times`: Elite, fast, and open wave allocation for full marathon.
- `test_assign_wave_full_bib_numbers`: Bib number fallback allocation when no qualifying time is provided.
- `test_assign_wave_half_qualifying_and_bib`: Half marathon wave routing with both qualifying times and bib fallbacks.
- `test_assign_wave_short_races`: 5k/10k wave allocations (Wave C vs Wave D).
- `test_determine_finisher_status_disqualified`: Verification of priority DQ flag handling.
- `test_determine_finisher_status_dnf`: Verification of DNF flag handling.
- `test_determine_finisher_status_over_time_limit`: Verification of 6-hour cut-off logic.
- `test_determine_finisher_status_valid_finisher`: Standard successful finisher recording.

### 4.2. Branch Coverage Suite (`BranchCoverageTest_marathon_registration.py`)
Consists of 24 rigorous test cases covering all 28 decision branches, including Boolean short-circuits and boundary conditions:
- **Fee Boundary Tests:**
  - `age=17` vs `age=18` vs `age=59` vs `age=60` across 5k, 10k, half, and full marathons.
  - Verification that minors entering 5k or 10k receive junior discounts ($5 off) without triggering the half/full rejection branch.
  - Early bird + junior discount compounding verification ($25 base - $5 junior = $20, minus 20% early bird = $16).
- **Wave Assignment Boundary Tests:**
  - Full marathon thresholds: `qualifying_time_minutes=179` (Wave A), `180` (Wave B), `239` (Wave B), `240` (Wave C).
  - Full marathon bib fallbacks: `qualifying_time_minutes=None` with `bib_number=999` (Wave A), `1000` (Wave B), `4999` (Wave B), `5000` (Wave C), and `bib_number=None` (Wave C).
  - Half marathon thresholds: `qualifying_time_minutes=89` (Wave A), `90` (Wave B), `119` (Wave B), `120` (Wave C).
  - Half marathon bib fallbacks: `bib_number=1999` (Wave A), `2000` (Wave B), `7999` (Wave B), `8000` (Wave C), and `bib_number=None` (Wave C).
  - 10k race wave allocation: `qualifying_time_minutes=44` (Wave B), `45` (Wave C), and `qualifying_time_minutes=None` (Wave C).
  - 5k race wave allocation: `bib_number=499` (Wave C), `500` (Wave D), and `bib_number=None` (Wave D).
- **Finisher Status Boundary Tests:**
  - `chip_time_seconds=21600` (exactly 6 hours -> Finisher).
  - `chip_time_seconds=21601` (exceeds 6 hours -> Time Limit Exceeded).
  - Conflict resolution: `dq=True, dnf=True` verifies that DQ takes precedence over DNF.
  - Invalid negative chip time validation.

---

## 5. Execution and Verification

### Virtual Environment Setup
Ensure dependencies (`coverage`, `pytest`, `pillow`, `python-docx`) are installed:
```bash
source ../.venv/bin/activate
cd lab-06
```

### Run Code Coverage Suite
```bash
coverage run --source=marathon_registration -m pytest CodeCoverageTest_marathon_registration.py
coverage report -m
```

### Run Branch Coverage Suite
```bash
coverage run --branch --source=marathon_registration -m pytest BranchCoverageTest_marathon_registration.py
coverage report -m
```

---

## 6. Directory Artifacts

```
lab-06/
├── 01-code-and-branch-coverage-report.docx    # Formal lab report in Word format
├── 01-code-and-branch-coverage-report.pdf     # Formal lab report in PDF format
├── BranchCoverageTest_marathon_registration.py # Branch coverage test suite (100% branch cov)
├── CodeCoverageTest_marathon_registration.py   # Code coverage test suite (100% stmt cov)
├── README.md                                  # Comprehensive documentation (this file)
├── baseline_branch_coverage.txt               # Baseline branch coverage terminal capture
├── baseline_code_coverage.txt                 # Baseline statement coverage terminal capture
├── branch_coverage_report.txt                 # Branch coverage terminal capture
├── branch_coverage_terminal.png               # High-resolution terminal screenshot for branch cov
├── code_coverage_report.txt                   # Code coverage terminal capture
├── code_coverage_terminal.png                 # High-resolution terminal screenshot for code cov
├── marathon_registration.py                   # Application under test
└── test_marathon_registration.py              # Starter test suite
```

---

## 7. Git Commit History

1. `8b58b5a`: `feat(lab-06): add initial marathon registration starter code and baseline coverage reports`
2. `d852912`: `feat(lab-06): add code coverage tests achieving 100% statement coverage`
3. `25560ef`: `feat(lab-06): add branch coverage tests achieving 100% branch coverage`
4. Pending commit: `docs(lab-06): add coverage analysis report and documentation`
