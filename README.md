# Guess the Secret Number

A simple head-to-head number guessing game built with Python and Tkinter.

## Game Play

- The match is played over 5 rounds.
- Each round, the player enters a secret number from **1 to 100**.
- The AI randomly picks its own secret number.
- The player guesses the AI's secret first.
- After each player guess, the game tells the player if the AI's secret is **higher** or **lower**.
- Then the AI makes a guess at the player's secret.
- The player responds with **Higher**, **Lower**, or **Correct**.
- The game tracks valid numeric bounds for AI feedback and detects invalid rule-breaking answers.
- The first side to guess correctly wins the round.
- After 5 rounds, the final match winner is displayed.

## Features

- Difficulty modes:
  - Easy: 10 attempts per side
  - Medium: 7 attempts per side
  - Hard: 5 attempts per side
- Continuous interactive GUI using Tkinter
- User input validation for numbers and bounds
- AI feedback validation and cheating detection
- Friendly log output and status updates

## Requirements

- Python 3.8 or later

## Run the Game

From the repository root:

```bash
python main.py
```

## Notes

- The game is implemented in `main.py`.
- No external dependencies are required beyond the Python standard library.
