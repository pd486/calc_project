"""Observer pattern implementation following Refactoring.Guru."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import List

from app.calculation import Calculation
from app.logger import get_logger

logger = get_logger("observer")


class Observer(ABC):
    """Abstract observer interface."""

    @abstractmethod
    def update(self, subject: "Subject", calculation: Calculation) -> None:
        """Receive update from subject."""


class Subject:
    """Maintains observers and notifies them of new calculations."""

    def __init__(self) -> None:
        self._observers: List[Observer] = []

    def attach(self, observer: Observer) -> None:
        """Register an observer."""
        if observer not in self._observers:
            self._observers.append(observer)

    def detach(self, observer: Observer) -> None:
        """Remove an observer."""
        if observer in self._observers:
            self._observers.remove(observer)

    def notify(self, calculation: Calculation) -> None:
        """Notify all registered observers about a new calculation."""
        for observer in self._observers:
            observer.update(self, calculation)


class LoggingObserver(Observer):
    """Concrete observer that logs each calculation."""

    def update(self, subject: Subject, calculation: Calculation) -> None:
        """Log calculation details."""
        logger.info(
            "Calculation performed: %s(%s, %s) = %s",
            calculation.operation,
            calculation.operand_a,
            calculation.operand_b,
            calculation.result,
        )


class AutoSaveObserver(Observer):
    """Concrete observer that automatically saves calculator history."""

    def update(self, subject: Subject, calculation: Calculation) -> None:
        """Save history when the subject supports CSV persistence."""
        if hasattr(subject, "save_to_csv"):
            subject.save_to_csv()
