def make_decision(rule, semantic, pii, text):
    injection_risk = max(rule["score"], semantic["score"])
    
    risk = injection_risk
    if pii["has_pii"]: risk += 0.3
    if pii["has_secret"]: risk += 0.4
    risk = min(round(risk, 2), 1.0)
    
    reason_codes = []
    if rule["is_attack"]: reason_codes.append("RULE_INJECTION")
    if semantic["is_attack"]: reason_codes.append("SEMANTIC_INJECTION")
    if pii["has_pii"]: reason_codes.append("PII_DETECTED")
    if pii["has_secret"]: reason_codes.append("SECRET_PII")
    
    if injection_risk >= 0.55:
        return {"decision": "BLOCK", "final_risk": risk, "reason_codes": reason_codes, "safe_text": None}
    if pii["has_pii"]:
        return {"decision": "MASK", "final_risk": risk, "reason_codes": reason_codes, "safe_text": pii["masked_text"]}
        
    return {"decision": "ALLOW", "final_risk": risk, "reason_codes": reason_codes, "safe_text": text}
