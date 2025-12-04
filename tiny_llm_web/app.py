from flask import Flask, render_template, request
from transformers import AutoTokenizer, AutoModelForCausalLM

app = Flask(__name__)

# Load tiny LLM
model_path = "./tiny_llm"
tokenizer = AutoTokenizer.from_pretrained(model_path)
model = AutoModelForCausalLM.from_pretrained(model_path)

@app.route("/", methods=["GET", "POST"])
def home():
    response_text = ""
    if request.method == "POST":
        prompt = request.form["prompt"]
        inputs = tokenizer(prompt, return_tensors="pt")
        outputs = model.generate(**inputs, max_length=50)
        response_text = tokenizer.decode(outputs[0], skip_special_tokens=True)
    return render_template("index.html", response=response_text)

if __name__ == "__main__":
    app.run(debug=True)
