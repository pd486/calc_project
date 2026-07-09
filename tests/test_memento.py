"""Tests for the Memento pattern history implementation."""

from decimal import Decimal

from app.calculation import Calculation
from app.calculator_memento import CalculatorHistoryOriginator, MementoCaretaker


def test_originator_add_and_clear():
    originator = CalculatorHistoryOriginator()
    calculation = Calculation("add", Decimal("2"), Decimal("3"))

    originator.add_calculation(calculation)
    assert len(originator.get_history()) == 1

    originator.clear()
    assert originator.get_history() == []


def test_undo_and_redo():
    originator = CalculatorHistoryOriginator()
    caretaker = MementoCaretaker(originator)

    caretaker.backup()
    originator.add_calculation(Calculation("add", Decimal("2"), Decimal("3")))

    assert len(originator.get_history()) == 1

    assert caretaker.undo() is True
    assert len(originator.get_history()) == 0

    assert caretaker.redo() is True
    assert len(originator.get_history()) == 1


def test_undo_redo_empty_stacks():
    originator = CalculatorHistoryOriginator()
    caretaker = MementoCaretaker(originator)

    assert caretaker.undo() is False
    assert caretaker.redo() is False


def test_restore_from_history():
    originator = CalculatorHistoryOriginator()
    history = [Calculation("add", Decimal("1"), Decimal("2"))]

    originator.restore_from_history(history)

    assert len(originator.get_history()) == 1
