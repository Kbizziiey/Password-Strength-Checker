"""
Unit tests for password_checker.py

IMPORTANT: None of the passwords below are real passwords used by
anyone. They are fictional test strings chosen only to exercise
specific rules (length, character types, common-password matching).
"""

import unittest
import os
import sys

# Allow importing password_checker.py from the src/ folder without
# needing to install the project as a package. This is a simple,
# beginner-friendly approach — no extra tooling required.
sys.path.insert(
    0, os.path.join(os.path.dirname(__file__), "..", "src")
)

from password_checker import (
    check_length,
    check_uppercase,
    check_lowercase,
    check_numbers,
    check_special_characters,
    check_not_common,
    calculate_score,
    classify_strength,
    evaluate_password,
)


class TestIndividualChecks(unittest.TestCase):
    """Tests for each individual check function in isolation."""

    def test_short_password_fails_length_check(self):
        self.assertFalse(check_length("Ab1!"))

    def test_long_password_passes_length_check(self):
        self.assertTrue(check_length("ThisIsFictional123!"))

    def test_missing_uppercase(self):
        self.assertFalse(check_uppercase("fictional123!"))

    def test_has_uppercase(self):
        self.assertTrue(check_uppercase("Fictional123!"))

    def test_missing_lowercase(self):
        self.assertFalse(check_lowercase("FICTIONAL123!"))

    def test_has_lowercase(self):
        self.assertTrue(check_lowercase("Fictional123!"))

    def test_missing_numbers(self):
        self.assertFalse(check_numbers("FictionalPass!"))

    def test_has_numbers(self):
        self.assertTrue(check_numbers("Fictional123!"))

    def test_missing_special_characters(self):
        self.assertFalse(check_special_characters("Fictional123"))

    def test_has_special_characters(self):
        self.assertTrue(check_special_characters("Fictional123!"))

    def test_common_password_detected(self):
        self.assertFalse(check_not_common("password123"))

    def test_common_password_detected_case_insensitive(self):
        self.assertFalse(check_not_common("Password123"))

    def test_uncommon_password_passes(self):
        self.assertTrue(check_not_common("XyQ7!mZebra_Fictional"))


class TestScoring(unittest.TestCase):
    """Tests for the score calculation logic."""

    def test_score_counts_passed_checks(self):
        results = {"a": True, "b": True, "c": False}
        score, total = calculate_score(results)
        self.assertEqual(score, 2)
        self.assertEqual(total, 3)

    def test_score_zero_when_all_fail(self):
        results = {"a": False, "b": False}
        score, total = calculate_score(results)
        self.assertEqual(score, 0)
        self.assertEqual(total, 2)


class TestClassification(unittest.TestCase):
    """Tests for turning a score into a strength label."""

    def test_full_score_is_very_strong(self):
        self.assertEqual(classify_strength(6, 6), "Very Strong")

    def test_zero_score_is_very_weak(self):
        self.assertEqual(classify_strength(0, 6), "Very Weak")

    def test_partial_score_is_moderate(self):
        # 3/6 = 0.5 -> Moderate (boundary case)
        self.assertEqual(classify_strength(3, 6), "Moderate")

    def test_high_partial_score_is_strong(self):
        # 5/6 ≈ 0.83 -> Strong
        self.assertEqual(classify_strength(5, 6), "Strong")


class TestFullEvaluation(unittest.TestCase):
    """End-to-end tests using evaluate_password() with realistic
    (but entirely fictional) example passwords for each category
    requested in the project requirements.
    """

    def test_very_weak_password(self):
        # Short, single character type, AND a listed common password
        # -> only the lowercase check passes (score 1/6).
        result = evaluate_password("password")
        self.assertEqual(result["strength"], "Very Weak")

    def test_short_password(self):
        result = evaluate_password("Ab1!")
        self.assertFalse(result["check_results"]["At least 12 characters"])

    def test_password_missing_uppercase(self):
        result = evaluate_password("fictional-pass123!")
        self.assertFalse(
            result["check_results"]["Contains uppercase letters"]
        )

    def test_password_missing_lowercase(self):
        result = evaluate_password("FICTIONAL-PASS123!")
        self.assertFalse(
            result["check_results"]["Contains lowercase letters"]
        )

    def test_password_missing_numbers(self):
        result = evaluate_password("Fictional-Password!")
        self.assertFalse(result["check_results"]["Contains numbers"])

    def test_password_missing_special_characters(self):
        result = evaluate_password("FictionalPassword123")
        self.assertFalse(
            result["check_results"]["Contains special characters"]
        )

    def test_strong_password(self):
        # Passes 5 of 6 checks (missing special characters).
        result = evaluate_password("FictionalPassword123")
        self.assertEqual(result["strength"], "Strong")

    def test_very_strong_password(self):
        # Passes all 6 checks.
        result = evaluate_password("Fictional-Pass_9284!")
        self.assertEqual(result["strength"], "Very Strong")
        self.assertEqual(result["score"], result["total"])

    def test_common_password_flagged_even_if_long(self):
        # Demonstrates that common-password matching only catches
        # exact known entries, not "long but predictable" passwords —
        # here we test an actual list entry.
        result = evaluate_password("password123")
        self.assertFalse(
            result["check_results"]["Not a commonly used password"]
        )

    def test_recommendations_present_when_checks_fail(self):
        result = evaluate_password("password")
        self.assertGreater(len(result["recommendations"]), 0)

    def test_positive_message_when_all_checks_pass(self):
        result = evaluate_password("Fictional-Pass_9284!")
        self.assertEqual(
            result["recommendations"],
            ["Your password meets the basic security requirements."],
        )


if __name__ == "__main__":
    unittest.main()
