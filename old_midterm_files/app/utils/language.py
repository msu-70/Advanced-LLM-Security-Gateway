"""
language.py  –  Detect the main language of an input string.

We use Unicode character ranges so there is NO extra library needed.
Supported: English (en), Urdu (ur), Korean (ko), Arabic (ar), Hindi (hi).
If nothing matches we return "en" as the safe default.
"""

import re


def detect_language(text: str) -> str:
    """Return a short language code for the dominant script in `text`."""

    # Count characters in each script range
    urdu_arabic_chars = len(re.findall(r'[\u0600-\u06FF]', text))
    korean_chars      = len(re.findall(r'[\uAC00-\uD7A3\u1100-\u11FF]', text))
    hindi_chars       = len(re.findall(r'[\u0900-\u097F]', text))
    latin_chars       = len(re.findall(r'[a-zA-Z]', text))

    # Build a simple ranking dict
    scores = {
        "ko": korean_chars,
        "hi": hindi_chars,
        "ur": urdu_arabic_chars,
        "en": latin_chars,
    }

    # If we have Urdu/Arabic script AND a lot of Latin too → mixed (label ur)
    dominant = max(scores, key=scores.get)

    # All zero → unknown, default to English
    if scores[dominant] == 0:
        return "en"

    # Arabic script is shared between Arabic and Urdu.
    # We label it "ur" here for simplicity (our dataset is Urdu-focused).
    return dominant
