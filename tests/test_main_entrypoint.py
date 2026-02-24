"""Tests for the slidr main module entry point."""

import runpy
import sys

import pytest


def test_main_module_invocation_exits_with_code_one(monkeypatch: pytest.MonkeyPatch):
    """Should exit with code 1 when invoked without args."""
    monkeypatch.setattr(sys, "argv", ["slidr"])
    with pytest.raises(SystemExit) as excinfo:
        runpy.run_module("slidr.main", run_name="__main__")

    assert excinfo.value.code == 1
