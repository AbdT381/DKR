"""Integration tests for the CLI."""

import io
import sys
from pathlib import Path

from src.cli import main


def run_cli(tmp_path: Path, source: str, monkeypatch) -> str:
    """Invoke CLI with given stdin and return output file contents."""
    out = tmp_path / "out.toml"
    monkeypatch.setattr(sys, "stdin", io.StringIO(source))
    assert main(["-o", str(out)]) == 0
    return out.read_text(encoding="utf-8")


def test_cli_ok(tmp_path, monkeypatch):
    src = "x := 0b101;\n?[+ x 0b1];\n"
    text = run_cli(tmp_path, src, monkeypatch)
    assert "x = 5" in text
    assert "# result = 6" in text


def test_cli_syntax_error(tmp_path, monkeypatch, capsys):
    out = tmp_path / "out.toml"
    monkeypatch.setattr(sys, "stdin", io.StringIO("x :="))
    assert main(["-o", str(out)]) == 1
    assert "error" in capsys.readouterr().err
