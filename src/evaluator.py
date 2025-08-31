# src/evaluator.py
import json

def evaluate_llm_output(prediction, reference):
    """
    Simple evaluation: returns 1 if prediction matches reference exactly, else 0.
    """
    return int(prediction.strip() == reference.strip())

def evaluate_file(pred_file, ref_file):
    """
    Evaluate predictions against reference JSON file.
    Returns a score and detailed report.
    """
    with open(pred_file, "r") as f:
        preds = json.load(f)
    with open(ref_file, "r") as f:
        refs = json.load(f)

    scores = []
    for p, r in zip(preds, refs):
        score = evaluate_llm_output(p["text"], r["text"])
        scores.append(score)

    accuracy = sum(scores) / len(scores)
    report = {"accuracy": accuracy, "total": len(scores), "correct": sum(scores)}
    return report
