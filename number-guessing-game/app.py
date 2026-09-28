from flask import Flask, render_template, request, session
import random

app = Flask(__name__)
app.secret_key = "change-this-secret-key-before-production"

DIFFICULTIES = {
    "easy": {"max": 50, "attempts": 10, "label": "Easy"},
    "medium": {"max": 100, "attempts": 7, "label": "Medium"},
    "hard": {"max": 200, "attempts": 6, "label": "Hard"},
}

def start_game(difficulty="medium"):
    settings = DIFFICULTIES[difficulty]
    session["difficulty"] = difficulty
    session["secret"] = random.randint(1, settings["max"])
    session["attempts"] = 0
    session["game_over"] = False
    session["won"] = False
    session["message"] = f"Guess a number between 1 and {settings['max']}."

@app.route("/", methods=["GET", "POST"])
def game():
    if "secret" not in session:
        start_game()

    if request.method == "POST":
        action = request.form.get("action")

        if action == "new_game":
            difficulty = request.form.get("difficulty", session.get("difficulty", "medium"))
            if difficulty not in DIFFICULTIES:
                difficulty = "medium"
            start_game(difficulty)

        elif action == "guess" and not session.get("game_over"):
            try:
                guess = int(request.form.get("guess", ""))
                difficulty = session["difficulty"]
                settings = DIFFICULTIES[difficulty]

                if not 1 <= guess <= settings["max"]:
                    session["message"] = f"Enter a number from 1 to {settings['max']}."
                else:
                    session["attempts"] += 1
                    secret = session["secret"]

                    if guess < secret:
                        session["message"] = "⬇️ Too low! Try again."
                    elif guess > secret:
                        session["message"] = "⬆️ Too high! Try again."
                    else:
                        session["message"] = f"🎉 Correct! The number was {secret}."
                        session["game_over"] = True
                        session["won"] = True

                    if session["attempts"] >= settings["attempts"] and not session["won"]:
                        session["message"] = f"😢 Game over! The number was {secret}."
                        session["game_over"] = True
            except ValueError:
                session["message"] = "Please enter a valid whole number."

    difficulty = session["difficulty"]
    settings = DIFFICULTIES[difficulty]

    return render_template(
        "index.html",
        difficulty=difficulty,
        settings=settings,
        message=session.get("message", ""),
        attempts=session.get("attempts", 0),
        game_over=session.get("game_over", False),
        won=session.get("won", False),
        remaining=max(settings["attempts"] - session.get("attempts", 0), 0),
    )

if __name__ == "__main__":
    app.run(debug=True)
