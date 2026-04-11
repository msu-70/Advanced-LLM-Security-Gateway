from fastapi import FastAPI
from detector import detect_injection
from pii import detect_pii
from policy import decide

app = FastAPI(title="LLM Security Gateway API")


@app.get("/")
def home():
    return {"message": "API is running successfully"}


@app.post("/process")
def process(data: dict):

    text = data.get("text", "")

    injection = detect_injection(text)
    pii = detect_pii(text)

    result = decide(
        injection,
        pii,
        pii["masked_text"],
        text
    )

    return {
        "input": text,
        "decision": result["decision"],
        "output": result["output"],
        "injection": injection,
        "pii": pii
    }