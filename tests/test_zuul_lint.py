import pytest
import sh


def test_invalid():
    try:
        sh.python(["-m", "zuul_lint", "tests/data/zuul-config-invalid.yaml"])
    except sh.ErrorReturnCode_1:
        return
    except sh.ErrorReturnCode as e:
        pytest.fail(e)
    pytest.fail("Expected to fail")


def test_valid():
    try:
        sh.python(["-m", "zuul_lint", "tests/data/zuul-config-valid.yaml"])
    except sh.ErrorReturnCode as e:
        pytest.fail(e)
