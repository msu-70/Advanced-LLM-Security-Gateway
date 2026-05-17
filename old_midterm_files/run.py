
from detector import detect_injection
from pii import detect_pii
from policy import decide

print("\n LLM SECURITY GATEWAY (CLEAN VERSION)")
print("Type 'exit' to stop\n")

while True:
    text = input("Enter text: ")

    if text.lower() == "exit":
        break

    injection = detect_injection(text)
    pii = detect_pii(text)

    result = decide(injection, pii, pii["masked_text"], text)

    print("\nRESULT:")
    print("Decision:", result["decision"])
    print("Output:", result["output"])
    print("Injection:", injection["is_attack"])
    print("PII:", pii["entities"])
    print("-"*40)
