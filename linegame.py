from flask import Flask, render_template_string, redirect, url_for

app = Flask(__name__)

ROWS = 5
COLS = 5

board = [["" for _ in range(COLS)] for _ in range(ROWS)]
current_player = "X"
winner = None

template = """
<!DOCTYPE html>
<html>
<head>
    <title>Line Connect Game</title>
    <style>
        body { font-family: Arial, sans-serif; text-align: center; }
        .board {
            display: grid;
            grid-template-columns: repeat({{ cols }}, 80px);
            gap: 5px;
            margin: 20px auto;
        }
        .cell {
            width: 80px; height: 80px; font-size: 32px;
            display: flex; align-items: center; justify-content: center;
            background: #f0f0f0; border-radius: 10px;
            cursor: pointer;
        }
        .cell:hover { background: #ddd; }
        .winner { font-size: 24px; margin: 10px; color: green; }
        .reset {
            background: #333; color: white; padding: 10px 20px;
            border-radius: 5px; text-decoration: none;
        }
    </style>
</head>
<body>
    <h1>Line Connect (Connect 3)</h1>
    {% if winner %}
        <div class="winner">{{ winner }}</div>
    {% else %}
        <h3>Current Player: {{ current_player }}</h3>
    {% endif %}
    <div class="board">
        {% for r in range(rows) %}
            {% for c in range(cols) %}
                <form method="POST" action="{{ url_for('move', row=r, col=c) }}">
                    <button class="cell" type="submit" {% if board[r][c] or winner %}disabled{% endif %}>
                        {{ board[r][c] }}
                    </button>
                </form>
            {% endfor %}
        {% endfor %}
    </div>
    <a href="{{ url_for('reset') }}" class="reset">Reset Game</a>
</body>
</html>
"""

def check_winner():
    global winner
    directions = [(1, 0), (0, 1), (1, 1), (1, -1)]  # down, right, diag down-right, diag down-left
    for r in range(ROWS):
        for c in range(COLS):
            if board[r][c] == "":
                continue
            for dr, dc in directions:
                try:
                    if (board[r][c] == board[r+dr][c+dc] ==
                        board[r+2*dr][c+2*dc]):
                        winner = f"Player {board[r][c]} wins!"
                        return
                except IndexError:
                    continue
    if all(cell != "" for row in board for cell in row):
        winner = "It's a Draw!"

@app.route("/")
def index():
    return render_template_string(template, board=board, rows=ROWS, cols=COLS,
                                  current_player=current_player, winner=winner)

@app.route("/move/<int:row>/<int:col>", methods=["POST"])
def move(row, col):
    global current_player
    if not board[row][col] and not winner:
        board[row][col] = current_player
        check_winner()
        current_player = "O" if current_player == "X" else "X"
    return redirect(url_for("index"))

@app.route("/reset")
def reset():
    global board, current_player, winner
    board = [["" for _ in range(COLS)] for _ in range(ROWS)]
    current_player = "X"
    winner = None
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(debug=True)