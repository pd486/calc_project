"""Configuration loading for the calculator application."""

import os
from dataclasses import dataclass
from decimal import Decimal

from dotenv import load_dotenv

from app.exceptions import ConfigurationError

DEFAULT_LOG_DIR = "logs"
DEFAULT_HISTORY_DIR = "history"
DEFAULT_MAX_HISTORY_SIZE = 100
DEFAULT_AUTO_SAVE = True
DEFAULT_PRECISION = 10
DEFAULT_MAX_INPUT_VALUE = Decimal("1e18")
DEFAULT_ENCODING = "utf-8"


def _str_to_bool(value: str) -> bool:
    """Convert a string from the .env file into True or False."""
    return value.strip().lower() in {"1", "true", "yes", "on"}


@dataclass
class CalculatorConfig:
    """Stores every configuration setting for the calculator."""

    log_dir: str = DEFAULT_LOG_DIR
    history_dir: str = DEFAULT_HISTORY_DIR
    max_history_size: int = DEFAULT_MAX_HISTORY_SIZE
    auto_save: bool = DEFAULT_AUTO_SAVE
    precision: int = DEFAULT_PRECISION
    max_input_value: Decimal = DEFAULT_MAX_INPUT_VALUE
    default_encoding: str = DEFAULT_ENCODING

    @property
    def log_file(self) -> str:
        """Return the full path to the calculator log file."""
        return os.path.join(self.log_dir, "calculator.log")

    @property
    def history_file(self) -> str:
        """Return the full path to the calculator history CSV file."""
        return os.path.join(self.history_dir, "history.csv")

    def validate(self) -> None:
        """Validate configuration settings."""
        if self.max_history_size <= 0:
            raise ConfigurationError(
                "CALCULATOR_MAX_HISTORY_SIZE must be a positive integer"
            )

        if self.precision < 0:
            raise ConfigurationError(
                "CALCULATOR_PRECISION cannot be negative"
            )

        if self.max_input_value <= 0:
            raise ConfigurationError(
                "CALCULATOR_MAX_INPUT_VALUE must be a positive number"
            )

        if not self.default_encoding:
            raise ConfigurationError(
                "CALCULATOR_DEFAULT_ENCODING cannot be empty"
            )

    def ensure_directories(self) -> None:
        """Create the log and history folders if they don't exist."""
        os.makedirs(self.log_dir, exist_ok=True)
        os.makedirs(self.history_dir, exist_ok=True)


def load_config(env_file: str = ".env") -> CalculatorConfig:
    """Load configuration from the .env file."""
    load_dotenv(dotenv_path=env_file, override=False)

    try:
        config = CalculatorConfig(
            log_dir=os.getenv("CALCULATOR_LOG_DIR", DEFAULT_LOG_DIR),
            history_dir=os.getenv("CALCULATOR_HISTORY_DIR", DEFAULT_HISTORY_DIR),
            max_history_size=int(
                os.getenv("CALCULATOR_MAX_HISTORY_SIZE", DEFAULT_MAX_HISTORY_SIZE)
            ),
            auto_save=_str_to_bool(
                os.getenv("CALCULATOR_AUTO_SAVE", str(DEFAULT_AUTO_SAVE))
            ),
            precision=int(
                os.getenv("CALCULATOR_PRECISION", DEFAULT_PRECISION)
            ),
            max_input_value=Decimal(
                os.getenv("CALCULATOR_MAX_INPUT_VALUE", str(DEFAULT_MAX_INPUT_VALUE))
            ),
            default_encoding=os.getenv(
                "CALCULATOR_DEFAULT_ENCODING", DEFAULT_ENCODING
            ),
        )
    except (ValueError, ArithmeticError) as exc:
        raise ConfigurationError(
            f"Invalid configuration value: {exc}"
        ) from exc

    config.validate()
    config.ensure_directories()

    return config