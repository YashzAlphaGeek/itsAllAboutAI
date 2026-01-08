from flask import Flask, request, jsonify, send_from_directory
import random

app = Flask(__name__, static_folder="static")

w1 = random.uniform(0.5, 1.0)
w2 = random.uniform(0.2, 0.5)
lr = 0.05

@app.route("/")
def index():
    return send_from_directory("static", "index.html")

@app.route("/get_action", methods=["POST"])
def get_action():
    global w1, w2
    # Compute angle + power
    angle = w1 + w2
    angle += random.uniform(-0.1, 0.1)  # small exploration
    angle = max(0.2, min(angle, 1.2))   # clamp to 0.2-1.2 rad
    power = 12.0
    return jsonify({"angle": angle, "power": power})

@app.route("/update", methods=["POST"])
def update():
    global w1, w2
    data = request.json
    reward = data.get("reward", 0.0)
    w1 += lr * reward
    w2 += lr * reward
    return jsonify({"status": "updated", "w1": w1, "w2": w2})

@app.route("/<path:path>")
def serve_static(path):
    return send_from_directory("static", path)

if __name__ == "__main__":
    print("Server running at http://localhost:5000")
    app.run(port=5000)
