from flask import Flask, request, jsonify, send_from_directory
import random

app = Flask(__name__, static_folder="static")

# Policy Gradient weights
w1 = random.uniform(0.5, 1.0)
w2 = random.uniform(0.2, 0.5)
lr = 0.05

@app.route("/")
def index():
    return send_from_directory("static", "index.html")

@app.route("/get_action", methods=["POST"])
def get_action():
    global w1, w2
    data = request.json
    ball_x = data.get("ball_x", 0)
    bin_x = data.get("bin_x", 0)

    # Compute distance
    distance = bin_x - ball_x

    # Adaptive angle & power
    angle = w1 + w2 + 0.03 * distance
    angle += random.uniform(-0.05, 0.05)  # exploration
    angle = max(0.2, min(angle, 1.2))

    power = 12 + 0.01 * distance
    power = max(10, min(power, 15))

    return jsonify({"angle": angle, "power": power})

@app.route("/update", methods=["POST"])
def update():
    global w1, w2
    data = request.json
    reward = data.get("reward", 0.0)

    # Policy gradient update
    w1 += lr * reward * 5
    w2 += lr * reward * 5

    return jsonify({"status": "updated","w1":w1,"w2":w2})

@app.route("/<path:path>")
def serve_static(path):
    return send_from_directory("static", path)

if __name__ == "__main__":
    print("Server running at http://localhost:5000")
    app.run(port=5000)
