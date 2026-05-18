#!/usr/bin/env python3
"""Guess the Number - GUI head-to-head (Tkinter)

This version provides a simple, beginner-friendly Tkinter UI where:
- The player and AI each pick a secret number (1-100).
- The player guesses the AI's secret first each round; then the AI guesses the player's secret.
- Turns alternate until one side guesses correctly or both run out of attempts.
- Match is best of 5 rounds; final winner displayed.
"""

import random
import tkinter as tk
from tkinter import messagebox, scrolledtext


class SimpleAI:
    """AI that keeps low/high bounds and chooses the midpoint as next guess."""

    def __init__(self):
        self.reset()

    def reset(self):
        self.low = 1
        self.high = 100
        self.last = None
        self.attempts = 0

    def guess(self) -> int:
        if self.low > self.high:
            g = random.randint(1, 100)
        else:
            g = (self.low + self.high) // 2
        self.last = g
        self.attempts += 1
        return g

    def can_apply_feedback(self, fb: str) -> bool:
        if self.last is None:
            return False
        if fb == "higher":
            new_low = max(self.low, self.last + 1)
            new_high = self.high
        elif fb == "lower":
            new_low = self.low
            new_high = min(self.high, self.last - 1)
        else:  # correct
            new_low = new_high = self.last
        return 1 <= new_low <= new_high <= 100

    def apply_feedback(self, fb: str):
        if self.last is None:
            return
        if fb == "higher":
            self.low = max(self.low, self.last + 1)
        elif fb == "lower":
            self.high = min(self.high, self.last - 1)


