import os
from groq import Groq
from dotenv import load_dotenv

# Load key
load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# 🎭 AI Personality + Rules
SYSTEM_PROMPT = """
You are the Number Whisperer — a mystical AI wizard.

You are playing a guessing game:
- The human thinks of a number between 1 and 100.
- Your job is to guess the number.
- You MUST reply with ONLY a number.
- Use binary search strategy.
- Learn from feedback: higher / lower.
- Never speak words, only numbers.
"""

class NumberWhispererAgent:
    def __init__(self):
        self.messages = [
            {"role": "system", "content": SYSTEM_PROMPT}
        ]
        self.turns = 0

    def make_guess(self):
        response = client.chat.completions.create(
            model="llama3-70b-8192",   # fast + smart Groq model
            messages=self.messages, # type: ignore
            temperature=0.2,
        )

        guess = response.choices[0].message.content.strip() # type: ignore
        self.messages.append({"role": "assistant", "content": guess})
        self.turns += 1
        return guess

    def update_feedback(self, feedback):
        self.messages.append({
            "role": "user",
            "content": f"The number is {feedback}"
        })


def show_intro():
    print("\n" + "="*40)
    print("🔮  WELCOME TO NUMBER WHISPERER  🔮")
    print("="*40)
    print("Think of a number between 1 and 100.")
    print("Reply with: higher / lower / correct")
    print("="*40 + "\n")


def get_player_feedback():
    while True:
        feedback = input("Your hint: ").lower().strip()
        if feedback in ["higher", "lower", "correct"]:
            return feedback
        print("Please type: higher / lower / correct")


def play_game():
    show_intro()
    agent = NumberWhispererAgent()

    while True:
        guess = agent.make_guess()
        print(f"\n🤖 AI guesses: {guess}")

        feedback = get_player_feedback()

        if feedback == "correct":
            print(f"\n🎉 AI guessed in {agent.turns} turns!")
            break

        agent.update_feedback(feedback)


if __name__ == "__main__":
    play_game()