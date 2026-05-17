
import re

def detect_pii(text: str):

    entities = []
    masked = text

    if re.search(r"\S+@\S+", text):
        entities.append("email")
        masked = re.sub(r"\S+@\S+", "[EMAIL]", masked)
       

    phone_pattern = r"(03[0-9]{9})"
    if re.search(phone_pattern, text):
        entities.append("phone")
        masked = re.sub(phone_pattern, "[PHONE]", masked)

    if re.search(r"EMP[0-9]+", text):
        entities.append("id")
        masked = re.sub(r"EMP[0-9]+", "[ID]", masked)

    return {"entities": entities, "masked_text": masked}
