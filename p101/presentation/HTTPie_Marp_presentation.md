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
    padding: 56px 68px;
  }
  section.lead {
    background: linear-gradient(135deg, #0f172a 0%, #1e293b 62%, #334155 100%);
    color: #f8fafc;
  }
  section.lead h1,
  section.lead h2 { color: #ffffff; }
  h1 {
    color: #0f172a;
    font-size: 44px;
    margin: 0 0 22px 0;
  }
  h2 {
    color: #334155;
    font-size: 28px;
    font-weight: 500;
  }
  h3 {
    color: #0f172a;
    margin-top: 0;
  }
  strong { color: #0f5ca8; }
  section.lead strong { color: #93c5fd; }
  code { font-size: 0.88em; }

  pre code {
    color: #f8fafc;
    font-size: 22px;
    line-height: 1.35;
  }
  .kicker {
    font-size: 20px;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    color: #64748b;
    margin-bottom: 10px;
  }
  section.lead .kicker { color: #cbd5e1; }
  .columns {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 34px;
    align-items: stretch;
  }
  .card {
    background: #ffffff;
    border: 1px solid #dbe2ea;
    border-radius: 14px;
    padding: 22px 24px;
  }
  .card p:last-child { margin-bottom: 0; }
  .statement {
    font-size: 31px;
    line-height: 1.25;
    font-weight: 650;
    margin: 18px 0;
  }
  .muted {
    color: #64748b;
    font-size: 20px;
  }
  .callout {
    margin-top: 24px;
    padding: 16px 20px;
    border-left: 5px solid #0f5ca8;
    background: #eaf3fb;
    font-size: 23px;
  }
  .flow {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 14px;
    margin: 26px 0 10px 0;
  }
  .flow div {
    background: #ffffff;
    border: 1px solid #cbd5e1;
    border-radius: 12px;
    padding: 18px 12px;
    text-align: center;
    font-weight: 650;
    font-size: 21px;
  }
  .toolgrid {
    display: grid;
    grid-template-columns: repeat(2, 1fr);
    gap: 18px;
    margin-top: 16px;
  }
  .tool {
    background: #ffffff;
    border: 1px solid #dbe2ea;
    border-radius: 12px;
    padding: 16px 18px;
  }
  .tool strong {
    display: block;
    font-size: 24px;
    margin-bottom: 6px;
  }
  ul {
    line-height: 1.34;
    margin-top: 8px;
  }
  li { margin: 8px 0; }

  pre {
    background: #0b132b !important;
    border-radius: 14px;
    padding: 0.9em 1em;
  }

  /* Base code text */
  pre code,
  .hljs {
    color: #f8fafc !important;
    font-size: 0.82em;
    line-height: 1.35;
  }

  /* Keywords: with, as, def, assert */
  .hljs-keyword,
  .hljs-built_in {
    color: #f472b6 !important;
  }

  /* Strings */
  .hljs-string {
    color: #93c5fd !important;
  }

  /* Function / call names */
  .hljs-title,
  .hljs-title.function_,
  .hljs-function {
    color: #facc15 !important;
  }

  /* Comments */
  .hljs-comment {
    color: #94a3b8 !important;
    font-style: italic;
  }

  /* Numbers / constants */
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

# Project introduction

<div class="columns">
<div>

<div class="statement">HTTPie CLI</div>

Command-line HTTP client.
<div class="kicker">Testing focus</div>

**`--offline` request construction**

Build and print the request  
**without sending it.**

</div>
<div>

```bash
http --offline example.org hello=world
```

```text
CLI input
   ↓
prepare request
   ↓
print request
   ↓
no network send
```

</div>
</div>

<div class="callout">
As I work alone my project is focused on a more narrowed scope: [--offline] request construction.
</div>

---

# Existing testing

<div class="columns">
<div class="card">

### Already in place

**Practice:** automated regression testing  
**Level:** CLI / integration-style  
**Framework:** pytest  
**Coverage:** pytest-cov

</div>
<div class="card">

### First decision

- Inspect existing tests
- Trace request-building code
- Map existing coverage
- Avoid duplicate tests

</div>
</div>

<div class="flow">
  <div>Test input</div>
  <div>HTTPie test helper</div>
  <div>Request construction</div>
  <div>Captured result</div>
</div>


---

# My testing work

<div class="columns">
<div>

### How I chose test cases

- Relevant to `--offline`
- Gap in existing coverage
- Clear and testable oracle
- Useful as a boundary or option interaction

</div>
<div>

### Areas I extended

- Explicit method + request data
- File and `Content-Type` handling
- Empty and extensionless files
- `--chunked` combined with file input
- Verify no network request sent

</div>
</div>


---

# A representative test

<div class="muted">Simplified from the project test.</div>

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

### Why this test matters
<br>
Printed output can still look correct

if a network request is sent.
<br>

**Oracle:** `Session.send()` must never be called.

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

<br>
<div class="callout">
Coverage changed little; branch and behavioural evidence became stronger.
</div>

---

# AI-assisted workflow

<div class="columns">
<div class="card">

### My work

- Read source code and tests
- Defined the project scope
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
<strong>AI was used as part of the workflow.</strong><br>
I reviewed suggestions against the code, existing tests and local results.
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

### What I learned

- Inspect before extending
- Strong oracle > test count
- Coverage needs interpretation
- Evidence must support the claim

</div>
</div>

