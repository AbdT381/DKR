"""Command-line interface for the configuration language translator."""

import argparse
import sys

from lark.exceptions import LarkError

from .evaluator import EvaluationError
from .parser import AstBuilder, build_parser
from .translator import TranslationError, translate


def parse_args(argv: list[str]) -> argparse.Namespace:
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(
        prog="config-translator",
        description="Translate educational config language to TOML.",
    )
    parser.add_argument(
        "-o", "--output", required=True,
        help="path to the output TOML file",
    )
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    """Entry point: read stdin, translate, write TOML to a file."""
    args = parse_args(argv or sys.argv[1:])
    source = sys.stdin.read()
    try:
        tree = build_parser().parse(source)
        ast = AstBuilder().transform(tree)
        result = translate(ast)
    except (LarkError, EvaluationError, TranslationError) as exc:
        print(f"syntax/evaluation error: {exc}", file=sys.stderr)
        return 1
    with open(args.output, "w", encoding="utf-8") as handle:
        handle.write(result)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
