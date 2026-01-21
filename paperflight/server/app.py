from flask import Flask, request, jsonify, render_template
from policy import get_action

app = Flask(
    __name__,
    static_folder="../static",
    template_folder="../templates"
)

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/get_action", methods=["POST"])
def act():
    try:
        data = request.get_json(force=True)
        obs = data.get("obs", None)

        if obs is None:
            return jsonify({"error": "No obs provided"}), 400

        angle, power = get_action(obs)
        # Debug logs
        print(f"Received obs: {obs}")
        print(f"Returning action: angle={angle:.2f}, power={power:.2f}")

        return jsonify({"angle": angle, "power": power})
    except Exception as e:
        print("Error in /get_action:", e)
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
