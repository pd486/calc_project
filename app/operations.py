"""Arithmetic operations implemented using the Factory design pattern."""

from abc import ABC, abstractmethod
from decimal import Decimal
from typing import Callable, Dict, Type

from app.exceptions import OperationError

_REGISTRY: Dict[str, Type["Operation"]] = {}

def register_operation(name: str, description: str) -> Callable:
    """Register an operation class under a command name."""

    def decorator(cls: Type["Operation"]) -> Type["Operation"]:
        cls.name = name
        cls.description = description
        _REGISTRY[name] = cls
        return cls

    return decorator

class Operation(ABC):
    """Base class for all two-number arithmetic operations."""

    name: str = ""
    description: str = ""

    @abstractmethod
    def execute(self, a: Decimal, b: Decimal) -> Decimal:
        """Execute the operation using two Decimal operands."""
        raise NotImplementedError  # pragma: no cover
    
@register_operation("add", "Add two numbers: a + b")
class Addition(Operation):
    def execute(self, a: Decimal, b: Decimal) -> Decimal:
        return a + b


@register_operation("subtract", "Subtract the second number from the first: a - b")
class Subtraction(Operation):
    def execute(self, a: Decimal, b: Decimal) -> Decimal:
        return a - b


@register_operation("multiply", "Multiply two numbers: a * b")
class Multiplication(Operation):
    def execute(self, a: Decimal, b: Decimal) -> Decimal:
        return a * b


@register_operation("divide", "Divide the first number by the second: a / b")
class Division(Operation):
    def execute(self, a: Decimal, b: Decimal) -> Decimal:
        if b == 0:
            raise OperationError("Cannot divide by zero")
        return a / b
    
@register_operation("power", "Raise the first number to the power of the second: a ** b")
class Power(Operation):
    def execute(self, a: Decimal, b: Decimal) -> Decimal:
        try:
            result = float(a) ** float(b)
        except OverflowError as exc:
            raise OperationError("Result of power operation is too large") from exc

        if isinstance(result, complex):
            raise OperationError("Power operation produced a complex result")

        return Decimal(str(result))


@register_operation("root", "Calculate the b-th root of a")
class Root(Operation):
    def execute(self, a: Decimal, b: Decimal) -> Decimal:
        if b == 0:
            raise OperationError("Cannot take the 0th root of a number")

        if a < 0 and float(b) % 2 == 0:
            raise OperationError("Cannot take an even root of a negative number")

        try:
            if a < 0:
                magnitude = abs(float(a)) ** (1 / float(b))
                result = -magnitude
            else:
                result = float(a) ** (1 / float(b))
        except (ZeroDivisionError, ValueError) as exc:
            raise OperationError(f"Cannot compute root: {exc}") from exc

        return Decimal(str(result))


@register_operation("modulus", "Compute the remainder of a divided by b")
class Modulus(Operation):
    def execute(self, a: Decimal, b: Decimal) -> Decimal:
        if b == 0:
            raise OperationError("Cannot compute modulus with a divisor of zero")
        return a % b


@register_operation("int_divide", "Perform integer division, discarding the remainder: a // b")
class IntegerDivision(Operation):
    def execute(self, a: Decimal, b: Decimal) -> Decimal:
        if b == 0:
            raise OperationError("Cannot perform integer division by zero")
        return a // b


@register_operation("percent", "Calculate (a / b) * 100")
class Percentage(Operation):
    def execute(self, a: Decimal, b: Decimal) -> Decimal:
        if b == 0:
            raise OperationError("Cannot calculate a percentage with a denominator of zero")
        return (a / b) * Decimal(100)


@register_operation("abs_diff", "Calculate the absolute difference between two numbers")
class AbsoluteDifference(Operation):
    def execute(self, a: Decimal, b: Decimal) -> Decimal:
        return abs(a - b)
    
class OperationFactory:
    """Creates operation instances by name."""

    @staticmethod
    def create(name: str) -> Operation:
        try:
            operation_cls = _REGISTRY[name]
        except KeyError as exc:
            raise OperationError(f"Unknown operation '{name}'") from exc

        return operation_cls()

    @staticmethod
    def available_operations() -> Dict[str, str]:
        """Return all registered operation names and descriptions."""
        return {
            name: cls.description
            for name, cls in _REGISTRY.items()
        }