
import yaml
import os

CONFIG_PATH = os.path.join(os.path.dirname(__file__), "..", "..", "config", "gateway_config.yaml")

with open(CONFIG_PATH, "r") as f:
    cfg = yaml.safe_load(f)

def make_decision(rule_result, semantic_result, pii_result, text):
    risk = max(rule_result["score"], semantic_result["score"])
    
    if pii_result["has_pii"]:
        risk += cfg["weights"]["pii_weight"]
    if pii_result.get("has_secret"):
        risk += cfg["weights"]["secret_weight"]
        
    risk = min(round(risk, 2), 1.0)
    
    reason_codes = []
    if rule_result["is_attack"]: reason_codes.append("RULE_INJECTION")
    if semantic_result["is_attack"]: reason_codes.append("SEMANTIC_INJECTION")
    if pii_result["has_pii"]: reason_codes.append("PII_DETECTED")
    if pii_result.get("has_secret"): reason_codes.append("SECRET_PII")
    
    if risk >= cfg["thresholds"]["final_block"]:
        return {
            "decision": "BLOCK",
            "final_risk": risk,
            "reason_codes": reason_codes,
            "safe_text": None
        }
        
    if pii_result["has_pii"] and risk >= cfg["thresholds"]["final_mask"]:
        return {
            "decision": "MASK",
            "final_risk": risk,
            "reason_codes": reason_codes,
            "safe_text": pii_result["masked_text"]
        }
        
    return {
        "decision": "ALLOW",
        "final_risk": risk,
        "reason_codes": reason_codes,
        "safe_text": text
    }

