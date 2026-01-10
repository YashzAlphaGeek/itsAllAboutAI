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
    obs = request.json["obs"]
    angle, power = get_action(obs)
    return jsonify({"angle": angle, "power": power})

if __name__ == "__main__":
    app.run(debug=True)
