"""Tests for the parser module."""

from src.parser import AstBuilder, build_parser


def parse(text: str):
    """Parse source text into an AST."""
    tree = build_parser().parse(text)
    return AstBuilder().transform(tree)


def test_decl_number():
    assert parse("x := 0b101;") == [("decl", "x", 5)]


def test_decl_dict():
    ast = parse("d := { a : 0b1, b : x };")
    assert ast == [("decl", "d", ("dict", {"a": 1, "b": "x"}))]


def test_sum_expr():
    assert parse("?[+ 0b1 0b10];") == [("eval", ("sum", 1, 2))]


def test_abs_call():
    assert parse("?[abs(0b11)];") == [("eval", ("abs", 3))]


def test_sqrt_call():
    assert parse("?[sqrt(0b100)];") == [("eval", ("sqrt", 4))]


def test_nested_expr():
    ast = parse("?[+ abs(0b10) sqrt(0b100)];")
    assert ast == [("eval", ("sum", ("abs", 2), ("sqrt", 4)))]


def test_comment_ignored():
    assert parse("(comment hi ) x := 0b1;") == [("decl", "x", 1)]