class Game:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("Guess the Number — Head-to-Head Match")
        self.root.geometry("1200x600")

        
        # Professional color scheme
        self.bg_color = "#f5f7fa"  # Light gray background
        self.fg_color = "#000000"  # Text forced to black

        self.primary_color = "#0066cc"  # Professional blue
        self.success_color = "#27ae60"  # Professional green
        self.danger_color = "#e74c3c"  # Professional red
        self.warning_color = "#f39c12"  # Professional orange
        self.secondary_color = "#34495e"  # Dark blue-gray
        self.border_color = "#bdc3c7"  # Light gray border
        self.section_bg = "#ffffff"  # White sections
        
        self.root.config(bg=self.bg_color)

        # Match settings
        # UI sizing (helps keep the right-side menu compact)
        self.sidebar_width = 280
        self.max_rounds = 5

        self.round_no = 0
        self.player_score = 0
        self.ai_score = 0
        self.attempts_allowed = 7  # default (medium)

        # Per-round state
        self.player_secret = None
        self.ai_secret = None
        self.player_attempts = 0
        self.ai_attempts = 0
        self.player_low = 1
        self.player_high = 100
        self.ai = SimpleAI()
        self.player_guesses = set()
        self.player_turn = True  # player starts guessing
        self.round_active = False

        self._build_ui()
        self._update_status()

    def _build_ui(self):
        # Header bar
        header = tk.Frame(self.root, bg=self.primary_color, height=38)
        header.pack(fill=tk.X, side=tk.TOP)
        header.pack_propagate(False)
        
        title = tk.Label(header, text="Guess the Number", font=("Segoe UI", 18, "bold"), 
                         bg=self.primary_color, fg="#000000")
        title.pack(side=tk.LEFT, padx=14, pady=6)
        
        subtitle = tk.Label(header, text="Head-to-Head Match", font=("Segoe UI", 9), 
                            bg=self.primary_color, fg="#000000")
        subtitle.pack(side=tk.LEFT, padx=5)
        
        # Main container
        main_container = tk.Frame(self.root, bg=self.bg_color)
        main_container.pack(fill=tk.BOTH, expand=True, padx=12, pady=12)
        
        # Left side: Log panel
        left_panel = tk.Frame(main_container, bg=self.section_bg, relief=tk.FLAT, bd=0)
        left_panel.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 8))
        
        log_title = tk.Label(left_panel, text="Game Log", font=("Segoe UI", 13, "bold"),
                            bg=self.section_bg, fg="#000000")
        log_title.pack(anchor=tk.W, padx=12, pady=(12, 8))
        
        self.log = scrolledtext.ScrolledText(left_panel, width=70, height=28, state=tk.DISABLED,
                                             bg="#fafbfc", fg=self.fg_color, font=("Consolas", 9),
                                             relief=tk.FLAT, bd=1, highlightthickness=0)
        self.log.pack(fill=tk.BOTH, expand=True, padx=12, pady=(0, 12))
        
        # Right side: Controls (compact width, full height)
        right_panel = tk.Frame(main_container, bg=self.bg_color, width=self.sidebar_width)
        right_panel.pack_propagate(False)
        right_panel.pack(side=tk.RIGHT, fill=tk.BOTH, expand=False, padx=(0, 8))

        
        # --- Match Status Section ---
        status_frame = tk.Frame(right_panel, bg=self.section_bg, relief=tk.FLAT, bd=0)
        status_frame.pack(fill=tk.X, pady=(0, 10), padx=8, ipady=10)
        
        status_title = tk.Label(status_frame, text="Match Status", font=("Segoe UI", 12, "bold"),
                               bg=self.section_bg, fg="#000000")
        status_title.pack(anchor=tk.W, padx=12, pady=(6, 12))
        
        self.lbl_round = tk.Label(status_frame, text="Round: 0 / 5", font=("Segoe UI", 10),
                                  bg=self.section_bg, fg="#000000")
        self.lbl_round.pack(anchor=tk.W, padx=12, pady=2)
        
        self.lbl_score = tk.Label(status_frame, text="Your Score: 0  |  AI Score: 0", 
                                  font=("Segoe UI", 10, "bold"), bg=self.section_bg, fg="#000000")
        self.lbl_score.pack(anchor=tk.W, padx=12, pady=2)
        
        self.lbl_attempts = tk.Label(status_frame, text="Attempts: You 0 | AI 0", 
                                     font=("Segoe UI", 9), bg=self.section_bg, fg="#000000")
        self.lbl_attempts.pack(anchor=tk.W, padx=12, pady=2)
        
        self.lbl_player_bounds = tk.Label(status_frame, text="Your Range: 1 - 100", 
                                          font=("Segoe UI", 9), bg=self.section_bg, fg="#000000")
        self.lbl_player_bounds.pack(anchor=tk.W, padx=12, pady=2)
        
        self.lbl_ai_bounds = tk.Label(status_frame, text="AI Range: 1 - 100", 
                                      font=("Segoe UI", 9), bg=self.section_bg, fg="#000000")
        self.lbl_ai_bounds.pack(anchor=tk.W, padx=12, pady=(2, 6))
        
        # --- Difficulty Section ---
        diff_frame = tk.Frame(right_panel, bg=self.section_bg, relief=tk.FLAT, bd=0)
        diff_frame.pack(fill=tk.X, pady=(0, 10), padx=8, ipady=10)
        
        diff_title = tk.Label(diff_frame, text="Difficulty Level", font=("Segoe UI", 12, "bold"),
                             bg=self.section_bg, fg="#000000")
        diff_title.pack(anchor=tk.W, padx=12, pady=(6, 8))
        
        self.diff_var = tk.StringVar(value="Medium")
        diff_menu = tk.OptionMenu(diff_frame, self.diff_var, "Easy", "Medium", "Hard", 
                                  command=self._on_diff_change)
        diff_menu.config(
            bg=self.primary_color,
            fg="#000000",
            activebackground=self.primary_color,
            activeforeground="#000000",
            font=("Segoe UI", 10),
            relief=tk.RAISED,
            bd=1,
            width=24,
        )
        diff_menu.pack(fill=tk.X, padx=12, pady=(0, 6))
        
        # --- Your Secret Section ---
        secret_frame = tk.Frame(right_panel, bg=self.section_bg, relief=tk.FLAT, bd=0)
        secret_frame.pack(fill=tk.X, pady=(0, 10), padx=8, ipady=10)
        
        secret_title = tk.Label(secret_frame, text="Step 1: Enter Your Secret", font=("Segoe UI", 12, "bold"),
                               bg=self.section_bg, fg="#000000")
        secret_title.pack(anchor=tk.W, padx=12, pady=(6, 8))
        
        secret_hint = tk.Label(secret_frame, text="(Number 1-100 that AI will guess)", 
                              font=("Segoe UI", 8), bg=self.section_bg, fg="#000000")
        secret_hint.pack(anchor=tk.W, padx=12, pady=(0, 6))
        
        self.entry_secret = tk.Entry(secret_frame, font=("Segoe UI", 11), bg="#a36de0", 
                                     fg="black", insertbackground="black",
                                     selectbackground="#a36de0", selectforeground="black",
                                     highlightthickness=1, highlightbackground="#a36de0",
                                     highlightcolor="#a36de0", relief=tk.FLAT, bd=1, width=26)
        self.entry_secret.pack(fill=tk.X, padx=12, pady=4)
        
        self.btn_start_round = tk.Button(secret_frame, text="Start Round", command=self.start_round,
                                         bg=self.success_color, fg="#000000", font=("Segoe UI", 10, "bold"),
                                         activebackground="#229954", relief=tk.FLAT, bd=0, padx=10, pady=6)
        self.btn_start_round.pack(fill=tk.X, padx=12, pady=(6, 6))
        
        # --- Guess Section ---
        guess_frame = tk.Frame(right_panel, bg=self.section_bg, relief=tk.FLAT, bd=0)
        guess_frame.pack(fill=tk.X, pady=(0, 10), padx=8, ipady=10)
        
        guess_title = tk.Label(guess_frame, text="Step 2: Guess AI's Number", font=("Segoe UI", 12, "bold"),
                              bg=self.section_bg, fg="#000000")
        guess_title.pack(anchor=tk.W, padx=12, pady=(6, 8))
        
        guess_hint = tk.Label(guess_frame, text="(Try to find the AI's secret)", 
                             font=("Segoe UI", 8), bg=self.section_bg, fg="#000000")
        guess_hint.pack(anchor=tk.W, padx=12, pady=(0, 6))
        
        self.entry_guess = tk.Entry(guess_frame, font=("Segoe UI", 11), bg="#5d1b9d", 
                                    fg="#000000", insertbackground="#000000",
                                    selectbackground="#5d1b9d", selectforeground="#000000",
                                    disabledbackground="#5d1b9d", disabledforeground="#000000",
                                    highlightthickness=1, highlightbackground="#5d1b9d",
                                    highlightcolor="#5d1b9d", relief=tk.FLAT, bd=1, width=26, state=tk.DISABLED)
        self.entry_guess.pack(fill=tk.X, padx=12, pady=4)
        
        self.btn_guess = tk.Button(guess_frame, text="Submit Guess", command=self.player_guess, state=tk.DISABLED,
                                   bg=self.primary_color, fg="#000000", font=("Segoe UI", 10, "bold"),
                                   activebackground="#015bb5", activeforeground="#000000",
                                   relief=tk.FLAT, bd=0, padx=10, pady=6)
        self.btn_guess.pack(fill=tk.X, padx=12, pady=(6, 6))
        
        # --- AI Feedback Section ---
        ai_frame = tk.Frame(right_panel, bg=self.section_bg, relief=tk.FLAT, bd=0)
        ai_frame.pack(fill=tk.X, pady=(0, 10), padx=8, ipady=10)
        
        ai_title = tk.Label(ai_frame, text="Step 3: Respond to AI", font=("Segoe UI", 12, "bold"),
                           bg=self.section_bg, fg="#000000")
        ai_title.pack(anchor=tk.W, padx=12, pady=(6, 8))
        
        self.lbl_ai_guess = tk.Label(ai_frame, text="AI will guess after your turn", 
                                     font=("Segoe UI", 9), bg="#2c2c2c", fg="#000000")
        self.lbl_ai_guess.pack(fill=tk.X, padx=12, pady=4)
        
        fb_frame = tk.Frame(ai_frame, bg=self.section_bg)
        fb_frame.pack(fill=tk.X, padx=12, pady=(8, 6))
        
        self.btn_higher = tk.Button(fb_frame, text="Higher", command=lambda: self.ai_feedback("higher"), 
                                    state=tk.DISABLED, bg=self.success_color, fg="#000000", 
                                    font=("Segoe UI", 9, "bold"), activebackground="#229954", 
                                    relief=tk.FLAT, bd=0, padx=6, pady=5)
        self.btn_higher.pack(side=tk.LEFT, padx=3)
        
        self.btn_lower = tk.Button(fb_frame, text="Lower", command=lambda: self.ai_feedback("lower"), 
                                   state=tk.DISABLED, bg=self.danger_color, fg="#000000", 
                                   font=("Segoe UI", 9, "bold"), activebackground="#c0392b", 
                                   relief=tk.FLAT, bd=0, padx=6, pady=5)
        self.btn_lower.pack(side=tk.LEFT, padx=3)
        
        self.btn_correct = tk.Button(fb_frame, text="Correct", command=lambda: self.ai_feedback("correct"), 
                                     state=tk.DISABLED, bg=self.warning_color, fg="#000000", 
                                     font=("Segoe UI", 9, "bold"), activebackground="#d68910", 
                                     relief=tk.FLAT, bd=0, padx=6, pady=5)
        self.btn_correct.pack(side=tk.LEFT, padx=3)
        
        # --- Control Section ---
        ctrl_frame = tk.Frame(right_panel, bg=self.section_bg, relief=tk.FLAT, bd=0)
        ctrl_frame.pack(fill=tk.X, pady=8, padx=8, ipady=10)
        
        self.btn_next_round = tk.Button(ctrl_frame, text="End Round", command=self._force_end_round, 
                                       state=tk.DISABLED, bg="#95a5a6", fg="#000000", 
                                       font=("Segoe UI", 10, "bold"), activebackground="#000000",
                                       relief=tk.FLAT, bd=0, padx=10, pady=6)
        self.btn_next_round.pack(fill=tk.X, padx=12, pady=6)


    def _on_diff_change(self, _=None):
        val = self.diff_var.get()
        mapping = {"Easy": 10, "Medium": 7, "Hard": 5}
        self.attempts_allowed = mapping.get(val, 7)
        self._log(f"Difficulty set to {val} ({self.attempts_allowed} attempts per side)")
        self._update_status()

    def _log(self, msg: str):
        self.log.config(state=tk.NORMAL)
        self.log.insert(tk.END, msg + "\n")
        self.log.see(tk.END)
        self.log.config(state=tk.DISABLED)

    def _update_status(self):
        self.lbl_round.config(text=f"Round: {self.round_no}/{self.max_rounds}")
        self.lbl_score.config(text=f"Score - You: {self.player_score}  AI: {self.ai_score}")
        left_p = max(0, self.attempts_allowed - self.player_attempts) if self.round_active else 0
        left_ai = max(0, self.attempts_allowed - self.ai.attempts) if self.round_active else 0
        self.lbl_attempts.config(text=f"Attempts left - You: {left_p}  AI: {left_ai}")
        self.lbl_player_bounds.config(text=f"Your bounds: {self.player_low}-{self.player_high}")
        self.lbl_ai_bounds.config(text=f"AI bounds: {self.ai.low}-{self.ai.high}")

    def start_round(self):
        if self.round_active:
            return

        # Validate player's secret
        raw = self.entry_secret.get().strip()
        if not raw.isdigit():
            messagebox.showwarning("Invalid", "Enter a valid integer between 1 and 100 for your secret.")
            return
        secret = int(raw)
        if not (1 <= secret <= 100):
            messagebox.showwarning("Out of range", "Secret must be between 1 and 100.")
            return

        # Initialize round
        self.player_secret = secret
        self.ai_secret = random.randint(1, 100)
        self.player_attempts = 0
        self.ai.attempts = 0
        self.player_low = 1
        self.player_high = 100
        self.ai.reset()
        self.player_guesses = set()
        self.player_turn = True
        self.round_active = True
        self.round_no += 1

        # UI state
        self.btn_guess.config(state=tk.NORMAL)
        self.entry_guess.config(state=tk.NORMAL)
        self.entry_secret.config(state=tk.DISABLED)
        self.btn_start_round.config(state=tk.DISABLED)
        self.btn_higher.config(state=tk.DISABLED)
        self.btn_lower.config(state=tk.DISABLED)
        self.btn_correct.config(state=tk.DISABLED)
        self.btn_next_round.config(state=tk.NORMAL)

        self._log(f"--- Round {self.round_no} start ---")
        self._log("You set your secret. AI has chosen its secret (hidden). You guess first.")
        self._update_status()

    def player_guess(self):
        if not self.round_active or not self.player_turn:
            return

        raw = self.entry_guess.get().strip()
        if not raw.lstrip("+-").isdigit():
            self._log("Enter a valid integer guess (1-100).")
            return
        guess = int(raw)
        if not (1 <= guess <= 100):
            self._log("Guess out of range. Enter 1-100.")
            return

        self.player_attempts += 1
        self.player_guesses.add(guess)
        self._log(f"You guessed: {guess}")

        if guess == self.ai_secret:
            self._log(f"Correct! You guessed AI's number in {self.player_attempts} attempts.")
            self._end_round("player")
            return
        elif guess < self.ai_secret: # type: ignore
            self.player_low = max(self.player_low, guess + 1)
            self._log("Too low. AI's number is higher.")
        else:
            self.player_high = min(self.player_high, guess - 1)
            self._log("Too high. AI's number is lower.")

        if self.player_low > self.player_high:
            self._log("Rules broken: your own guesses contradict previous hints.")
            self._log("AI wins this round due to invalid player feedback.")
            self._end_round("ai")
            return

        self._log(f"Your bounds are now {self.player_low} to {self.player_high}.")

        # After player guess, switch to AI's turn
        self.player_turn = False
        self.entry_guess.delete(0, tk.END)
        self._update_status()
        self.root.after(400, self._ai_turn)

    def _ai_turn(self):
        if not self.round_active:
            return
        # Check AI attempts left
        if self.ai.attempts >= self.attempts_allowed:
            self._log("AI has no attempts left to guess.")
            # back to player or end if both exhausted
            self.player_turn = True
            self._check_round_exhaustion()
            return

        guess = self.ai.guess()
        self._log(f"AI guesses: {guess}")
        # Show AI guess and enable feedback buttons for player
        self.lbl_ai_guess.config(text=f"AI guessed: {guess}")
        self.btn_higher.config(state=tk.NORMAL)
        self.btn_lower.config(state=tk.NORMAL)
        self.btn_correct.config(state=tk.NORMAL)
        self._update_status()

    def ai_feedback(self, kind: str):
        if not self.round_active or self.player_turn:
            return

        # Validate feedback against AI's existing bounds first.
        if kind != "correct" and not self.ai.can_apply_feedback(kind):
            self._log("Rules broken: your feedback contradicts previous answers.")
            self._log("AI detects impossible bounds and wins this round.")
            self._end_round("ai")
            return

        # Apply feedback to AI internal bounds
        if kind == "correct":
            self._log(f"AI guessed correctly! It found your secret ({self.ai.last}).")
            self._end_round("ai")
            return

        # higher: AI's guess was too low -> secret is higher
        # lower: AI's guess was too high -> secret is lower
        self.ai.apply_feedback(kind)
        self._log(f"You told AI: {kind.upper()}")
        self._log(f"AI bounds are now {self.ai.low} to {self.ai.high}.")

        # disable feedback until next AI guess
        self.btn_higher.config(state=tk.DISABLED)
        self.btn_lower.config(state=tk.DISABLED)
        self.btn_correct.config(state=tk.DISABLED)

        # After giving feedback, switch back to player
        self.player_turn = True
        self._update_status()

        # If AI used all attempts after its guess, check exhaustion
        if self.ai.attempts >= self.attempts_allowed:
            self._check_round_exhaustion()

    def _check_round_exhaustion(self):
        # If both exhausted, end round as draw
        player_left = self.attempts_allowed - self.player_attempts
        ai_left = self.attempts_allowed - self.ai.attempts
        if player_left <= 0 and ai_left <= 0:
            self._log("Both sides exhausted attempts. Round ends with no winner.")
            self._end_round("none")

    def _end_round(self, winner: str):
        self.round_active = False
        self.btn_guess.config(state=tk.DISABLED)
        self.entry_guess.config(state=tk.DISABLED)
        self.entry_secret.config(state=tk.NORMAL)
        self.btn_start_round.config(state=tk.NORMAL)
        self.btn_higher.config(state=tk.DISABLED)
        self.btn_lower.config(state=tk.DISABLED)
        self.btn_correct.config(state=tk.DISABLED)
        self.btn_next_round.config(state=tk.DISABLED)

        if winner == "player":
            self.player_score += 1
            self._log("You win this round! 🎉")
        elif winner == "ai":
            self.ai_score += 1
            self._log("AI wins this round. 🤖")
        else:
            self._log("Round was a draw.")

        self._update_status()

        # If match over, show final
        if self.round_no >= self.max_rounds:
            self._show_match_result()

    def _show_match_result(self):
        self._log("=== Match Over ===")
        self._log(f"Final Score - You: {self.player_score}  AI: {self.ai_score}")
        if self.player_score > self.ai_score:
            messagebox.showinfo("Match Result", "🏆 You won the match! Congratulations!")
        elif self.player_score < self.ai_score:
            messagebox.showinfo("Match Result", "🤖 AI won the match. Better luck next time!")
        else:
            messagebox.showinfo("Match Result", "It's a tie! Well played.")

    def _force_end_round(self):
        if not self.round_active:
            return
        self._log("Round force-ended by player.")
        self._end_round("none")


def main():
    root = tk.Tk()
    game = Game(root)
    root.mainloop()


if __name__ == "__main__":
    main()
