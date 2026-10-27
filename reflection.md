# Reflection

## 1. What did the static analysis tools identify?

Pylint identified missing documentation, naming problems, unused values, the
late-bound lambda bug, and general maintainability issues. Flake8 highlighted
unused imports, whitespace, line length, and the bare exception. Bandit found
the most security-relevant problems: MD5, predictable random values, unsafe
`pulldom` XML parsing, a hardcoded password, swallowed exceptions, and hidden
bidirectional Unicode characters.

## 2. Which issue was most significant, and why?

The unsafe XML parser and weak MD5 hash were the most significant security
issues. XML is external input, so an unsafe parser can expose the program to
resource-exhaustion or entity-related attacks. MD5 is no longer an appropriate
cryptographic hash. The hidden Unicode characters were also important because
they can make source code appear to say something different from what it
executes.

## 3. How did the fixes improve the program?

The revised program now rejects duplicate and invalid votes, enforces the
18:00 closing boundary, handles empty elections without division errors, and
produces correct announcements. It also uses safer XML parsing, SHA-256, and
cryptographically secure receipt randomness. Clear names, docstrings, and
formatting make the code easier to review and maintain. The final checks
achieved a 10.00 Pylint score with no Bandit or Flake8 findings.

## 4. What are the limitations of static analysis?

Static analysis is excellent at finding patterns, but it does not prove that
the election rules are correct or that all runtime inputs are safe. It did not
by itself identify every behavior bug, such as duplicate voting, accepting
`"bob"` instead of `"Bob"`, or the incorrect poll-closing boundary. Tests and
manual review are still needed. In a production system I would add automated
unit and integration tests, secure external configuration, audit logging, and
continuous analysis in CI.
