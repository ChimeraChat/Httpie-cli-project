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

