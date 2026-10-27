# Static Analysis Issue Log

The line numbers in the table refer to the original `election_system.py` supplied
for the lab. High- and medium-severity findings are listed first.

| Issue | Type | Line(s) | Description | Fix Approach |
|-------|------|---------|-------------|--------------|
| Trojan Source bidirectional characters | Security (Bandit B613) | 22 | Hidden Unicode control characters made the role comparison misleading. | Removed the control characters and rewrote the officer check with normalized role names. |
| Weak MD5 hash | Security (Bandit B324) | 17 | MD5 is unsuitable for security-sensitive identifiers. | Replaced it with SHA-256 and explicit UTF-8 encoding. |
| Unsafe XML parser | Security (Bandit B409/B319) | 7, 75 | `xml.dom.pulldom` can process malicious XML entity content. | Replaced it with `defusedxml.ElementTree` and handled parse errors explicitly. |
| Duplicate votes accepted | Logic bug | 26-33 | A voter could cast multiple ballots because the `voted` flag was never checked. | Reject a vote when the registered voter has already voted. |
| Invalid candidates accepted | Logic bug | 26-33 | Any string, including `"bob"`, was appended to the tally. | Validate candidates against the fixed candidate list before recording a vote. |
| Hardcoded password | Security (Bandit B105) | 9 | A password was embedded in source code even though it was not used. | Removed the unused credential; real credentials must come from secure configuration. |
| Predictable receipt IDs | Security (Bandit B311) | 72 | `random.randint` is not suitable for security-sensitive receipt identifiers. | Used `secrets.randbelow` to generate receipt numbers. |
| Bare exception with silent failure | Reliability (Bandit B110, Flake8 E722) | 82-83 | All exceptions were swallowed, hiding malformed input and making debugging difficult. | Catch the XML parser's explicit exceptions and return a clear invalid-input result. |
| Poll closing boundary error | Logic bug | 29 | Checking only the hour allowed votes after 18:00, such as 18:30. | Compare the complete time against `18:00`. |
| Division by zero | Logic bug | 52, 55 | Empty elections or no registered voters caused runtime errors. | Return `0.0` for percentages when the denominator is zero. |
| Late-bound announcement lambdas | Logic bug | 65-69 | Every lambda captured the final candidate name. | Build announcements directly from each candidate and its tally. |
| Unused imports and variables | Quality (Pylint/Flake8) | 1-3, 32, 45, 55 | Dead code obscured behavior and lowered maintainability. | Removed unused imports and variables. |

## Verification

- Pylint: **10.00/10**
- Bandit: **No issues identified**
- Flake8: **No violations**
