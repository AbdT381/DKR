"""Tests for the evaluator module."""

import pytest

from src.evaluator import EvaluationError, evaluate


def test_sum():
    assert evaluate(("sum", 1, 2), {}) == 3


def test_abs():
    assert evaluate(("abs", 5), {}) == 5


def test_sqrt():
    assert evaluate(("sqrt", 9), {}) == 3


def test_name_lookup():
    assert evaluate("x", {"x": 7}) == 7


def test_unknown_name():
    with pytest.raises(EvaluationError):
        evaluate("y", {})


def test_sqrt_negative():
    with pytest.raises(EvaluationError):
        evaluate(("sqrt", -1), {})


def test_nested():
    assert evaluate(("sum", ("abs", 3), ("sqrt", 16)), {}) == 7
