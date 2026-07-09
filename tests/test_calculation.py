"""Tests for the Calculation model."""

from decimal import Decimal

import pytest

from app.calculation import Calculation
from app.exceptions import OperationError


def test_calculation_computes_result():
    calculation = Calculation("add", Decimal("2"), Decimal("3"))
    assert calculation.result == Decimal("5")
    assert str(calculation) == "add(2, 3) = 5"


def test_calculation_to_dict_and_from_dict():
    original = Calculation("multiply", Decimal("4"), Decimal("5"))
    data = original.to_dict()

    restored = Calculation.from_dict(data)

    assert restored.operation == "multiply"
    assert restored.operand_a == Decimal("4")
    assert restored.operand_b == Decimal("5")
    assert restored.result == Decimal("20")


def test_calculation_from_dict_rejects_bad_row():
    with pytest.raises(OperationError):
        Calculation.from_dict({"operation": "add"})
