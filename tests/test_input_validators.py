"""Tests for input validation helpers."""

import pytest

from app.calculator_config import CalculatorConfig
from app.exceptions import ValidationError
from app.input_validators import validate_number, validate_operand_count


def test_validate_number_accepts_valid_input():
    config = CalculatorConfig()
    assert validate_number("42", config) == 42


def test_validate_number_rejects_empty_input():
    config = CalculatorConfig()
    with pytest.raises(ValidationError):
        validate_number("", config)


def test_validate_number_rejects_non_number():
    config = CalculatorConfig()
    with pytest.raises(ValidationError):
        validate_number("abc", config)


def test_validate_number_rejects_out_of_range():
    config = CalculatorConfig(max_input_value=10)
    with pytest.raises(ValidationError):
        validate_number("999", config)


def test_validate_operand_count_accepts_expected_count():
    validate_operand_count([1, 2], 2)


def test_validate_operand_count_rejects_wrong_count():
    with pytest.raises(ValidationError):
        validate_operand_count([1], 2)
