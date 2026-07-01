"""Input validation helpers."""

from decimal import Decimal, InvalidOperation

from app.calculator_config import CalculatorConfig
from app.exceptions import ValidationError


def validate_number(raw_value: str, config: CalculatorConfig) -> Decimal:
    """Convert input into a Decimal and check its allowed range."""

    if raw_value is None or str(raw_value).strip() == "":
        raise ValidationError("Input cannot be empty")

    try:
        number = Decimal(str(raw_value).strip())
    except InvalidOperation as exc:
        raise ValidationError(f"'{raw_value}' is not a valid number") from exc

    limit = config.max_input_value

    if number > limit or number < -limit:
        raise ValidationError(
            f"'{raw_value}' is outside the allowed range of [-{limit}, {limit}]"
        )

    return number


def validate_operand_count(operands: list, expected: int = 2) -> None:
    """Confirm that an operation received the correct number of operands."""

    if len(operands) != expected:
        raise ValidationError(
            f"Expected {expected} operands, received {len(operands)}"
        )