# Lab 7: Fuzzing for Input Validation Bugs

- **Student Name:** `Shakthi Raja G P`
- **SRN:** `PES1UG25CS843`
- **Section:** `L`
- **Semester:** `5`
- **Assigned Problem & Repository:** Problem #60: Marathon Registration Parser (`SETAPESU26/L6_L7_60_marathon_registration`)
- **Module Under Test:** [`marathon_registration_parser.py`](marathon_registration_parser.py)
- **Fuzzing Test Suite:** [`test_marathon_registration_parser.py`](test_marathon_registration_parser.py)

---

## 1. Executive Summary

This lab explores **Fuzz Testing** as a dynamic security and quality assurance methodology using the **Hypothesis** property-based testing framework in Python. 

The application under test (`marathon_registration_parser.py`) processes user-provided inputs for marathon race registration:
1. `format_bib_name(name)`: Formats and truncates a runner's name for bib printing.
2. `parse_finish_time(text)`: Converts a finish time string written as `H:MM:SS` into total seconds.
3. `average_split(text)`: Computes the arithmetic mean of 5 km interval splits given in minutes separated by spaces.

Initially, the application assumed all inputs were well-formed non-empty strings. Using property-based fuzzing with Hypothesis (`st.text() | st.none()`), critical unhandled crashes were automatically discovered:
- `AttributeError` on `None` inputs across all functions.
- `ValueError` on empty, single-token, or non-numeric finish time strings.
- `ZeroDivisionError` on empty split strings and `ValueError` on non-numeric splits.

Through systematic defensive programming, each function was hardened to validate types, check boundaries, and handle malformed data gracefully without throwing unhandled exceptions.

---

## 2. Bug Discovery & Falsifying Examples

| Function | Root Cause in Buggy Code | Minimal Falsifying Input | Exception Raised | Hardened Safe Behavior |
|:---|:---|:---:|:---:|:---|
| `format_bib_name` | Assumed non-empty string, called `name.strip()` directly | `s = None` | `AttributeError: 'NoneType' object has no attribute 'strip'` | Checks `isinstance(name, str)`; returns `""` for invalid/null inputs |
| `parse_finish_time` | Unpacked `text.split(':')` expecting exactly 3 items; converted to `int` without validation | `s = ''`<br>`s = None`<br>`s = 'a:b:c'` | `ValueError: not enough values to unpack`<br>`AttributeError: 'NoneType' has no split`<br>`ValueError: invalid literal for int()` | Validates string type, ensures exactly 3 parts, validates non-negative integers; returns `None` on error |
| `average_split` | Executed `len(splits)` division without checking for empty list; converted items to `int` | `s = ''`<br>`s = ':'`<br>`s = None` | `ZeroDivisionError: division by zero`<br>`ValueError: invalid literal for int()`<br>`AttributeError: 'NoneType' has no split` | Checks for non-empty split list, validates integer conversions; returns `None` on error |

---

## 3. Terminal Verification Screenshots

All screenshots were captured from the user's active **Alacritty** terminal running **Fish Shell** with the **Noctalia** theme:

| ID | Filename | Description |
|:---:|:---|:---|
| **SS1** | [`SS1_buggy_run.png`](SS1_buggy_run.png) | Interactive execution of `python marathon_registration_parser.py` on the initial buggy module with standard valid inputs. |
| **SS2** | [`SS2_hypothesis_failing.png`](SS2_hypothesis_failing.png) | Execution of `pytest test_marathon_registration_parser.py` on the buggy module showing all 3 test functions failing with falsifying examples. |
| **SS3** | [`SS3_fixed_run.png`](SS3_fixed_run.png) | Interactive execution of `python marathon_registration_parser.py` on the hardened module verifying correct happy-path operation. |
| **SS4** | [`SS4_hypothesis_passing.png`](SS4_hypothesis_passing.png) | Execution of `pytest test_marathon_registration_parser.py` on the hardened module showing all 3 Hypothesis fuzzing property tests passing (100%). |

---

## 4. Execution Commands

### Virtual Environment Setup
```bash
source ../.venv/bin/activate
cd lab-07
```

### Run Application Interactively
```bash
python marathon_registration_parser.py
```

### Run Hypothesis Fuzzing Test Suite
```bash
pytest test_marathon_registration_parser.py
```

---

## 5. Deliverables & Artifacts

```
lab-07/
├── 01-fuzz-testing-report.docx              # Formal academic lab report in Word format
├── 01-fuzz-testing-report.pdf               # Formal academic lab report in PDF format
├── PES1UG25CS843_Shakthi_Raja_LAB7.pdf      # Student-named lab report copy
├── README.md                                # Comprehensive documentation (this file)
├── marathon_registration_parser.py          # Hardened application under test
├── test_marathon_registration_parser.py     # Completed Hypothesis property-based fuzz tests
├── SS1_buggy_run.png                        # Alacritty screenshot: buggy app execution
├── SS2_hypothesis_failing.png               # Alacritty screenshot: Hypothesis test failures
├── SS3_fixed_run.png                        # Alacritty screenshot: hardened app execution
└── SS4_hypothesis_passing.png               # Alacritty screenshot: Hypothesis tests passing
```

---

## 6. Local Git Commit Progression

1. `3db1f26`: `feat(lab-07): add initial marathon registration parser starter code and test template`
2. `9c17b4b`: `test(lab-07): implement hypothesis fuzz testing and capture test failures on buggy code`
3. `c17ea70`: `fix(lab-07): harden parser functions against edge cases and malformed inputs`
4. Pending commit: `docs(lab-07): add fuzz testing report and documentation`
