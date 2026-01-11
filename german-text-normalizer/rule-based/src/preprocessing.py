def clean_text(text: str) -> str:
    """
    Simple text cleaning:
    - Lowercase text
    - Remove extra spaces
    """
    text = text.strip().lower()
    text = " ".join(text.split())
    return text
