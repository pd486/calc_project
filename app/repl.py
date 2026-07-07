"""Command-line REPL for the calculator application."""

from decimal import Decimal

from app.calculator import Calculator
from app.exceptions import HistoryError, OperationError, ValidationError
from app.input_validators import validate_number
from app.operations import OperationFactory


OPERATIONS = {
    "add",
    "subtract",
    "multiply",
    "divide",
    "power",
    "root",
    "modulus",
    "int_divide",
    "percent",
    "abs_diff",
}


class CalculatorREPL:
    """Simple Read-Eval-Print Loop interface."""

    def __init__(self) -> None:
        self.calculator = Calculator()

    def show_help(self) -> None:
        """Display available commands."""
        print("\nAvailable commands:")

        for name, description in OperationFactory.available_operations().items():
            print(f"  {name} <a> <b> - {description}")

        print("  history - Show calculation history")
        print("  clear   - Clear history")
        print("  undo    - Undo last calculation")
        print("  redo    - Redo last undone calculation")
        print("  save    - Save history to CSV")
        print("  load    - Load history from CSV")
        print("  help    - Show this help menu")
        print("  exit    - Exit the calculator\n")

    def handle_operation(self, command: str, args: list[str]) -> None:
        """Handle arithmetic commands."""
        if len(args) != 2:
            raise ValidationError(f"{command} requires exactly two numbers")

        a = validate_number(args[0], self.calculator.config)
        b = validate_number(args[1], self.calculator.config)

        calculation = self.calculator.calculate(command, a, b)
        print(f"Result: {calculation.result}")

    def show_history(self) -> None:
        """Display calculation history."""
        history = self.calculator.get_history()

        if not history:
            print("History is empty")
            return

        for index, calculation in enumerate(history, start=1):
            print(f"{index}. {calculation}")

    def handle_command(self, raw_command: str) -> bool:
        """Handle one command. Return False when the REPL should exit."""
        parts = raw_command.strip().split()

        if not parts:
            return True

        command = parts[0].lower()
        args = parts[1:]

        if command == "exit":
            print("Goodbye!")
            return False

        if command == "help":
            self.show_help()

        elif command in OPERATIONS:
            self.handle_operation(command, args)

        elif command == "history":
            self.show_history()

        elif command == "clear":
            self.calculator.clear_history()
            print("History cleared")

        elif command == "undo":
            if self.calculator.undo():
                print("Undo successful")
            else:
                print("Nothing to undo")

        elif command == "redo":
            if self.calculator.redo():
                print("Redo successful")
            else:
                print("Nothing to redo")

        elif command == "save":
            path = self.calculator.save_to_csv()
            print(f"History saved to {path}")

        elif command == "load":
            count = self.calculator.load_from_csv()
            print(f"Loaded {count} history entries")

        else:
            print(f"Unknown command: {command}")
            print("Type 'help' to see available commands.")

        return True

    def run(self) -> None:
        """Run the REPL."""
        print("Advanced Calculator")
        print("Type 'help' for commands or 'exit' to quit.")

        running = True

        while running:
            try:
                raw_command = input(">>> ")
                running = self.handle_command(raw_command)
            except (ValidationError, OperationError, HistoryError) as error:
                print(f"Error: {error}")
            except KeyboardInterrupt:
                print("\nGoodbye!")
                break


def main() -> None:
    """Start the calculator REPL."""
    CalculatorREPL().run()


if __name__ == "__main__":
    main()