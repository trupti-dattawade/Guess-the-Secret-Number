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
        self.low = self.last + 1

    def lower(self):
        self.high = self.last - 1


# ---------- GAME ----------
class Game:
    def __init__(self, root):
        self.root = root
        self.root.title("Guess Duel")
        self.root.geometry("520x680")

        self.ai = AIPlayer()
        self.build_ui()

        self.turn = None

    # ---------- UI ----------
    def build_ui(self):
        main = tk.Frame(self.root)
        main.pack(padx=20, pady=20, fill="both", expand=True)

        tk.Label(main, text="Number Guess Duel", font=("Arial",18,"bold")).pack(pady=10)

        # USER SECRET
        tk.Label(main, text="Your Secret Number (AI will guess)").pack()
        self.secret_entry = tk.Entry(main)
        self.secret_entry.pack()

        tk.Button(main, text="Start Round", command=self.start_round).pack(pady=10)

        ttk.Separator(main).pack(fill="x", pady=10)

        # AI GUESS AREA
        self.ai_guess_label = tk.Label(main, text="Round not started", font=("Arial",12,"bold"))
        self.ai_guess_label.pack(pady=10)

        fb = tk.Frame(main)
        fb.pack(pady=5)

        self.higher_btn = tk.Button(fb, text="Higher", width=10, command=self.ai_higher)
        self.lower_btn = tk.Button(fb, text="Lower", width=10, command=self.ai_lower)
        self.correct_btn = tk.Button(fb, text="Correct", width=10, command=self.ai_correct)

        self.higher_btn.grid(row=0,column=0,padx=5)
        self.lower_btn.grid(row=0,column=1,padx=5)
        self.correct_btn.grid(row=0,column=2,padx=5)

        ttk.Separator(main).pack(fill="x", pady=20)

        # PLAYER GUESS AREA
        tk.Label(main, text="Guess AI Number").pack()
        self.guess_entry = tk.Entry(main)
        self.guess_entry.pack()

        self.guess_btn = tk.Button(main, text="Submit Guess", command=self.player_guess)
        self.guess_btn.pack(pady=10)

        self.result_label = tk.Label(main, text="", font=("Arial",12,"bold"))
        self.result_label.pack(pady=10)

        # LOG
        self.log = tk.Text(main, height=10)
        self.log.pack(fill="both", expand=True)

        self.disable_all()

    def log_msg(self, msg):
        self.log.insert("end", msg+"\n")
        self.log.see("end")

    # ---------- ROUND CONTROL ----------
    def start_round(self):
        if not self.secret_entry.get().isdigit():
            return

        self.user_secret = int(self.secret_entry.get())
        self.ai_secret = random.randint(1,100)
        self.ai.reset()

        self.log.delete("1.0","end")
        self.result_label.config(text="")
        self.log_msg("New Round Started!")

        self.turn = "AI"
        self.enable_ai_buttons()
        self.ai_turn()

    # ---------- TURN MANAGEMENT ----------
    def enable_ai_buttons(self):
        self.higher_btn.config(state="normal")
        self.lower_btn.config(state="normal")
        self.correct_btn.config(state="normal")
        self.guess_btn.config(state="disabled")

    def enable_player_turn(self):
        self.higher_btn.config(state="disabled")
        self.lower_btn.config(state="disabled")
        self.correct_btn.config(state="disabled")
        self.guess_btn.config(state="normal")

    def disable_all(self):
        self.higher_btn.config(state="disabled")
        self.lower_btn.config(state="disabled")
        self.correct_btn.config(state="disabled")
        self.guess_btn.config(state="disabled")

    # =================================================
    # 🤖 AI TURN
    # =================================================
    def ai_turn(self):
        if self.turn != "AI": return
        guess = self.ai.guess()
        self.ai_guess_label.config(text=f"AI guesses: {guess}")
        self.log_msg(f"AI guessed {guess}")

    def ai_higher(self):
        if self.turn != "AI": return
        self.ai.higher()
        self.turn = "PLAYER"
        self.enable_player_turn()

    def ai_lower(self):
        if self.turn != "AI": return
        self.ai.lower()
        self.turn = "PLAYER"
        self.enable_player_turn()

    def ai_correct(self):
        if self.turn != "AI": return
        self.ai_guess_label.config(text="AI guessed your number! 🤖🎉")
        self.log_msg("AI wins!")
        self.disable_all()

    # =================================================
    # 🧑 PLAYER TURN
    # =================================================
    def player_guess(self):
        if self.turn != "PLAYER": return
        if not self.guess_entry.get().isdigit(): return

        guess = int(self.guess_entry.get())

        if guess < self.ai_secret:
            self.result_label.config(text="Too Low")
            self.log_msg(f"You guessed {guess} → Too Low")
            self.turn = "AI"
            self.enable_ai_buttons()
            self.ai_turn()

        elif guess > self.ai_secret:
            self.result_label.config(text="Too High")
            self.log_msg(f"You guessed {guess} → Too High")
            self.turn = "AI"
            self.enable_ai_buttons()
            self.ai_turn()

        else:
            self.result_label.config(text="Correct! 🎉 You win!")
            self.log_msg("You guessed AI number!")
            self.disable_all()


root = tk.Tk()
Game(root)
root.mainloop()