import time
import uuid
import json
import os
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from pydantic import BaseModel

from detector.semantic_detector import semantic_detect
from detector.pii_detector import analyze_pii
from detector.language_detector import detect_language
from detector.rule_detector import rule_detect
from policy_engine import make_decision

app = FastAPI(title="LLM Security Gateway")

class AnalyzeRequest(BaseModel):
    text: str

@app.post("/analyze")
def analyze(request: AnalyzeRequest):
    start_time = time.time()
    text = request.text.strip()
    
    if not text:
        return JSONResponse(status_code=400, content={"error": "Text is required"})

    lang = detect_language(text)
    rule = rule_detect(text)
    semantic = semantic_detect(text)
    pii = analyze_pii(text)
    policy = make_decision(rule, semantic, pii, text)

    response = {
        "input_id": str(uuid.uuid4())[:8],
        "language": lang,
        "rule_score": rule["score"],
        "semantic_score": semantic["score"],
        "pii_entities": pii["entities"],
        "final_risk": policy["final_risk"],
        "decision": policy["decision"],
        "safe_text": policy["safe_text"],
        "reason_codes": policy["reason_codes"],
        "latency_ms": round((time.time() - start_time) * 1000, 1)
    }

    os.makedirs("results", exist_ok=True)
    with open("results/audit_log.jsonl", "a", encoding="utf-8") as f:
        f.write(json.dumps(response) + "\n")

    return response