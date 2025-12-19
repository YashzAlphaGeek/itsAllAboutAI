from PIL import Image
import torch
from transformers import BlipProcessor, BlipForConditionalGeneration

# ----------------------------
# Load pretrained BLIP model
# ----------------------------
processor = BlipProcessor.from_pretrained(
    "Salesforce/blip-image-captioning-base"
)
model = BlipForConditionalGeneration.from_pretrained(
    "Salesforce/blip-image-captioning-base"
)

# ----------------------------
# Load image (same folder)
# ----------------------------
image_path = "test.jpg"   # change if needed
image = Image.open(image_path).convert("RGB")

# ----------------------------
# Generate caption
# ----------------------------
inputs = processor(image, return_tensors="pt")

with torch.no_grad():
    output = model.generate(**inputs, max_length=50)

caption = processor.decode(output[0], skip_special_tokens=True)

print("Generated Caption:")
print(caption)
