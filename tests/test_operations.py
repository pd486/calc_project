"""Tests for arithmetic operations and OperationFactory."""

from decimal import Decimal

import pytest

from app.exceptions import OperationError
from app.operations import OperationFactory


@pytest.mark.parametrize(
    "operation,a,b,expected",
    [
        ("add", "2", "3", Decimal("5")),
        ("subtract", "10", "4", Decimal("6")),
        ("multiply", "6", "7", Decimal("42")),
        ("divide", "10", "2", Decimal("5")),
        ("modulus", "10", "3", Decimal("1")),
        ("int_divide", "10", "3", Decimal("3")),
        ("percent", "25", "200", Decimal("12.500")),
        ("abs_diff", "5", "12", Decimal("7")),
    ],
)
def test_operations(operation, a, b, expected):
    result = OperationFactory.create(operation).execute(Decimal(a), Decimal(b))
    assert result == expected


def test_power_operation():
    result = OperationFactory.create("power").execute(Decimal("2"), Decimal("3"))
    assert result == Decimal("8.0")


def test_root_operation():
    result = OperationFactory.create("root").execute(Decimal("9"), Decimal("2"))
    assert result == Decimal("3.0")


@pytest.mark.parametrize("operation", ["divide", "modulus", "int_divide", "percent"])
def test_zero_division_errors(operation):
    with pytest.raises(OperationError):
        OperationFactory.create(operation).execute(Decimal("10"), Decimal("0"))


def test_unknown_operation():
    with pytest.raises(OperationError):
        OperationFactory.create("missing")


def test_available_operations_contains_required_commands():
    commands = OperationFactory.available_operations()
    for command in [
        "add",
        "subtract",
        "multiply",
        "divide",
        "power",
        "root",
        "modulus",
        "int_divide",
        "percent",
        "abs_diff",
    ]:
        assert command in commands
