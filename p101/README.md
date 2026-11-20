# DV033G: testing HTTPie offline request construction

Repository: <https://github.com/ChimeraChat/Httpie-cli-project>, branch `dv033g`.
Baseline: `5b604c37c6c67e18e7c3e9aee6c88a8c22b98345`, HTTPie 3.2.4.
The submitted report identifies the final tag or commit; the baseline above is
the starting point, not the final submission identifier.

## Scope and contribution

HTTPie `--offline` builds and prints an HTTP request without sending it. This
project extends `tests/test_offline.py` from nine original tests to seventeen,
adding eight checks for explicit methods, file bodies, Content-Type selection,
chunked output, empty and extensionless files, no-send behaviour, and an invalid
file-field error followed by correction using `--form`.

These are CLI/integration-style tests: they exercise real parsing, request
construction and output code through HTTPie's existing test helper. Only the
no-send checks replace `requests.sessions.Session.send` with a failing mock.
Production HTTPie code has not been changed.

The focus is functional correctness, file-input robustness and one narrow
error-and-recovery scenario. The project does not establish general usability,
network-stack correctness, performance, security or cross-platform compatibility.
Mutation testing was optional in the plan and was not performed.

Test design used documented CLI behaviour as the primary oracle, with inspection
of existing tests and implementation to understand paths and avoid duplication.
The new error check overlaps with upstream upload validation but additionally
checks offline recovery and absence of calls to the send boundary. It does not
claim discovery of an entirely untested validation rule.

