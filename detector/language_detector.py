import re

def detect_language(text: str):
    if re.search(r'[\u0600-\u06FF]', text): return "ur"
    if re.search(r'[\uAC00-\uD7AF]', text): return "ko"
    return "en"
