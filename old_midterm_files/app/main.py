
import time
import uuid
import json
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from pydantic import BaseModel

from app.detectors.rule_detector      import rule_detect
from app.detectors.semantic_detector  import semantic_detect
from app.pii.presidio_custom          import analyze_pii
from app.policy.policy_engine         import make_decision
from app.utils.language               import detect_language

app = FastAPI(title="LLM Security Gateway")

class AnalyzeRequest(BaseModel):
    text: str

@app.post("/analyze")
def analyze(request: AnalyzeRequest):
    start_time = time.time()
    text = request.text.strip()
    input_id = str(uuid.uuid4())[:8]

    if not text:
        return JSONResponse(status_code=400, content={"error": "Text is required"})

    language = detect_language(text)
    rule_result = rule_detect(text)
    semantic_result = semantic_detect(text)
    pii_result = analyze_pii(text)
    policy = make_decision(rule_result, semantic_result, pii_result, text)

    latency_ms = round((time.time() - start_time) * 1000, 1)

    response = {
        "input_id": input_id,
        "language": language,
        "rule_score": rule_result["score"],
        "semantic_score": semantic_result["score"],
        "pii_entities": pii_result["entities"],
        "final_risk": policy["final_risk"],
        "decision": policy["decision"],
        "safe_text": policy["safe_text"],
        "reason_codes": policy["reason_codes"],
        "latency_ms": latency_ms
    }

    # Audit logging
    with open("results/audit_log.jsonl", "a", encoding="utf-8") as f:
        f.write(json.dumps(response) + "\n")

    return response
