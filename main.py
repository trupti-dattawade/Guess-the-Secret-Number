import random
import tkinter as tk
from tkinter import scrolledtext, messagebox, simpledialog


# 🎚 Difficulty AI (guess strategy only)
class AIAgent:
    def __init__(self, low: int = 1, high: int = 100):
        self.low = low
        self.high = high
        self.last_guess = None
        self.turns = 0

    def guess(self, difficulty: str) -> int:
        rng = self.high - self.low

        if self.low > self.high:
            raise ValueError("Inconsistent bounds")

        if difficulty == "Easy":
            g = random.randint(self.low, self.high)
        elif difficulty == "Medium":
            mid = (self.low + self.high) // 2
            spread = max(2, rng // 3)
            g = random.randint(max(self.low, mid - spread), min(self.high, mid + spread))
        else:  # Hard
            mid = (self.low + self.high) // 2
            spread = max(1, rng // 8)
            g = random.randint(max(self.low, mid - spread), min(self.high, mid + spread))

        self.last_guess = g
        self.turns += 1
        return g


class GameEngine:
    def __init__(self):
        self.reset_match()

    def reset_match(self):
        self.round = 1
        self.max_rounds = 5
        self.player_score = 0
        self.ai_score = 0
        self.dashboard = []  # (round_no, winner, ai_turns, player_turns)
        self.start_round()

    def start_round(self):
        self.ai = AIAgent(1, 100)
        self.user_secret = None  # number the AI is trying to find (you provide)
        self.ai_secret = random.randint(1, 100)  # number you are trying to find
        self.round_over = False
        self.winner = None  # 'player' or 'ai'
        self.player_turns = 0


CHEAT_MSG = "This is out of rule and you are cheating"


# ---------------- UI Setup ----------------
root = tk.Tk()
root.withdraw()
username = simpledialog.askstring("Login", "Enter username:")
root.deiconify()
if not username:
    username = "Player"

root.title("🔮 Number Whisperer Duel")
root.geometry("1050x820")
root.config(bg="#0f172a")

# Difficulty selector
difficulty = tk.StringVar(value="Medium")

welcome_lbl = tk.Label(
    root,
    text=f"Welcome {username}",
    font=("Helvetica", 22, "bold"),
    fg="#38bdf8",
    bg="#0f172a",
)
welcome_lbl.pack(pady=10)

frame_diff = tk.Frame(root, bg="#0f172a")
frame_diff.pack(pady=6)

tk.Label(frame_diff, text="Difficulty:", fg="white", bg="#0f172a", font=("Helvetica", 12)).grid(
    row=0, column=0, padx=10
)
tk.OptionMenu(frame_diff, difficulty, "Easy", "Medium", "Hard").grid(row=0, column=1)

score_label = tk.Label(root, font=("Helvetica", 12), fg="#facc15", bg="#0f172a")
score_label.pack(pady=6)

main_frame = tk.Frame(root, bg="#0f172a")
main_frame.pack(fill="both", expand=True, padx=14, pady=10)

left = tk.Frame(main_frame, bg="#0f172a")
left.pack(side="left", fill="both", expand=True)

right = tk.Frame(main_frame, bg="#0f172a")
right.pack(side="right", fill="y", padx=10)

# Log panel
log = scrolledtext.ScrolledText(
    left,
    width=70,
    height=22,
    bg="#020617",
    fg="white",
    font=("Consolas", 11),
)
log.pack(pady=10)

# Dashboard
dash = tk.LabelFrame(
    right,
    text="🏆 Creative Dashboard (5 rounds)",
    bg="#0f172a",
    fg="white",
    padx=10,
    pady=10,
)
dash.pack(fill="x", pady=8)

cards_frame = tk.Frame(dash, bg="#0f172a")
cards_frame.pack()

round_cards = []
for i in range(5):
    c = tk.LabelFrame(cards_frame, text=f"Round {i+1}", bg="#0f172a", fg="white", padx=8, pady=6)
    c.grid(row=0, column=i, padx=6)

    winner_lbl = tk.Label(c, text="—", bg="#0f172a", fg="#e5e7eb", font=("Helvetica", 11, "bold"))
    winner_lbl.pack()

    meta_lbl = tk.Label(c, text="", bg="#0f172a", fg="#94a3b8", font=("Consolas", 9))
    meta_lbl.pack(pady=(6, 0))

    round_cards.append((winner_lbl, meta_lbl))


# Gameplay controls (right side)
user_secret_box = tk.LabelFrame(
    right,
    text="1) Your Secret (AI must guess it)",
    bg="#0f172a",
    fg="white",
    padx=10,
    pady=10,
)
user_secret_box.pack(fill="x", pady=8)

entry_secret_user = tk.Entry(user_secret_box, font=("Helvetica", 16))
entry_secret_user.pack(pady=6, fill="x")

btn_submit_secret = tk.Button(
    user_secret_box,
    text="Start Round / Submit Secret",
    bg="#38bdf8",
    fg="white",
    font=("Helvetica", 11, "bold"),
    command=lambda: on_submit_user_secret(),
    height=2,
)
btn_submit_secret.pack(pady=6, fill="x")

ai_feedback_box = tk.LabelFrame(
    right,
    text="2) Buttons for AI's guess",
    bg="#0f172a",
    fg="white",
    padx=10,
    pady=10,
)
ai_feedback_box.pack(fill="x", pady=8)

btn_frame = tk.Frame(ai_feedback_box, bg="#0f172a")
btn_frame.pack()

btn_higher = tk.Button(btn_frame, text="Higher", bg="#22c55e", fg="white", width=12,
                       command=lambda: ai_feedback_handler("higher"))
btn_higher.grid(row=0, column=0, padx=5, pady=5)

btn_lower = tk.Button(btn_frame, text="Lower", bg="#f59e0b", fg="white", width=12,
                      command=lambda: ai_feedback_handler("lower"))
btn_lower.grid(row=0, column=1, padx=5, pady=5)

btn_correct = tk.Button(btn_frame, text="Correct", bg="#ef4444", fg="white", width=12,
                        command=lambda: ai_feedback_handler("correct"))
btn_correct.grid(row=0, column=2, padx=5, pady=5)

ai_guess_box = tk.LabelFrame(
    right,
    text="3) Guess AI's Secret (You must guess it)",
    bg="#0f172a",
    fg="white",
    padx=10,
    pady=10,
)
ai_guess_box.pack(fill="x", pady=8)

entry_ai_guess = tk.Entry(ai_guess_box, font=("Helvetica", 16))
entry_ai_guess.pack(pady=6, fill="x")

guess_ai_btn = tk.Button(
    ai_guess_box,
    text="Guess AI Number 🎯",
    command=lambda: player_guess(),
    bg="#38bdf8",
    fg="white",
    font=("Helvetica", 11, "bold"),
    height=2,
)
guess_ai_btn.pack(pady=6, fill="x")


# ---------------- Game Logic ----------------
engine = GameEngine()

# UI state references that are used in multiple functions
ai_last_guess_lbl = None


def write(msg: str):
    log.insert(tk.END, msg + "\n")
    log.see(tk.END)


def update_score():
    score_label.config(
        text=f"Round {engine.round}/{engine.max_rounds} | {username}: {engine.player_score} | AI: {engine.ai_score}"
    )


def set_controls_enabled(enabled: bool):
    st = "normal" if enabled else "disabled"
    for w in (btn_higher, btn_lower, btn_correct, guess_ai_btn, entry_secret_user, entry_ai_guess):
        try:
            w.config(state=st)
        except Exception:
            pass
    try:
        btn_submit_secret.config(state=st)
    except Exception:
        pass


def enable_ai_buttons(enabled: bool):
    st = "normal" if enabled else "disabled"
    for w in (btn_higher, btn_lower, btn_correct):
        w.config(state=st)


def cheating_out_of_rule():
    messagebox.showerror("Cheating detected", CHEAT_MSG)


def lock_round(winner: str):
    engine.round_over = True
    engine.winner = winner
    set_controls_enabled(False)


def finish_round_if_needed():
    if engine.winner is None:
        return

    if engine.winner == "player":
        engine.player_score += 1
        title = "🎉 You won"
    else:
        engine.ai_score += 1
        title = "🤖 AI won"

    rno = engine.round
    ai_turns = engine.ai.turns
    player_turns = engine.player_turns

    winner_lbl, meta_lbl = round_cards[rno - 1]
    winner_lbl.config(text=title)
    meta_lbl.config(text=f"AI turns: {ai_turns} | Your turns: {player_turns}")

    write(f"\n🏁 End of Round {rno}: {title}\n")

    if engine.round == engine.max_rounds:
        if engine.player_score > engine.ai_score:
            messagebox.showinfo("Match Over", "🏆 YOU WON THE MATCH!")
        elif engine.player_score < engine.ai_score:
            messagebox.showinfo("Match Over", "🤖 AI WON THE MATCH!")
        else:
            messagebox.showinfo("Match Over", "It's a tie! 🤝")

        # Reset match
        engine.reset_match()
        log.delete(1.0, tk.END)
        for i in range(5):
            round_cards[i][0].config(text="—")
            round_cards[i][1].config(text="")
        update_score()
        start_new_round_ui()
        return

    engine.round += 1
    engine.start_round()
    update_score()
    start_new_round_ui()


def start_new_round_ui():
    set_controls_enabled(True)
    enable_ai_buttons(False)

    log.delete(1.0, tk.END)
    write("Enter your secret number (1-100). AI will start guessing it.")
    write("Then answer AI with Higher / Lower / Correct.")
    write("You also try to guess AI's secret number. First to be correct wins the round.\n")

    entry_secret_user.delete(0, tk.END)
    entry_ai_guess.delete(0, tk.END)

    engine.user_secret = None
    engine.round_over = False
    engine.winner = None

    write("Waiting for your secret...\n")


# --- Submission: user secret ---

def on_submit_user_secret():
    if engine.round_over:
        return

    try:
        s = int(entry_secret_user.get())
    except Exception:
        write("Enter a valid integer for your secret number (1-100).")
        return

    if not (1 <= s <= 100):
        write("Your secret must be between 1 and 100.")
        return

    engine.user_secret = s

    # Reset AI bounds tracking for this round
    engine.ai.low = 1
    engine.ai.high = 100
    engine.ai.last_guess = None
    engine.ai.turns = 0

    enable_ai_buttons(True)

    first = engine.ai.guess(difficulty.get())
    write(f"🤖 AI starts guessing: {first} (bounds: {engine.ai.low}-{engine.ai.high})")


# --- AI feedback handling with strict consistency checks ---

def ai_feedback_handler(kind: str):
    if engine.round_over:
        return

    if engine.user_secret is None:
        write("Submit your secret number first.")
        return

    if engine.ai.last_guess is None:
        write("AI has not guessed yet.")
        return

    g = engine.ai.last_guess

    # Current bounds are engine.ai.low..engine.ai.high.
    cur_low, cur_high = engine.ai.low, engine.ai.high

    # Translate feedback into new bounds.
    if kind == "higher":
        new_low, new_high = g + 1, cur_high
    elif kind == "lower":
        new_low, new_high = cur_low, g - 1
    else:  # correct
        new_low, new_high = g, g

    # Cheating/out-of-rule rule:
    # If it would make the solution impossible, or contradict existing bounds.
    if new_low > new_high or new_low < 1 or new_high > 100:
        cheating_out_of_rule()
        return

    if new_low < cur_low or new_high > cur_high:
        cheating_out_of_rule()
        return

    # Apply updated bounds
    engine.ai.low, engine.ai.high = new_low, new_high

    # If AI deduced the exact secret, AI wins immediately (whoever guesses first wins)
    if kind == "correct" or engine.ai.low == engine.ai.high:
        # If user clicked incorrect feedback earlier, the consistency checks would have blocked.
        lock_round("ai")
        write(f"AI deduced your secret! Secret = {engine.ai.low}")
        finish_round_if_needed()
        return

    # Next guess
    nxt = engine.ai.guess(difficulty.get())
    write(f"🤖 AI guesses: {nxt} (bounds: {engine.ai.low}-{engine.ai.high})")


# --- Your guess of AI secret ---

def player_guess():
    if engine.round_over:
        return

    try:
        guess = int(entry_ai_guess.get())
    except Exception:
        write("Enter a valid integer for your guess (1-100).")
        return

    engine.player_turns += 1

    if guess == engine.ai_secret:
        lock_round("player")
        write(f"🎯 You guessed AI's number in {engine.player_turns} turns! (AI secret = {engine.ai_secret})")
        finish_round_if_needed()
    elif guess < engine.ai_secret:
        write("AI says: HIGHER")
    else:
        write("AI says: LOWER")


# Initialize
update_score()
start_new_round_ui()

root.mainloop()

