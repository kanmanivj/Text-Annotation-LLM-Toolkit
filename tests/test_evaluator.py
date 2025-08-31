
from src.evaluator import evaluate_file
# Run evaluation
results = evaluate_file(pred_file="data/pred.json", ref_file="data/ref.json")

# Access accuracy from the returned dictionary
accuracy = results["accuracy"]
print(f"Overall accuracy: {accuracy*100:.2f}%")
