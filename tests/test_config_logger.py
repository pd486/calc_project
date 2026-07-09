"""Tests for configuration and logger setup."""

import logging

import pytest

from app.calculator_config import CalculatorConfig, load_config
from app.exceptions import ConfigurationError
from app.logger import configure_logging, get_logger


def test_config_properties_and_directories(tmp_path):
    config = CalculatorConfig(
        log_dir=str(tmp_path / "logs"),
        history_dir=str(tmp_path / "history"),
    )

    config.ensure_directories()

    assert config.log_file.endswith("calculator.log")
    assert config.history_file.endswith("history.csv")
    assert (tmp_path / "logs").exists()
    assert (tmp_path / "history").exists()


@pytest.mark.parametrize(
    "kwargs",
    [
        {"max_history_size": 0},
        {"precision": -1},
        {"max_input_value": 0},
        {"default_encoding": ""},
    ],
)
def test_config_validation_errors(kwargs):
    config = CalculatorConfig(**kwargs)

    with pytest.raises(ConfigurationError):
        config.validate()


def test_load_config_from_env_file(tmp_path):
    env_file = tmp_path / ".env"
    env_file.write_text(
        "\n".join(
            [
                "CALCULATOR_LOG_DIR=mylogs",
                "CALCULATOR_HISTORY_DIR=myhistory",
                "CALCULATOR_MAX_HISTORY_SIZE=25",
                "CALCULATOR_AUTO_SAVE=false",
                "CALCULATOR_PRECISION=4",
                "CALCULATOR_MAX_INPUT_VALUE=1000",
                "CALCULATOR_DEFAULT_ENCODING=utf-8",
            ]
        )
    )

    config = load_config(str(env_file))

    assert config.max_history_size == 25
    assert config.auto_save is False
    assert config.precision == 4


def test_configure_logging(tmp_path):
    config = CalculatorConfig(
        log_dir=str(tmp_path / "logs"),
        history_dir=str(tmp_path / "history"),
    )
    config.ensure_directories()

    logger = configure_logging(config)

    assert isinstance(logger, logging.Logger)
    assert get_logger("test").name == "calculator.test"
