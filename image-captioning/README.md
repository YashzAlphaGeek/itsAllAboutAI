# 🖼️ Image Captioning with AI (TensorFlow & BLIP)

This project demonstrates **two approaches to image captioning**:

1. **CNN + LSTM (TensorFlow/Keras)** – for learning and understanding how image captioning works  
2. **BLIP (Transformer, Pretrained)** – for generating **accurate captions instantly**

---

## 📂 Project Structure

```
image-captioning/
│
├── image_captioning.py   # CNN + LSTM (educational / demo)
├── blip_caption.py       # Pretrained BLIP (accurate captions)
├── test.jpg              # Sample image (replace with your own)
└── README.md
```

---

## 🔹 1. image_captioning.py (CNN + LSTM – Learning Demo)

### 📌 Description
This script implements a **basic image captioning pipeline** using:
- InceptionV3 as the **CNN encoder**
- LSTM as the **text decoder**

⚠️ **Note:**  
This file is meant for **educational purposes only**.  
It does **NOT** produce accurate captions unless trained on a large dataset (e.g., Flickr8k).

---

### 🛠️ Requirements
```bash
pip install tensorflow numpy pillow
```

---

### ▶️ How to Run
1. Place an image in the same folder (e.g., `test.jpg`)
2. Run:
```bash
python image_captioning.py
```

---

### 📤 Example Output
```
Generated Caption:
start a riding a bike end
```

This output confirms the **pipeline works**, but accuracy is limited due to minimal training data.

---

### ✅ What This Script Teaches
- CNN feature extraction
- Text tokenization
- Sequence modeling with LSTM
- End-to-end caption generation logic

---

## 🔹 2. blip_caption.py (Pretrained BLIP – Accurate Captions)

### 📌 Description
This script uses **BLIP**, a state-of-the-art **Vision–Language Transformer**, pretrained on millions of images.

✔ No training required  
✔ Accurate captions  
✔ Recommended for real use cases  

---

### 🛠️ Requirements
```bash
pip install transformers torch torchvision pillow
```

---

### ▶️ How to Run
1. Place your image in the folder (e.g., `test.jpg`)
2. Run:
```bash
python blip_caption.py
```

---

### 📤 Example Output
```
Generated Caption:
a man riding a bicycle on a city street
```

This caption is **based on the actual image content**.

---

## 🧠 Which Script Should I Use?

| Goal | Recommended Script |
|----|------------------|
Learn image captioning internals | `image_captioning.py` |
Get correct captions instantly | `blip_caption.py` |
Academic / coursework | `image_captioning.py` |
Production / demo | `blip_caption.py` |

---
