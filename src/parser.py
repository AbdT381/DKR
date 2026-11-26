"""Parser module for the educational configuration language."""

from pathlib import Path
from typing import Any

from lark import Lark, Transformer, Tree


GRAMMAR_PATH = Path(__file__).parent / "grammar.lark"


def load_grammar() -> str:
    """Load the Lark grammar from disk."""
    return GRAMMAR_PATH.read_text(encoding="utf-8")


def build_parser() -> Lark:
    """Create a LALR parser instance for the configuration language."""
    return Lark(load_grammar(), parser="lalr", start="start")


class AstBuilder(Transformer):
    """Transform the Lark parse tree into a plain Python AST."""

    def start(self, items: list[Any]) -> list[Any]:
        """Return the list of top-level statements."""
        return items

    def const_decl(self, items: list[Any]) -> tuple:
        """Build a constant declaration node."""
        return ("decl", str(items[0]), items[1])

    def expr_stmt(self, items: list[Any]) -> tuple:
        """Build a constant expression evaluation node."""
        return ("eval", items[0])

    def sum_expr(self, items: list[Any]) -> tuple:
        """Build a sum expression node."""
        return ("sum", items[0], items[1])

    def abs_call(self, items: list[Any]) -> tuple:
        """Build an absolute-value call node."""
        return ("abs", items[0])

    def sqrt_call(self, items: list[Any]) -> tuple:
        """Build a square-root call node."""
        return ("sqrt", items[0])

    def dict(self, items: list[Any]) -> tuple:
        """Build a dictionary literal node."""
        return ("dict", dict(items))

    def pair(self, items: list[Any]) -> tuple:
        """Build a key-value pair for a dictionary."""
        return (str(items[0]), items[1])

    def NUMBER(self, token: Any) -> int:
        """Convert a binary literal token into an integer."""
        return int(str(token), 2)

    def NAME(self, token: Any) -> str:
        """Convert a name token into a plain string."""
        return str(token)
