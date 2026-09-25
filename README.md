# Password Strength Checker

A command-line tool that evaluates password strength locally and explains
*why* a password received its rating — not just a pass/fail score.

## Overview

This project checks a password against six independent security criteria
(length, character variety, and common-password matching), calculates a
score, classifies the result into a strength category, and gives specific,
actionable suggestions for improvement. It was built as a learning project
to practice both Python fundamentals and core password-security concepts.

## Features

- Interactive command-line prompt with **hidden password input** (nothing
  is echoed to the terminal as you type)
- Six independent checks:
  - Minimum length (12+ characters)
  - Uppercase letters
  - Lowercase letters
  - Numbers
  - Special characters
  - Not a commonly used / breached-style password
- Simple, transparent scoring system (X out of 6 checks passed)
- Five-tier classification: **Very Weak, Weak, Moderate, Strong, Very Strong**
- Specific recommendations for each failed check
- 100% local — no network calls, no external services
- The password itself is **never stored, logged, or printed back**

## Technologies

- **Python 3** (standard library only — `re`, `string`, `getpass`)
- **unittest** for automated testing

No third-party packages are required (see `requirements.txt`).

## How it works

1. `getpass.getpass()` reads the password without echoing it to the screen.
2. Six check functions (`check_length`, `check_uppercase`, etc.) each
   return `True`/`False` for one specific rule.
3. `calculate_score()` counts how many checks passed.
4. `classify_strength()` converts the score into one of five strength
   labels.
5. `get_recommendations()` looks at exactly which checks failed and
   returns targeted advice.
6. `print_report()` displays everything — except the password itself,
   which is deleted from memory (`del password`) immediately after
   evaluation and never touches the display, disk, or network.

## Project structure

```
password-strength-checker/
├── src/
│   └── password_checker.py       # All logic + CLI entry point
├── tests/
│   └── test_password_checker.py  # unittest suite
├── README.md
└── requirements.txt
```

## Installation

Requires Python 3.8 or newer. No dependencies to install.

```bash
git clone https://github.com/YOUR_USERNAME/password-strength-checker.git
cd password-strength-checker
```

## Running the app

```bash
python src/password_checker.py
```

You'll be prompted to enter a password (input will be hidden), and the
report will be printed immediately.

## Running the tests

From the project root:

```bash
python -m unittest discover tests -v
```

The test suite (30 tests) covers:
- Each individual check function in isolation
- Score calculation
- Strength classification boundaries
- End-to-end evaluation for very weak, weak, missing-uppercase,
  missing-lowercase, missing-numbers, missing-special-character,
  strong, very strong, and common passwords

All test passwords are fictional strings created solely to exercise
specific rules — none are real credentials.

## Security considerations

This tool follows a **data minimization** approach: it only ever holds
a password in memory for the brief moment needed to evaluate it.

- **No storage** — the password is never written to a file or database.
- **No logging** — the password is never printed to the console or
  included in any log output.
- **No network activity** — all evaluation happens locally; nothing is
  sent to an external API or service.
- **Hidden input** — `getpass.getpass()` prevents the password from
  appearing in the terminal or shell history.
- **Explicit cleanup** — the password variable is deleted (`del password`)
  as soon as evaluation is complete.

### Limitations (by design, for a learning project)

- The common-password list is small and local. A production system
  would check against a much larger breach-derived dataset (e.g. via
  k-anonymity APIs like Have I Been Pwned — which this project
  deliberately avoids using, to keep everything local).
- This tool estimates strength using rule-based heuristics, not true
  entropy calculation or pattern-detection algorithms (like `zxcvbn`).
  It's a solid learning foundation, not a replacement for a production
  password-strength library.

## Example output

```
Password Strength Checker
Enter password:
Strength: Strong
Score: 5/6

Checks:
✓ At least 12 characters
✓ Contains uppercase letters
✓ Contains lowercase letters
✓ Contains numbers
✗ Contains special characters
✓ Not a commonly used password

Recommendation:
- Add at least one special character (e.g. ! @ # $ % &).
```
