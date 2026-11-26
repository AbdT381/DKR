"""Translator from the educational language into TOML."""

from typing import Any

from .evaluator import EvaluationError, evaluate


class TranslationError(Exception):
    """Raised when translation to TOML fails."""


def _to_toml_value(value: Any) -> str:
    """Serialize a Python value into a TOML literal."""
    if isinstance(value, bool):
        return "true" if value else "false"
    if isinstance(value, int):
        return str(value)
    if isinstance(value, dict):
        return _to_toml_table(value)
    raise TranslationError(f"unsupported value: {value!r}")


def _to_toml_table(table: dict[str, Any]) -> str:
    """Serialize a dictionary into an inline TOML table."""
    parts = [f"{key} = {_to_toml_value(val)}"
             for key, val in table.items()]
    return "{ " + ", ".join(parts) + " }"


def translate(ast: list[Any]) -> str:
    """Translate the parsed AST into TOML text."""
    env: dict[str, Any] = {}
    out: list[str] = []
    for node in ast:
        if node[0] == "decl":
            env[node[1]] = evaluate(node[2], env)
        elif node[0] == "eval":
            result = evaluate(node[1], env)
            out.append(f"# result = {_to_toml_value(result)}")
        else:
            raise TranslationError(f"unknown statement: {node!r}")
    for key, value in env.items():
        out.append(f"{key} = {_to_toml_value(value)}")
    return "\n".join(out) + "\n"
