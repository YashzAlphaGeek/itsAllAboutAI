# Tiny LLM Web Application

This project demonstrates a **Tiny LLM Web Application** using a small, pretrained language model (`distilgpt2`) from Hugging Face. You can interact with the model via a simple web interface built with **Flask**.

---

## Overview

The application allows you to type a prompt and receive a generated response from a **local, lightweight LLM**. This project is ideal for learning about LLMs, experimenting with prompts, and understanding the basics of **text generation** without training a model from scratch.

---

## How It Works

### 1. Model Loading

I used the Hugging Face Transformers library to load a **pretrained model and tokenizer**:

```python
from transformers import AutoModelForCausalLM, AutoTokenizer

model_name = "distilgpt2"
model = AutoModelForCausalLM.from_pretrained(model_name)
tokenizer = AutoTokenizer.from_pretrained(model_name)
```

* **Tokenizer:** Converts text into tokens (numbers the model understands) and back.
* **Model:** Predicts the next token based on previous tokens using learned weights.

We then save this model locally:

```python
model.save_pretrained("./tiny_llm")
tokenizer.save_pretrained("./tiny_llm")
```

---

### 2. Web Interface (Flask)

The Flask app provides a **web-based input form** for prompts:

```python
from flask import Flask, render_template, request

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def home():
    response_text = ""
    if request.method == "POST":
        prompt = request.form["prompt"]
        inputs = tokenizer(prompt, return_tensors="pt")
        outputs = model.generate(**inputs, max_length=50, temperature=0.5, top_p=0.9)
        response_text = tokenizer.decode(outputs[0], skip_special_tokens=True)
    return render_template("index.html", response=response_text)
```

* User types a prompt in the input box.
* Flask captures the prompt and sends it to the model.
* The model generates a response using **causal language modeling**.
* Response is rendered back in the browser.

---

### 3. AI Technique Used

This project uses a **single LLM technique**:

* **Pretrained Causal Language Model (distilgpt2)**

  * Trained with **self-supervised learning** to predict the next token.
  * No additional fine-tuning or RLHF is applied.
  * Lightweight and suitable for experimentation.
  
---

### 4. Installation

1. Clone the repository:

```bash
git clone <repository-url>
cd tiny_llm_web
```

2. Install dependencies:

```bash
pip install flask transformers torch
```

3. Make sure you have Python 3.8+ installed.

---

### 5. Running the App

```bash
python app.py
```

* Open your browser and go to `http://127.0.0.1:5000/`
* Type a prompt and click **Send** to get a response.

---

### 6. Example

**Input:**

```
Hello
```

**Output:**

```
Hello The first time I saw a new game, I was really excited to see it. I was really excited to see it. I was really excited to see it. I was really excited to see it. I was really excited to see it.
```
![output.png](templates%2Foutput.png)

---

### 7. Summary

* This Tiny LLM demonstrates **text generation** with **pretrained LLMs**.
* Uses **self-supervised learning** (causal language modeling).
* No training from scratch is required — ideal for learning and prototyping.
* Can be extended to include **RAG, fine-tuning, or larger models** for improved accuracy and relevance.

---

### 8. References

* [Hugging Face Transformers](https://huggingface.co/transformers/)
* [distilgpt2 Model](https://huggingface.co/distilgpt2)
* [Flask Documentation](https://flask.palletsprojects.com/)
