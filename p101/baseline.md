\# P101 Baseline



\## Repository



Repository:

https://github.com/ChimeraChat/Httpie-cli-project



Working branch:

`dv033g`



Baseline commit:

`5b604c37c6c67e18e7c3e9aee6c88a8c22b98345`



\## Environment attempt 1



Date:

2026-10-03



Python:

`3.14.0`



pip:

`26.0.1`



HTTPie:

`3.2.4`



\## CLI sanity check



Command:



`http --version`



Result:



PASS — HTTPie started successfully and reported version 3.2.4.



Evidence:



`p101/evidence/setup/environment-python314.txt`



\## Offline request construction



Command:



`http --offline example.org hello=world`



Result:



PASS — HTTPie constructed and printed a POST request in offline mode.



Evidence:



`p101/evidence/setup/offline-python314.txt`



\## Existing test suite



Command:



`python -m pytest`



Result:



BLOCKED BEFORE TEST COLLECTION.



Pytest failed while loading the `pytest\_httpbin` plugin. The failure occurred in

the dependency chain before HTTPie's tests were collected.



Final exception:



`AttributeError: module 'ast' has no attribute 'Str'`



Evidence:



`p101/evidence/setup/pytest-python314.txt`



\## Interpretation



The failure is currently classified as a test-environment compatibility issue,

not as a failure in HTTPie's production code or an HTTPie test failure, because

pytest terminated during plugin loading before test collection.



HTTPie itself and the selected offline functionality were executable under

Python 3.14.0.



\## Next action



Test the existing HTTPie test environment with an earlier Python version before

making changes to the HTTPie source code or test suite.



The Python 3.14 result is retained as baseline/setup evidence.


## Environment attempt 2

Date:
2026-10-04

Python:
`3.13.16`

HTTPie:
`3.2.4`

pytest:
`9.1.1`

### Existing test suite

Command:

`python -m pytest`

Result:

1028 tests collected.

- 1003 passed
- 2 failed
- 19 skipped
- 4 xfailed
- 113 warnings

Execution time:
approximately 118 seconds.

The two failures occurred in `tests/test_encoding.py` and both concern
Big5 charset detection:

- `test_terminal_output_response_charset_detection`
- `test_terminal_output_request_charset_detection`

The second failing test exercises request charset detection in offline mode.

The dedicated `tests/test_offline.py` test group otherwise passed during the
full baseline run.

### Interpretation

Python 3.13 provides a usable development and test environment for this
project. Unlike Python 3.14, pytest successfully loads the test environment
and executes the existing suite.

The two encoding failures are retained as part of the baseline. They are not
currently classified as newly discovered defects because related upstream
work already exists concerning these exact tests and Big5 charset detection.

No HTTPie source code has been modified at this stage.

### Evidence

- `p101/evidence/setup/environment-python313.txt`
- `p101/evidence/setup/pip-freeze-python313.txt`
- `p101/evidence/setup/pytest-python313.txt`
- `p101/evidence/setup/pytest-offline-python313.txt`
- `p101/evidence/setup/pytest-encoding-python313.txt`
