# Advanced Calculator Project

## Overview

This project is an advanced command-line calculator developed for IS601. It demonstrates software engineering best practices by implementing the Factory, Memento, and Observer design patterns. The calculator supports calculation history, undo/redo functionality, CSV persistence, logging, configuration through environment variables, and automated testing.

## Features

- Command-line REPL interface
- Arithmetic operations:
  - add
  - subtract
  - multiply
  - divide
  - power
  - root
  - modulus
  - int_divide
  - percent
  - abs_diff
- Calculation history
- Undo and redo
- Save and load history using CSV
- Input validation
- Logging
- Automated tests with pytest
- GitHub Actions CI

## Design Patterns

### Factory Pattern
Used to create arithmetic operation objects through `OperationFactory`.

### Memento Pattern
Used to implement undo and redo through calculator history snapshots.

### Observer Pattern
Used to notify logging and auto-save observers whenever a calculation is performed.

## Installation

Clone the repository:

```bash
git clone https://github.com/pd486/calc_project.git
cd calc_project
```

Create a virtual environment:

```bash
python3 -m venv venv
source venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

## Running the Calculator

```bash
python -m app.repl
```

## Running the Tests

```bash
pytest
```

Run tests with coverage:

```bash
pytest --cov=app --cov-report=term-missing
```

## Project Structure

```
app/
tests/
.github/
README.md
requirements.txt
```