# AlfaGeir Chess AI

This is a chess AI that uses decision-tree solution with min-max algorithm and alpha-beta pruning algorithm.

## Installation and Setup

### Using UV (Recommended)

UV is a fast Python package manager. If you have UV installed, you can set up the project easily:

```bash
# Install dependencies
uv sync

# Run the game
uv run alfageir
```

### Manual Installation

To run the program you need to have pygame installed as it is what we uses to view the board. 
To install pygame you can run:
    python3 -m pip install -U pygame --user

The program also uses a chess library for representing the board and it also have move validation. 
To install python-chess:
    pip install python-chess

### Installing UV

If you don't have UV installed, you can install it with:

```bash
# On macOS and Linux
curl -LsSf https://astral.sh/uv/install.sh | sh

# On Windows
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"

# Or using pip
pip install uv
```

## Running the Game

To run the program you have to run the chessboard.py file:

```bash
python chessboard.py
```

Or if you installed it with UV:

```bash
uv run alfageir
```

## Game Modes

At the start of the program you will get a few options in the terminal where you can chose between:
1. player vs AI
2. AI vs AI
3. player vs player

To chose a mode you have to write the corresponding number in the terminal

## How to Play

To move a piece you press it's square and then the square you want to move the piece to.
If it is a legal move it will do the move, and if it's not a legal move it will ignore the move request.

When a player wins the window shuts down.

## Development

### Running Tests

```bash
uv run pytest
```

### Code Formatting

```bash
uv run black .
uv run isort .
```

### Type Checking

```bash
uv run mypy .
```