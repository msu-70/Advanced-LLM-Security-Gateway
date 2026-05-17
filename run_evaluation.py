import csv, json, time, os, sys

# Ensure modules can be imported
sys.path.insert(0, os.path.dirname(__file__))

from detector.language_detector import detect_language
from detector.rule_detector import rule_detect
from detector.semantic_detector import semantic_detect
from detector.pii_detector import analyze_pii
from policy_engine import make_decision

DATA_FILE = "data/final_eval.csv"
RESULTS_FILE = "results/evaluation_results.csv"

os.makedirs("results", exist_ok=True)

def run_evaluation():
    # Load dataset
    rows = []
    with open(DATA_FILE, encoding="utf-8") as f:
        for r in csv.DictReader(f):
            rows.append(r)
    print(f"Loaded {len(rows)} prompts.")

    results = []
    correct = 0

    for row in rows:
        prompt = row["prompt"]
        expected = row["expected_policy"].strip().upper()

        # Pipeline (no HTTP request – direct imports for speed)
        language = detect_language(prompt)
        rule_res = rule_detect(prompt)
        semantic_res = semantic_detect(prompt)
        pii_res = analyze_pii(prompt)
        decision = make_decision(rule_res, semantic_res, pii_res, prompt)

        predicted = decision["decision"]
        if predicted == expected:
            correct += 1

        results.append({
            "id": row["id"],
            "language": language,
            "expected": expected,
            "predicted": predicted,
            "rule_score": rule_res["score"],
            "semantic_score": semantic_res["score"],
            "final_risk": decision["final_risk"],
            "reason_codes": "|".join(decision["reason_codes"]),
        })

    # Write per‑prompt CSV
    fieldnames = ["id", "language", "expected", "predicted", "rule_score", "semantic_score", "final_risk", "reason_codes"]
    with open(RESULTS_FILE, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(results)

    accuracy = round(correct / len(rows), 3) if rows else 0
    print(f"Overall BLOCK-detection accuracy: {accuracy*100:.1f}% ({correct}/{len(rows)})")
    print(f"Results saved to {RESULTS_FILE}")

if __name__ == "__main__":
    run_evaluation()
