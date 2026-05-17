def rule_detect(text: str):
    text_lower = text.lower()
    
    patterns = [
        "ignore previous instruction", "ignore instruction", "jailbreak",
        "developer mode", "system prompt", "bypass", "act as", "hack",
        "reveal", "forget rules", "drop table", "select *", "delete from",
        "پچھلی ہدایات", "سسٹم پرامپٹ", "دکھائیں", "ہیک", "بائی پاس",
        "이전 지침을 무시", "시스템 프롬프트", "보여주세요", "해킹"
    ]
    
    matched = []
    for p in patterns:
        if p in text_lower or p in text:
            matched.append(p)
            
    if matched:
        return {"is_attack": True, "score": 1.0, "matched": matched}
        
    return {"is_attack": False, "score": 0.0, "matched": []}

