---
marp: true
theme: default
paginate: true
size: 16:9
html: true
style: |
  section {
    font-family: "Aptos", "Segoe UI", sans-serif;
    background: #f7f8fa;
    color: #1f2937;
    padding: 52px 64px;
  }

  section.lead {
    background: linear-gradient(135deg, #0f172a 0%, #1e293b 62%, #334155 100%);
    color: #f8fafc;
  }

  section.lead h1,
  section.lead h2 {
    color: #ffffff;
  }

  h1 {
    color: #0f172a;
    font-size: 44px;
    margin: 0 0 20px 0;
  }

  h2 {
    color: #334155;
    font-size: 28px;
    font-weight: 500;
  }

  h3 {
    color: #0f172a;
    margin-top: 0;
    margin-bottom: 12px;
  }

  strong {
    color: #0f5ca8;
  }

  section.lead strong {
    color: #93c5fd;
  }

  .kicker {
    font-size: 18px;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    color: #64748b;
    margin-bottom: 8px;
  }

  section.lead .kicker {
    color: #cbd5e1;
  }

  .statement {
    font-size: 31px;
    line-height: 1.2;
    font-weight: 650;
    margin: 12px 0 16px 0;
  }

  .columns {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 32px;
    align-items: stretch;
  }

  .card {
    background: #ffffff;
    border: 1px solid #dbe2ea;
    border-radius: 14px;
    padding: 20px 22px;
  }

  .card p:last-child {
    margin-bottom: 0;
  }

  .muted {
    color: #64748b;
    font-size: 18px;
  }

  .callout {
    margin-top: 20px;
    padding: 14px 18px;
    border-left: 5px solid #0f5ca8;
    background: #eaf3fb;
    font-size: 21px;
  }

  .flow {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 12px;
    margin-top: 20px;
  }

  .flow div {
    background: #ffffff;
    border: 1px solid #cbd5e1;
    border-radius: 12px;
    padding: 16px 10px;
    text-align: center;
    font-weight: 650;
    font-size: 20px;
  }

  .toolgrid {
    display: grid;
    grid-template-columns: repeat(2, 1fr);
    gap: 16px;
    margin-top: 14px;
  }

  .tool {
    background: #ffffff;
    border: 1px solid #dbe2ea;
    border-radius: 12px;
    padding: 16px 18px;
  }

  .tool strong {
    display: block;
    font-size: 23px;
    margin-bottom: 5px;
  }

  ul {
    line-height: 1.28;
    margin-top: 8px;
    padding-left: 26px;
  }

  li {
    margin: 7px 0;
  }

  code {
    font-size: 0.9em;
  }

  pre {
    background: #0b132b !important;
    border-radius: 14px;
    padding: 0.8em 0.95em;
  }

  pre code,
  .hljs {
    color: #f8fafc !important;
    font-size: 20px;
    line-height: 1.3;
  }

  .hljs-keyword,
  .hljs-built_in {
    color: #f472b6 !important;
  }

  .hljs-string {
    color: #93c5fd !important;
  }

  .hljs-title,
  .hljs-title.function_,
  .hljs-function {
    color: #facc15 !important;
  }

  .hljs-comment {
    color: #94a3b8 !important;
    font-style: italic;
  }

  .hljs-number,
  .hljs-literal {
    color: #c4b5fd !important;
  }
---

<!-- _class: lead -->

<div class="kicker">DV033G · Principles & Practices in Software Testing</div>

# HTTPie CLI
## Testing `--offline` request construction

**Louise Larsen**

---

# What is HTTPie?

<div class="columns">
<div>

<div class="statement">Command-line HTTP client</div>

Used to create, send and inspect HTTP requests.

- API testing
- debugging requests
- quick API interaction

</div>
<div>

```bash
http POST example.org name=Louise
```

<div class="flow">
  <div>CLI command</div>
  <div>HTTP request</div>
  <div>Server / API</div>
</div>

</div>
</div>

<div class="callout">
HTTPie lets a developer interact with an API directly from the terminal instead of writing a separate script.
</div>

---

# My testing focus

<div class="columns">
<div>

<div class="statement">`--offline` request construction</div>

HTTPie still builds the request — but **does not send it**.

```bash
http --offline POST example.org \
  name=Louise course=DV033G
```

</div>
<div>

<div class="flow">
  <div>Build</div>
  <div>Print</div>
  <div>No send</div>
</div>

<div style="margin-top: 28px; font-size: 23px; line-height: 1.35;">
Useful for inspecting a request before any network communication takes place.
</div>

</div>
</div>

<div class="callout">
Working alone, I chose a focused scope so I could test one behaviour in greater depth.
</div>

---

# Existing testing

<div class="columns">
<div>

### Already in place

- Automated regression tests
- CLI / integration-style tests
- `pytest`
- `pytest-cov`

<div class="callout">
First decision: understand the existing suite before adding anything new.
</div>

</div>
<div>

### Existing test example

<div class="muted">Simplified from the original `--offline` tests.</div>

```python
def test_offline_json():
    r = http(
        '--offline',
        URL,
        'foo=bar'
    )

    assert 'POST /foo' in r
    assert r.json == {'foo': 'bar'}
```

</div>
</div>

---

# My testing work

<div class="columns">
<div>

### Test selection

- Relevant to `--offline`
- Gap in existing coverage
- Clear, testable oracle
- Boundary / option interaction

</div>
<div>

### Areas I extended

- Explicit method + request data
- File / `Content-Type` handling
- Empty / extensionless files
- `--chunked` + file input
- Verify no network request sent

</div>
</div>

<div class="callout">
<strong>Goal:</strong> stronger evidence — not simply more tests.
</div>

---

# A representative test

<div class="muted">Simplified from my project test.</div>

<div class="columns">
<div>

```python
with mock.patch(
    "requests.sessions.Session.send"
) as send:
    send.side_effect = AssertionError(
        "network send attempted"
    )

    http(
        "--offline", "POST",
        URL, "hello=world"
    )

    send.assert_not_called()
```

</div>
<div>

### Why this test?

Printed output can still look correct even if a network request is sent.

**Oracle:** `Session.send()` must never be called.

<div class="callout">
The test checks the behaviour promised by `--offline`, not only the printed output.
</div>

</div>
</div>

---

# Tools and evidence

<div class="toolgrid">
<div class="tool">
<strong>pytest</strong>
Repeatable behavioural checks
</div>

<div class="tool">
<strong>pytest-cov</strong>
Branch-path evidence
</div>

<div class="tool">
<strong>unittest.mock</strong>
Verify no network send
</div>

<div class="tool">
<strong>Code inspection</strong>
Connect tests to implementation
</div>
</div>

<div class="callout">
Coverage changed little; branch and behavioural evidence became stronger.
</div>

---

# AI-assisted workflow

<div class="columns">
<div class="card">

### My work

- Read source code and tests
- Defined project scope
- Selected test cases
- Wrote and revised tests
- Ran tests and coverage
- Evaluated the evidence

</div>
<div class="card">

### AI support

- Codebase orientation
- Explain unfamiliar code paths
- Brainstorm candidate test gaps
- Suggest test code / assertions
- Review test structure and oracles
- Organise findings

</div>
</div>

<div class="callout">
<strong>AI supported the workflow.</strong> Suggestions were reviewed against the code, existing tests and local results.
</div>

---

# Challenges and lessons learned

<div class="columns">
<div class="card">

### Challenges

- Mature existing suite
- Many duplicate test ideas
- Finding meaningful gaps
- Choosing stable oracles

</div>
<div class="card">

### Lessons learned

- Inspect before extending
- Strong oracle > test count
- Coverage needs interpretation
- Evidence must support the claim

</div>
</div>

<div class="callout">
<strong>Next:</strong> conference feedback → remaining investigation → final report.
</div>
