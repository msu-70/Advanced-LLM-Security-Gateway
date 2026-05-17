
def decide(injection, pii, masked, original):

    if injection["is_attack"]:
        return {"decision": "BLOCK", "output": "Blocked due to security risk"}

    if len(pii["entities"]) > 0:
        return {"decision": "MASK", "output": masked}

    return {"decision": "ALLOW", "output": original}
