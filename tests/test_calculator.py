"""Tests for Calculator facade, persistence, undo, and redo."""

from decimal import Decimal

import pytest

from app.calculator import Calculator
from app.calculator_config import CalculatorConfig
from app.exceptions import HistoryError


def make_calculator(tmp_path):
    config = CalculatorConfig(
        log_dir=str(tmp_path / "logs"),
        history_dir=str(tmp_path / "history"),
    )
    config.ensure_directories()
    return Calculator(config)


def test_calculator_calculate_and_history(tmp_path):
    calculator = make_calculator(tmp_path)

    result = calculator.calculate("add", Decimal("2"), Decimal("3"))

    assert result.result == Decimal("5")
    assert len(calculator.get_history()) == 1


def test_calculator_clear_history(tmp_path):
    calculator = make_calculator(tmp_path)
    calculator.calculate("add", Decimal("2"), Decimal("3"))

    calculator.clear_history()

    assert calculator.get_history() == []


def test_calculator_undo_redo(tmp_path):
    calculator = make_calculator(tmp_path)
    calculator.calculate("add", Decimal("2"), Decimal("3"))

    assert calculator.undo() is True
    assert len(calculator.get_history()) == 0

    assert calculator.redo() is True
    assert len(calculator.get_history()) == 1


def test_save_and_load_csv(tmp_path):
    calculator = make_calculator(tmp_path)
    calculator.calculate("multiply", Decimal("4"), Decimal("5"))

    path = calculator.save_to_csv()
    assert path.endswith("history.csv")

    new_calculator = make_calculator(tmp_path)
    count = new_calculator.load_from_csv()

    assert count == 1
    assert len(new_calculator.get_history()) == 1
    assert new_calculator.get_history()[0].result == Decimal("20")


def test_load_missing_csv_raises_error(tmp_path):
    calculator = make_calculator(tmp_path)

    with pytest.raises(HistoryError):
        calculator.load_from_csv()


def test_clear_history_can_be_undone(tmp_path):
    calculator = make_calculator(tmp_path)

    calculator.calculate("add", Decimal("2"), Decimal("3"))
    calculator.clear_history()

    assert calculator.get_history() == []

    assert calculator.undo() is True
    assert len(calculator.get_history()) == 1


def test_save_empty_history_creates_csv(tmp_path):
    calculator = make_calculator(tmp_path)

    path = calculator.save_to_csv()

    assert path.endswith("history.csv")


def test_load_empty_csv_returns_zero(tmp_path):
    calculator = make_calculator(tmp_path)

    calculator.save_to_csv()
    count = calculator.load_from_csv()

    assert count == 0
