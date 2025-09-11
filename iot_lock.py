from flask import Flask, request, jsonify

app = Flask(__name__)

# Simulated lock state
lock_state = {"status": "LOCKED", "pin": "1234"}  # Default PIN is 1234


@app.route("/")
def home():
    return f"""
    <h1>🔐 IoT Door Lock</h1>
    <p>Current State: <b>{lock_state['status']}</b></p>
    <form action="/unlock" method="post">
        <input type="password" name="pin" placeholder="Enter PIN" required>
        <button type="submit">Unlock</button>
    </form>
    <a href="/lock"><button>Lock</button></a>
    """


@app.route("/unlock", methods=["POST"])
def unlock():
    user_pin = request.form.get("pin")
    if user_pin == lock_state["pin"]:
        lock_state["status"] = "UNLOCKED"
        print("🔓 Door UNLOCKED")
        return f"<h2>✅ Door is now UNLOCKED</h2><a href='/'>Go Back</a>"
    else:
        return f"<h2>❌ Wrong PIN</h2><a href='/'>Try Again</a>"


@app.route("/lock", methods=["GET"])
def lock():
    lock_state["status"] = "LOCKED"
    print("🔒 Door LOCKED")
    return f"<h2>🔒 Door is now LOCKED</h2><a href='/'>Go Back</a>"


@app.route("/status", methods=["GET"])
def status():
    return jsonify(lock_state)


if __name__ == "__main__":
    print("🚀 IoT Door Lock Simulation Running at http://127.0.0.1:5000/")
    app.run(debug=True)