"""Tests for the translator module."""

from src.translator import translate


def test_decl_and_eval():
    ast = [("decl", "x", 5), ("eval", ("sum", "x", 1))]
    result = translate(ast)
    assert "# result = 6" in result
    assert "x = 5" in result


def test_dict_output():
    ast = [("decl", "d", ("dict", {"a": 1, "b": 2}))]
    result = translate(ast)
    assert "d = { a = 1, b = 2 }" in result
