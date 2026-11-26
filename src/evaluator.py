"""Evaluator for constant expressions of the configuration language."""

import math
from typing import Any


class EvaluationError(Exception):
    """Raised when a constant expression cannot be evaluated."""


MAX_DEPTH = 100


def evaluate(node: Any, env: dict[str, Any], depth: int = 0) -> Any:
    """Recursively evaluate an AST node against the environment."""
    if depth > MAX_DEPTH:
        raise EvaluationError("expression nesting is too deep")
    tag = node[0]
    if tag == "sum":
        left = evaluate(node[1], env, depth + 1)
        right = evaluate(node[2], env, depth + 1)
        return left + right
    if tag == "abs":
        return abs(evaluate(node[1], env, depth + 1))
    if tag == "sqrt":
        value = evaluate(node[1], env, depth + 1)
        if value < 0:
            raise EvaluationError("sqrt of negative value")
        return math.isqrt(value)
    if tag == "dict":
        return {key: evaluate(val, env, depth + 1)
                for key, val in node[1].items()}
    if isinstance(node, int):
        return node
    if isinstance(node, str):
        if node not in env:
            raise EvaluationError(f"unknown name: {node}")
        return env[node]
    raise EvaluationError(f"unknown node: {node!r}")
