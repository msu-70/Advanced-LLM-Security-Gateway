
def detect_injection(text: str):
    text = text.lower()

    patterns = [
        "ignore previous instruction",
        "ignore instruction",
        "jailbreak",
        "developer mode",
        "system prompt",
        "bypass",
        "act as",
        "hack",
        "reveal",
        "forget rules",
        "drop table",
        "select *",
        "delete from",
        "insert into",
        "update users",
        "exec(",
        "system("
    ]

    for p in patterns:
        if p in text:
            return {"is_attack": True, "score": 1, "match": p}

    return {"is_attack": False, "score": 0, "match": None}
