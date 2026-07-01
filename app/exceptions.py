"""Custom exception hierarchy for the calculator application."""


class CalculatorError(Exception):
    """Base class for every calculator-specific error."""


class ValidationError(CalculatorError):
    """Raised when user input is invalid."""


class OperationError(CalculatorError):
    """Raised when a calculation cannot be completed."""


class ConfigurationError(CalculatorError):
    """Raised when configuration values are invalid."""


class HistoryError(CalculatorError):
    """Raised when history cannot be saved, loaded, or changed."""