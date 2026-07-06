"""Calculator facade that connects operations, history, memento, and observers."""

from decimal import Decimal
from typing import List

import pandas as pd

from app.calculation import Calculation
from app.calculator_config import CalculatorConfig, load_config
from app.calculator_memento import CalculatorHistoryOriginator, MementoCaretaker
from app.exceptions import HistoryError
from app.observer import AutoSaveObserver, LoggingObserver, Subject


class Calculator(Subject):
    """Calculator acts as the Subject for Observer pattern notifications."""

    def __init__(self, config: CalculatorConfig = None) -> None:
        super().__init__()
        self.config = config or load_config()

        self._history_originator = CalculatorHistoryOriginator()
        self._caretaker = MementoCaretaker(self._history_originator)

        self.attach(LoggingObserver())
        self.attach(AutoSaveObserver())

    def calculate(
        self,
        operation: str,
        operand_a: Decimal,
        operand_b: Decimal,
    ) -> Calculation:
        """Perform a calculation, store it, and notify observers."""
        self._caretaker.backup()

        calculation = Calculation(operation, operand_a, operand_b)
        self._history_originator.add_calculation(calculation)

        self.notify(calculation)

        return calculation

    def get_history(self) -> List[Calculation]:
        """Return calculation history."""
        return self._history_originator.get_history()

    def clear_history(self) -> None:
        """Clear calculation history."""
        self._caretaker.backup()
        self._history_originator.clear()

    def undo(self) -> bool:
        """Undo the previous history-changing action."""
        return self._caretaker.undo()

    def redo(self) -> bool:
        """Redo the most recently undone action."""
        return self._caretaker.redo()

    def save_to_csv(self) -> str:
        """Save calculation history to CSV using pandas."""
        try:
            rows = [
                calculation.to_dict()
                for calculation in self._history_originator.get_history()
            ]

            frame = pd.DataFrame(rows)

            if frame.empty:
                frame = pd.DataFrame(
                    columns=[
                        "operation",
                        "operand_a",
                        "operand_b",
                        "result",
                        "timestamp",
                    ]
                )

            frame.to_csv(
                self.config.history_file,
                index=False,
                encoding=self.config.default_encoding,
            )

            return self.config.history_file

        except OSError as exc:
            raise HistoryError(f"Could not save history: {exc}") from exc

    def load_from_csv(self) -> int:
        """Load calculation history from CSV using pandas."""
        try:
            frame = pd.read_csv(
                self.config.history_file,
                encoding=self.config.default_encoding,
            )

        except FileNotFoundError as exc:
            raise HistoryError(
                f"History file '{self.config.history_file}' does not exist"
            ) from exc

        except pd.errors.EmptyDataError:
            self._caretaker.backup()
            self._history_originator.clear()
            return 0

        except pd.errors.ParserError as exc:
            raise HistoryError(
                f"History file '{self.config.history_file}' is malformed"
            ) from exc

        loaded_history = [
            Calculation.from_dict(row.to_dict())
            for _, row in frame.iterrows()
        ]

        self._caretaker.backup()
        self._history_originator.restore_from_history(loaded_history)

        return len(loaded_history)