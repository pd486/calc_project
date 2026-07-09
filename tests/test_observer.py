"""Tests for Observer pattern classes."""

from decimal import Decimal

from app.calculation import Calculation
from app.observer import AutoSaveObserver, Observer, Subject


class FakeObserver(Observer):
    def __init__(self):
        self.updated = False

    def update(self, subject, calculation):
        self.updated = True
        self.calculation = calculation


class FakeSubject(Subject):
    def __init__(self):
        super().__init__()
        self.saved = False

    def save_to_csv(self):
        self.saved = True


def test_subject_attach_notify_and_detach():
    subject = Subject()
    observer = FakeObserver()
    calculation = Calculation("add", Decimal("2"), Decimal("3"))

    subject.attach(observer)
    subject.notify(calculation)

    assert observer.updated is True
    assert observer.calculation == calculation

    observer.updated = False
    subject.detach(observer)
    subject.notify(calculation)

    assert observer.updated is False


def test_autosave_observer_calls_save_to_csv():
    subject = FakeSubject()
    observer = AutoSaveObserver()
    calculation = Calculation("add", Decimal("2"), Decimal("3"))

    observer.update(subject, calculation)

    assert subject.saved is True
