# Guess the Secret Number

`Guess the Secret Number` is a simple desktop number-guessing game where the player and the AI challenge each other in the same window. It is designed as a clean Python GUI project with a professional-looking Tkinter interface and straightforward game logic.

## What This Game Does

The game includes two parallel challenges:

- The AI tries to guess your secret number between `1` and `100`.
- You try to guess the AI's secret number between `1` and `100`.

The interface is split into clear sections so both parts of the game are easy to play.

## How To Play

### 1. Let the AI guess your number

1. Enter a secret number from `1` to `100`.
2. Click `Start AI Round`.
3. The AI will make a guess.
4. Use the buttons to guide it:
   - `Higher` if your number is bigger
   - `Lower` if your number is smaller
   - `Correct` if the AI guessed right

### 2. Guess the AI's number

1. Enter your guess in the player section.
2. Click `Submit Guess`.
3. The game will tell you whether your guess is too high, too low, or correct.
4. If you guess correctly, a new AI secret number is generated automatically.

## Features

- Clean and modern Tkinter desktop UI
- Card-based layout for better readability
- AI guessing logic based on binary search
- Player guessing system with instant feedback
- Input validation for numbers from `1` to `100`
- Match activity log that records game events
- Built entirely with Python standard library modules

## Built With

This game was created using:

- `Python` for the game logic
- `Tkinter` for the graphical user interface
- `ttk` for styled modern widgets
- `random` for generating the AI's secret number

## Project Structure

- `main.py` - contains the full game logic and UI code
- `README.md` - project documentation

## Requirements

- Python `3.8` or later

## Run The Game

From the project folder, run:

```bash
python main.py
```

## Notes

- No external packages are required.
- The project currently uses a single-file implementation for simplicity.
