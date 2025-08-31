from src.evaluator import evaluate_file

# Evaluate predicted vs reference
evaluation = evaluate_file("data/output.json", "data/ref.json")
print(f"Accuracy: {evaluation['accuracy']*100:.2f}%")
print(f"Precision: {evaluation['precision']*100:.2f}%")
print(f"Recall: {evaluation['recall']*100:.2f}%")
print(f"F1-score: {evaluation['f1']*100:.2f}%")
