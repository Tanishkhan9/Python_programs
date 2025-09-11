from flask import Flask, jsonify, request

app = Flask(__name__)

# Simulated light bulb state
light_state = {"status": "OFF"}

@app.route("/")
def home():
    return """
    <h1>💡 IoT Light Bulb</h1>
    <p>Current State: <b>{}</b></p>
    <a href="/on"><button>Turn ON</button></a>
    <a href="/off"><button>Turn OFF</button></a>
    """.format(light_state["status"])

@app.route("/on", methods=["GET"])
def turn_on():
    light_state["status"] = "ON"
    print("💡 Light turned ON")
    return jsonify(light_state)

@app.route("/off", methods=["GET"])
def turn_off():
    light_state["status"] = "OFF"
    print("💡 Light turned OFF")
    return jsonify(light_state)

@app.route("/status", methods=["GET"])
def status():
    return jsonify(light_state)

if __name__ == "__main__":
    print("🚀 IoT Light Bulb Simulation Running at http://127.0.0.1:5000/")
    app.run(debug=True)