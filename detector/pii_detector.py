from presidio_analyzer import AnalyzerEngine, PatternRecognizer, Pattern
from presidio_anonymizer import AnonymizerEngine
from presidio_anonymizer.entities import OperatorConfig

analyzer = AnalyzerEngine()
anonymizer = AnonymizerEngine()

analyzer.registry.add_recognizer(PatternRecognizer(supported_entity="CNIC", patterns=[Pattern("CNIC", r"\b\d{5}-\d{7}-\d\b", 0.9)]))
analyzer.registry.add_recognizer(PatternRecognizer(supported_entity="STUDENT_ID", patterns=[Pattern("STD", r"\b[A-Z]{2}\d{2}-[A-Z]{2,4}-\d{2,4}\b", 0.9)]))
analyzer.registry.add_recognizer(PatternRecognizer(supported_entity="API_KEY", patterns=[Pattern("API", r"\b[A-Za-z0-9_\-]{20,}\b", 0.6)]))

def analyze_pii(text: str):
    results = [r for r in analyzer.analyze(text=text, language="en") if r.score >= 0.4]
    
    if not results:
        return {"entities": [], "masked_text": text, "has_pii": False, "has_secret": False, "pii_risk": 0.0}
        
    ops = {
        "EMAIL_ADDRESS": OperatorConfig("replace", {"new_value": "<EMAIL>"}),
        "PHONE_NUMBER": OperatorConfig("replace", {"new_value": "<PHONE>"}),
        "CNIC": OperatorConfig("replace", {"new_value": "<CNIC>"}),
        "STUDENT_ID": OperatorConfig("replace", {"new_value": "<STUDENT_ID>"}),
        "API_KEY": OperatorConfig("replace", {"new_value": "<API_KEY>"}),
        "PERSON": OperatorConfig("replace", {"new_value": "<PERSON>"})
    }
    anonymized = anonymizer.anonymize(text=text, analyzer_results=results, operators=ops)
    entities = [{"type": r.entity_type, "text": text[r.start:r.end], "score": round(r.score, 2)} for r in results]
    types = [e["type"] for e in entities]
    
    return {
        "entities": entities,
        "masked_text": anonymized.text,
        "has_pii": True,
        "has_secret": "API_KEY" in types or "CNIC" in types,
        "pii_risk": round(len(entities) * 0.3, 2)
    }