- [HTTPie offline-mode documentation](https://httpie.io/docs/cli/offline-mode)
- [HTTPie file-upload documentation](https://httpie.io/docs/cli#file-upload-forms)
- [Risk, test and oracle table](test-design.md)
- [Environment and baseline findings](baseline.md)

## Environment and installation

Recorded execution environment: Windows, Python **3.13.16**, pytest **9.1.1**.
Python 3.14 failed before collection in a dependency; see the baseline notes.
Internet access is needed to install dependencies. The focused offline tests do
not need a live HTTP service. The full suite uses local HTTP/HTTPS test servers
and subprocesses, and some cases contact `pie.dev` or install plugin build
dependencies. Network, package-index or process restrictions can block those cases.

From the repository root, with Python 3.13 installed, use PowerShell:

```powershell
py -3.13 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -e '.[dev]'
.\.venv\Scripts\python.exe -m httpie --version
```

The editable development install follows the repository's existing dependency
declarations. Unpinned dependencies can change; the original installed versions
are recorded in [pip-freeze-python313.txt](evidence/setup/pip-freeze-python313.txt).
The final environment is separately recorded in
[pip-freeze-2026-10-28.txt](evidence/final/pip-freeze-2026-10-28.txt); it should
not be assumed identical to the earlier snapshot. These files are environment
snapshots, not portable lockfiles. Fresh dependency
installation has not been repeated for this final verification. On Linux/macOS,
use `python3.13 -m venv .venv` and `.venv/bin/python` in the commands below.

## Reproduce the tests

Run these commands from the repository root, not from `p101`. Activation of the
virtual environment is unnecessary when its interpreter is called explicitly.

```powershell
# Complete offline suite (9 original + 8 project additions).
.\.venv\Scripts\python.exe -m pytest tests/test_offline.py -vv

# Focused error message and successful correction, both offline.
.\.venv\Scripts\python.exe -m pytest tests/test_offline.py::test_offline_file_field_error_suggests_form -vv

# Full regression suite, including doctest collection.
.\.venv\Scripts\python.exe -m pytest httpie tests -vv

# Branch-aware coverage of the three selected production modules.
.\.venv\Scripts\python.exe -m pytest tests/test_offline.py -vv --cov=httpie.client --cov=httpie.uploads --cov=httpie.cli.argparser --cov-branch --cov-report=term-missing
```

To measure only the original nine tests on the unchanged production code,
select their exact node IDs. This avoids editing files or excluding new tests
using fragile name patterns:

```powershell
$originalTests = @(
    'tests/test_offline.py::test_offline'
    'tests/test_offline.py::test_offline_raw'
    'tests/test_offline.py::test_offline_raw_empty_should_use_POST'
    'tests/test_offline.py::test_offline_form'
    'tests/test_offline.py::test_offline_json'
    'tests/test_offline.py::test_offline_multipart'
    'tests/test_offline.py::test_offline_from_file'
    'tests/test_offline.py::test_offline_chunked'
    'tests/test_offline.py::test_offline_download'
)
.\.venv\Scripts\python.exe -m pytest @originalTests -vv --cov=httpie.client --cov=httpie.uploads --cov=httpie.cli.argparser --cov-branch --cov-report=term-missing
```

Final verification redirected `TEMP`/`TMP` to a writable directory under the
ignored `artifacts/` directory, disabled pytest's cache using
`-p no:cacheprovider`, and supplied a fresh `--basetemp` for each run. These are
environment accommodations, not changes to assertions. Each saved final log
records the actual command, environment location and Python process exit code.
Use a new, dedicated directory when supplying `--basetemp`: pytest manages and
can clear that directory.

## Results and evidence

Historical baseline full suite: **1003 passed, 2 failed, 19 skipped, 4 xfailed**
from 1028 collected tests. Both failures concern Big5 encoding and predate the
test additions. See [the original log](evidence/setup/pytest-python313.txt).

The 28 October comparison reruns the original nine test functions and all
seventeen tests against the same production code and installed environment:

| Selected production scope | Original 9: coverage / missed statements / partial branches | Extended 17: coverage / missed statements / partial branches |
| --- | --- | --- |
| `httpie.cli.argparser` | 44% / 154 / 33 | 48% / 141 / 30 |
| `httpie.client` | 65% / 50 / 17 | 65% / 50 / 17 |
| `httpie.uploads` | 34% / 79 / 2 | 34% / 79 / 2 |
| **Total** | **48% / 283 / 52** | **50% / 270 / 49** |

- [Original nine: 9 passed, process exit 0](evidence/final/coverage-original-9-2026-10-28.txt).
- [Extended suite: 17 passed, process exit 0](evidence/final/coverage-extended-17-2026-10-28.txt).
- Final full suite: **980 passed, 33 failed, 19 skipped, 4 xfailed**, 1036
  collected, process exit **1**, in 168.44 seconds. See
  [pytest-full-2026-10-28.txt](evidence/final/pytest-full-2026-10-28.txt).
- [Machine-readable run summary](evidence/final/run-summary-2026-10-28.json).
- [Earlier 16-test evidence](evidence/testing/pytest-offline-16-tests.txt) and
  [coverage](evidence/coverage/coverage-offline-extended-16.txt) are preserved.

The final full run is not green and is not directly comparable to the original
less-restricted baseline. The failures divide into:

- **19 external-service cases:** `pie.dev` connections rejected with Windows
  socket permission error 10013.
- **12 plugin-installation cases:** the fixture cannot install its dummy
  plugins. A separate [installation diagnostic](evidence/final/plugin-install-diagnostic-2026-10-28.txt)
  reproduces the failure; a [verbose pip diagnostic](evidence/final/plugin-build-diagnostic-2026-10-28.txt)
  shows isolated build setup cannot obtain `setuptools>=40.8.0` from the available
  package source. That diagnostic used zero pip retries and a five-second timeout.
- **2 Big5 charset cases:** the same named failures recorded in the original
  baseline.

The [failure classification](evidence/final/failure-classification-2026-10-28.json)
lists the exact node IDs. All seventeen offline tests passed within the full
run. A full run in an environment permitting external-service access and plugin
build-dependency installation is still needed to compare the broader suite
without these restrictions. No full-regression success is claimed.

`Cover` is coverage.py's combined statement/branch-aware percentage, rounded to
whole numbers; it is not branch coverage alone or coverage of all HTTPie code.
`BrPart` counts partially covered branches. The final invalid-file-field test
also executes error-reporting paths, accounting for newly reached statements;
this should not be interpreted as equivalent growth in fault-detection ability.

The empty-file test checks a distinct boundary without requiring extra measured
coverage. The no-send test checks a side effect that printed output alone does
not establish. The final error/recovery test checks a corrective hint and that
following it produces the intended multipart request. Passing these assertions
adds bounded behavioural evidence; no functional defect was exposed by the
offline additions.

## Warnings, limitations and CI

ResourceWarnings about unclosed request-body files recur in the original and
extended suites, including at interpreter shutdown. Their underlying ownership
and cleanup cause has not been established, so they are recorded as unresolved
observations, not dismissed as environment-only warnings or claimed as a
confirmed product defect. Warning counts depend on collection and cleanup timing.

The final test runner captured stdout/stderr directly and recorded Python's
exit code. Historical PowerShell logs can contain `NativeCommandError` after a
passing pytest summary because shutdown warnings were written to stderr; read
the pytest result and wrapper behaviour separately.

`Session.send.assert_not_called()` establishes non-invocation of that boundary
for the tested inputs. It is not packet monitoring or proof against every
possible network path. Output assertions do not test user comprehension with
participants. Conclusions are limited to the selected cases and recorded
environment.

The upstream [test workflow](../.github/workflows/tests.yml) runs for matching
pull requests and pushes to `master`; a push to `dv033g` alone does not trigger
it. Its Python matrix differs from this local Python 3.13 environment. No new
hosted CI run or fresh installation is claimed by these local logs.

## Evidence navigation

| Artifact | Purpose |
| --- | --- |
| `tests/test_offline.py` | Nine upstream tests and eight additions |
| `p101/test-design.md` | Behaviour/risk, rationale, oracle and outcomes |
| `p101/baseline.md` | Baseline identity and setup/failure interpretation |
| `p101/evidence/setup/` | Original environment snapshots and full-suite baseline |
| `p101/evidence/testing/` | Historical focused test results |
| `p101/evidence/coverage/` | Historical scoped coverage comparisons |
| `p101/evidence/final/` | Final local verification, actual commands and exit codes |
| `p101/presentation/` | Conference presentation source; a historical snapshot |

The assessed PDF contains the source comparison, individual reflection and final
repository identifier. The local personal work plan is outside this repository.
