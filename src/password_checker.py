"""
Password Strength Checker
--------------------------
A local, command-line tool that evaluates password strength and
explains the result. No password is ever stored, logged, printed
back, or sent anywhere — everything happens in memory and is
discarded when the program exits.
"""

import re
import string
import getpass

# A small list of extremely common / weak passwords.
# This is intentionally short and local — for a real product you'd
# use a much larger breach-derived list (e.g. "Have I Been Pwned"
# style datasets), but a short local list is enough to teach the
# concept and catch the most obvious cases.
COMMON_PASSWORDS = {
    "password", "123456", "123456789", "qwerty", "abc123",
    "password1", "111111", "12345678", "letmein", "iloveyou",
    "admin", "welcome", "monkey", "dragon", "football",
    "123123", "000000", "1234567890", "qwerty123", "password123",
}

MIN_LENGTH_FOR_FULL_MARKS = 12


def check_length(password):
    """Returns True if the password meets the minimum length requirement."""
    return len(password) >= MIN_LENGTH_FOR_FULL_MARKS


def check_uppercase(password):
    """Returns True if the password contains at least one uppercase letter."""
    return any(char in string.ascii_uppercase for char in password)


def check_lowercase(password):
    """Returns True if the password contains at least one lowercase letter."""
    return any(char in string.ascii_lowercase for char in password)


def check_numbers(password):
    """Returns True if the password contains at least one digit."""
    return any(char in string.digits for char in password)


def check_special_characters(password):
    """Returns True if the password contains at least one special character."""
    special_characters = re.compile(r"[!@#$%^&*(),.?\":{}|<>_\-+=\[\];'`~/\\]")
    return bool(special_characters.search(password))


def check_not_common(password):
    """Returns True if the password is NOT in the common password list.

    The check is case-insensitive, since 'Password123' is just as
    predictable as 'password123' to an attacker.
    """
    return password.lower() not in COMMON_PASSWORDS


def run_all_checks(password):
    """Runs every individual check and returns the results as a dictionary.

    Keys are human-readable labels; values are True/False.
    Using a dictionary (rather than separate variables) makes it easy
    to loop over the results later for scoring, display, and testing.
    """
    return {
        "At least 12 characters": check_length(password),
        "Contains uppercase letters": check_uppercase(password),
        "Contains lowercase letters": check_lowercase(password),
        "Contains numbers": check_numbers(password),
        "Contains special characters": check_special_characters(password),
        "Not a commonly used password": check_not_common(password),
    }


def calculate_score(check_results):
    """Calculates a simple score: 1 point per passed check.

    check_results is the dictionary returned by run_all_checks().
    Returns a tuple of (score, total_possible).
    """
    score = sum(1 for passed in check_results.values() if passed)
    total = len(check_results)
    return score, total


def classify_strength(score, total):
    """Classifies the password based on the fraction of checks passed.

    We use a fraction (score/total) rather than raw score so the
    classification logic still works if checks are added or removed
    later. A tiny epsilon is added to each boundary to avoid floating
    point comparison bugs (e.g. 2/6 not being exactly 0.333...).

    With the current 6 checks, this maps to:
      0-1 passed -> Very Weak
      2 passed   -> Weak
      3 passed   -> Moderate
      4-5 passed -> Strong
      6 passed   -> Very Strong
    """
    fraction = score / total
    epsilon = 1e-9

    if fraction <= (1 / 6) + epsilon:
        return "Very Weak"
    elif fraction <= (2 / 6) + epsilon:
        return "Weak"
    elif fraction <= (3 / 6) + epsilon:
        return "Moderate"
    elif fraction < 1.0:
        return "Strong"
    else:
        return "Very Strong"


def get_recommendations(check_results):
    """Builds a list of specific, actionable suggestions based on
    which checks failed.

    If every check passed, returns a single positive message instead.
    """
    suggestions = []

    if not check_results["At least 12 characters"]:
        suggestions.append("Make your password at least 12 characters long.")
    if not check_results["Contains uppercase letters"]:
        suggestions.append("Add at least one uppercase letter (A-Z).")
    if not check_results["Contains lowercase letters"]:
        suggestions.append("Add at least one lowercase letter (a-z).")
    if not check_results["Contains numbers"]:
        suggestions.append("Add at least one number (0-9).")
    if not check_results["Contains special characters"]:
        suggestions.append(
            "Add at least one special character (e.g. ! @ # $ % &)."
        )
    if not check_results["Not a commonly used password"]:
        suggestions.append(
            "Avoid common passwords and predictable patterns — "
            "consider a random passphrase instead."
        )

    if not suggestions:
        suggestions.append(
            "Your password meets the basic security requirements."
        )

    return suggestions


def print_report(check_results, score, total, strength, recommendations):
    """Prints the full strength report to the console.

    Important: this function never receives or prints the password
    itself — only the results derived from it.
    """
    print(f"\nStrength: {strength}")
    print(f"Score: {score}/{total}")

    print("\nChecks:")
    for label, passed in check_results.items():
        symbol = "\u2713" if passed else "\u2717"  # ✓ or ✗
        print(f"{symbol} {label}")

    print("\nRecommendation:")
    for suggestion in recommendations:
        print(f"- {suggestion}")


def evaluate_password(password):
    """Runs the full evaluation pipeline for a given password string.

    Returns a dictionary with all results, so this function can be
    reused directly by both the CLI and the unit tests without
    duplicating logic.
    """
    check_results = run_all_checks(password)
    score, total = calculate_score(check_results)
    strength = classify_strength(score, total)
    recommendations = get_recommendations(check_results)

    return {
        "check_results": check_results,
        "score": score,
        "total": total,
        "strength": strength,
        "recommendations": recommendations,
    }


def main():
    """Entry point for the command-line application."""
    print("Password Strength Checker")

    # getpass.getpass() hides the password as it's typed (no echo to
    # the terminal), unlike input(). This is a standard-library
    # function made exactly for this purpose.
    password = getpass.getpass("Enter password: ")

    result = evaluate_password(password)

    # We immediately discard the password after evaluation — there is
    # no line anywhere in this program that stores it in a file,
    # prints it, or sends it over a network.
    del password

    print_report(
        result["check_results"],
        result["score"],
        result["total"],
        result["strength"],
        result["recommendations"],
    )


if __name__ == "__main__":
    main()
