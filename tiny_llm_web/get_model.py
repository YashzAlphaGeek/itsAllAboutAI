from transformers import AutoModelForCausalLM, AutoTokenizer

model_name = "distilgpt2"
model = AutoModelForCausalLM.from_pretrained(model_name)
tokenizer = AutoTokenizer.from_pretrained(model_name)

save_dir = "./tiny_llm"
model.save_pretrained(save_dir)
tokenizer.save_pretrained(save_dir)

print(f"Model and tokenizer from {model_name} saved to {save_dir}")
