"""Calculation model for completed arithmetic operations."""

from dataclasses import dataclass, field
from datetime import datetime
from decimal import Decimal, InvalidOperation

from app.exceptions import OperationError
from app.operations import OperationFactory


@dataclass
class Calculation:
    """Stores one completed calculation."""

    operation: str
    operand_a: Decimal
    operand_b: Decimal
    result: Decimal = field(default=None)
    timestamp: datetime = field(default_factory=datetime.now)

    def __post_init__(self) -> None:
        """Compute the result automatically if it was not supplied."""
        if self.result is None:
            self.result = self.compute()

    def compute(self) -> Decimal:
        """Run the operation using the OperationFactory."""
        operation_object = OperationFactory.create(self.operation)
        return operation_object.execute(self.operand_a, self.operand_b)

    def to_dict(self) -> dict:
        """Convert this calculation into a dictionary for CSV storage."""
        return {
            "operation": self.operation,
            "operand_a": str(self.operand_a),
            "operand_b": str(self.operand_b),
            "result": str(self.result),
            "timestamp": self.timestamp.isoformat(),
        }

    @classmethod
    def from_dict(cls, row: dict) -> "Calculation":
        """Rebuild a Calculation object from a dictionary."""
        try:
            return cls(
                operation=str(row["operation"]),
                operand_a=Decimal(str(row["operand_a"])),
                operand_b=Decimal(str(row["operand_b"])),
                result=Decimal(str(row["result"])),
                timestamp=datetime.fromisoformat(str(row["timestamp"])),
            )
        except (KeyError, InvalidOperation, ValueError) as exc:
            raise OperationError(f"Malformed history row: {exc}") from exc

    def __str__(self) -> str:
        """Return a readable calculation string."""
        return f"{self.operation}({self.operand_a}, {self.operand_b}) = {self.result}"