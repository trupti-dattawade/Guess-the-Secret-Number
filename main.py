import tkinter as tk
from tkinter import ttk
import random

# ---------- AI BINARY SEARCH ----------
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
        self.low = self.last + 1 # type: ignore

    def lower(self):
        self.high = self.last - 1 # type: ignore


# ---------- MAIN GAME ----------
class Game:
    def __init__(self, root):
        self.root = root
        self.root.title("Guessing Battle")
        self.root.geometry("500x650")

        self.ai = AIPlayer()
        self.ai_secret = random.randint(1,100)

        self.build_ui()

    # ---------- UI ----------
    def build_ui(self):
        main = tk.Frame(self.root)
        main.pack(padx=20, pady=20, fill="both", expand=True)

        # TITLE
        tk.Label(main, text="Number Guess Duel", font=("Arial",18,"bold")).pack(pady=10)

        # -------- USER SECRET --------
        tk.Label(main, text="Enter YOUR Secret Number (AI will guess)").pack()
        self.secret_entry = tk.Entry(main)
        self.secret_entry.pack(pady=5)

        tk.Button(main, text="Start AI Guessing", command=self.start_ai_guess).pack(pady=10)

        # AI GUESS LABEL
        self.ai_guess_label = tk.Label(main, text="AI Guess will appear here", font=("Arial",12,"bold"))
        self.ai_guess_label.pack(pady=10)

        # FEEDBACK BUTTONS
        fb = tk.Frame(main)
        fb.pack(pady=10)

        tk.Button(fb, text="Higher", width=10, command=self.ai_higher).grid(row=0,column=0,padx=5)
        tk.Button(fb, text="Lower", width=10, command=self.ai_lower).grid(row=0,column=1,padx=5)
        tk.Button(fb, text="Correct", width=10, command=self.ai_correct).grid(row=0,column=2,padx=5)

        ttk.Separator(main).pack(fill="x", pady=20)

        # -------- PLAYER GUESS AI NUMBER --------
        tk.Label(main, text="Guess AI's Secret Number").pack()
        self.guess_entry = tk.Entry(main)
        self.guess_entry.pack(pady=5)

        tk.Button(main, text="Submit Guess", command=self.player_guess).pack(pady=10)

        self.result_label = tk.Label(main, text="", font=("Arial",12,"bold"))
        self.result_label.pack(pady=10)

        # LOG BOX
        self.log = tk.Text(main, height=10)
        self.log.pack(fill="both", expand=True)

    # ---------- LOG ----------
    def log_msg(self, msg):
        self.log.insert("end", msg+"\n")
        self.log.see("end")

    # =====================================================
    # 🤖 AI GUESSES USER NUMBER
    # =====================================================
    def start_ai_guess(self):
        if not self.secret_entry.get().isdigit():
            return

        self.user_secret = int(self.secret_entry.get())
        self.ai.reset()
        self.ai_turn()

    def ai_turn(self):
        guess = self.ai.guess()
        self.ai_guess_label.config(text=f"AI guesses: {guess}")
        self.log_msg(f"AI guessed {guess}")

    def ai_higher(self):
        self.ai.higher()
        self.ai_turn()

    def ai_lower(self):
        self.ai.lower()
        self.ai_turn()

    def ai_correct(self):
        self.ai_guess_label.config(text="AI guessed correctly! 🤖🎉")
        self.log_msg("AI guessed your number!")

    # =====================================================
    # 🧑 PLAYER GUESSES AI NUMBER
    # =====================================================
    def player_guess(self):
        if not self.guess_entry.get().isdigit():
            return

        guess = int(self.guess_entry.get())

        if guess < self.ai_secret:
            self.result_label.config(text="AI says: TOO LOW")
            self.log_msg(f"You guessed {guess} → Too Low")
        elif guess > self.ai_secret:
            self.result_label.config(text="AI says: TOO HIGH")
            self.log_msg(f"You guessed {guess} → Too High")
        else:
            self.result_label.config(text="AI says: CORRECT 🎉")
            self.log_msg("You guessed AI number correctly!")
            self.ai_secret = random.randint(1,100)


# RUN
root = tk.Tk()
Game(root)
root.mainloop()