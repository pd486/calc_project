"""Calculator facade that connects operations, history, and observers."""

from decimal import Decimal
from typing import List

import pandas as pd

from app.calculation import Calculation
from app.calculator_config import CalculatorConfig, load_config
from app.exceptions import HistoryError
from app.observer import AutoSaveObserver, LoggingObserver, Subject


class Calculator(Subject):
    """Calculator acts as the Subject for Observer pattern notifications."""

    def __init__(self, config: CalculatorConfig = None) -> None:
        super().__init__()
        self.config = config or load_config()
        self._history: List[Calculation] = []

        self.attach(LoggingObserver())
        self.attach(AutoSaveObserver())

    def calculate(
        self,
        operation: str,
        operand_a: Decimal,
        operand_b: Decimal,
    ) -> Calculation:
        """Perform a calculation, store it, and notify observers."""
        calculation = Calculation(operation, operand_a, operand_b)
        self._history.append(calculation)
        self.notify(calculation)
        return calculation

    def get_history(self) -> List[Calculation]:
        """Return calculation history."""
        return list(self._history)

    def clear_history(self) -> None:
        """Clear calculation history."""
        self._history.clear()

    def save_to_csv(self) -> str:
        """Save calculation history to CSV using pandas."""
        try:
            rows = [calculation.to_dict() for calculation in self._history]
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