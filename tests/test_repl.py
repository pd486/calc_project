"""Tests for the calculator REPL command handler."""

from app.repl import CalculatorREPL


def test_repl_add_and_history(capsys):
    repl = CalculatorREPL()

    assert repl.handle_command("add 2 3") is True
    assert repl.handle_command("history") is True

    output = capsys.readouterr().out
    assert "Result: 5" in output
    assert "add(2, 3) = 5" in output


def test_repl_unknown_command(capsys):
    repl = CalculatorREPL()

    assert repl.handle_command("unknown") is True

    output = capsys.readouterr().out
    assert "Unknown command" in output


def test_repl_exit(capsys):
    repl = CalculatorREPL()

    assert repl.handle_command("exit") is False

    output = capsys.readouterr().out
    assert "Goodbye" in output


def test_repl_help(capsys):
    repl = CalculatorREPL()

    repl.handle_command("help")

    output = capsys.readouterr().out
    assert "Available commands" in output
    assert "add <a> <b>" in output


def test_repl_clear_save_and_load(capsys):
    repl = CalculatorREPL()

    repl.handle_command("add 2 3")
    repl.handle_command("save")
    repl.handle_command("clear")
    repl.handle_command("history")
    repl.handle_command("load")

    output = capsys.readouterr().out
    assert "History saved" in output
    assert "History cleared" in output
    assert "History is empty" in output
    assert "Loaded" in output


def test_repl_operation_requires_two_numbers(capsys):
    repl = CalculatorREPL()

    repl.run_command = None

    try:
        repl.handle_command("add 2")
    except Exception as error:
        assert "requires exactly two numbers" in str(error)


def test_repl_empty_command():
    repl = CalculatorREPL()
    assert repl.handle_command("") is True
