
def detect_injection(text: str):
    text = text.lower()

    patterns = [
        "ignore previous instructions",
        "ignore instructions",
        "jailbreak",
        "developer mode",
        "system prompt",
        "bypass",
        "act as",
        "hack",
        "reveal",
        "forget rules"
    ]

    for p in patterns:
        if p in text:
            return {"is_attack": True, "score": 1, "match": p}

    return {"is_attack": False, "score": 0, "match": None}
