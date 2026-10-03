# Project Baseline

## Repository

- Repository: https://github.com/ChimeraChat/Httpie-cli-project
- Branch: `dv033g`
- Baseline commit: `5b604c37c6c67e18e7c3e9aee6c88a8c22b98345`
- HTTPie version: `3.2.4`

No HTTPie source code had been modified when this baseline was established.

---

## Environment attempt 1 — Python 3.14

**Date:** 2026-10-03
**Python:** `3.14.0`
**pip:** `26.0.1`

### CLI sanity check

`http --version`

**Result:** PASS — HTTPie started successfully.

### Offline request construction

`http --offline example.org hello=world`

**Result:** PASS — HTTPie constructed and printed a POST request in offline mode.

### Existing test suite

`python -m pytest`

**Result:** BLOCKED BEFORE TEST COLLECTION.

Pytest failed while loading `pytest_httpbin` through the httpbin/Flask/Werkzeug dependency chain.

Final exception:

`AttributeError: module 'ast' has no attribute 'Str'`

### Interpretation

HTTPie itself and the selected offline functionality worked under Python 3.14, but the existing test environment was incompatible with this Python version. The failure occurred before HTTPie tests were collected and is therefore treated as an environment/setup issue rather than an HTTPie test failure.

### Evidence

- `p101/evidence/setup/environment-python314.txt`
- `p101/evidence/setup/offline-python314.txt`
- `p101/evidence/setup/pytest-python314.txt`

---

## Environment attempt 2 — Python 3.13

**Date:** 2026-10-04
**Python:** `3.13.16`
**HTTPie:** `3.2.4`
**pytest:** `9.1.1`

### Full existing test suite

`python -m pytest`

**Result:**

- 1028 tests collected
- 1003 passed
- 2 failed
- 19 skipped
- 4 xfailed
- 113 warnings
- Execution time: approximately 118 s

Both failures occurred in `tests/test_encoding.py` and concern Big5 charset detection:

- `test_terminal_output_response_charset_detection`
- `test_terminal_output_request_charset_detection`

The second failure exercises request charset detection in offline mode.

### Focused offline baseline

`python -m pytest tests/test_offline.py -vv`

**Result:**

- 9 collected
- 9 passed
- 0 failed
- 1 warning
- Execution time: 0.76 s

The warning was a `ResourceWarning` related to an unclosed file handle during `test_offline_chunked`.

### Interpretation

Python 3.13 provides a usable development and test environment for the project.

The two Big5 test failures are included in the baseline, but they were already documented in the project before this
test run. They are therefore not treated as new defects found during this project.

The dedicated offline test suite passed all tests. This environment will therefore be used for continued baseline
analysis and test development.

### Evidence

- `p101/evidence/setup/environment-python313.txt`
- `p101/evidence/setup/pip-freeze-python313.txt`
- `p101/evidence/setup/pytest-python313.txt`
- `p101/evidence/setup/pytest-offline-python313.txt`
- `p101/evidence/setup/pytest-encoding-python313.txt`

---

The usable project baseline is:

- Python `3.13.16`
- HTTPie `3.2.4`
- baseline commit `5b604c37c6c67e18e7c3e9aee6c88a8c22b98345`
- existing suite: `1003 passed / 2 failed`
- offline suite: `9 passed / 0 failed`

