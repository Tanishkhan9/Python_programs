from flask import Flask, render_template_string, request, redirect, url_for

app = Flask(__name__)

# Global game state
board = [""] * 9
current_player = "X"
winner = None

# HTML template (inline for single-file app)
template = """
<!DOCTYPE html>
<html>
<head>
    <title>Tic Tac Toe</title>
    <style>
        body { font-family: Arial, sans-serif; text-align: center; }
        .board { display: grid; grid-template-columns: repeat(3, 100px); gap: 5px; margin: 20px auto; }
        .cell {
            width: 100px; height: 100px; font-size: 36px; display: flex;
            align-items: center; justify-content: center; background: #f2f2f2; cursor: pointer;
            border-radius: 10px;
        }
        .cell:hover { background: #ddd; }
        .winner { font-size: 24px; margin: 10px; color: green; }
        .reset { background: #333; color: white; padding: 10px 20px; border-radius: 5px; text-decoration: none; }
    </style>
</head>
<body>
    <h1>Tic Tac Toe</h1>
    {% if winner %}
        <div class="winner">{{ winner }}</div>
    {% else %}
        <h3>Current Player: {{ current_player }}</h3>
    {% endif %}
    <div class="board">
        {% for i in range(9) %}
            <form method="POST" action="{{ url_for('move', index=i) }}">
                <button class="cell" type="submit" {% if board[i] or winner %}disabled{% endif %}>
                    {{ board[i] }}
                </button>
            </form>
        {% endfor %}
    </div>
    <a href="{{ url_for('reset') }}" class="reset">Reset Game</a>
</body>
</html>
"""

def check_winner():
    global winner
    wins = [(0, 1, 2), (3, 4, 5), (6, 7, 8), 
            (0, 3, 6), (1, 4, 7), (2, 5, 8),
            (0, 4, 8), (2, 4, 6)]
    for a, b, c in wins:
        if board[a] == board[b] == board[c] and board[a] != "":
            winner = f"Player {board[a]} wins!"
            return
    if all(cell != "" for cell in board):
        winner = "It's a Draw!"

@app.route("/", methods=["GET"])
def index():
    return render_template_string(template, board=board, current_player=current_player, winner=winner)

@app.route("/move/<int:index>", methods=["POST"])
def move(index):
    global current_player
    if not board[index] and not winner:
        board[index] = current_player
        check_winner()
        current_player = "O" if current_player == "X" else "X"
    return redirect(url_for("index"))

@app.route("/reset")
def reset():
    global board, current_player, winner
    board = [""] * 9
    current_player = "X"
    winner = None
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(debug=True)