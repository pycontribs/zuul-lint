"""Zuul Linter Tests."""
import subprocess

import pytest


def test_invalid():
    """Test that the linter correctly detects errors in an invalid Zuul YAML file.

    Raises
    ------
        pytest.fail: If the linter does not fail as expected.
    """
    try:
        subprocess.check_call(["python", "-m", "zuul_lint",
                               "tests/data/zuul-config-invalid.yaml"])
    except subprocess.CalledProcessError as e:
        if e.returncode == 1:
            return
        pytest.fail(e)
    pytest.fail("Expected to fail")


def test_valid():
    """Test that the linter does not detect errors in a valid Zuul YAML file.

    Raises
    ------
    pytest.fail: If the linter fails unexpectedly.
    """
    try:
        subprocess.check_call(["python", "-m", "zuul_lint",
                               "tests/data/zuul-config-valid.yaml"])
    except subprocess.CalledProcessError as e:
        pytest.fail(e)
