
import re

def detect_pii(text: str):

    entities = []
    masked = text

    if re.search(r"\S+@\S+", text):
        entities.append("email")
        masked = re.sub(r"\S+@\S+", "[EMAIL]", masked)

    if re.search(r"03[0-9]{9}", text):
        entities.append("phone")
        masked = re.sub(r"03[0-9]{9}", "[PHONE]", masked)

    if re.search(r"EMP[0-9]+", text):
        entities.append("id")
        masked = re.sub(r"EMP[0-9]+", "[ID]", masked)

    return {"entities": entities, "masked_text": masked}
