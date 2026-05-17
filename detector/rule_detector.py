def rule_detect(text: str):
    t = text.lower().replace("0", "o").replace("1", "i").replace("3", "e").replace("@", "a").replace("$", "s").replace("!", "i")
    patterns = [
        "ignore previous instruction", "ignore all instructions", "ignore instruction", "disregard previous", "disregard all",
        "jailbreak", "developer mode", "act as", "pretend you are", "you are now", "roleplay as", "bypass all safety", "bypass safety",
        "reveal the system prompt", "show the system prompt", "print the system prompt", "what are your instructions",
        "api key", "api keys", "reveal password", "show password", "extract password",
        "forget rules", "system prompt", "bypass", "hack", "reveal", "drop table", "select *", "delete from", "exec(", "system(",
        "پچھلی ہدایات", "سسٹم پرامپٹ", "دکھائیں", "ہیک", "بائی پاس", "پابندی نہیں", "پاس ورڈ",
        "이전 지침을 무시", "시스템 프롬프트", "보여주세요", "해킹", "우회", "제한 없이", "비밀번호"
    ]
    matched = [p for p in patterns if p in t or p in text]
    if matched:
        return {"is_attack": True, "score": 1.0, "matched": matched}
    return {"is_attack": False, "score": 0.0, "matched": []}
