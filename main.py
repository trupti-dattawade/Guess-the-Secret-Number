import random
import tkinter as tk
from tkinter import ttk


class AIPlayer:
    def __init__(self):
        self.reset()

    def reset(self):
        self.low = 1
        self.high = 100
        self.last = None

    def guess(self):
        self.last = (self.low + self.high) // 2
        return self.last

    def higher(self):
        if self.last is not None:
            self.low = self.last + 1

    def lower(self):
        if self.last is not None:
            self.high = self.last - 1


class Game:
    def __init__(self, root):
        self.root = root
        self.root.title("Guessing Battle")
        self.root.geometry("900x560")
        self.root.minsize(860, 540)
        self.root.configure(bg="#f3f6fb")

        self.ai = AIPlayer()
        self.max_rounds = 5
        self.start_new_match()

        self.setup_styles()
        self.build_ui()

    def setup_styles(self):
        style = ttk.Style()
        style.theme_use("clam")

        style.configure("App.TFrame", background="#f3f6fb")
        style.configure("Card.TFrame", background="#ffffff", relief="flat")
        style.configure("Header.TLabel", background="#f3f6fb", foreground="#10233f", font=("Segoe UI", 18, "bold"))
        style.configure("SubHeader.TLabel", background="#f3f6fb", foreground="#5a6b84", font=("Segoe UI", 9))
        style.configure("CardTitle.TLabel", background="#ffffff", foreground="#10233f", font=("Segoe UI", 11, "bold"))
        style.configure("Body.TLabel", background="#ffffff", foreground="#41536d", font=("Segoe UI", 9))
        style.configure("Status.TLabel", background="#edf3ff", foreground="#163968", font=("Segoe UI", 10, "bold"), padding=(10, 8))
        style.configure("Feedback.TLabel", background="#ffffff", foreground="#163968", font=("Segoe UI", 9, "bold"))
        style.configure("ScoreValue.TLabel", background="#ffffff", foreground="#10233f", font=("Segoe UI", 14, "bold"))
        style.configure("ScoreCaption.TLabel", background="#ffffff", foreground="#6b7a90", font=("Segoe UI", 8, "bold"))

        style.configure("Primary.TButton", font=("Segoe UI", 9, "bold"), padding=(10, 7), background="#1f6feb", foreground="#ffffff", borderwidth=0)
        style.map("Primary.TButton", background=[("active", "#1857ba")])

        style.configure("Secondary.TButton", font=("Segoe UI", 9, "bold"), padding=(10, 7), background="#e8eef8", foreground="#183153", borderwidth=0)
        style.map("Secondary.TButton", background=[("active", "#d9e5f5")])

        style.configure("Success.TButton", font=("Segoe UI", 9, "bold"), padding=(10, 7), background="#1f8f5f", foreground="#ffffff", borderwidth=0)
        style.map("Success.TButton", background=[("active", "#15724b")])

        style.configure("App.TEntry", padding=6)

    def build_ui(self):
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)

        app = ttk.Frame(self.root, style="App.TFrame", padding=16)
        app.grid(sticky="nsew")
        app.columnconfigure(0, weight=1)
        app.rowconfigure(3, weight=1)

        ttk.Label(app, text="Number Guess Duel", style="Header.TLabel").grid(row=0, column=0, sticky="w")
        ttk.Label(
            app,
            text="A cleaner head-to-head game where you challenge the AI while it tries to solve your number.",
            style="SubHeader.TLabel",
        ).grid(row=1, column=0, sticky="w", pady=(2, 10))

        self.build_scoreboard(app)

        content = ttk.Frame(app, style="App.TFrame")
        content.grid(row=3, column=0, sticky="nsew")
        content.columnconfigure(0, weight=1)
        content.columnconfigure(1, weight=1)
        content.rowconfigure(1, weight=1)

        self.build_ai_panel(content)
        self.build_player_panel(content)
        self.build_log_panel(content)

        self.refresh_scoreboard()

    def build_scoreboard(self, parent):
        panel = ttk.Frame(parent, style="Card.TFrame", padding=12)
        panel.grid(row=2, column=0, sticky="ew", pady=(0, 10))
        panel.columnconfigure(3, weight=1)

        ttk.Label(panel, text="Match Scoreboard", style="CardTitle.TLabel").grid(row=0, column=0, sticky="w")
        self.round_label = ttk.Label(panel, text="", style="Body.TLabel")
        self.round_label.grid(row=1, column=0, sticky="w", pady=(2, 0))

        ttk.Label(panel, text="PLAYER", style="ScoreCaption.TLabel").grid(row=0, column=1, padx=(18, 8))
        self.player_score_label = ttk.Label(panel, text="0", style="ScoreValue.TLabel")
        self.player_score_label.grid(row=1, column=1, padx=(18, 8))

        ttk.Label(panel, text="AI", style="ScoreCaption.TLabel").grid(row=0, column=2, padx=8)
        self.ai_score_label = ttk.Label(panel, text="0", style="ScoreValue.TLabel")
        self.ai_score_label.grid(row=1, column=2, padx=8)

        self.match_status_label = ttk.Label(panel, text="", style="Body.TLabel")
        self.match_status_label.grid(row=0, column=3, rowspan=2, sticky="e")

    def build_ai_panel(self, parent):
        panel = ttk.Frame(parent, style="Card.TFrame", padding=12)
        panel.grid(row=0, column=0, sticky="nsew", padx=(0, 8), pady=(0, 8))
        panel.columnconfigure(0, weight=1)

        ttk.Label(panel, text="AI Guessing Your Number", style="CardTitle.TLabel").grid(row=0, column=0, sticky="w")
        ttk.Label(panel, text="Set a number from 1 to 100 and guide the AI.", style="Body.TLabel", wraplength=250).grid(row=1, column=0, sticky="w", pady=(4, 10))

        ttk.Label(panel, text="Your secret number", style="Body.TLabel").grid(row=2, column=0, sticky="w")
        self.secret_entry = ttk.Entry(panel, style="App.TEntry")
        self.secret_entry.grid(row=3, column=0, sticky="ew", pady=(4, 8))

        ttk.Button(panel, text="Start AI Round", style="Primary.TButton", command=self.start_ai_guess).grid(row=4, column=0, sticky="ew")

        self.ai_guess_label = ttk.Label(panel, text="AI guess will appear here.", style="Status.TLabel", anchor="center")
        self.ai_guess_label.grid(row=5, column=0, sticky="ew", pady=(10, 10))

        actions = ttk.Frame(panel, style="Card.TFrame")
        actions.grid(row=6, column=0, sticky="ew")
        actions.columnconfigure((0, 1, 2), weight=1)

        ttk.Button(actions, text="Higher", style="Secondary.TButton", command=self.ai_higher).grid(row=0, column=0, sticky="ew", padx=(0, 4))
        ttk.Button(actions, text="Lower", style="Secondary.TButton", command=self.ai_lower).grid(row=0, column=1, sticky="ew", padx=2)
        ttk.Button(actions, text="Correct", style="Success.TButton", command=self.ai_correct).grid(row=0, column=2, sticky="ew", padx=(4, 0))

    def build_player_panel(self, parent):
        panel = ttk.Frame(parent, style="Card.TFrame", padding=12)
        panel.grid(row=0, column=1, sticky="nsew", padx=(8, 0), pady=(0, 8))
        panel.columnconfigure(0, weight=1)

        ttk.Label(panel, text="Your Turn To Guess", style="CardTitle.TLabel").grid(row=0, column=0, sticky="w")
        ttk.Label(panel, text="Guess the AI's number and get instant feedback.", style="Body.TLabel", wraplength=250).grid(row=1, column=0, sticky="w", pady=(4, 10))

        ttk.Label(panel, text="Enter your guess", style="Body.TLabel").grid(row=2, column=0, sticky="w")
        self.guess_entry = ttk.Entry(panel, style="App.TEntry")
        self.guess_entry.grid(row=3, column=0, sticky="ew", pady=(4, 8))

        ttk.Button(panel, text="Submit Guess", style="Primary.TButton", command=self.player_guess).grid(row=4, column=0, sticky="ew")

        self.result_label = ttk.Label(panel, text="Waiting for your first guess.", style="Feedback.TLabel", anchor="center")
        self.result_label.grid(row=5, column=0, sticky="ew", pady=(10, 0))

    def build_log_panel(self, parent):
        panel = ttk.Frame(parent, style="Card.TFrame", padding=12)
        panel.grid(row=1, column=0, columnspan=2, sticky="nsew")
        panel.columnconfigure(0, weight=1)
        panel.rowconfigure(1, weight=1)

        ttk.Label(panel, text="Match Activity", style="CardTitle.TLabel").grid(row=0, column=0, sticky="w")

        self.log = tk.Text(
            panel,
            height=7,
            bg="#f8fbff",
            fg="#29405f",
            bd=0,
            relief="flat",
            insertbackground="#29405f",
            font=("Consolas", 9),
            padx=8,
            pady=8,
            wrap="word",
        )
        self.log.grid(row=1, column=0, sticky="nsew", pady=(8, 0))
        self.log.insert("end", "Game ready. Start a round from either panel.\n")
        self.log.configure(state="disabled")

    def start_new_match(self):
        self.current_round = 1
        self.player_score = 0
        self.ai_score = 0
        self.round_results = []
        self.round_over = False
        self.user_secret = None
        self.ai_secret = random.randint(1, 100)
        self.ai.reset()

    def reset_round_state(self):
        self.round_over = False
        self.user_secret = None
        self.ai_secret = random.randint(1, 100)
        self.ai.reset()

        if hasattr(self, "secret_entry"):
            self.secret_entry.delete(0, "end")
        if hasattr(self, "guess_entry"):
            self.guess_entry.delete(0, "end")
        if hasattr(self, "ai_guess_label"):
            self.ai_guess_label.config(text="AI guess will appear here.")
        if hasattr(self, "result_label"):
            self.result_label.config(text=f"Round {self.current_round}: waiting for your first guess.")

    def refresh_scoreboard(self):
        if not hasattr(self, "player_score_label"):
            return

        self.round_label.config(text=f"Round {self.current_round} of {self.max_rounds}")
        self.player_score_label.config(text=str(self.player_score))
        self.ai_score_label.config(text=str(self.ai_score))

        if self.round_results:
            summary = " | ".join(
                f"R{index + 1}: {winner}" for index, winner in enumerate(self.round_results)
            )
        else:
            summary = "No rounds completed yet."
        self.match_status_label.config(text=summary)

    def log_msg(self, msg):
        self.log.configure(state="normal")
        self.log.insert("end", f"{msg}\n")
        self.log.see("end")
        self.log.configure(state="disabled")

    def parse_number(self, entry, field_name):
        value = entry.get().strip()
        if not value.isdigit():
            self.result_label.config(text=f"{field_name} must be a number from 1 to 100.")
            self.log_msg(f"Invalid input for {field_name.lower()}.")
            return None

        number = int(value)
        if not 1 <= number <= 100:
            self.result_label.config(text=f"{field_name} must stay within 1 to 100.")
            self.log_msg(f"Out-of-range input for {field_name.lower()}: {number}")
            return None

        return number

    def start_ai_guess(self):
        if self.round_over:
            self.result_label.config(text="This round is already finished.")
            return

        secret = self.parse_number(self.secret_entry, "Secret number")
        if secret is None:
            return

        self.user_secret = secret
        self.ai.reset()
        self.result_label.config(text="AI round started. Use Higher, Lower, or Correct.")
        self.log_msg("AI round started.")
        self.ai_turn()

    def ai_turn(self):
        if self.round_over:
            return

        if self.ai.low > self.ai.high:
            self.ai_guess_label.config(text="Feedback conflict detected. Restart the AI round.")
            self.log_msg("AI round entered an invalid state due to conflicting feedback.")
            return

        guess = self.ai.guess()
        self.ai_guess_label.config(text=f"AI guesses {guess}")
        self.log_msg(f"AI guessed {guess}")

    def ai_higher(self):
        if self.round_over:
            self.result_label.config(text="Round finished. Start the next round.")
            return
        if self.ai.last is None:
            self.result_label.config(text="Start the AI round before giving feedback.")
            return
        self.ai.higher()
        self.ai_turn()

    def ai_lower(self):
        if self.round_over:
            self.result_label.config(text="Round finished. Start the next round.")
            return
        if self.ai.last is None:
            self.result_label.config(text="Start the AI round before giving feedback.")
            return
        self.ai.lower()
        self.ai_turn()

    def ai_correct(self):
        if self.round_over:
            self.result_label.config(text="Round finished. Start the next round.")
            return
        if self.ai.last is None:
            self.result_label.config(text="Start the AI round before confirming the answer.")
            return
        self.ai_guess_label.config(text=f"AI solved it: {self.ai.last}")
        self.finish_round("AI", "AI guessed your number correctly.")

    def player_guess(self):
        if self.round_over:
            self.result_label.config(text="Round finished. Start the next round.")
            return

        guess = self.parse_number(self.guess_entry, "Guess")
        if guess is None:
            return

        if guess < self.ai_secret:
            self.result_label.config(text="Too low. Try a higher number.")
            self.log_msg(f"You guessed {guess} -> Too low")
        elif guess > self.ai_secret:
            self.result_label.config(text="Too high. Try a lower number.")
            self.log_msg(f"You guessed {guess} -> Too high")
        else:
            self.finish_round("Player", "You guessed the AI number correctly.")

    def finish_round(self, winner, message):
        self.round_over = True
        self.round_results.append(winner)

        if winner == "Player":
            self.player_score += 1
        else:
            self.ai_score += 1

        self.result_label.config(text=f"{message} Round {self.current_round} goes to {winner}.")
        self.log_msg(f"{message} Round {self.current_round} winner: {winner}")
        self.refresh_scoreboard()

        if self.current_round >= self.max_rounds:
            self.end_match()
            return

        self.current_round += 1
        self.reset_round_state()
        self.refresh_scoreboard()
        self.log_msg(f"Round {self.current_round} started.")

    def end_match(self):
        if self.player_score > self.ai_score:
            final_message = f"Match complete. You win {self.player_score}-{self.ai_score}."
        elif self.ai_score > self.player_score:
            final_message = f"Match complete. AI wins {self.ai_score}-{self.player_score}."
        else:
            final_message = f"Match complete. It's a draw at {self.player_score}-{self.ai_score}."

        self.result_label.config(text=final_message)
        self.ai_guess_label.config(text="Five rounds completed.")
        self.log_msg(final_message)


root = tk.Tk()
Game(root)
root.mainloop()
