"""Memento pattern implementation for calculator history undo/redo.

This module follows the Refactoring.Guru Memento structure:

- CalculatorHistoryOriginator: owns the state that changes over time
- CalculatorMemento: stores a snapshot of that state
- MementoCaretaker: manages undo and redo stacks
"""

from copy import deepcopy
from datetime import datetime
from typing import List, Optional

from app.calculation import Calculation


class CalculatorMemento:
    """Snapshot of the calculator history state."""

    def __init__(self, state: List[Calculation]) -> None:
        self._state = deepcopy(state)
        self._date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def get_state(self) -> List[Calculation]:
        """Return a copy of the saved history state."""
        return deepcopy(self._state)

    def get_name(self) -> str:
        """Return metadata describing this snapshot."""
        return f"{self._date} / {len(self._state)} calculation(s)"

    def get_date(self) -> str:
        """Return the timestamp when the snapshot was created."""
        return self._date


class CalculatorHistoryOriginator:
    """Originator whose calculation history state can be saved/restored."""

    def __init__(self) -> None:
        self._history: List[Calculation] = []

    def add_calculation(self, calculation: Calculation) -> None:
        """Add a calculation to the current history state."""
        self._history.append(calculation)

    def clear(self) -> None:
        """Clear the current history state."""
        self._history.clear()

    def get_history(self) -> List[Calculation]:
        """Return a copy of the current history."""
        return list(self._history)

    def save(self) -> CalculatorMemento:
        """Save the current history state inside a memento."""
        return CalculatorMemento(self._history)

    def restore(self, memento: CalculatorMemento) -> None:
        """Restore history state from a memento."""
        self._history = memento.get_state()


class MementoCaretaker:
    """Caretaker that manages undo and redo stacks of mementos."""

    def __init__(self, originator: CalculatorHistoryOriginator) -> None:
        self._originator = originator
        self._undo_stack: List[CalculatorMemento] = []
        self._redo_stack: List[CalculatorMemento] = []

    def backup(self) -> None:
        """Save the originator's current state before a change."""
        self._undo_stack.append(self._originator.save())
        self._redo_stack.clear()

    def undo(self) -> bool:
        """Restore the previous saved state."""
        if not self._undo_stack:
            return False

        self._redo_stack.append(self._originator.save())
        memento = self._undo_stack.pop()
        self._originator.restore(memento)
        return True

    def redo(self) -> bool:
        """Restore the most recently undone state."""
        if not self._redo_stack:
            return False

        self._undo_stack.append(self._originator.save())
        memento = self._redo_stack.pop()
        self._originator.restore(memento)
        return True

    def show_history(self) -> List[str]:
        """Return metadata for saved undo snapshots."""
        return [memento.get_name() for memento in self._undo_stack]

    @property
    def can_undo(self) -> bool:
        """Return True if undo is available."""
        return bool(self._undo_stack)

    @property
    def can_redo(self) -> bool:
        """Return True if redo is available."""
        return bool(self._redo_stack)