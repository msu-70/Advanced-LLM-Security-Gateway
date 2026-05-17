

from presidio_analyzer import AnalyzerEngine, PatternRecognizer, Pattern
from presidio_anonymizer import AnonymizerEngine
from presidio_anonymizer.entities import OperatorConfig

analyzer = AnalyzerEngine()
anonymizer = AnonymizerEngine()

# Custom Recognizer 1: CNIC
analyzer.registry.add_recognizer(PatternRecognizer("CNIC", [Pattern("CNIC", r"\b\d{5}-\d{7}-\d\b", 0.9)]))

# Custom Recognizer 2: Student ID
analyzer.registry.add_recognizer(PatternRecognizer("STUDENT_ID", [Pattern("STD", r"\b[A-Z]{2}\d{2}-[A-Z]{2,4}-\d{2,4}\b", 0.9)]))

# Custom Recognizer 3: API Key
analyzer.registry.add_recognizer(PatternRecognizer("API_KEY", [Pattern("API", r"\b[A-Za-z0-9_\-]{20,}\b", 0.6)]))

def analyze_pii(text: str):
    results = analyzer.analyze(text=text, language="en")
    
    # Custom Thresholding (ignore low confidence)
    results = [r for r in results if r.score >= 0.4]
    
    if not results:
        return {
            "entities": [],
            "masked_text": text,
            "has_pii": False,
            "has_secret": False,
            "pii_risk": 0.0
        }
        
    # Anonymize (Masking)
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
    has_secret = "API_KEY" in types or "CNIC" in types
    
    return {
        "entities": entities,
        "masked_text": anonymized.text,
        "has_pii": True,
        "has_secret": has_secret,
        "pii_risk": round(len(entities) * 0.3, 2)
    }

